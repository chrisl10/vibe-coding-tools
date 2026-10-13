"""Private, no-clobber batch publication for forensic derived outputs.

Requires a user-owned mode-0700 output parent. Creates missing parents privately;
never chmods existing paths. All destinations are checked before publication.
Directory descriptors anchor writes so symlink swaps cannot redirect them.
"""
import os
import secrets
import stat
import sys
from pathlib import Path


def checked_path(value):
    path = Path(value)
    if '..' in path.parts or any(ord(c) < 32 or ord(c) == 127 for c in str(path)):
        raise ValueError('output path contains traversal or control characters')
    path = path.absolute()
    aliases = {'/tmp': '/private/tmp', '/var': '/private/var', '/etc': '/private/etc'}
    for item in [*reversed(path.parents), path]:
        try:
            info = item.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode):
            if sys.platform == 'darwin' and str(item) in aliases and os.path.realpath(item) == aliases[str(item)]:
                continue
            raise ValueError('symlink output path refused: ' + str(item))
        if item != path and not stat.S_ISDIR(info.st_mode):
            raise ValueError('non-directory output ancestor refused')
    return path


def private_directory(value):
    path = checked_path(value)
    missing = []
    current = path
    while not current.exists():
        missing.append(current)
        current = current.parent
    for item in reversed(missing):
        checked_path(item.parent)
        os.mkdir(item, 0o700)
        checked_path(item)
    info = path.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.geteuid() or stat.S_IMODE(info.st_mode) != 0o700:
        raise ValueError('existing output directory must be user-owned mode 0700; choose a fresh private workspace')
    return path


def _absent(path):
    try:
        path.lstat()
    except FileNotFoundError:
        return
    raise FileExistsError('output already exists; refusing overwrite: ' + str(path))


def write_batch(outputs):
    """Publish byte/text payloads, refusing every collision before first file write."""
    items = list(outputs.items()) if isinstance(outputs, dict) else list(outputs)
    normalized = [(checked_path(path), data.encode('utf-8') if isinstance(data, str) else bytes(data)) for path, data in items]
    paths = [path for path, _ in normalized]
    if len(set(paths)) != len(paths):
        raise ValueError('duplicate output destination')
    for path in paths:
        _absent(path)
    directories = {}
    records = []
    published = []
    try:
        for parent in dict.fromkeys(path.parent for path in paths):
            private_directory(parent)
            fd = os.open(parent, os.O_RDONLY | os.O_DIRECTORY | getattr(os, 'O_NOFOLLOW', 0))
            info = os.fstat(fd)
            if info.st_uid != os.geteuid() or stat.S_IMODE(info.st_mode) != 0o700:
                os.close(fd)
                raise ValueError('output directory changed during preflight')
            directories[parent] = fd
        # Recheck every leaf relative to the anchored directory before any write.
        for path in paths:
            try:
                os.stat(path.name, dir_fd=directories[path.parent], follow_symlinks=False)
            except FileNotFoundError:
                continue
            raise FileExistsError('output already exists; refusing overwrite: ' + str(path))
        for path, data in normalized:
            directory_fd = directories[path.parent]
            temporary = '.forensic-' + secrets.token_hex(16) + '.tmp'
            fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o600, dir_fd=directory_fd)
            records.append((directory_fd, temporary, path.name))
            with os.fdopen(fd, 'wb') as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
        for directory_fd, temporary, destination in records:
            os.link(temporary, destination, src_dir_fd=directory_fd, dst_dir_fd=directory_fd, follow_symlinks=False)
            info = os.stat(destination, dir_fd=directory_fd, follow_symlinks=False)
            published.append((directory_fd, destination, info.st_dev, info.st_ino))
    except Exception:
        # Roll back only links we created, if their inode still matches.
        for fd, name, dev, ino in reversed(published):
            try:
                info = os.stat(name, dir_fd=fd, follow_symlinks=False)
                if info.st_dev == dev and info.st_ino == ino:
                    os.unlink(name, dir_fd=fd)
            except FileNotFoundError:
                pass  # Already absent; no existing user file is touched.
        raise
    finally:
        for directory_fd, temporary, _ in records:
            try:
                os.unlink(temporary, dir_fd=directory_fd)
            except FileNotFoundError:
                pass  # Our task-created temporary entry is already absent.
        for fd in directories.values():
            os.close(fd)
    return paths
