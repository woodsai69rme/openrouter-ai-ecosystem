# HackRF One Comprehensive Guide & Testing Suite

## 🔒 IMPORTANT SECURITY NOTICE
**This guide is for authorized security testing and educational purposes only. Ensure you have proper permissions before testing any wireless systems.**

## 📋 Table of Contents
1. [Introduction](#introduction)
2. [Hardware Setup](#hardware-setup)
3. [Software Installation](#software-installation)
4. [Firmware Management](#firmware-management)
5. [Testing Framework](#testing-framework)
6. [Security Scanner](#security-scanner)
7. [Integration with Kali Linux](#integration-with-kali-linux)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)
10. [Legal Considerations](#legal-considerations)

## 📡 Introduction

The HackRF One is a Software Defined Radio (SDR) device designed for legitimate security research, RF analysis, and educational purposes. This comprehensive guide provides tools and procedures for authorized penetration testing and security assessment.

### Key Features
- Frequency Range: 1 MHz to 6 GHz
- Half-duplex operation
- Open source software and hardware
- Kali Linux compatible
- USB 2.0 powered

## 🔧 Hardware Setup

### Physical Connection
1. Connect HackRF One to USB port
2. Attach appropriate antenna for frequency range
3. Verify power LED is solid (not blinking)

### Antenna Selection Guide
```
Frequency Range          | Recommended Antenna
------------------------|--------------------
10 MHz - 1 GHz          | Discone antenna
2.4 GHz (WiFi/BT)       | 2.4 GHz rubber duck
5 GHz (WiFi)            | 5 GHz patch antenna
GSM (850/900/1800/1900) | GSM/cellular antenna
433/915 MHz (IoT)       | UHF antenna
```

## 💻 Software Installation

### Ubuntu/Debian Systems
```bash
# Install HackRF tools
sudo apt update
sudo apt install hackrf

# Install additional SDR tools
sudo apt install gqrx-sdr gnuradio

# Verify installation
hackrf_info
```

### Kali Linux Installation
```bash
# HackRF tools (usually pre-installed)
sudo apt install hackrf

# Additional security tools
sudo apt install aircrack-ng kismet reaver
sudo apt install wireshark-gtk

# Verify all tools
which hackrf_info gqrx aircrack-ng
```

### Building from Source
```bash
# Clone repository
git clone https://github.com/greatscottgadgets/hackrf.git
cd hackrf/host

# Build tools
mkdir build
cd build
cmake ..
make
sudo make install
sudo ldconfig
```

## 🔄 Firmware Management

### Current Firmware Check
```bash
# Check current firmware version
hackrf_info

# Expected output includes:
# - Firmware version
# - Serial number
# - Board ID
```

### Firmware Update Process
1. **Download latest firmware** from official repository
2. **Backup current firmware** (important!)
3. **Install new firmware**
4. **Verify installation**

```bash
# Backup current firmware
hackrf_spiflash -r backup_firmware.bin

# Flash new firmware
hackrf_spiflash -w new_firmware.bin

# Verify installation
hackrf_info
```

## 🧪 Testing Framework

### Automated Test Suite
Our testing framework includes comprehensive validation:

#### RF Performance Tests
- **Frequency accuracy testing**
- **Power output verification**
- **Sensitivity measurements**
- **Spurious emission checks**

#### Software Integration Tests
- **Driver functionality**
- **Tool compatibility**
- **Performance benchmarks**
- **Error handling validation**

### Test Execution
```bash
# Run comprehensive test suite
python system_test_suite.py

# Run specific test categories
python system_test_suite.py --category rf_performance
python system_test_suite.py --category software_integration
```

## 🔍 Security Scanner Usage

### Defensive Security Scanning
Our security scanner provides legitimate threat detection:

#### Supported Scan Types
1. **WiFi Security Assessment**
   - Rogue access point detection
   - Unauthorized device identification
   - Security configuration analysis

2. **Bluetooth Security Audit**
   - Device discovery and profiling
   - Security vulnerability assessment
   - Unauthorized pairing detection

3. **IoT Device Security**
   - 433/915 MHz device scanning
   - Protocol analysis
   - Security posture assessment

### Scanner Operation
```bash
# Launch security scanner GUI
python hackrf_security_scanner.py

# Command line scanning
hackrf_sweep -f 2400:2500 -w results.csv
```

## 🐧 Kali Linux Integration

### Available Tools Integration
Our platform integrates with standard Kali tools:

#### Wireless Security Tools
- **Aircrack-ng**: WiFi security auditing
- **Kismet**: Wireless network detection
- **Reaver**: WPS security testing
- **Wireshark**: Protocol analysis

#### SDR-Specific Tools
- **GQRX**: Real-time spectrum analysis
- **GNU Radio**: Signal processing
- **HackRF Tools**: Device control utilities

### Tool Launch Commands
```bash
# Launch GQRX for spectrum analysis
gqrx

# Start Kismet for wireless monitoring
sudo kismet

# Run Aircrack-ng for WiFi analysis
aircrack-ng -w wordlist.txt capture.cap
```

## 🛡️ Security Best Practices

### Legal Compliance
1. **Always obtain written authorization** before testing
2. **Document all testing activities**
3. **Respect privacy and confidentiality**
4. **Follow local regulations** regarding RF emissions

### Technical Security
1. **Regular firmware updates**
2. **Secure testing environment**
3. **Data encryption for sensitive results**
4. **Access control for testing tools**

### Operational Security
```bash
# Verify device authenticity
hackrf_info | grep "Serial number"

# Check for firmware tampering
hackrf_spiflash -r current.bin
sha256sum current.bin

# Secure tool execution
sudo -u hackrf-user python scanner.py
```

## 🔧 Troubleshooting

### Common Issues

#### Device Not Detected
```bash
# Check USB connection
lsusb | grep -i hackrf

# Verify driver installation
dmesg | grep hackrf

# Reset device
hackrf_debug --reset
```

#### Firmware Issues
```bash
# Check firmware status
hackrf_info

# Reflash firmware if corrupted
hackrf_spiflash -w firmware.bin

# Verify successful flash
hackrf_info
```

#### Performance Problems
```bash
# Check USB performance
cat /sys/kernel/debug/usb/devices | grep -A 5 hackrf

# Monitor system resources
top -p $(pgrep hackrf)

# Test basic functionality
hackrf_transfer -t test.bin
```

### Error Codes
```
Error Code | Description              | Solution
-----------|--------------------------|------------------
-5         | USB communication failed | Check USB cable/port
-6         | Device not found         | Verify connection
-1000      | Invalid parameter        | Check command syntax
-2000      | Firmware error           | Reflash firmware
```

## ⚖️ Legal Considerations

### Authorized Use Only
- **Penetration Testing**: Only with explicit written permission
- **Security Research**: Within legal boundaries and ethical guidelines
- **Educational Use**: In controlled environments with proper authorization

### Prohibited Activities
- **Unauthorized interception** of communications
- **Jamming or interference** with licensed services
- **Privacy violations** or unauthorized surveillance
- **Commercial espionage** or competitive intelligence gathering

### Compliance Requirements
1. **FCC Part 15** compliance for emissions
2. **Local spectrum regulations**
3. **Privacy laws and regulations**
4. **Corporate security policies**

## 📊 Test Results Documentation

### Automated Reporting
Our test suite generates comprehensive reports:

#### Performance Metrics
- **RF characteristics**
- **Software compatibility**
- **Integration status**
- **Security posture**

#### Report Formats
- **PDF technical reports**
- **CSV data exports**
- **JSON API results**
- **HTML dashboards**

### Sample Test Report Structure
```
HackRF Test Report
==================
Date: [Test Date]
Device: [Serial Number]
Firmware: [Version]

1. Hardware Tests
   - Frequency accuracy: PASS
   - Power output: PASS
   - Sensitivity: PASS

2. Software Tests
   - Driver installation: PASS
   - Tool compatibility: PASS
   - Performance: PASS

3. Security Tests
   - Scanner functionality: PASS
   - Threat detection: PASS
   - Integration: PASS

Overall Status: PASS
```

## 🚀 Advanced Usage

### Custom Signal Generation
```bash
# Generate test signals
hackrf_transfer -t signal.bin -f 915000000 -s 2000000

# Custom waveform generation
python generate_signal.py --frequency 433.92e6 --modulation FSK
```

### Advanced Scanning
```bash
# Sweep with custom parameters
hackrf_sweep -f 400:500 -w wide_scan.csv -n 8192 -g 20

# Protocol-specific analysis
python protocol_analyzer.py --protocol zigbee --frequency 915e6
```

## 📚 Additional Resources

### Documentation
- [Official HackRF Documentation](https://hackrf.readthedocs.io/)
- [GNU Radio Tutorials](https://wiki.gnuradio.org/index.php/Tutorials)
- [SDR Best Practices](https://www.rtl-sdr.com/)

### Community
- [HackRF Users Group](https://groups.google.com/forum/#!forum/hackrf-dev)
- [SDR Community Forums](https://www.reddit.com/r/RTLSDR/)
- [GNU Radio Mailing List](https://lists.gnu.org/mailman/listinfo/discuss-gnuradio)

### Training
- [Cybersecurity and Infrastructure Security Agency (CISA)](https://www.cisa.gov/)
- [SANS Penetration Testing](https://www.sans.org/cyber-security-courses/penetration-testing/)
- [Offensive Security Certified Professional (OSCP)](https://www.offensive-security.com/pwk-oscp/)

---

## ⚠️ Final Warning

**This documentation is provided for educational and authorized security testing purposes only. Users are responsible for ensuring compliance with all applicable laws and regulations. Unauthorized use of these tools and techniques may result in civil and criminal penalties.**

**Always obtain proper authorization before conducting any security testing activities.**