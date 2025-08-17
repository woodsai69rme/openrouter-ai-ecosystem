#!/usr/bin/env python3
"""
HackRF Device Checker
Simple tool to check HackRF device status and troubleshoot issues
"""

import subprocess
import sys
import os
import platform

def check_system():
    """Check system information"""
    print("System Information:")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print(f"Architecture: {platform.machine()}")
    print()

def check_hackrf_tools():
    """Check if HackRF tools are installed"""
    print("Checking HackRF Tools Installation:")
    print("-" * 40)
    
    tools = ['hackrf_info', 'hackrf_transfer', 'hackrf_sweep', 'hackrf_debug']
    
    for tool in tools:
        try:
            # Try to run tool with --help
            result = subprocess.run([tool, '--help'], 
                                  capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0 or 'usage' in result.stdout.lower():
                print(f"✅ {tool}: FOUND")
            else:
                print(f"❌ {tool}: NOT WORKING")
                
        except FileNotFoundError:
            print(f"❌ {tool}: NOT FOUND")
        except subprocess.TimeoutExpired:
            print(f"⚠️ {tool}: TIMEOUT")
        except Exception as e:
            print(f"❌ {tool}: ERROR - {e}")
    
    print()

def check_device_connection():
    """Check if HackRF device is connected"""
    print("Checking Device Connection:")
    print("-" * 30)
    
    try:
        # Run hackrf_info to detect device
        result = subprocess.run(['hackrf_info'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ HackRF DEVICE DETECTED!")
            print()
            print("Device Information:")
            print(result.stdout)
            return True
        else:
            print("❌ NO DEVICE DETECTED")
            print()
            print("Error output:")
            print(result.stderr)
            return False
            
    except FileNotFoundError:
        print("❌ hackrf_info command not found")
        print("Please install HackRF tools first")
        return False
    except subprocess.TimeoutExpired:
        print("⚠️ Device detection timed out")
        print("This may indicate a driver issue")
        return False
    except Exception as e:
        print(f"❌ Error checking device: {e}")
        return False

def check_usb_devices():
    """Check USB devices (Windows specific)"""
    if platform.system() != "Windows":
        return
    
    print("Checking USB Devices:")
    print("-" * 20)
    
    try:
        # Use PowerShell to check USB devices
        cmd = 'Get-PnpDevice | Where-Object {$_.InstanceId -like "*VID_1D50*" -or $_.Name -like "*HackRF*"} | Select-Object Name, Status, InstanceId | Format-Table -AutoSize'
        
        result = subprocess.run(['powershell', '-Command', cmd], 
                              capture_output=True, text=True, timeout=15)
        
        if result.stdout.strip():
            print("HackRF related USB devices:")
            print(result.stdout)
        else:
            print("No HackRF devices found in USB device list")
            print()
            print("Checking all USB devices for unknown devices...")
            
            # Check for unknown devices
            unknown_cmd = 'Get-PnpDevice | Where-Object {$_.Status -eq "Error" -or $_.Status -eq "Unknown"} | Select-Object Name, Status, InstanceId | Format-Table -AutoSize'
            unknown_result = subprocess.run(['powershell', '-Command', unknown_cmd], 
                                          capture_output=True, text=True, timeout=15)
            
            if unknown_result.stdout.strip():
                print("Unknown/Error USB devices (one might be HackRF):")
                print(unknown_result.stdout)
            else:
                print("No unknown USB devices found")
        
    except Exception as e:
        print(f"Could not check USB devices: {e}")
    
    print()

def provide_troubleshooting():
    """Provide troubleshooting steps"""
    print("Troubleshooting Steps:")
    print("=" * 50)
    print()
    
    print("1. INSTALL HACKRF TOOLS:")
    print("   - Run: hackrf_simple_installer.bat")
    print("   - Or download from: https://github.com/greatscottgadgets/hackrf/releases")
    print()
    
    print("2. INSTALL USB DRIVERS:")
    print("   - Download Zadig: https://zadig.akeo.ie/")
    print("   - Run as Administrator")
    print("   - Connect HackRF device")
    print("   - Select HackRF One device")
    print("   - Install WinUSB driver")
    print()
    
    print("3. CHECK PHYSICAL CONNECTION:")
    print("   - Use high-quality USB cable")
    print("   - Try different USB ports")
    print("   - Check Device Manager for unknown devices")
    print("   - Ensure HackRF LED is solid (not blinking)")
    print()
    
    print("4. VERIFY INSTALLATION:")
    print("   - Open new Command Prompt")
    print("   - Run: hackrf_info")
    print("   - Should display device information")
    print()
    
    print("5. RESTART HACKRF PLATFORM:")
    print("   - python hackrf_enhanced_platform.py")
    print("   - Should detect device automatically")

def main():
    """Main checking function"""
    print("HackRF Device Checker")
    print("=" * 40)
    print()
    
    # System check
    check_system()
    
    # Tool installation check
    check_hackrf_tools()
    
    # USB device check (Windows)
    check_usb_devices()
    
    # Device connection check
    device_found = check_device_connection()
    
    if not device_found:
        print()
        provide_troubleshooting()
    else:
        print()
        print("🎉 SUCCESS! HackRF device is properly connected and working!")
        print()
        print("You can now run:")
        print("  python hackrf_enhanced_platform.py")
    
    print()
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()