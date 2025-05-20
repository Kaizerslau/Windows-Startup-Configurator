# Windows-Startup-Launcher

A simple Windows application to automatically launch programs on startup.

## Installation

1. Extract the archive to a convenient location
2. Run `register_task.exe` as administrator to register autostart
3. Configure the list of programs in the `config.json` file

## Configuration

Edit the `config.json` file to configure the list of programs:

```json
[
    {
        "Name": "Program Name",
        "Path": "C:\\path\\to\\program.exe",
        "Delay": 2,
        "Enabled": true
    }
]
```

Parameters:
- `Name` - Display name of the program
- `Path` - Full path to the executable file
- `Delay` - Delay before launching in seconds
- `Enabled` - Enable/disable autostart for the program

## Uninstallation

1. Run `uninstall.exe` to remove the autostart task
2. Delete the program folder 
