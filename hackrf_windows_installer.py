#!/usr/bin/env python3
"""
HackRF Windows Installation Helper
Automated installer for HackRF tools on Windows
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
import tempfile
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HackRFWindowsInstaller:
    """Install HackRF tools on Windows"""
    
    def __init__(self):
        self.tools_dir = Path("C:/Program Files/HackRF")
        self.download_urls = {
            'hackrf_tools': 'https://github.com/greatscottgadgets/hackrf/releases/download/v2024.02.1/hackrf-tools-win64.zip',
            'zadig_driver': 'https://github.com/pbatard/libwdi/releases/download/b730/zadig-2.5.exe'
        }
        
    def check_admin_rights(self):
        """Check if running with admin privileges"""
        try:
            return os.getuid() == 0
        except AttributeError:
            # Windows
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
    
    def download_file(self, url, filename):
        """Download file from URL"""
        logger.info(f"Downloading {filename}...")
        
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.tmp') as tmp_file:
                urllib.request.urlretrieve(url, tmp_file.name)
                return tmp_file.name
        except Exception as e:
            logger.error(f"Download failed: {e}")
            return None
    
    def install_hackrf_tools(self):
        """Install HackRF command line tools"""
        logger.info("Installing HackRF tools...")
        
        # Download tools
        zip_file = self.download_file(
            self.download_urls['hackrf_tools'], 
            'hackrf-tools-win64.zip'
        )
        
        if not zip_file:
            return False
        
        try:
            # Create tools directory
            self.tools_dir.mkdir(parents=True, exist_ok=True)
            
            # Extract tools
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(self.tools_dir)
            
            # Add to PATH
            self.add_to_path(str(self.tools_dir))
            
            logger.info(f"HackRF tools installed to: {self.tools_dir}")
            return True
            
        except Exception as e:
            logger.error(f"Installation failed: {e}")
            return False
        finally:
            # Cleanup
            if os.path.exists(zip_file):
                os.unlink(zip_file)
    
    def add_to_path(self, directory):
        """Add directory to Windows PATH"""
        try:
            # Get current PATH
            import winreg
            
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
                0,
                winreg.KEY_ALL_ACCESS
            )
            
            current_path, _ = winreg.QueryValueEx(key, "PATH")
            
            if directory not in current_path:
                new_path = current_path + ";" + directory
                winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
                logger.info(f"Added {directory} to PATH")
            
            winreg.CloseKey(key)
            
        except Exception as e:
            logger.warning(f"Could not update PATH: {e}")
            logger.info(f"Manually add to PATH: {directory}")
    
    def install_drivers(self):
        """Install HackRF USB drivers using Zadig"""
        logger.info("Installing USB drivers...")
        
        # Download Zadig
        zadig_file = self.download_file(
            self.download_urls['zadig_driver'],
            'zadig.exe'
        )
        
        if zadig_file:
            logger.info("Zadig downloaded. Please run manually to install drivers:")
            logger.info(f"File location: {zadig_file}")
            logger.info("Instructions:")
            logger.info("1. Run Zadig as Administrator")
            logger.info("2. Connect HackRF device")
            logger.info("3. Select HackRF One device")
            logger.info("4. Install WinUSB driver")
            
            # Try to open Zadig
            try:
                subprocess.Popen([zadig_file])
            except Exception as e:
                logger.warning(f"Could not auto-launch Zadig: {e}")
        
        return zadig_file is not None
    
    def verify_installation(self):
        """Verify HackRF installation"""
        logger.info("Verifying installation...")
        
        try:
            # Test hackrf_info
            result = subprocess.run(['hackrf_info'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                logger.info("✅ hackrf_info working - device detected!")
                print(result.stdout)
                return True
            else:
                logger.warning("⚠️ hackrf_info found but no device detected")
                logger.info("Make sure:")
                logger.info("1. HackRF is connected to USB")
                logger.info("2. USB drivers are installed (use Zadig)")
                logger.info("3. Device shows in Windows Device Manager")
                return False
                
        except FileNotFoundError:
            logger.error("❌ hackrf_info not found in PATH")
            logger.info("Installation may have failed or PATH not updated")
            return False
        except subprocess.TimeoutExpired:
            logger.warning("⚠️ hackrf_info timeout - driver issue?")
            return False
    
    def install(self):
        """Complete installation process"""
        print("HackRF Windows Installation Helper")
        print("=" * 40)
        
        if not self.check_admin_rights():
            print("⚠️ Warning: Not running as Administrator")
            print("Some operations may fail. Consider running as Admin.")
        
        # Install tools
        if self.install_hackrf_tools():
            print("✅ HackRF tools installed")
        else:
            print("❌ HackRF tools installation failed")
            return False
        
        # Install drivers
        if self.install_drivers():
            print("✅ Driver installer downloaded")
        else:
            print("❌ Driver download failed")
        
        # Verify
        print("\nVerifying installation...")
        success = self.verify_installation()
        
        if success:
            print("🎉 Installation successful!")
        else:
            print("⚠️ Installation completed but device not detected")
            print("Please check USB connection and drivers")
        
        return success

def main():
    """Main installation function"""
    installer = HackRFWindowsInstaller()
    installer.install()
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()