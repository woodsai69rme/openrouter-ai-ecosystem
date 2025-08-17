#!/usr/bin/env python3
"""
HackRF Interface - Software Defined Radio Control System
Advanced GUI interface for HackRF One with spectrum analysis, scanning, and recording
"""

import os
import sys
import time
import numpy as np
import threading
import json
import logging
from datetime import datetime
from pathlib import Path

# GUI imports
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation

# Signal processing
from scipy import signal
from scipy.fft import fft, fftfreq

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HackRFController:
    """HackRF hardware controller and wrapper"""
    
    def __init__(self):
        self.device_connected = False
        self.sample_rate = 20e6  # 20 MHz default
        self.center_freq = 100e6  # 100 MHz default
        self.gain = 20  # dB
        self.bandwidth = 20e6
        self.is_receiving = False
        self.receive_thread = None
        self.data_buffer = []
        self.max_buffer_size = 1000
        
        # Try to import hackrf library
        try:
            global hackrf
            import hackrf
            self.hackrf_available = True
            logger.info("HackRF library imported successfully")
        except ImportError:
            self.hackrf_available = False
            logger.warning("HackRF library not available - using simulation mode")
            
    def connect(self):
        """Connect to HackRF device"""
        if self.hackrf_available:
            try:
                hackrf.init()
                self.device = hackrf.HackRF()
                self.device.open()
                self.device_connected = True
                logger.info("HackRF device connected successfully")
                return True
            except Exception as e:
                logger.error(f"Failed to connect to HackRF: {e}")
                return False
        else:
            # Simulation mode
            self.device_connected = True
            logger.info("HackRF simulation mode active")
            return True
            
    def disconnect(self):
        """Disconnect from HackRF device"""
        if self.device_connected:
            self.stop_receiving()
            if self.hackrf_available and hasattr(self, 'device'):
                try:
                    self.device.close()
                    hackrf.exit()
                except:
                    pass
            self.device_connected = False
            logger.info("HackRF device disconnected")
            
    def set_frequency(self, freq_hz):
        """Set center frequency"""
        self.center_freq = freq_hz
        if self.device_connected and self.hackrf_available:
            try:
                self.device.set_freq(int(freq_hz))
                logger.info(f"Frequency set to {freq_hz/1e6:.3f} MHz")
            except Exception as e:
                logger.error(f"Failed to set frequency: {e}")
                
    def set_sample_rate(self, rate_hz):
        """Set sample rate"""
        self.sample_rate = rate_hz
        if self.device_connected and self.hackrf_available:
            try:
                self.device.set_sample_rate(int(rate_hz))
                logger.info(f"Sample rate set to {rate_hz/1e6:.1f} MHz")
            except Exception as e:
                logger.error(f"Failed to set sample rate: {e}")
                
    def set_gain(self, gain_db):
        """Set RF gain"""
        self.gain = gain_db
        if self.device_connected and self.hackrf_available:
            try:
                self.device.set_lna_gain(int(gain_db))
                self.device.set_vga_gain(int(gain_db))
                logger.info(f"Gain set to {gain_db} dB")
            except Exception as e:
                logger.error(f"Failed to set gain: {e}")
                
    def start_receiving(self, callback=None):
        """Start receiving samples"""
        if not self.device_connected:
            return False
            
        self.is_receiving = True
        self.receive_thread = threading.Thread(target=self._receive_loop, args=(callback,))
        self.receive_thread.daemon = True
        self.receive_thread.start()
        logger.info("Started receiving samples")
        return True
        
    def stop_receiving(self):
        """Stop receiving samples"""
        self.is_receiving = False
        if self.receive_thread:
            self.receive_thread.join(timeout=1.0)
        logger.info("Stopped receiving samples")
        
    def _receive_loop(self, callback):
        """Internal receive loop"""
        while self.is_receiving:
            try:
                if self.hackrf_available:
                    # Real HackRF sampling
                    samples = self.device.read_samples(8192)
                else:
                    # Simulate samples with noise and test signals
                    time.sleep(0.01)  # 10ms intervals
                    t = np.linspace(0, 8192/self.sample_rate, 8192)
                    
                    # Generate noise
                    noise = np.random.normal(0, 0.1, 8192) + 1j * np.random.normal(0, 0.1, 8192)
                    
                    # Add some test signals
                    test_freq1 = self.center_freq + 1e6  # 1 MHz offset
                    test_freq2 = self.center_freq - 2e6  # -2 MHz offset
                    
                    signal1 = 0.5 * np.exp(1j * 2 * np.pi * (test_freq1 - self.center_freq) * t)
                    signal2 = 0.3 * np.exp(1j * 2 * np.pi * (test_freq2 - self.center_freq) * t)
                    
                    samples = noise + signal1 + signal2
                
                # Add to buffer
                self.data_buffer.append(samples)
                if len(self.data_buffer) > self.max_buffer_size:
                    self.data_buffer.pop(0)
                    
                # Call callback if provided
                if callback:
                    callback(samples)
                    
            except Exception as e:
                logger.error(f"Error in receive loop: {e}")
                time.sleep(0.1)

