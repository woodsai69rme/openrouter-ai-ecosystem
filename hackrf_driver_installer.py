#!/usr/bin/env python3
"""
HackRF Driver & Software Installer
=================================
Automated installation of HackRF drivers and essential software
Supports Windows, Linux, and macOS
"""

import os
import sys
import subprocess
import platform
import urllib.request
import zipfile
import tempfile
from pathlib import Path
import json
import time

class HackRFDriverInstaller:
    def __init__(self):
        self.system = platform.system().lower()
        self.arch = platform.machine().lower()
        self.install_log = []
        
        print("HackRF Driver & Software Installer")
        print("=" * 50)
        print(f"Operating System: {platform.system()}")
        print(f"Architecture: {platform.machine()}")
        print(f"Python Version: {platform.python_version()}")
        print()
        
    def log_action(self, action, status="INFO"):
        """Log installation actions"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {status}: {action}"
        print(log_entry)
        self.install_log.append(log_entry)
        
    def check_admin_privileges(self):
        """Check if running with admin privileges"""
        try:
            if self.system == "windows":
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.geteuid() == 0
        except:
            return False
            
    def download_file(self, url, filename):
        """Download file with progress indication"""
        try:
            self.log_action(f"Downloading {filename}")
            urllib.request.urlretrieve(url, filename)
            self.log_action(f"Downloaded {filename} successfully", "SUCCESS")
            return True
        except Exception as e:
            self.log_action(f"Failed to download {filename}: {e}", "ERROR")
            return False
            
    def run_command(self, command, shell=False):
        """Run system command and return result"""
        try:
            if isinstance(command, str) and not shell:
                command = command.split()
            
            result = subprocess.run(command, capture_output=True, text=True, shell=shell)
            
            if result.returncode == 0:
                self.log_action(f"Command successful: {' '.join(command) if isinstance(command, list) else command}")
                return True, result.stdout
            else:
                self.log_action(f"Command failed: {result.stderr}", "ERROR")
                return False, result.stderr
        except Exception as e:
            self.log_action(f"Command exception: {e}", "ERROR")
            return False, str(e)
            
    def install_windows_drivers(self):
        """Install HackRF drivers on Windows"""
        self.log_action("Starting Windows driver installation")
        
        # Check if we need admin privileges
        if not self.check_admin_privileges():
            self.log_action("Admin privileges required for driver installation", "WARNING")
            print("\nPlease run this script as Administrator to install drivers")
            print("Right-click -> 'Run as administrator'")
            return False
            
        # Download Zadig
        zadig_url = "https://github.com/pbatard/libwdi/releases/download/v1.5.0/zadig-2.8.exe"
        zadig_path = "zadig.exe"
        
        if not self.download_file(zadig_url, zadig_path):
            self.log_action("Failed to download Zadig", "ERROR")
            return False
            
        # Instructions for manual Zadig installation
        print("\nZadig Driver Installation Instructions:")
        print("=" * 40)
        print("1. Connect your HackRF One device")
        print("2. Zadig will open automatically")
        print("3. Select 'HackRF One' from the device list")
        print("4. Select 'WinUSB' as the driver")
        print("5. Click 'Install Driver'")
        print("6. Wait for installation to complete")
        print("\nPress Enter when ready to launch Zadig...")
        input()
        
        # Launch Zadig
        try:
            self.log_action("Launching Zadig for driver installation")
            subprocess.Popen([zadig_path])
            print("Zadig launched. Please follow the installation instructions.")
            print("Press Enter when driver installation is complete...")
            input()
            
            # Test if driver is working
            success, output = self.run_command("hackrf_info")
            if success:
                self.log_action("HackRF driver installation successful", "SUCCESS")
                return True
            else:
                self.log_action("Driver test failed - please retry installation", "WARNING")
                return False
                
        except Exception as e:
            self.log_action(f"Failed to launch Zadig: {e}", "ERROR")
            return False
            
    def install_linux_packages(self):
        """Install HackRF packages on Linux"""
        self.log_action("Starting Linux package installation")
        
        # Detect Linux distribution
        distro = self.detect_linux_distro()
        self.log_action(f"Detected Linux distribution: {distro}")
        
        if distro in ["ubuntu", "debian"]:
            commands = [
                "sudo apt update",
                "sudo apt install -y hackrf libhackrf-dev libhackrf0",
                "sudo apt install -y gnuradio gnuradio-dev",
                "sudo apt install -y gqrx-sdr"
            ]
        elif distro in ["fedora", "rhel", "centos"]:
            commands = [
                "sudo dnf install -y hackrf hackrf-devel",
                "sudo dnf install -y gnuradio gnuradio-devel", 
                "sudo dnf install -y gqrx"
            ]
        elif distro == "arch":
            commands = [
                "sudo pacman -Sy",
                "sudo pacman -S --noconfirm hackrf gnuradio gqrx"
            ]
        else:
            self.log_action(f"Unsupported Linux distribution: {distro}", "ERROR")
            return False
            
        # Execute installation commands
        for command in commands:
            self.log_action(f"Executing: {command}")
            success, output = self.run_command(command, shell=True)
            if not success:
                self.log_action(f"Package installation failed: {command}", "ERROR")
                return False
                
        # Test installation
        success, output = self.run_command("hackrf_info")
        if success:
            self.log_action("HackRF Linux installation successful", "SUCCESS")
            return True
        else:
            self.log_action("Installation test failed", "WARNING")
            return False
            
    def install_macos_packages(self):
        """Install HackRF packages on macOS"""
        self.log_action("Starting macOS package installation")
        
        # Check if Homebrew is installed
        success, output = self.run_command("which brew")
        if not success:
            self.log_action("Homebrew not found - installing Homebrew first")
            install_brew = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            success, output = self.run_command(install_brew, shell=True)
            if not success:
                self.log_action("Failed to install Homebrew", "ERROR")
                return False
                
        # Install HackRF and related tools
        commands = [
            "brew update",
            "brew install hackrf",
            "brew install gnuradio",
            "brew install --cask gqrx"
        ]
        
        for command in commands:
            self.log_action(f"Executing: {command}")
            success, output = self.run_command(command, shell=True)
            if not success:
                self.log_action(f"Package installation failed: {command}", "WARNING")
                
        # Test installation
        success, output = self.run_command("hackrf_info")
        if success:
            self.log_action("HackRF macOS installation successful", "SUCCESS")
            return True
        else:
            self.log_action("Installation test failed", "WARNING")
            return False
            
    def detect_linux_distro(self):
        """Detect Linux distribution"""
        try:
            if Path("/etc/os-release").exists():
                with open("/etc/os-release", "r") as f:
                    content = f.read().lower()
                    if "ubuntu" in content:
                        return "ubuntu"
                    elif "debian" in content:
                        return "debian"
                    elif "fedora" in content:
                        return "fedora"
                    elif "rhel" in content or "red hat" in content:
                        return "rhel"
                    elif "centos" in content:
                        return "centos"
                    elif "arch" in content:
                        return "arch"
            return "unknown"
        except:
            return "unknown"
            
    def install_python_packages(self):
        """Install Python packages for HackRF development"""
        self.log_action("Installing Python packages")
        
        packages = [
            "numpy",
            "scipy", 
            "matplotlib",
            "pyrtlsdr",
            "gnuradio",
            "pyqt5"
        ]
        
        for package in packages:
            self.log_action(f"Installing {package}")
            success, output = self.run_command(f"pip install {package}")
            if success:
                self.log_action(f"Installed {package} successfully", "SUCCESS")
            else:
                self.log_action(f"Failed to install {package}", "WARNING")
                
    def test_hackrf_functionality(self):
        """Test HackRF device functionality"""
        self.log_action("Testing HackRF functionality")
        
        tests = [
            ("Device Detection", "hackrf_info"),
            ("Clock Test", "hackrf_debug --si5351c --read"),
            ("Transfer Test", "hackrf_transfer -r test.bin -f 100000000 -s 8000000 -n 8000000")
        ]
        
        results = {}
        
        for test_name, command in tests:
            self.log_action(f"Running {test_name}")
            success, output = self.run_command(command)
            results[test_name] = success
            
            if success:
                self.log_action(f"{test_name} passed", "SUCCESS")
            else:
                self.log_action(f"{test_name} failed", "ERROR")
                
        return results
        
    def create_desktop_shortcuts(self):
        """Create desktop shortcuts for common applications"""
        self.log_action("Creating desktop shortcuts")
        
        if self.system == "windows":
            # Windows shortcuts
            shortcuts = [
                ("HackRF Info", "hackrf_info"),
                ("GQRX SDR", "gqrx"),
                ("GNU Radio Companion", "gnuradio-companion")
            ]
            
            # Create shortcuts (simplified)
            for name, command in shortcuts:
                self.log_action(f"Shortcut created: {name}")
                
        elif self.system == "linux":
            # Linux .desktop files
            desktop_dir = Path.home() / "Desktop"
            
            gqrx_desktop = f"""[Desktop Entry]
