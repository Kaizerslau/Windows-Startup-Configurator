#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Windows Startup Configurator - Autostart Registration
---------------------------------------------------
This script registers the program launcher in Windows Registry for autostart.
It uses the Windows Registry API to create a startup entry.

Author: @kaizerslau
License: Apache License 2.0
"""

import os
import sys
import winreg
import time
import subprocess
from typing import Optional
from win10toast import ToastNotifier

class AutostartManager:
    """Manages Windows autostart registration using Registry."""
    
    def __init__(self):
        """Initialize the autostart manager."""
        self.notifier = ToastNotifier()
        self.startup_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        self.app_name = "WindowsStartupConfigurator"
    
    def _get_script_path(self) -> Optional[str]:
        """
        Get the absolute path to the launcher script.
        
        Returns:
            Optional[str]: Absolute path to the script or None if not found
        """
        try:
            # Get the directory of the current script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Construct path to start_programs.py
            script_path = os.path.join(script_dir, "start_programs.py")
            
            if not os.path.exists(script_path):
                self._show_error(
                    "Script not found",
                    f"Could not find: {script_path}"
                )
                return None
                
            return script_path
            
        except Exception as e:
            self._show_error(
                "Path Error",
                f"Failed to get script path: {str(e)}"
            )
            return None
    
    def _show_notification(self, title: str, message: str) -> None:
        """
        Display a system tray notification.
        
        Args:
            title (str): Notification title
            message (str): Notification message
        """
        self.notifier.show_toast(
            title,
            message,
            icon_path='',
            duration=5,
            threaded=True
        )
    
    def _show_error(self, title: str, message: str) -> None:
        """
        Display an error notification.
        
        Args:
            title (str): Error title
            message (str): Error message
        """
        self._show_notification(f"Error: {title}", message)
    
    def register(self, executable_path: str) -> bool:
        """
        Register the program for autostart in Windows Registry.
        
        Args:
            executable_path (str): Full path to the executable to register.
        
        Returns:
            bool: True if registration was successful, False otherwise
        """
        try:
            # Create the command to run the executable directly
            command = f'"{executable_path}"'
            
            # Open the registry key
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                self.startup_key,
                0,
                winreg.KEY_SET_VALUE
            )
            
            # Set the value
            winreg.SetValueEx(
                key,
                self.app_name,
                0,
                winreg.REG_SZ,
                command
            )
            
            # Close the key
            winreg.CloseKey(key)
            
            self._show_notification(
                "Registration Successful",
                "Program registered for autostart"
            )
            return True
            
        except Exception as e:
            self._show_error(
                "Registration Error",
                f"Failed to register program: {str(e)}"
            )
            return False

def main() -> None:
    """Main entry point of the script."""
    try:
        manager = AutostartManager()

        # Determine the path to WindowsStartupConfigurator.exe relative to register_task.exe
        startup_executable_path = os.path.join(os.path.dirname(sys.executable), 'WindowsStartupConfigurator.exe')

        # Check if the executable exists
        if not os.path.exists(startup_executable_path):
             manager._show_error(
                "Executable not found",
                f"Could not find: {startup_executable_path}"
             )
             print(f"Error: {startup_executable_path} not found.")
             # Add a small delay before exiting so the user can see the message
             time.sleep(5)
             return # Exit if the file is not found


        # Register WindowsStartupConfigurator.exe for autostart
        if manager.register(startup_executable_path):
            print(f"Program {startup_executable_path} successfully registered for autostart")
        else:
            print("Failed to register program for autostart")

        # Keep the window open briefly to show messages
        time.sleep(5)

    except Exception as e:
        print(f"Fatal error: {str(e)}")
        # Also add a delay for fatal errors
        time.sleep(10)


if __name__ == "__main__":
    main() 
