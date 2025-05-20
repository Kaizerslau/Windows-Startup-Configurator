# Windows Startup Configurator

A configurable Windows startup manager that allows you to automatically launch programs with customizable delays. Features include system tray notifications and registry-based autostart.

## Features

- 🚀 Automatic program launching at Windows startup
- ⏱️ Configurable delays between program launches
- 🔔 System tray notifications for program status
- 🔧 Easy configuration through JSON file
- 🔐 Registry-based autostart (no admin rights required)
- 🗑️ Simple uninstallation

## Installation

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Windows-Startup-Configurator.git
   cd Windows-Startup-Configurator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your programs in `config.json`:
   ```json
   {
     "Delay": 2,
     "Programs": [
       {
         "Name": "Notepad",
         "Path": "C:\\Windows\\notepad.exe",
         "Enabled": true
       }
     ]
   }
   ```

4. Run the registration script:
   ```bash
   python register_task.py
   ```

### From Release

1. Download the latest release from the [Releases](https://github.com/Kaizerslau/Windows-Startup-Configurator/releases) page
2. Extract the archive
3. Edit `config.json` to add your programs
4. Run `register_task.exe`

## Configuration

The `config.json` file supports the following options:

- `Delay`: Time in seconds to wait between program launches
- `Programs`: Array of program configurations
  - `Name`: Display name of the program
  - `Path`: Full path to the program executable
  - `Enabled`: Whether to launch the program (optional, defaults to true)

## Usage

- `start_programs.py`: Main script that launches programs
- `register_task.py`: Registers the program for autostart
- `uninstall.py`: Removes the program from autostart

## Building from Source

To build executable files:

```bash
pyinstaller --noconsole start_programs.py
pyinstaller --noconsole register_task.py
pyinstaller --noconsole uninstall.py
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Security

This program uses the Windows Registry for autostart configuration. It does not require administrator privileges and only modifies the current user's registry settings.

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/Kaizerslau/Windows-Startup-Configurator/issues).
