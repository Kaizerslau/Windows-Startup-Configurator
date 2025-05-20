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
    
    def register(self) -> bool:
        """
        Register the program for autostart in Windows Registry.
        
        Returns:
            bool: True if registration was successful, False otherwise
        """
        try:
            script_path = self._get_script_path()
            if not script_path:
                return False
            
            # Create the command to run the script with Python
            python_exe = sys.executable
            command = f'"{python_exe}" "{script_path}"'
            
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
        if manager.register():
            print("Program successfully registered for autostart")
        else:
            print("Failed to register program for autostart")
    except Exception as e:
        print(f"Fatal error: {str(e)}")
    finally:
        input("Press Enter to exit...")

if __name__ == "__main__":
    main() 
