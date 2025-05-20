#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Windows Startup Configurator - Uninstaller
----------------------------------------
This script removes the program from Windows autostart registry.
It cleans up the registry entry created by register_task.py.

Author: @kaizerslau
License: Apache License 2.0
"""

import sys
import os
import winreg
from typing import Optional
from win10toast import ToastNotifier

class Uninstaller:
    """Handles program uninstallation by removing registry entries."""
    
    def __init__(self):
        """Initialize the uninstaller."""
        self.notifier = ToastNotifier()
        self.app_name = "WindowsStartupConfigurator"
    
    def notify(self, title, message):
        """
        Display a system tray notification.
        
        Args:
            title (str): Notification title
            message (str): Notification message
        """
        try:
            self.notifier.show_toast(title, message, icon_path='')
        except Exception as e:
            print(f"Error showing notification: {e}")
    
    def unregister_autostart(self):
        """
        Remove the program from Windows autostart.
        
        Returns:
            bool: True if uninstallation was successful, False otherwise
        """
        # Registry key for user autostart programs
        run_key = r"Software\Microsoft\Windows\CurrentVersion\Run"

        try:
            # Open the registry key with write access
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, run_key, 0, winreg.KEY_SET_VALUE)

            # Delete the registry value
            winreg.DeleteValue(key, self.app_name)

            # Close the registry key
            winreg.CloseKey(key)

            print(f"Successfully unregistered '{self.app_name}' from autostart.")
            self.notify("Autostart Uninstallation", f"'{self.app_name}' unregistered successfully from autostart.")

        except FileNotFoundError:
            print(f"Autostart entry for '{self.app_name}' not found in registry. Nothing to uninstall.")
            self.notify("Autostart Uninstallation", f"Autostart entry for '{self.app_name}' not found. Nothing to uninstall.")
        except Exception as e:
            print(f"Error unregistering from autostart: {e}")
            self.notify("Autostart Uninstallation", f"Failed to unregister '{self.app_name}' from autostart: {e}")

def main() -> None:
    """Main entry point of the script."""
    try:
        uninstaller = Uninstaller()
        uninstaller.unregister_autostart()
    except Exception as e:
        print(f"Fatal error: {str(e)}")
    finally:
        input("Press Enter to exit...")

if __name__ == "__main__":
    main() 
