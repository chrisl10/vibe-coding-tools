# Electron applications, distilled on 2026-09-05

| Claim | Evidence |
|---|---|
| Remote-content renderers should not have Node integration; preload plus `contextBridge` is the documented constrained alternative. | [raw/electron-security.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/backend-and-desktop-tools/skills/electron-app-stinger/references/research/raw/electron-security.md) |
| The IPC tutorial uses a named `ipcMain.handle` and a narrow preload method rather than exposing full `ipcRenderer`. | [raw/electron-ipc.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/backend-and-desktop-tools/skills/electron-app-stinger/references/research/raw/electron-ipc.md) |
| Electron warns that exposing full `ipcRenderer` or an event sender can leak more authority to renderer code. | [raw/electron-ipc.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/backend-and-desktop-tools/skills/electron-app-stinger/references/research/raw/electron-ipc.md) |

The Electron release version and platform support are mutable. Refresh the official docs before asserting either.
