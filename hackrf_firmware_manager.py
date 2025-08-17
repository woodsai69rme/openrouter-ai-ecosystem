#!/usr/bin/env python3
"""
HackRF Firmware Manager
Legitimate firmware update and device management for HackRF One
"""

import os
import sys
import json
import requests
import hashlib
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HackRFFirmwareManager:
    """HackRF firmware management and updates"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.firmware_info = {
            'current_version': 'Unknown',
            'latest_version': None,
            'device_serial': 'Unknown',
            'device_board_id': 'Unknown'
        }
        
        # Official HackRF firmware sources
        self.firmware_sources = {
            'official': {
                'name': 'Official HackRF Firmware',
                'url': 'https://api.github.com/repos/greatscottgadgets/hackrf/releases/latest',
                'description': 'Official firmware from Great Scott Gadgets'
            }
        }
        
        self.create_gui()
        
    def create_gui(self):
        """Create firmware manager GUI"""
        self.window = tk.Toplevel(self.parent) if self.parent else tk.Tk()
        self.window.title("HackRF Firmware Manager")
        self.window.geometry("600x500")
        self.window.configure(bg='#2b2b2b')
        
        # Main frame
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Device info frame
        info_frame = ttk.LabelFrame(main_frame, text="Device Information")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        info_grid = ttk.Frame(info_frame)
        info_grid.pack(fill=tk.X, padx=10, pady=10)
        
        # Device info labels
        ttk.Label(info_grid, text="Current Firmware:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.current_fw_label = ttk.Label(info_grid, text="Unknown", foreground='orange')
        self.current_fw_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        ttk.Label(info_grid, text="Device Serial:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.serial_label = ttk.Label(info_grid, text="Unknown")
        self.serial_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        ttk.Label(info_grid, text="Board ID:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.board_label = ttk.Label(info_grid, text="Unknown")
        self.board_label.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        ttk.Button(info_grid, text="Refresh Device Info", command=self.refresh_device_info).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Firmware update frame
        update_frame = ttk.LabelFrame(main_frame, text="Firmware Updates")
        update_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Check for updates
        check_frame = ttk.Frame(update_frame)
        check_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(check_frame, text="Check for Updates", command=self.check_for_updates).pack(side=tk.LEFT)
        self.update_status_label = ttk.Label(check_frame, text="Click to check for updates")
        self.update_status_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Available updates list
        list_frame = ttk.Frame(update_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        ttk.Label(list_frame, text="Available Firmware:").pack(anchor=tk.W)
        
        self.firmware_tree = ttk.Treeview(list_frame, columns=('Version', 'Size', 'Date'), show='headings', height=6)
        self.firmware_tree.heading('Version', text='Version')
        self.firmware_tree.heading('Size', text='Size')
        self.firmware_tree.heading('Date', text='Release Date')
        
        self.firmware_tree.column('Version', width=150)
        self.firmware_tree.column('Size', width=100)
        self.firmware_tree.column('Date', width=150)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.firmware_tree.yview)
        self.firmware_tree.configure(yscrollcommand=scrollbar.set)
        
        self.firmware_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Update buttons
        button_frame = ttk.Frame(update_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Download Selected", command=self.download_firmware).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Install Firmware", command=self.install_firmware).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Backup Current", command=self.backup_firmware).pack(side=tk.LEFT, padx=5)
        
        # Advanced options frame
        advanced_frame = ttk.LabelFrame(main_frame, text="Advanced Options")
        advanced_frame.pack(fill=tk.X)
        
        adv_buttons = ttk.Frame(advanced_frame)
        adv_buttons.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(adv_buttons, text="Enter DFU Mode", command=self.enter_dfu_mode).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(adv_buttons, text="Reset Device", command=self.reset_device).pack(side=tk.LEFT, padx=5)
        ttk.Button(adv_buttons, text="Load Custom Firmware", command=self.load_custom_firmware).pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(10, 0))
        
    def refresh_device_info(self):
        """Refresh device information"""
        logger.info("Refreshing device information...")
        
        try:
            # Try to get hackrf_info output
            result = subprocess.run(['hackrf_info'], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                output = result.stdout
                
                # Parse hackrf_info output
                for line in output.split('\n'):
                    if 'firmware version' in line.lower():
                        version = line.split(':')[-1].strip()
                        self.firmware_info['current_version'] = version
                        self.current_fw_label.config(text=version, foreground='green')
                        
                    elif 'serial number' in line.lower():
                        serial = line.split(':')[-1].strip()
                        self.firmware_info['device_serial'] = serial
                        self.serial_label.config(text=serial)
                        
                    elif 'board id' in line.lower():
                        board_id = line.split(':')[-1].strip()
                        self.firmware_info['device_board_id'] = board_id
                        self.board_label.config(text=board_id)
                        
                logger.info("Device information updated successfully")
                
            else:
                logger.error("hackrf_info command failed")
                messagebox.showerror("Error", "Could not retrieve device information. Is HackRF connected?")
                
        except subprocess.TimeoutExpired:
            logger.error("hackrf_info command timed out")
            messagebox.showerror("Error", "Device information request timed out")
            
        except FileNotFoundError:
            logger.error("hackrf_info command not found")
            messagebox.showerror("Error", "hackrf_info tool not found. Please install HackRF tools.")
            
        except Exception as e:
            logger.error(f"Error refreshing device info: {e}")
            messagebox.showerror("Error", f"Failed to get device information: {str(e)}")
            
    def check_for_updates(self):
        """Check for firmware updates"""
        logger.info("Checking for firmware updates...")
        self.progress.start()
        self.update_status_label.config(text="Checking for updates...")
        
        try:
            # Clear existing entries
            for item in self.firmware_tree.get_children():
                self.firmware_tree.delete(item)
                
            # Check official firmware repository
            response = requests.get(self.firmware_sources['official']['url'], timeout=10)
            
            if response.status_code == 200:
                release_data = response.json()
                
                version = release_data['tag_name']
                date = release_data['published_at'][:10]  # Just the date part
                
                # Look for firmware files in assets
                for asset in release_data.get('assets', []):
                    if asset['name'].endswith('.bin') or 'firmware' in asset['name'].lower():
                        size = f"{asset['size'] / 1024:.1f} KB"
                        
                        self.firmware_tree.insert('', tk.END, values=(
                            f"{version} - {asset['name']}", 
                            size, 
                            date
                        ), tags=(asset['browser_download_url'],))
                        
                self.firmware_info['latest_version'] = version
                self.update_status_label.config(text=f"Latest version: {version}")
                
                # Check if update available
                if self.firmware_info['current_version'] != 'Unknown':
                    if version != self.firmware_info['current_version']:
                        self.update_status_label.config(text=f"Update available: {version}", foreground='orange')
                    else:
                        self.update_status_label.config(text="Firmware is up to date", foreground='green')
                        
                logger.info(f"Found firmware version: {version}")
                
            else:
                logger.error(f"Failed to check for updates: HTTP {response.status_code}")
                self.update_status_label.config(text="Failed to check for updates", foreground='red')
                
        except requests.RequestException as e:
            logger.error(f"Network error checking for updates: {e}")
            self.update_status_label.config(text="Network error", foreground='red')
            
        except Exception as e:
            logger.error(f"Error checking for updates: {e}")
            self.update_status_label.config(text="Error checking updates", foreground='red')
            
        finally:
            self.progress.stop()
            
    def download_firmware(self):
        """Download selected firmware"""
        selection = self.firmware_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select firmware to download")
            return
            
        item = self.firmware_tree.item(selection[0])
        download_url = self.firmware_tree.item(selection[0])['tags'][0]
        filename = download_url.split('/')[-1]
        
        # Ask user where to save
        save_path = filedialog.asksaveasfilename(
            initialname=filename,
            defaultextension=".bin",
            filetypes=[("Firmware files", "*.bin"), ("All files", "*.*")]
        )
        
        if not save_path:
            return
            
        logger.info(f"Downloading firmware from {download_url}")
        self.progress.start()
        
        try:
            response = requests.get(download_url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
            logger.info(f"Firmware downloaded successfully to {save_path}")
            messagebox.showinfo("Success", f"Firmware downloaded to:\n{save_path}")
            
        except Exception as e:
            logger.error(f"Error downloading firmware: {e}")
            messagebox.showerror("Error", f"Failed to download firmware:\n{str(e)}")
            
        finally:
            self.progress.stop()
            
    def install_firmware(self):
        """Install firmware to device"""
        firmware_file = filedialog.askopenfilename(
            title="Select firmware file",
            filetypes=[("Firmware files", "*.bin"), ("All files", "*.*")]
        )
        
        if not firmware_file:
            return
            
        # Confirm installation
        result = messagebox.askyesno(
            "Confirm Firmware Installation",
            f"This will flash firmware to your HackRF device.\n\n"
            f"File: {Path(firmware_file).name}\n"
            f"Size: {Path(firmware_file).stat().st_size} bytes\n\n"
            f"WARNING: Incorrect firmware can damage your device!\n\n"
            f"Continue with installation?"
        )
        
        if not result:
            return
            
        logger.info(f"Installing firmware: {firmware_file}")
        self.progress.start()
        
        try:
            # Use hackrf_spiflash to install firmware
            cmd = ['hackrf_spiflash', '-w', firmware_file]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                logger.info("Firmware installation completed successfully")
                messagebox.showinfo("Success", 
                    "Firmware installed successfully!\n\n"
                    "Please disconnect and reconnect your HackRF device.")
            else:
                logger.error(f"Firmware installation failed: {result.stderr}")
                messagebox.showerror("Error", 
                    f"Firmware installation failed:\n{result.stderr}")
                
        except subprocess.TimeoutExpired:
            logger.error("Firmware installation timed out")
            messagebox.showerror("Error", "Firmware installation timed out")
            
        except FileNotFoundError:
            logger.error("hackrf_spiflash command not found")
            messagebox.showerror("Error", 
                "hackrf_spiflash tool not found.\n"
                "Please install HackRF tools.")
                
        except Exception as e:
            logger.error(f"Error installing firmware: {e}")
            messagebox.showerror("Error", f"Failed to install firmware:\n{str(e)}")
            
        finally:
            self.progress.stop()
            
    def backup_firmware(self):
        """Backup current firmware"""
        backup_file = filedialog.asksaveasfilename(
            defaultextension=".bin",
            filetypes=[("Firmware files", "*.bin"), ("All files", "*.*")],
            initialname=f"hackrf_firmware_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bin"
        )
        
        if not backup_file:
            return
            
        logger.info(f"Backing up firmware to: {backup_file}")
        self.progress.start()
        
        try:
            # Use hackrf_spiflash to read current firmware
            cmd = ['hackrf_spiflash', '-r', backup_file]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                logger.info("Firmware backup completed successfully")
                messagebox.showinfo("Success", f"Firmware backed up to:\n{backup_file}")
            else:
                logger.error(f"Firmware backup failed: {result.stderr}")
                messagebox.showerror("Error", f"Firmware backup failed:\n{result.stderr}")
                
        except Exception as e:
            logger.error(f"Error backing up firmware: {e}")
            messagebox.showerror("Error", f"Failed to backup firmware:\n{str(e)}")
            
        finally:
            self.progress.stop()
            
    def enter_dfu_mode(self):
        """Enter DFU (Device Firmware Update) mode"""
        result = messagebox.askyesno(
            "Enter DFU Mode",
            "This will put the HackRF into DFU mode for firmware updates.\n\n"
            "The device will need to be reset after firmware operations.\n\n"
            "Continue?"
        )
        
        if result:
            try:
                subprocess.run(['hackrf_debug', '--dfu'], timeout=10)
                messagebox.showinfo("DFU Mode", "Device should now be in DFU mode")
                logger.info("Device entered DFU mode")
                
            except Exception as e:
                logger.error(f"Error entering DFU mode: {e}")
                messagebox.showerror("Error", f"Failed to enter DFU mode:\n{str(e)}")
                
    def reset_device(self):
        """Reset HackRF device"""
        result = messagebox.askyesno(
            "Reset Device",
            "This will reset the HackRF device.\n\n"
            "Continue?"
        )
        
        if result:
            try:
                subprocess.run(['hackrf_debug', '--reset'], timeout=10)
                messagebox.showinfo("Reset", "Device reset command sent")
                logger.info("Device reset")
                
            except Exception as e:
                logger.error(f"Error resetting device: {e}")
                messagebox.showerror("Error", f"Failed to reset device:\n{str(e)}")
                
    def load_custom_firmware(self):
        """Load custom firmware file"""
        firmware_file = filedialog.askopenfilename(
            title="Select custom firmware file",
            filetypes=[("Firmware files", "*.bin"), ("All files", "*.*")]
        )
        
        if firmware_file:
            result = messagebox.askyesno(
                "Custom Firmware Warning",
                f"You are about to install custom firmware:\n\n"
                f"{Path(firmware_file).name}\n\n"
                f"WARNING: Custom firmware may void warranty and could damage your device!\n"
                f"Only install firmware from trusted sources.\n\n"
                f"Continue at your own risk?"
            )
            
            if result:
                self.install_firmware_file(firmware_file)
                
    def install_firmware_file(self, firmware_file):
        """Install specific firmware file"""
        # This would call the same installation process as install_firmware
        # but with a pre-selected file
        pass

def main():
    """Main function for standalone firmware manager"""
    root = tk.Tk()
    app = HackRFFirmwareManager()
    
    logger.info("HackRF Firmware Manager started")
    root.mainloop()

if __name__ == "__main__":
    main()