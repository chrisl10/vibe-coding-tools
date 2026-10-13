#!/usr/bin/env python3
"""Synthetic SQLite mechanics in task-owned temporary files; no Tauri/native acceptance."""
import json
import sqlite3
import tempfile
from pathlib import Path


def exercise():
    results = []
    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        results.append(name)
    with tempfile.TemporaryDirectory(prefix='wasp-synthetic-sqlite-') as folder:
        root = Path(folder)
        db = sqlite3.connect(root / 'owned.db', timeout=0)
        restored = None
        other = None
        try:
            db.execute('CREATE TABLE notes(id INTEGER PRIMARY KEY, body TEXT NOT NULL)')
            db.execute('INSERT INTO notes VALUES (?,?)', (1, 'SYNTHETIC_CANARY'))
            db.execute('PRAGMA user_version=1')
            db.commit()
            check('schema-one', db.execute('PRAGMA user_version').fetchone()[0] == 1)
            backup = sqlite3.connect(root / 'owned-backup.db')
            try:
                db.backup(backup)
                check('backup-integrity', backup.execute('PRAGMA integrity_check').fetchone()[0] == 'ok')
                check('backup-has-original-row', backup.execute('SELECT body FROM notes').fetchone()[0] == 'SYNTHETIC_CANARY')
            finally:
                backup.close()
            try:
                db.execute('BEGIN IMMEDIATE')
                db.execute('ALTER TABLE notes ADD COLUMN status TEXT')
                db.execute('INSERT INTO missing_table VALUES (1)')
            except sqlite3.OperationalError:
                db.rollback()
            else:
                raise AssertionError('expected invalid migration to fail')
            check('failed-ddl-rolled-back', [r[1] for r in db.execute('PRAGMA table_info(notes)')] == ['id', 'body'])
            check('failed-row-retained', db.execute('SELECT count(*) FROM notes').fetchone()[0] == 1)
            check('failed-version-retained', db.execute('PRAGMA user_version').fetchone()[0] == 1)
            db.execute('BEGIN IMMEDIATE')
            db.execute('ALTER TABLE notes ADD COLUMN status TEXT')
            db.execute('PRAGMA user_version=2')
            db.commit()
            check('successful-schema-two', db.execute('PRAGMA user_version').fetchone()[0] == 2)
            check('unknown-backfill-remains-null', db.execute('SELECT status FROM notes').fetchone()[0] is None)
            if db.execute('PRAGMA user_version').fetchone()[0] == 1:
                raise AssertionError('version guard should prevent repeated ALTER')
            check('reopen-guard-avoids-duplicate-alter', [r[1] for r in db.execute('PRAGMA table_info(notes)')].count('status') == 1)
            other = sqlite3.connect(root / 'owned.db', timeout=0)
            db.execute('BEGIN IMMEDIATE')
            try:
                other.execute('BEGIN IMMEDIATE')
            except sqlite3.OperationalError as exc:
                check('second-writer-busy', 'locked' in str(exc).lower())
            else:
                raise AssertionError('expected exclusive writer contention')
            db.rollback()
            other.execute('BEGIN IMMEDIATE')
            other.rollback()
            check('writer-can-retry-after-owner-release', not other.in_transaction)
            restored = sqlite3.connect(root / 'owned-backup.db')
            check('backup-still-schema-one', restored.execute('PRAGMA user_version').fetchone()[0] == 1)
            check('restore-source-integrity', restored.execute('PRAGMA integrity_check').fetchone()[0] == 'ok')
            check('restore-source-exact-row', restored.execute('SELECT id,body FROM notes').fetchall() == [(1, 'SYNTHETIC_CANARY')])
        finally:
            if other is not None: other.close()
            if restored is not None: restored.close()
            db.close()
    return {'evidence_level': 'synthetic SQLite mechanics only', 'sqlite_version': sqlite3.sqlite_version,
            'checks': results, 'passed': len(results), 'native_tauri_acceptance': 'OPEN',
            'limitations': ['No Tauri SQL plugin execution', 'No crash or power-loss test',
                           'No actual consumer migration', 'No OS storage/vault proof',
                           'Backup opened for verification, not an app-level restore/reinstall']}


if __name__ == '__main__':
    print(json.dumps(exercise(), indent=2))