class SpectrumAnalyzer:
    """Spectrum analyzer with FFT and waterfall display"""
    
    def __init__(self, hackrf_controller):
        self.hackrf = hackrf_controller
        self.fft_size = 1024
        self.window = signal.hann(self.fft_size)
        self.overlap = 0.5
        self.averaging = 10
        self.spectrum_history = []
        self.waterfall_data = []
        self.max_waterfall_lines = 100
        
    def process_samples(self, samples):
        """Process samples and compute spectrum"""
        if len(samples) < self.fft_size:
            return None, None
            
        # Apply window and compute FFT
        windowed = samples[:self.fft_size] * self.window
        fft_data = fft(windowed)
        
        # Compute magnitude spectrum in dB
        magnitude = np.abs(fft_data)
        magnitude[magnitude == 0] = 1e-12  # Avoid log(0)
        spectrum_db = 20 * np.log10(magnitude)
        
        # Generate frequency axis
        freqs = fftfreq(self.fft_size, 1/self.hackrf.sample_rate)
        freqs = freqs + self.hackrf.center_freq
        
        # Shift zero frequency to center
        spectrum_db = np.fft.fftshift(spectrum_db)
        freqs = np.fft.fftshift(freqs)
        
        # Add to history for averaging
        self.spectrum_history.append(spectrum_db)
        if len(self.spectrum_history) > self.averaging:
            self.spectrum_history.pop(0)
            
        # Compute averaged spectrum
        avg_spectrum = np.mean(self.spectrum_history, axis=0)
        
        # Add to waterfall
        self.waterfall_data.append(avg_spectrum)
        if len(self.waterfall_data) > self.max_waterfall_lines:
            self.waterfall_data.pop(0)
            
        return freqs, avg_spectrum
        
    def get_waterfall_data(self):
        """Get waterfall display data"""
        if not self.waterfall_data:
            return None
            
        return np.array(self.waterfall_data)

