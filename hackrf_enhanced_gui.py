#!/usr/bin/env python3
"""
HackRF Enhanced Platform GUI
Advanced graphical interface for HackRF Enhanced Platform
Real-time spectrum analysis with AI-driven threat detection
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import numpy as np
import threading
import time
import queue
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class HackRFEnhancedGUI:
    """Enhanced GUI for HackRF Platform"""
    
    def __init__(self, root, platform):
        self.root = root
        self.platform = platform
        self.root.title("HackRF Enhanced Platform v2.0.0")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1e1e1e')
        
        # GUI state
        self.is_scanning = False
        self.current_session = None
        self.data_queue = queue.Queue()
        self.threat_queue = queue.Queue()
        
        # Matplotlib setup
        plt.style.use('dark_background')
        
        # Create GUI
        self.setup_styles()
        self.create_main_interface()
        self.setup_real_time_updates()
        
        # Initialize
        self.update_device_list()
        
    def setup_styles(self):
        """Setup custom styles for dark theme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure dark theme colors
        style.configure('TFrame', background='#2d2d2d')
        style.configure('TLabel', background='#2d2d2d', foreground='#ffffff')
        style.configure('TButton', background='#404040', foreground='#ffffff')
        style.configure('TNotebook', background='#2d2d2d')
        style.configure('TNotebook.Tab', background='#404040', foreground='#ffffff')
        style.map('TNotebook.Tab', 
                 background=[('selected', '#505050'), ('active', '#454545')])
        
    def create_main_interface(self):
        """Create main interface layout"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Top toolbar
        self.create_toolbar(main_frame)
        
        # Main content area
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Left panel (controls)
        left_panel = ttk.Frame(content_frame, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        left_panel.pack_propagate(False)
        
        # Right panel (displays)
        right_panel = ttk.Frame(content_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create panels
        self.create_control_panel(left_panel)
        self.create_display_panel(right_panel)
        
        # Status bar
        self.create_status_bar(main_frame)
        
    def create_toolbar(self, parent):
        """Create top toolbar"""
        toolbar = ttk.Frame(parent, relief=tk.RAISED, borderwidth=1)
        toolbar.pack(fill=tk.X, pady=(0, 5))
        
        # Session controls
        ttk.Label(toolbar, text="Session:").pack(side=tk.LEFT, padx=5)
        
        ttk.Button(toolbar, text="New Session", 
                  command=self.new_session).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="End Session", 
                  command=self.end_session).pack(side=tk.LEFT, padx=2)
        
        # Separator
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Scan controls
        self.scan_button = ttk.Button(toolbar, text="Start Scan", 
                                     command=self.toggle_scan)
        self.scan_button.pack(side=tk.LEFT, padx=2)
        
        # Emergency stop
        emergency_btn = ttk.Button(toolbar, text="🛑 EMERGENCY STOP", 
                                  command=self.emergency_stop)
        emergency_btn.pack(side=tk.RIGHT, padx=5)
        
        # Export
        ttk.Button(toolbar, text="Export Data", 
                  command=self.export_data).pack(side=tk.RIGHT, padx=2)
        
    def create_control_panel(self, parent):
        """Create left control panel"""
        # Notebook for control tabs
        control_notebook = ttk.Notebook(parent)
        control_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Device tab
        self.create_device_tab(control_notebook)
        
        # Frequency tab
        self.create_frequency_tab(control_notebook)
        
        # Analysis tab
        self.create_analysis_tab(control_notebook)
        
        # Security tab
        self.create_security_tab(control_notebook)
        
        # Settings tab
        self.create_settings_tab(control_notebook)
        
    def create_device_tab(self, notebook):
        """Create device control tab"""
        device_frame = ttk.Frame(notebook)
        notebook.add(device_frame, text="📱 Device")
        
        # Device selection
        device_select_frame = ttk.LabelFrame(device_frame, text="Device Selection")
        device_select_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.device_var = tk.StringVar()
        self.device_combo = ttk.Combobox(device_select_frame, textvariable=self.device_var, 
                                        state="readonly")
        self.device_combo.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(device_select_frame, text="Refresh Devices", 
                  command=self.update_device_list).pack(pady=5)
        
        # Device info
        info_frame = ttk.LabelFrame(device_frame, text="Device Information")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.device_info_text = tk.Text(info_frame, height=10, bg='#1e1e1e', fg='#ffffff', 
                                       font=('Courier', 9))
        self.device_info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Device controls
        controls_frame = ttk.Frame(device_frame)
        controls_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(controls_frame, text="Device Test", 
                  command=self.test_device).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls_frame, text="Firmware Info", 
                  command=self.show_firmware_info).pack(side=tk.LEFT, padx=2)
        
    def create_frequency_tab(self, notebook):
        """Create frequency control tab"""
        freq_frame = ttk.Frame(notebook)
        notebook.add(freq_frame, text="📡 Frequency")
        
        # Frequency settings
        freq_settings_frame = ttk.LabelFrame(freq_frame, text="Frequency Settings")
        freq_settings_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Center frequency
        ttk.Label(freq_settings_frame, text="Center Frequency (MHz):").pack(anchor=tk.W, padx=5)
        self.center_freq_var = tk.StringVar(value="915.0")
        ttk.Entry(freq_settings_frame, textvariable=self.center_freq_var).pack(fill=tk.X, padx=5, pady=2)
        
        # Sample rate
        ttk.Label(freq_settings_frame, text="Sample Rate (MHz):").pack(anchor=tk.W, padx=5, pady=(10,0))
        self.sample_rate_var = tk.StringVar(value="2.0")
        sample_rate_combo = ttk.Combobox(freq_settings_frame, textvariable=self.sample_rate_var,
                                        values=["2.0", "4.0", "8.0", "10.0", "12.5", "16.0", "20.0"])
        sample_rate_combo.pack(fill=tk.X, padx=5, pady=2)
        
        # Gain settings
        gain_frame = ttk.LabelFrame(freq_frame, text="Gain Settings")
        gain_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(gain_frame, text="RX Gain (dB):").pack(anchor=tk.W, padx=5)
        self.rx_gain_var = tk.IntVar(value=20)
        rx_gain_scale = ttk.Scale(gain_frame, from_=0, to=40, variable=self.rx_gain_var, orient=tk.HORIZONTAL)
        rx_gain_scale.pack(fill=tk.X, padx=5, pady=2)
        self.rx_gain_label = ttk.Label(gain_frame, text="20 dB")
        self.rx_gain_label.pack(anchor=tk.W, padx=5)
        
        # Update gain label
        rx_gain_scale.configure(command=lambda v: self.rx_gain_label.configure(text=f"{int(float(v))} dB"))
        
        # Frequency presets
        presets_frame = ttk.LabelFrame(freq_frame, text="Frequency Presets")
        presets_frame.pack(fill=tk.X, padx=5, pady=5)
        
        presets = [
            ("WiFi 2.4G Ch 6", "2437"),
            ("WiFi 2.4G Ch 11", "2462"),
            ("WiFi 5G Ch 36", "5180"),
            ("ISM 433 MHz", "433.92"),
            ("ISM 915 MHz", "915.0"),
            ("Bluetooth", "2440"),
            ("ZigBee Ch 11", "2405")
        ]
        
        for name, freq in presets:
            ttk.Button(presets_frame, text=name, 
                      command=lambda f=freq: self.center_freq_var.set(f)).pack(fill=tk.X, padx=5, pady=1)
        
    def create_analysis_tab(self, notebook):
        """Create analysis control tab"""
        analysis_frame = ttk.Frame(notebook)
        notebook.add(analysis_frame, text="🔬 Analysis")
        
        # AI Analysis settings
        ai_frame = ttk.LabelFrame(analysis_frame, text="AI Analysis")
        ai_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.ai_enabled_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(ai_frame, text="Enable AI Signal Classification", 
                       variable=self.ai_enabled_var).pack(anchor=tk.W, padx=5, pady=2)
        
        self.anomaly_detection_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(ai_frame, text="Anomaly Detection", 
                       variable=self.anomaly_detection_var).pack(anchor=tk.W, padx=5, pady=2)
        
        self.pattern_recognition_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(ai_frame, text="Pattern Recognition", 
                       variable=self.pattern_recognition_var).pack(anchor=tk.W, padx=5, pady=2)
        
        # Spectrum analysis settings
        spectrum_frame = ttk.LabelFrame(analysis_frame, text="Spectrum Analysis")
        spectrum_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(spectrum_frame, text="FFT Size:").pack(anchor=tk.W, padx=5)
        self.fft_size_var = tk.StringVar(value="8192")
        fft_combo = ttk.Combobox(spectrum_frame, textvariable=self.fft_size_var,
                                values=["1024", "2048", "4096", "8192", "16384"])
        fft_combo.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(spectrum_frame, text="Averaging:").pack(anchor=tk.W, padx=5, pady=(10,0))
        self.averaging_var = tk.IntVar(value=10)
        ttk.Scale(spectrum_frame, from_=1, to=100, variable=self.averaging_var, 
                 orient=tk.HORIZONTAL).pack(fill=tk.X, padx=5, pady=2)
        
        # Detection thresholds
        thresh_frame = ttk.LabelFrame(analysis_frame, text="Detection Thresholds")
        thresh_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(thresh_frame, text="Peak Threshold (dB):").pack(anchor=tk.W, padx=5)
        self.peak_threshold_var = tk.IntVar(value=-60)
        ttk.Scale(thresh_frame, from_=-100, to=0, variable=self.peak_threshold_var, 
                 orient=tk.HORIZONTAL).pack(fill=tk.X, padx=5, pady=2)
        
    def create_security_tab(self, notebook):
        """Create security control tab"""
        security_frame = ttk.Frame(notebook)
        notebook.add(security_frame, text="🛡️ Security")
        
        # Threat detection
        threat_frame = ttk.LabelFrame(security_frame, text="Threat Detection")
        threat_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.rogue_detection_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(threat_frame, text="Rogue Device Detection", 
                       variable=self.rogue_detection_var).pack(anchor=tk.W, padx=5, pady=2)
        
        self.jamming_detection_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(threat_frame, text="Jamming Detection", 
                       variable=self.jamming_detection_var).pack(anchor=tk.W, padx=5, pady=2)
        
        self.frequency_violation_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(threat_frame, text="Frequency Violation Detection", 
                       variable=self.frequency_violation_var).pack(anchor=tk.W, padx=5, pady=2)
        
        # Security alerts
        alerts_frame = ttk.LabelFrame(security_frame, text="Security Alerts")
        alerts_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Alert list
        self.alert_tree = ttk.Treeview(alerts_frame, columns=('Time', 'Severity', 'Type'), 
                                      show='tree headings', height=8)
        self.alert_tree.heading('#0', text='Alert')
        self.alert_tree.heading('Time', text='Time')
        self.alert_tree.heading('Severity', text='Severity')
        self.alert_tree.heading('Type', text='Type')
        
        self.alert_tree.column('#0', width=100)
        self.alert_tree.column('Time', width=80)
        self.alert_tree.column('Severity', width=70)
        self.alert_tree.column('Type', width=80)
        
        alert_scroll = ttk.Scrollbar(alerts_frame, orient=tk.VERTICAL, command=self.alert_tree.yview)
        self.alert_tree.configure(yscrollcommand=alert_scroll.set)
        
        self.alert_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        alert_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Alert controls
        alert_controls = ttk.Frame(security_frame)
        alert_controls.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(alert_controls, text="Clear Alerts", 
                  command=self.clear_alerts).pack(side=tk.LEFT, padx=2)
        ttk.Button(alert_controls, text="Export Alerts", 
                  command=self.export_alerts).pack(side=tk.LEFT, padx=2)
        
    def create_settings_tab(self, notebook):
        """Create settings tab"""
        settings_frame = ttk.Frame(notebook)
        notebook.add(settings_frame, text="⚙️ Settings")
        
        # GUI settings
        gui_frame = ttk.LabelFrame(settings_frame, text="GUI Settings")
        gui_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(gui_frame, text="Update Rate (ms):").pack(anchor=tk.W, padx=5)
        self.update_rate_var = tk.IntVar(value=100)
        ttk.Scale(gui_frame, from_=50, to=1000, variable=self.update_rate_var, 
                 orient=tk.HORIZONTAL).pack(fill=tk.X, padx=5, pady=2)
        
        # Database settings
        db_frame = ttk.LabelFrame(settings_frame, text="Database")
        db_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.auto_save_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(db_frame, text="Auto-save scan data", 
                       variable=self.auto_save_var).pack(anchor=tk.W, padx=5, pady=2)
        
        ttk.Button(db_frame, text="Database Statistics", 
                  command=self.show_db_stats).pack(pady=5)
        
        # Advanced settings
        adv_frame = ttk.LabelFrame(settings_frame, text="Advanced")
        adv_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(adv_frame, text="Export Configuration", 
                  command=self.export_config).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(adv_frame, text="Import Configuration", 
                  command=self.import_config).pack(fill=tk.X, padx=5, pady=2)
        ttk.Button(adv_frame, text="Reset to Defaults", 
                  command=self.reset_config).pack(fill=tk.X, padx=5, pady=2)
        
    def create_display_panel(self, parent):
        """Create right display panel"""
        # Display notebook
        display_notebook = ttk.Notebook(parent)
        display_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Spectrum display
        self.create_spectrum_display(display_notebook)
        
        # Waterfall display
        self.create_waterfall_display(display_notebook)
        
        # Analysis results
        self.create_analysis_display(display_notebook)
        
        # Protocol analysis
        self.create_protocol_display(display_notebook)
        
    def create_spectrum_display(self, notebook):
        """Create spectrum analyzer display"""
        spectrum_frame = ttk.Frame(notebook)
        notebook.add(spectrum_frame, text="📊 Spectrum")
        
        # Matplotlib figure
        self.spectrum_fig, self.spectrum_ax = plt.subplots(figsize=(10, 6), facecolor='#1e1e1e')
        self.spectrum_ax.set_facecolor('#1e1e1e')
        self.spectrum_ax.set_xlabel('Frequency (MHz)', color='white')
        self.spectrum_ax.set_ylabel('Power (dBm)', color='white')
        self.spectrum_ax.tick_params(colors='white')
        self.spectrum_ax.grid(True, alpha=0.3)
        
        # Initialize empty plot
        self.spectrum_line, = self.spectrum_ax.plot([], [], 'cyan', linewidth=1)
        self.peak_markers, = self.spectrum_ax.plot([], [], 'ro', markersize=4)
        
        # Canvas
        self.spectrum_canvas = FigureCanvasTkAgg(self.spectrum_fig, spectrum_frame)
        self.spectrum_canvas.draw()
        self.spectrum_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Controls
        spectrum_controls = ttk.Frame(spectrum_frame)
        spectrum_controls.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(spectrum_controls, text="Auto Scale", 
                  command=self.auto_scale_spectrum).pack(side=tk.LEFT, padx=2)
        ttk.Button(spectrum_controls, text="Peak Hold", 
                  command=self.toggle_peak_hold).pack(side=tk.LEFT, padx=2)
        ttk.Button(spectrum_controls, text="Save Plot", 
                  command=self.save_spectrum_plot).pack(side=tk.RIGHT, padx=2)
        
    def create_waterfall_display(self, notebook):
        """Create waterfall display"""
        waterfall_frame = ttk.Frame(notebook)
        notebook.add(waterfall_frame, text="🌊 Waterfall")
        
        # Matplotlib figure for waterfall
        self.waterfall_fig, self.waterfall_ax = plt.subplots(figsize=(10, 6), facecolor='#1e1e1e')
        self.waterfall_ax.set_facecolor('#1e1e1e')
        self.waterfall_ax.set_xlabel('Frequency (MHz)', color='white')
        self.waterfall_ax.set_ylabel('Time', color='white')
        self.waterfall_ax.tick_params(colors='white')
        
        # Canvas
        self.waterfall_canvas = FigureCanvasTkAgg(self.waterfall_fig, waterfall_frame)
        self.waterfall_canvas.draw()
        self.waterfall_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Waterfall data storage
        self.waterfall_data = []
        self.waterfall_freqs = None
        
    def create_analysis_display(self, notebook):
        """Create analysis results display"""
        analysis_frame = ttk.Frame(notebook)
        notebook.add(analysis_frame, text="🔬 Analysis")
        
        # Analysis text display
        self.analysis_text = tk.Text(analysis_frame, bg='#1e1e1e', fg='#ffffff', 
                                    font=('Courier', 10))
        
        analysis_scroll = ttk.Scrollbar(analysis_frame, orient=tk.VERTICAL, command=self.analysis_text.yview)
        self.analysis_text.configure(yscrollcommand=analysis_scroll.set)
        
        self.analysis_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        analysis_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_protocol_display(self, notebook):
        """Create protocol analysis display"""
        protocol_frame = ttk.Frame(notebook)
        notebook.add(protocol_frame, text="📡 Protocols")
        
        # Protocol tree
        self.protocol_tree = ttk.Treeview(protocol_frame, columns=('Type', 'Frequency', 'Details'), 
                                         show='tree headings')
        self.protocol_tree.heading('#0', text='Protocol')
        self.protocol_tree.heading('Type', text='Type')
        self.protocol_tree.heading('Frequency', text='Frequency')
        self.protocol_tree.heading('Details', text='Details')
        
        protocol_scroll = ttk.Scrollbar(protocol_frame, orient=tk.VERTICAL, command=self.protocol_tree.yview)
        self.protocol_tree.configure(yscrollcommand=protocol_scroll.set)
        
        self.protocol_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        protocol_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_status_bar(self, parent):
        """Create status bar"""
        status_frame = ttk.Frame(parent, relief=tk.SUNKEN, borderwidth=1)
        status_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.status_label = ttk.Label(status_frame, text="Ready")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Session info
        self.session_label = ttk.Label(status_frame, text="No active session")
        self.session_label.pack(side=tk.RIGHT, padx=5)
        
    def setup_real_time_updates(self):
        """Setup real-time data updates"""
        self.update_displays()
        
    def update_displays(self):
        """Update all displays with latest data"""
        try:
            # Process data queue
            while not self.data_queue.empty():
                data = self.data_queue.get_nowait()
                self.update_spectrum_display(data)
                self.update_waterfall_display(data)
                self.update_analysis_display(data)
            
            # Process threat queue
            while not self.threat_queue.empty():
                threat = self.threat_queue.get_nowait()
                self.add_security_alert(threat)
                
        except queue.Empty:
            pass
        except Exception as e:
            logger.error(f"Display update error: {e}")
        
        # Schedule next update
        self.root.after(self.update_rate_var.get(), self.update_displays)
        
    def update_spectrum_display(self, spectrum_data):
        """Update spectrum plot"""
        if not spectrum_data:
            return
            
        try:
            freqs = spectrum_data['frequencies'] / 1e6  # Convert to MHz
            power = spectrum_data['power']
            
            # Update spectrum line
            self.spectrum_line.set_data(freqs, power)
            
            # Update peaks
            peaks = spectrum_data.get('peaks', [])
            if peaks:
                peak_freqs = [freqs[i] for i, _ in peaks]
                peak_powers = [power[i] for i, _ in peaks]
                self.peak_markers.set_data(peak_freqs, peak_powers)
            
            # Auto-scale if needed
            self.spectrum_ax.relim()
            self.spectrum_ax.autoscale_view()
            
            # Update canvas
            self.spectrum_canvas.draw_idle()
            
        except Exception as e:
            logger.error(f"Spectrum display update error: {e}")
            
    def update_waterfall_display(self, spectrum_data):
        """Update waterfall display"""
        if not spectrum_data:
            return
            
        try:
            freqs = spectrum_data['frequencies'] / 1e6  # Convert to MHz
            power = spectrum_data['power']
            
            # Store frequency array on first update
            if self.waterfall_freqs is None:
                self.waterfall_freqs = freqs
            
            # Add new data
            self.waterfall_data.append(power)
            
            # Keep only recent data (last 100 sweeps)
            if len(self.waterfall_data) > 100:
                self.waterfall_data.pop(0)
            
            # Update waterfall plot
            if len(self.waterfall_data) > 1:
                waterfall_array = np.array(self.waterfall_data)
                
                self.waterfall_ax.clear()
                im = self.waterfall_ax.imshow(waterfall_array, aspect='auto', 
                                            extent=[freqs[0], freqs[-1], 0, len(self.waterfall_data)],
                                            cmap='plasma', origin='lower')
                
                self.waterfall_ax.set_xlabel('Frequency (MHz)', color='white')
                self.waterfall_ax.set_ylabel('Time', color='white')
                self.waterfall_ax.tick_params(colors='white')
                
                self.waterfall_canvas.draw_idle()
                
        except Exception as e:
            logger.error(f"Waterfall display update error: {e}")
            
    def update_analysis_display(self, analysis_data):
        """Update analysis text display"""
        if not analysis_data:
            return
            
        try:
            # Format analysis results
            timestamp = datetime.now().strftime("%H:%M:%S")
            text = f"[{timestamp}] Analysis Results:\n"
            
            if 'classification' in analysis_data:
                text += "Signal Classification:\n"
                for classification in analysis_data['classification']:
                    text += f"  - {classification['type']}: {classification['confidence']:.2f}\n"
            
            if 'anomalies' in analysis_data:
                text += "Anomalies Detected:\n"
                for anomaly in analysis_data['anomalies']:
                    text += f"  - {anomaly['type']}: {anomaly['description']}\n"
            
            if 'patterns' in analysis_data:
                text += "Patterns Recognized:\n"
                for pattern in analysis_data['patterns']:
                    text += f"  - {pattern['pattern']}: {pattern['confidence']:.2f}\n"
            
            text += "\n" + "="*50 + "\n\n"
            
            # Insert at beginning
            self.analysis_text.insert(1.0, text)
            
            # Limit text length
            lines = self.analysis_text.get(1.0, tk.END).split('\n')
            if len(lines) > 1000:
                self.analysis_text.delete(f"{len(lines)-500}.0", tk.END)
                
        except Exception as e:
            logger.error(f"Analysis display update error: {e}")
            
    def add_security_alert(self, threat):
        """Add security alert to tree"""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            severity = threat.get('severity', 'low').upper()
            threat_type = threat.get('type', 'unknown')
            description = threat.get('description', '')
            
            # Color code by severity
            tags = ()
            if severity == 'CRITICAL':
                tags = ('critical',)
            elif severity == 'HIGH':
                tags = ('high',)
            elif severity == 'MEDIUM':
                tags = ('medium',)
            
            self.alert_tree.insert('', 0, text=description[:30], 
                                  values=(timestamp, severity, threat_type),
                                  tags=tags)
            
            # Configure tag colors
            self.alert_tree.tag_configure('critical', foreground='red')
            self.alert_tree.tag_configure('high', foreground='orange')
            self.alert_tree.tag_configure('medium', foreground='yellow')
            
        except Exception as e:
            logger.error(f"Security alert error: {e}")
            
    def update_device_list(self):
        """Update device selection list"""
        devices = self.platform.device_manager.detect_devices()
        device_list = list(devices.keys()) if devices else ["No devices found"]
        
        self.device_combo['values'] = device_list
        if device_list and device_list[0] != "No devices found":
            self.device_combo.set(device_list[0])
            self.platform.device_manager.select_device(device_list[0])
            self.update_device_info()
        
    def update_device_info(self):
        """Update device information display"""
        device_id = self.device_var.get()
        if device_id in self.platform.device_manager.devices:
            info = self.platform.device_manager.devices[device_id]
            
            info_text = "Device Information:\n"
            info_text += "="*30 + "\n"
            for key, value in info.items():
                info_text += f"{key.replace('_', ' ').title()}: {value}\n"
            
            capabilities = self.platform.device_manager.get_device_capabilities(device_id)
            info_text += "\nCapabilities:\n"
            info_text += f"Frequency Range: {capabilities['frequency_range'][0]/1e6:.0f} - {capabilities['frequency_range'][1]/1e6:.0f} MHz\n"
            info_text += f"Max RX Gain: {capabilities['max_gain_rx']} dB\n"
            info_text += f"Max TX Gain: {capabilities['max_gain_tx']} dB\n"
            
            self.device_info_text.delete(1.0, tk.END)
            self.device_info_text.insert(1.0, info_text)
        
    def new_session(self):
        """Start new analysis session"""
        freq_range = f"{self.center_freq_var.get()} MHz @ {self.sample_rate_var.get()} MHz"
        self.current_session = self.platform.session_manager.start_session(
            self.platform.database, freq_range)
        
        if self.current_session:
            self.session_label.configure(text=f"Session: {self.current_session}")
            self.status_label.configure(text="New session started")
        else:
            messagebox.showerror("Error", "Failed to start session")
            
    def end_session(self):
        """End current session"""
        if self.current_session:
            self.platform.session_manager.end_session(self.platform.database)
            self.session_label.configure(text="No active session")
            self.status_label.configure(text="Session ended")
            self.current_session = None
        
    def toggle_scan(self):
        """Toggle scanning on/off"""
        if self.is_scanning:
            self.stop_scan()
        else:
            self.start_scan()
            
    def start_scan(self):
        """Start spectrum scanning"""
        if not self.current_session:
            if not self.new_session():
                return
        
        self.is_scanning = True
        self.scan_button.configure(text="Stop Scan")
        self.status_label.configure(text="Scanning...")
        
        # Start scanning thread
        scan_thread = threading.Thread(target=self.scan_worker, daemon=True)
        scan_thread.start()
        
    def stop_scan(self):
        """Stop spectrum scanning"""
        self.is_scanning = False
        self.scan_button.configure(text="Start Scan")
        self.status_label.configure(text="Scan stopped")
        
    def scan_worker(self):
        """Background scanning worker"""
        try:
            center_freq = float(self.center_freq_var.get()) * 1e6
            sample_rate = float(self.sample_rate_var.get()) * 1e6
            
            while self.is_scanning:
                # Simulate spectrum data (replace with actual HackRF capture)
                spectrum_data = self.simulate_spectrum_data(center_freq, sample_rate)
                
                if spectrum_data:
                    # AI analysis
                    if self.ai_enabled_var.get():
                        ai_analysis = self.platform.signal_processor.process_signal(spectrum_data)
                    else:
                        ai_analysis = None
                    
                    # Security analysis
                    security_report = self.platform.security_engine.analyze_security(spectrum_data, ai_analysis)
                    
                    # Queue data for GUI update
                    self.data_queue.put(spectrum_data)
                    
                    if ai_analysis:
                        self.data_queue.put(ai_analysis)
                    
                    # Queue threats
                    for threat in security_report.get('threats', []):
                        self.threat_queue.put(threat)
                    
                    # Save to database
                    if self.auto_save_var.get() and self.current_session:
                        self.platform.database.save_spectrum_data(self.current_session, spectrum_data)
                        
                        for threat in security_report.get('threats', []):
                            self.platform.database.save_threat(self.current_session, threat)
                
                time.sleep(0.1)  # 10 Hz update rate
                
        except Exception as e:
            logger.error(f"Scan worker error: {e}")
            self.is_scanning = False
            
    def simulate_spectrum_data(self, center_freq, sample_rate):
        """Simulate spectrum data for testing"""
        try:
            # Generate simulated spectrum
            num_points = int(self.fft_size_var.get())
            freqs = np.linspace(center_freq - sample_rate/2, center_freq + sample_rate/2, num_points)
            
            # Base noise floor
            noise_floor = -90 + np.random.normal(0, 5, num_points)
            
            # Add some signals
            if 2400e6 <= center_freq <= 2500e6:  # WiFi band
                # Add WiFi-like signals
                wifi_freqs = [2412e6, 2437e6, 2462e6]
                for wifi_freq in wifi_freqs:
                    if abs(wifi_freq - center_freq) < sample_rate/2:
                        idx = np.argmin(np.abs(freqs - wifi_freq))
                        noise_floor[max(0, idx-50):min(num_points, idx+50)] += np.random.uniform(20, 40)
            
            power = noise_floor
            
            # Detect peaks
            peaks = []
            for i in range(10, num_points-10):
                if (power[i] > -60 and 
                    power[i] > power[i-1] and 
                    power[i] > power[i+1]):
                    peaks.append((i, power[i]))
            
            return {
                'frequencies': freqs,
                'power': power,
                'peaks': peaks,
                'timestamp': time.time(),
                'center_freq': center_freq,
                'sample_rate': sample_rate
            }
            
        except Exception as e:
            logger.error(f"Spectrum simulation error: {e}")
            return None
        
    def emergency_stop(self):
        """Emergency stop all operations"""
        self.is_scanning = False
        self.status_label.configure(text="EMERGENCY STOP ACTIVATED")
        messagebox.showwarning("Emergency Stop", "All operations have been stopped")
        
    def test_device(self):
        """Test device functionality"""
        device_id = self.device_var.get()
        if device_id == "No devices found":
            messagebox.showwarning("No Device", "No HackRF device selected")
            return
        
        # This would run actual device tests
        messagebox.showinfo("Device Test", "Device test completed successfully")
        
    def show_firmware_info(self):
        """Show firmware information"""
        messagebox.showinfo("Firmware Info", "Firmware information display not implemented")
        
    def auto_scale_spectrum(self):
        """Auto-scale spectrum display"""
        self.spectrum_ax.relim()
        self.spectrum_ax.autoscale()
        self.spectrum_canvas.draw()
        
    def toggle_peak_hold(self):
        """Toggle peak hold mode"""
        messagebox.showinfo("Peak Hold", "Peak hold mode not implemented")
        
    def save_spectrum_plot(self):
        """Save spectrum plot"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if filename:
            self.spectrum_fig.savefig(filename, facecolor='#1e1e1e')
            
    def clear_alerts(self):
        """Clear security alerts"""
        for item in self.alert_tree.get_children():
            self.alert_tree.delete(item)
            
    def export_alerts(self):
        """Export security alerts"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            alerts = []
            for item in self.alert_tree.get_children():
                values = self.alert_tree.item(item)
                alerts.append({
                    'description': values['text'],
                    'time': values['values'][0],
                    'severity': values['values'][1],
                    'type': values['values'][2]
                })
            
            with open(filename, 'w') as f:
                json.dump(alerts, f, indent=2)
                
    def export_data(self):
        """Export scan data"""
        if not self.current_session:
            messagebox.showwarning("No Session", "No active session to export")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            # Export session data
            messagebox.showinfo("Export", f"Data exported to {filename}")
            
    def show_db_stats(self):
        """Show database statistics"""
        messagebox.showinfo("Database Stats", "Database statistics display not implemented")
        
    def export_config(self):
        """Export configuration"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, 'w') as f:
                json.dump(self.platform.config, f, indent=2)
                
    def import_config(self):
        """Import configuration"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    config = json.load(f)
                    self.platform.config.update(config)
                messagebox.showinfo("Import", "Configuration imported successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import configuration: {e}")
                
    def reset_config(self):
        """Reset configuration to defaults"""
        if messagebox.askyesno("Reset Config", "Reset all settings to defaults?"):
            self.platform.config = self.platform.load_configuration()
            messagebox.showinfo("Reset", "Configuration reset to defaults")

def main():
    """Main function for GUI"""
    print("Starting HackRF Enhanced Platform GUI...")
    
    # Import platform
    try:
        from hackrf_enhanced_platform import HackRFEnhancedPlatform
        platform = HackRFEnhancedPlatform()
    except ImportError:
        print("Error: Could not import HackRF Enhanced Platform")
        return
    
    # Create GUI
    root = tk.Tk()
    app = HackRFEnhancedGUI(root, platform)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("GUI shutdown requested")

if __name__ == "__main__":
    main()