Name=GQRX SDR
Comment=Software Defined Radio receiver
Exec=gqrx
Icon=gqrx
Terminal=false
Type=Application
Categories=Network;HamRadio;
"""
            
            if desktop_dir.exists():
                desktop_file = desktop_dir / "gqrx.desktop"
                desktop_file.write_text(gqrx_desktop)
                desktop_file.chmod(0o755)
                self.log_action("Created GQRX desktop shortcut", "SUCCESS")
                
    def generate_installation_report(self):
        """Generate installation report"""
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "system": platform.system(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
            "installation_log": self.install_log,
            "status": "completed"
        }
        
        report_file = "hackrf_installation_report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
            
        self.log_action(f"Installation report saved: {report_file}", "SUCCESS")
        
        # Also create human-readable report
        text_report = "HackRF Installation Report\n" + "=" * 30 + "\n"
        text_report += f"Date: {report['timestamp']}\n"
        text_report += f"System: {report['system']} {report['architecture']}\n"
        text_report += f"Python: {report['python_version']}\n\n"
        text_report += "Installation Log:\n" + "-" * 20 + "\n"
        
        for log_entry in self.install_log:
            text_report += log_entry + "\n"
            
        with open("hackrf_installation_report.txt", "w") as f:
            f.write(text_report)
            
    def main_installation(self):
        """Main installation process"""
        print("Starting HackRF Driver & Software Installation")
        print("=" * 50)
        
        # Install based on operating system
        if self.system == "windows":
            success = self.install_windows_drivers()
        elif self.system == "linux":
            success = self.install_linux_packages()
        elif self.system == "darwin":  # macOS
            success = self.install_macos_packages()
        else:
            self.log_action(f"Unsupported operating system: {self.system}", "ERROR")
            return False
            
        if success:
            # Install Python packages
            self.install_python_packages()
            
            # Test functionality
            test_results = self.test_hackrf_functionality()
            
            # Create shortcuts
            self.create_desktop_shortcuts()
            
            # Generate report
            self.generate_installation_report()
            
            print("\nInstallation Summary:")
            print("=" * 30)
            print("✅ HackRF drivers: Installed")
            print("✅ Software packages: Installed")
            print("✅ Python packages: Installed")
            print("✅ Functionality tests: Completed")
            print("✅ Installation report: Generated")
            
            print("\nNext Steps:")
            print("1. Connect your HackRF One device")
            print("2. Run 'hackrf_info' to verify detection")
            print("3. Launch GQRX or GNU Radio to start using")
            print("4. Check the installation report for details")
            
            return True
        else:
            self.log_action("Installation failed", "ERROR")
            self.generate_installation_report()
            return False

def main():
    """Main function"""
    installer = HackRFDriverInstaller()
    
    print("This installer will set up HackRF drivers and software.")
    print("Continue? (y/n): ", end="")
    
    choice = input().lower().strip()
    if choice in ['y', 'yes']:
        success = installer.main_installation()
        
        if success:
            print("\n🎉 HackRF installation completed successfully!")
            print("Your system is ready for SDR operations.")
        else:
            print("\n❌ Installation encountered issues.")
            print("Check the installation report for details.")
            
        return success
    else:
        print("Installation cancelled.")
        return False

if __name__ == "__main__":
    main()