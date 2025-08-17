#!/usr/bin/env python3
"""
HackRF Security Scanner - Legitimate Defensive Security Tool
For authorized security testing, research, and defensive purposes only
Compatible with Kali Linux and defensive security frameworks
"""

import os
import sys
import time
import numpy as np
import json
from datetime import datetime
import logging
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DefensiveRadarScanner:
    """Legitimate radar and spectrum scanning for defensive security purposes"""
    
    def __init__(self):
        self.scan_ranges = {
            'wifi_2_4ghz': {
                'name': 'WiFi 2.4GHz Security Scan',
                'start_freq': 2400e6,
                'stop_freq': 2500e6,
                'description': 'Scan for unauthorized WiFi devices and rogue access points'
            },
            'wifi_5ghz': {
                'name': 'WiFi 5GHz Security Scan', 
                'start_freq': 5150e6,
                'stop_freq': 5850e6,
                'description': 'Scan 5GHz WiFi bands for security assessment'
            },
            'bluetooth': {
                'name': 'Bluetooth Security Scan',
                'start_freq': 2400e6,
                'stop_freq': 2485e6,
                'description': 'Detect Bluetooth devices for security audit'
            },
            'iot_433': {
                'name': 'IoT 433MHz Security Scan',
                'start_freq': 430e6,
                'stop_freq': 440e6,
                'description': 'Scan for unauthorized IoT devices on 433MHz'
            },
            'iot_915': {
                'name': 'IoT 915MHz Security Scan',
                'start_freq': 902e6,
                'stop_freq': 928e6,
                'description': 'Scan for unauthorized IoT devices on 915MHz'
            },
            'custom': {
                'name': 'Custom Frequency Range',
                'start_freq': 100e6,
                'stop_freq': 1000e6,
                'description': 'User-defined frequency range for security scanning'
            }
        }
        
        self.detected_devices = []
        self.is_scanning = False
        self.whitelist = set()  # Known good devices
        self.threat_signatures = self.load_threat_signatures()
        
    def load_threat_signatures(self):
        """Load known threat signatures for defensive detection"""
        return {
            'rogue_ap_patterns': [
                'strong_signal_unusual_location',
                'suspicious_ssid_patterns',
                'unusual_encryption_methods'
            ],
            'unauthorized_devices': [
                'unknown_mac_prefixes',
                'suspicious_device_names',
                'unusual_transmission_patterns'
            ],
            'jamming_patterns': [
                'continuous_high_power',
                'frequency_sweeping',
                'denial_of_service_signatures'
            ]
        }
        
    def scan_frequency_range(self, scan_config, callback=None):
        """Scan frequency range for security threats"""
        logger.info(f"Starting defensive security scan: {scan_config['name']}")
        
        start_freq = scan_config['start_freq']
        stop_freq = scan_config['stop_freq']
        step_size = 1e6  # 1 MHz steps
        
        current_freq = start_freq
        detections = []
        
        while current_freq <= stop_freq and self.is_scanning:
            try:
                # Simulate scanning (replace with actual HackRF code)
                power_level = self.measure_power_at_frequency(current_freq)
                
                # Analyze for security threats
                threat_level = self.analyze_threat_level(current_freq, power_level)
                
                if threat_level > 0.7:  # High threat threshold
                    detection = {
                        'frequency': current_freq,
                        'power': power_level,
                        'threat_level': threat_level,
                        'timestamp': datetime.now().isoformat(),
                        'scan_type': scan_config['name']
                    }
                    detections.append(detection)
                    
                    if callback:
                        callback(detection)
                        
                current_freq += step_size
                time.sleep(0.01)  # Small delay
                
            except Exception as e:
                logger.error(f"Error during scan at {current_freq}: {e}")
                
        return detections
        
    def measure_power_at_frequency(self, frequency):
        """Measure power level at specific frequency"""
        # Simulate power measurement
        import random
        base_noise = -80  # dBm
        return base_noise + random.uniform(-10, 30)
        
    def analyze_threat_level(self, frequency, power):
        """Analyze threat level based on frequency and power"""
        threat_score = 0.0
        
        # High power signals could indicate unauthorized transmitters
        if power > -30:  # Very high power
            threat_score += 0.5
        elif power > -50:  # Moderate power
            threat_score += 0.3
            
        # Check against known good frequencies
        if self.is_whitelisted_frequency(frequency):
            threat_score *= 0.1  # Reduce threat for known good
            
        # Check for suspicious patterns
        if self.matches_threat_signature(frequency, power):
            threat_score += 0.4
            
        return min(threat_score, 1.0)
        
    def is_whitelisted_frequency(self, frequency):
        """Check if frequency is in whitelist"""
        # Check against authorized frequencies
        authorized_ranges = [
            (2400e6, 2485e6),  # WiFi/Bluetooth
            (5150e6, 5850e6),  # 5GHz WiFi
        ]
        
        for start, stop in authorized_ranges:
            if start <= frequency <= stop:
                return True
        return False
        
    def matches_threat_signature(self, frequency, power):
        """Check if signal matches known threat signatures"""
        # Simple threat detection logic
        # In real implementation, this would be much more sophisticated
        
        # Check for jamming patterns
        if power > -20:  # Very high power could indicate jamming
            return True
            
        # Check for unauthorized frequency usage
        forbidden_ranges = [
            (450e6, 470e6),   # Emergency services
            (460e6, 470e6),   # Public safety
        ]
        
        for start, stop in forbidden_ranges:
            if start <= frequency <= stop:
                return True
                
        return False

