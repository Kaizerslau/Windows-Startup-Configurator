#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Windows Startup Configurator - Program Launcher
----------------------------------------------
This script launches programs specified in config.json with customizable delays.
It provides system tray notifications for program status and errors.

Author: @kaizerslau
License: Apache License 2.0
"""

import json
import time
import subprocess
import os
from typing import Dict, List, Optional
from win10toast import ToastNotifier

class ProgramLauncher:
    """Handles program launching with notifications and error handling."""
    
    def __init__(self, config_file='config.json'):
        """
        Initialize the program launcher.
        
        Args:
            config_file (str): Path to the configuration file
        """
        self.config_file = config_file
        self.notifier = ToastNotifier()
    
    def read_config(self):
        """
        Read and validate configuration from JSON file.
        
        Returns:
            List: List of program configurations
        
        Raises:
            FileNotFoundError: If config file doesn't exist
            json.JSONDecodeError: If config file is invalid JSON
        """
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('Programs', []) # Expecting a list of programs under 'Programs' key
        except FileNotFoundError:
            self.notify("Configuration Error", f"Configuration file '{self.config_file}' not found.")
            return None
        except json.JSONDecodeError:
            self.notify("Configuration Error", f"Could not decode JSON from '{self.config_file}'. Check file format.")
            return None
        except Exception as e:
            self.notify("Configuration Error", f"An unexpected error occurred: {e}")
            return None
    
    def is_program_enabled(self, program):
        """
        Check if a program is enabled.
        
        Args:
            program (Dict): Program configuration dictionary
        
        Returns:
            bool: True if the program is enabled, False otherwise
        """
        return program.get('Enabled', True) # Default to True if 'Enabled' is not specified
    
    def get_program_path(self, program):
        """
        Get the program path, expanding environment variables.
        
        Args:
            program (Dict): Program configuration dictionary
        
        Returns:
            str: Program path
        """
        path = program.get('Path')
        if path:
            return os.path.expandvars(path)
        return None
    
    def get_program_delay(self, program):
        """
        Get the delay before launching the program.
        
        Args:
            program (Dict): Program configuration dictionary
        
        Returns:
            float: Program delay in seconds
        """
        return program.get('Delay', 0) # Default delay is 0 seconds
    
    def launch_program(self, program):
        """
        Launch a single program with error handling.
        
        Args:
            program (Dict): Program configuration dictionary
        """
        name = program.get('Name', 'Unknown Program')
        path = self.get_program_path(program)
        delay = self.get_program_delay(program)

        if not path:
            print(f"Error: Path not specified for program '{name}'. Skipping.")
            self.notify("Launch Error", f"Path not specified for '{name}'. Skipping.")
            return

        print(f"Waiting for {delay} seconds before launching '{name}'...")
        time.sleep(delay)

        print(f"Launching '{name}' from '{path}'...")
        try:
            subprocess.Popen([path])
            self.notify("Program Launched", f"'{name}' launched successfully.")
        except FileNotFoundError:
            print(f"Error: Program file not found at '{path}'. Skipping.")
            self.notify("Launch Error", f"Program file not found for '{name}'. Skipping.")
        except Exception as e:
            print(f"An unexpected error occurred while launching '{name}': {e}")
            self.notify("Launch Error", f"An unexpected error occurred while launching '{name}': {e}")
    
    def notify(self, title, message):
        """
        Display a system tray notification.
        
        Args:
            title (str): Notification title
            message (str): Notification message
        """
        try:
            self.notifier.show_toast(title, message, icon_path='') # Added icon_path=''
        except Exception as e:
            print(f"Error showing notification: {e}")
    
    def run(self):
        """
        Launch all enabled programs with configured delays.
        """
        print("Windows Startup Configurator: Starting program launch...")
        self.notify("Startup Configurator", "Starting program launch...")

        config = self.read_config()
        if config is None:
            print("Failed to read configuration. Aborting.")
            self.notify("Startup Configurator", "Failed to read configuration. Aborting.")
            return

        if not config:
            print("No programs found in the configuration file.")
            self.notify("Startup Configurator", "No programs found in configuration.")
            return

        for program in config:
            if self.is_program_enabled(program):
                self.launch_program(program)
            else:
                name = program.get('Name', 'Unknown Program')
                print(f"Program '{name}' is disabled. Skipping.")
                self.notify("Startup Configurator", f"'{name}' is disabled. Skipping.")

        print("Windows Startup Configurator: Program launch finished.")
        self.notify("Startup Configurator", "Program launch finished.")

def main() -> None:
    """Main entry point of the script."""
    try:
        launcher = ProgramLauncher()
        launcher.run()
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main() 