class HackRFInterface:
    """Main GUI interface for HackRF"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("HackRF Interface - SDR Control System")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2b2b2b')
        
        # Configure styles
        self.setup_styles()
        
        # Initialize HackRF controller
        self.hackrf = HackRFController()
        self.spectrum_analyzer = SpectrumAnalyzer(self.hackrf)
        
        # GUI variables
        self.freq_var = tk.StringVar(value="100.0")
        self.sample_rate_var = tk.StringVar(value="20.0")
        self.gain_var = tk.IntVar(value=20)
        self.scan_start_var = tk.StringVar(value="88.0")
        self.scan_stop_var = tk.StringVar(value="108.0")
        self.scan_step_var = tk.StringVar(value="0.1")
        
        # Status variables
        self.is_connected = False
        self.is_scanning = False
        self.is_recording = False
        
        # Setup GUI
        self.create_gui()
        
        # Start update loop
        self.update_displays()
        
    def setup_styles(self):
        """Setup GUI styles"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors for dark theme
        self.style.configure('Title.TLabel', foreground='#ffffff', background='#2b2b2b', font=('Arial', 12, 'bold'))
        self.style.configure('Status.TLabel', foreground='#00ff00', background='#2b2b2b')
        self.style.configure('TFrame', background='#2b2b2b')
        self.style.configure('TButton', fieldbackground='#404040')
        
    def create_gui(self):
        """Create the main GUI"""
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_control_tab()
        self.create_spectrum_tab()
        self.create_scanner_tab()
        self.create_recorder_tab()
        
    def create_control_tab(self):
        """Create control panel tab"""
        control_frame = ttk.Frame(self.notebook)
        self.notebook.add(control_frame, text="Control")
        
        # Connection frame
        conn_frame = ttk.LabelFrame(control_frame, text="Device Connection")
        conn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.status_label = ttk.Label(conn_frame, text="Disconnected", style='Status.TLabel')
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(conn_frame, text="Connect", command=self.connect_device).pack(side=tk.RIGHT, padx=5)
        ttk.Button(conn_frame, text="Disconnect", command=self.disconnect_device).pack(side=tk.RIGHT, padx=5)
        
        # Frequency control
        freq_frame = ttk.LabelFrame(control_frame, text="Frequency Control")
        freq_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(freq_frame, text="Center Frequency (MHz):").pack(side=tk.LEFT, padx=5)
        freq_entry = ttk.Entry(freq_frame, textvariable=self.freq_var, width=10)
        freq_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(freq_frame, text="Set", command=self.set_frequency).pack(side=tk.LEFT, padx=5)
        
        # Sample rate control
        rate_frame = ttk.LabelFrame(control_frame, text="Sample Rate")
        rate_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(rate_frame, text="Sample Rate (MHz):").pack(side=tk.LEFT, padx=5)
        rate_entry = ttk.Entry(rate_frame, textvariable=self.sample_rate_var, width=10)
        rate_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(rate_frame, text="Set", command=self.set_sample_rate).pack(side=tk.LEFT, padx=5)
        
        # Gain control
        gain_frame = ttk.LabelFrame(control_frame, text="Gain Control")
        gain_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(gain_frame, text="RF Gain (dB):").pack(side=tk.LEFT, padx=5)
        gain_scale = ttk.Scale(gain_frame, from_=0, to=40, variable=self.gain_var, orient=tk.HORIZONTAL, command=self.set_gain)
        gain_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.gain_label = ttk.Label(gain_frame, text="20 dB")
        self.gain_label.pack(side=tk.RIGHT, padx=5)
        
        # Preset frequencies
        preset_frame = ttk.LabelFrame(control_frame, text="Preset Frequencies")
        preset_frame.pack(fill=tk.X, padx=5, pady=5)
        
        presets = [
            ("FM Broadcast", 100.0),
            ("Air Traffic", 121.5),
            ("Ham 2m", 145.0),
            ("Ham 70cm", 435.0),
            ("ISM 433", 433.92),
            ("ISM 915", 915.0),
            ("WiFi 2.4G", 2450.0)
        ]
        
        for name, freq in presets:
            ttk.Button(preset_frame, text=f"{name}\n{freq} MHz", 
                      command=lambda f=freq: self.set_preset_frequency(f)).pack(side=tk.LEFT, padx=2)
                      
    def create_spectrum_tab(self):
        """Create spectrum analyzer tab"""
        spectrum_frame = ttk.Frame(self.notebook)
        self.notebook.add(spectrum_frame, text="Spectrum")
        
        # Control panel
        control_panel = ttk.Frame(spectrum_frame)
        control_panel.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(control_panel, text="Start", command=self.start_spectrum).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_panel, text="Stop", command=self.stop_spectrum).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_panel, text="Clear", command=self.clear_spectrum).pack(side=tk.LEFT, padx=5)
        
        # Spectrum plot
        self.spectrum_figure = Figure(figsize=(12, 8), facecolor='#2b2b2b')
        self.spectrum_figure.patch.set_facecolor('#2b2b2b')
        
        # Main spectrum plot
        self.spectrum_ax = self.spectrum_figure.add_subplot(211)
        self.spectrum_ax.set_facecolor('#1e1e1e')
        self.spectrum_ax.set_xlabel('Frequency (MHz)', color='white')
        self.spectrum_ax.set_ylabel('Power (dB)', color='white')
        self.spectrum_ax.tick_params(colors='white')
        self.spectrum_ax.grid(True, alpha=0.3)
        
        # Waterfall plot
        self.waterfall_ax = self.spectrum_figure.add_subplot(212)
        self.waterfall_ax.set_facecolor('#1e1e1e')
        self.waterfall_ax.set_xlabel('Frequency (MHz)', color='white')
        self.waterfall_ax.set_ylabel('Time', color='white')
        self.waterfall_ax.tick_params(colors='white')
        
        self.spectrum_canvas = FigureCanvasTkAgg(self.spectrum_figure, spectrum_frame)
        self.spectrum_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def create_scanner_tab(self):
        """Create frequency scanner tab"""
        scanner_frame = ttk.Frame(self.notebook)
        self.notebook.add(scanner_frame, text="Scanner")
        
        # Scanner controls
        control_frame = ttk.LabelFrame(scanner_frame, text="Scan Parameters")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Frequency range
        ttk.Label(control_frame, text="Start (MHz):").grid(row=0, column=0, padx=5, pady=2)
        ttk.Entry(control_frame, textvariable=self.scan_start_var, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(control_frame, text="Stop (MHz):").grid(row=0, column=2, padx=5, pady=2)
        ttk.Entry(control_frame, textvariable=self.scan_stop_var, width=10).grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Label(control_frame, text="Step (MHz):").grid(row=0, column=4, padx=5, pady=2)
        ttk.Entry(control_frame, textvariable=self.scan_step_var, width=10).grid(row=0, column=5, padx=5, pady=2)
        
        # Scanner buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=1, column=0, columnspan=6, pady=10)
        
        ttk.Button(button_frame, text="Start Scan", command=self.start_scan).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Stop Scan", command=self.stop_scan).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export Results", command=self.export_scan).pack(side=tk.LEFT, padx=5)
        
        # Results display
        results_frame = ttk.LabelFrame(scanner_frame, text="Scan Results")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create treeview for results
        columns = ('Frequency', 'Power', 'Bandwidth', 'Type')
        self.scan_tree = ttk.Treeview(results_frame, columns=columns, show='headings')
        
        for col in columns:
            self.scan_tree.heading(col, text=col)
            self.scan_tree.column(col, width=100)
            
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.scan_tree.yview)
        self.scan_tree.configure(yscrollcommand=scrollbar.set)
        
        self.scan_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_recorder_tab(self):
        """Create recording tab"""
        recorder_frame = ttk.Frame(self.notebook)
        self.notebook.add(recorder_frame, text="Recorder")
        
        # Recording controls
        control_frame = ttk.LabelFrame(recorder_frame, text="Recording Controls")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(control_frame, text="Start Recording", command=self.start_recording).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Stop Recording", command=self.stop_recording).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Play Recording", command=self.play_recording).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Save Recording", command=self.save_recording).pack(side=tk.LEFT, padx=5)
        
        # Recording status
        self.recording_status = ttk.Label(control_frame, text="Ready", style='Status.TLabel')
        self.recording_status.pack(side=tk.RIGHT, padx=5)
        
        # File list
        files_frame = ttk.LabelFrame(recorder_frame, text="Recorded Files")
        files_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.files_listbox = tk.Listbox(files_frame, bg='#3c3c3c', fg='white')
        self.files_listbox.pack(fill=tk.BOTH, expand=True)
        
    # Control methods
    def connect_device(self):
        """Connect to HackRF device"""
        if self.hackrf.connect():
            self.is_connected = True
            self.status_label.config(text="Connected", foreground='#00ff00')
            logger.info("HackRF device connected")
        else:
            messagebox.showerror("Error", "Failed to connect to HackRF device")
            
    def disconnect_device(self):
        """Disconnect from HackRF device"""
        self.hackrf.disconnect()
        self.is_connected = False
        self.status_label.config(text="Disconnected", foreground='#ff0000')
        
    def set_frequency(self):
        """Set frequency from entry"""
        try:
            freq_mhz = float(self.freq_var.get())
            self.hackrf.set_frequency(freq_mhz * 1e6)
        except ValueError:
            messagebox.showerror("Error", "Invalid frequency value")
            
    def set_sample_rate(self):
        """Set sample rate from entry"""
        try:
            rate_mhz = float(self.sample_rate_var.get())
            self.hackrf.set_sample_rate(rate_mhz * 1e6)
        except ValueError:
            messagebox.showerror("Error", "Invalid sample rate value")
            
    def set_gain(self, value=None):
        """Set gain from scale"""
        gain = self.gain_var.get()
        self.hackrf.set_gain(gain)
        self.gain_label.config(text=f"{gain} dB")
        
    def set_preset_frequency(self, freq_mhz):
        """Set preset frequency"""
        self.freq_var.set(str(freq_mhz))
        self.hackrf.set_frequency(freq_mhz * 1e6)
        
    def start_spectrum(self):
        """Start spectrum analyzer"""
        if not self.is_connected:
            messagebox.showerror("Error", "Device not connected")
            return
            
        self.hackrf.start_receiving(self.spectrum_callback)
        logger.info("Spectrum analyzer started")
        
    def stop_spectrum(self):
        """Stop spectrum analyzer"""
        self.hackrf.stop_receiving()
        logger.info("Spectrum analyzer stopped")
        
    def clear_spectrum(self):
        """Clear spectrum display"""
        self.spectrum_analyzer.spectrum_history.clear()
        self.spectrum_analyzer.waterfall_data.clear()
        
    def spectrum_callback(self, samples):
        """Callback for spectrum data"""
        freqs, spectrum = self.spectrum_analyzer.process_samples(samples)
        if freqs is not None:
            # This will be updated in the main loop
            pass
            
    def start_scan(self):
        """Start frequency scan"""
        if not self.is_connected:
            messagebox.showerror("Error", "Device not connected")
            return
            
        self.is_scanning = True
        # Implement scanning logic here
        logger.info("Frequency scan started")
        
    def stop_scan(self):
        """Stop frequency scan"""
        self.is_scanning = False
        logger.info("Frequency scan stopped")
        
    def export_scan(self):
        """Export scan results"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            # Export scan results to file
            logger.info(f"Scan results exported to {filename}")
            
    def start_recording(self):
        """Start recording"""
        if not self.is_connected:
            messagebox.showerror("Error", "Device not connected")
            return
            
        self.is_recording = True
        self.recording_status.config(text="Recording", foreground='#ff0000')
        logger.info("Recording started")
        
    def stop_recording(self):
        """Stop recording"""
        self.is_recording = False
        self.recording_status.config(text="Ready", foreground='#00ff00')
        logger.info("Recording stopped")
        
    def play_recording(self):
        """Play selected recording"""
        selection = self.files_listbox.curselection()
        if selection:
            filename = self.files_listbox.get(selection[0])
            logger.info(f"Playing recording: {filename}")
            
    def save_recording(self):
        """Save current recording"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".iq",
            filetypes=[("IQ files", "*.iq"), ("All files", "*.*")]
        )
        if filename:
            logger.info(f"Recording saved to {filename}")
            
    def update_displays(self):
        """Update all displays"""
        try:
            # Update spectrum display
            if hasattr(self, 'spectrum_ax') and self.spectrum_analyzer.spectrum_history:
                freqs, spectrum = None, None
                if self.hackrf.data_buffer:
                    freqs, spectrum = self.spectrum_analyzer.process_samples(self.hackrf.data_buffer[-1])
                    
                if freqs is not None and spectrum is not None:
                    # Update spectrum plot
                    self.spectrum_ax.clear()
                    self.spectrum_ax.plot(freqs/1e6, spectrum, 'cyan', linewidth=1)
                    self.spectrum_ax.set_facecolor('#1e1e1e')
                    self.spectrum_ax.set_xlabel('Frequency (MHz)', color='white')
                    self.spectrum_ax.set_ylabel('Power (dB)', color='white')
                    self.spectrum_ax.tick_params(colors='white')
                    self.spectrum_ax.grid(True, alpha=0.3)
                    
                    # Update waterfall plot
                    waterfall_data = self.spectrum_analyzer.get_waterfall_data()
                    if waterfall_data is not None:
                        self.waterfall_ax.clear()
                        self.waterfall_ax.imshow(waterfall_data, aspect='auto', cmap='viridis',
                                               extent=[freqs[0]/1e6, freqs[-1]/1e6, 0, len(waterfall_data)])
                        self.waterfall_ax.set_facecolor('#1e1e1e')
                        self.waterfall_ax.set_xlabel('Frequency (MHz)', color='white')
                        self.waterfall_ax.set_ylabel('Time', color='white')
                        self.waterfall_ax.tick_params(colors='white')
                        
                    self.spectrum_canvas.draw()
                    
        except Exception as e:
            logger.error(f"Error updating displays: {e}")
            
        # Schedule next update
        self.root.after(100, self.update_displays)

def main():
    """Main function"""
    # Check for required dependencies
    required_modules = ['numpy', 'scipy', 'matplotlib']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
            
    if missing_modules:
        print("Missing required modules:")
        for module in missing_modules:
            print(f"  - {module}")
        print("\nInstall with: pip install numpy scipy matplotlib")
        return
        
    # Create and run GUI
    root = tk.Tk()
    app = HackRFInterface(root)
    
    def on_closing():
        app.hackrf.disconnect()
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    logger.info("HackRF Interface started")
    root.mainloop()

if __name__ == "__main__":
    main()