class KaliLinuxIntegration:
    """Integration with Kali Linux security tools"""
    
    def __init__(self):
        self.available_tools = self.detect_kali_tools()
        
    def detect_kali_tools(self):
        """Detect available Kali Linux tools"""
        tools = {}
        
        # Check for common RF security tools
        tool_commands = {
            'hackrf_tools': 'hackrf_info',
            'gqrx': 'gqrx',
            'gnuradio': 'gnuradio-companion',
            'aircrack_ng': 'aircrack-ng',
            'reaver': 'reaver',
            'kismet': 'kismet',
            'wireshark': 'wireshark'
        }
        
        for tool_name, command in tool_commands.items():
            try:
                result = subprocess.run(['which', command], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    tools[tool_name] = {
                        'available': True,
                        'path': result.stdout.strip(),
                        'description': self.get_tool_description(tool_name)
                    }
                else:
                    tools[tool_name] = {'available': False}
            except:
                tools[tool_name] = {'available': False}
                
        return tools
        
    def get_tool_description(self, tool_name):
        """Get description of security tool"""
        descriptions = {
            'hackrf_tools': 'HackRF command-line utilities',
            'gqrx': 'Software Defined Radio receiver',
            'gnuradio': 'Open source SDR development toolkit',
            'aircrack_ng': 'WiFi security auditing suite',
            'reaver': 'WPS security testing tool',
            'kismet': 'Wireless network detector and sniffer',
            'wireshark': 'Network protocol analyzer'
        }
        return descriptions.get(tool_name, 'Security tool')
        
    def launch_tool(self, tool_name, args=None):
        """Launch Kali Linux security tool"""
        if tool_name not in self.available_tools or not self.available_tools[tool_name]['available']:
            logger.error(f"Tool {tool_name} not available")
            return False
            
        try:
            command = [self.available_tools[tool_name]['path']]
            if args:
                command.extend(args)
                
            subprocess.Popen(command)
            logger.info(f"Launched {tool_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error launching {tool_name}: {e}")
            return False

class SecurityScannerGUI:
    """GUI for the defensive security scanner"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("HackRF Defensive Security Scanner - Kali Linux Compatible")
        self.root.geometry("1000x700")
        self.root.configure(bg='#0a0a0a')  # Kali-style dark theme
        
        self.scanner = DefensiveRadarScanner()
        self.kali_integration = KaliLinuxIntegration()
        
        self.create_gui()
        
    def create_gui(self):
        """Create the security scanner GUI"""
        
        # Main notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_scanner_tab()
        self.create_detection_tab()
        self.create_tools_tab()
        self.create_reports_tab()
        
    def create_scanner_tab(self):
        """Create scanner configuration tab"""
        scanner_frame = ttk.Frame(self.notebook)
        self.notebook.add(scanner_frame, text="🔍 Scanner")
        
        # Warning label
        warning_frame = ttk.Frame(scanner_frame)
        warning_frame.pack(fill=tk.X, padx=5, pady=5)
        
        warning_text = "⚠️ DEFENSIVE SECURITY TOOL - AUTHORIZED USE ONLY ⚠️\nFor legitimate security testing and research purposes only"
        warning_label = tk.Label(warning_frame, text=warning_text, 
                                fg='orange', bg='#0a0a0a', font=('Arial', 10, 'bold'))
        warning_label.pack()
        
        # Scan type selection
        scan_frame = ttk.LabelFrame(scanner_frame, text="Security Scan Type")
        scan_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.scan_type_var = tk.StringVar(value='wifi_2_4ghz')
        
        for scan_id, scan_config in self.scanner.scan_ranges.items():
            ttk.Radiobutton(scan_frame, text=f"{scan_config['name']}\n{scan_config['description']}", 
                           variable=self.scan_type_var, value=scan_id).pack(anchor=tk.W, padx=5, pady=2)
                           
        # Custom frequency range
        custom_frame = ttk.LabelFrame(scanner_frame, text="Custom Frequency Range")
        custom_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(custom_frame, text="Start Freq (MHz):").grid(row=0, column=0, padx=5)
        self.start_freq_var = tk.StringVar(value="100")
        ttk.Entry(custom_frame, textvariable=self.start_freq_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(custom_frame, text="Stop Freq (MHz):").grid(row=0, column=2, padx=5)
        self.stop_freq_var = tk.StringVar(value="1000")
        ttk.Entry(custom_frame, textvariable=self.stop_freq_var, width=10).grid(row=0, column=3, padx=5)
        
        # Control buttons
        control_frame = ttk.Frame(scanner_frame)
        control_frame.pack(fill=tk.X, padx=5, pady=10)
        
        ttk.Button(control_frame, text="Start Security Scan", 
                  command=self.start_security_scan, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Stop Scan", 
                  command=self.stop_scan).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Export Results", 
                  command=self.export_results).pack(side=tk.RIGHT, padx=5)
                  
        # Progress indicator
        self.progress = ttk.Progressbar(scanner_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=5, pady=5)
        
    def create_detection_tab(self):
        """Create threat detection tab"""
        detection_frame = ttk.Frame(self.notebook)
        self.notebook.add(detection_frame, text="🚨 Detections")
        
        # Threat level indicator
        status_frame = ttk.Frame(detection_frame)
        status_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(status_frame, text="Current Threat Level:").pack(side=tk.LEFT)
        self.threat_level_label = tk.Label(status_frame, text="LOW", 
                                          fg='green', font=('Arial', 12, 'bold'))
        self.threat_level_label.pack(side=tk.LEFT, padx=10)
        
        # Detections list
        list_frame = ttk.LabelFrame(detection_frame, text="Security Detections")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ('Time', 'Frequency', 'Power', 'Threat', 'Type', 'Action')
        self.detection_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        for col in columns:
            self.detection_tree.heading(col, text=col)
            self.detection_tree.column(col, width=100)
            
        scrollbar_det = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.detection_tree.yview)
        self.detection_tree.configure(yscrollcommand=scrollbar_det.set)
        
        self.detection_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_det.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_tools_tab(self):
        """Create Kali tools integration tab"""
        tools_frame = ttk.Frame(self.notebook)
        self.notebook.add(tools_frame, text="🛠️ Kali Tools")
        
        # Available tools
        avail_frame = ttk.LabelFrame(tools_frame, text="Available Kali Linux Security Tools")
        avail_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        for tool_name, tool_info in self.kali_integration.available_tools.items():
            tool_frame = ttk.Frame(avail_frame)
            tool_frame.pack(fill=tk.X, padx=5, pady=2)
            
            status_color = 'green' if tool_info['available'] else 'red'
            status_text = '✓ Available' if tool_info['available'] else '✗ Not Available'
            
            ttk.Label(tool_frame, text=tool_name.replace('_', ' ').title()).pack(side=tk.LEFT)
            tk.Label(tool_frame, text=status_text, fg=status_color, bg='#0a0a0a').pack(side=tk.LEFT, padx=10)
            
            if tool_info['available']:
                ttk.Button(tool_frame, text="Launch", 
                          command=lambda t=tool_name: self.launch_tool(t)).pack(side=tk.RIGHT)
                          
    def create_reports_tab(self):
        """Create security reports tab"""
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="📊 Reports")
        
        # Report generation
        gen_frame = ttk.LabelFrame(reports_frame, text="Generate Security Report")
        gen_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(gen_frame, text="Generate PDF Report", 
                  command=self.generate_pdf_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(gen_frame, text="Export CSV Data", 
                  command=self.export_csv_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(gen_frame, text="Save Configuration", 
                  command=self.save_config).pack(side=tk.LEFT, padx=5)
                  
        # Report preview
        preview_frame = ttk.LabelFrame(reports_frame, text="Report Preview")
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.report_text = tk.Text(preview_frame, bg='#1e1e1e', fg='white', 
                                  font=('Courier', 10))
        self.report_text.pack(fill=tk.BOTH, expand=True)
        
    def start_security_scan(self):
        """Start defensive security scan"""
        scan_type = self.scan_type_var.get()
        
        if scan_type == 'custom':
            try:
                start_freq = float(self.start_freq_var.get()) * 1e6
                stop_freq = float(self.stop_freq_var.get()) * 1e6
                scan_config = {
                    'name': 'Custom Security Scan',
                    'start_freq': start_freq,
                    'stop_freq': stop_freq,
                    'description': f'Custom range {start_freq/1e6}-{stop_freq/1e6} MHz'
                }
            except ValueError:
                messagebox.showerror("Error", "Invalid frequency values")
                return
        else:
            scan_config = self.scanner.scan_ranges[scan_type]
            
        # Confirm scan
        result = messagebox.askyesno(
            "Confirm Security Scan",
            f"Start security scan: {scan_config['name']}?\n\n"
            f"Range: {scan_config['start_freq']/1e6:.1f} - {scan_config['stop_freq']/1e6:.1f} MHz\n"
            f"Purpose: {scan_config['description']}\n\n"
            f"Ensure you have authorization to perform this scan."
        )
        
        if result:
            self.scanner.is_scanning = True
            self.progress.start()
            logger.info(f"Starting security scan: {scan_config['name']}")
            
            # Start scan in background thread
            scan_thread = threading.Thread(
                target=self.run_scan, 
                args=(scan_config,)
            )
            scan_thread.daemon = True
            scan_thread.start()
            
    def run_scan(self, scan_config):
        """Run security scan in background"""
        detections = self.scanner.scan_frequency_range(
            scan_config, 
            callback=self.on_detection
        )
        
        self.root.after(0, self.scan_completed, detections)
        
    def on_detection(self, detection):
        """Handle new threat detection"""
        # Update GUI in main thread
        self.root.after(0, self.add_detection_to_tree, detection)
        
    def add_detection_to_tree(self, detection):
        """Add detection to tree view"""
        threat_text = f"{detection['threat_level']:.2f}"
        
        # Color code by threat level
        if detection['threat_level'] > 0.8:
            tags = ('high_threat',)
        elif detection['threat_level'] > 0.5:
            tags = ('medium_threat',)
        else:
            tags = ('low_threat',)
            
        self.detection_tree.insert('', 0, values=(
            detection['timestamp'][:19],
            f"{detection['frequency']/1e6:.3f} MHz",
            f"{detection['power']:.1f} dBm",
            threat_text,
            detection['scan_type'],
            "Review"
        ), tags=tags)
        
    def scan_completed(self, detections):
        """Handle scan completion"""
        self.progress.stop()
        self.scanner.is_scanning = False
        
        logger.info(f"Security scan completed. {len(detections)} threats detected.")
        messagebox.showinfo("Scan Complete", 
                           f"Security scan completed.\n{len(detections)} potential threats detected.")
        
    def stop_scan(self):
        """Stop current scan"""
        self.scanner.is_scanning = False
        self.progress.stop()
        logger.info("Security scan stopped")
        
    def launch_tool(self, tool_name):
        """Launch Kali Linux tool"""
        if self.kali_integration.launch_tool(tool_name):
            messagebox.showinfo("Tool Launched", f"{tool_name} has been launched")
        else:
            messagebox.showerror("Error", f"Failed to launch {tool_name}")
            
    def export_results(self):
        """Export scan results"""
        # Implementation for exporting results
        logger.info("Exporting scan results")
        
    def generate_pdf_report(self):
        """Generate PDF security report"""
        logger.info("Generating PDF security report")
        
    def export_csv_data(self):
        """Export data as CSV"""
        logger.info("Exporting CSV data")
        
    def save_config(self):
        """Save current configuration"""
        logger.info("Saving configuration")

def main():
    """Main function"""
    print("=" * 60)
    print("HackRF Defensive Security Scanner")
    print("Kali Linux Compatible")
    print("=" * 60)
    print("⚠️  FOR AUTHORIZED SECURITY TESTING ONLY ⚠️")
    print("This tool is for legitimate defensive security purposes")
    print("Ensure you have proper authorization before scanning")
    print("=" * 60)
    
    root = tk.Tk()
    app = SecurityScannerGUI(root)
    
    # Configure theme for Kali Linux style
    style = ttk.Style()
    style.theme_use('clam')
    
    root.mainloop()

if __name__ == "__main__":
    main()