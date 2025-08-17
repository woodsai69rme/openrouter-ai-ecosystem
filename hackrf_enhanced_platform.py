#!/usr/bin/env python3
"""
HackRF Enhanced Platform - Ultimate SDR Management System
Advanced Software Defined Radio platform for authorized security testing
Integrates all HackRF tools with enhanced capabilities and AI-driven analysis
"""

import os
import sys
import json
import time
import threading
import subprocess
import logging
import hashlib
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from collections import defaultdict, deque
import requests
import queue
import signal

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('hackrf_platform.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class HackRFEnhancedPlatform:
    """Enhanced HackRF platform with AI-driven capabilities"""
    
    def __init__(self):
        self.version = "2.0.0"
        self.device_manager = HackRFDeviceManager()
        self.spectrum_analyzer = EnhancedSpectrumAnalyzer()
        self.signal_processor = AISignalProcessor()
        self.security_engine = AdvancedSecurityEngine()
        self.protocol_analyzer = ProtocolAnalyzer()
        self.database = HackRFDatabase()
        self.session_manager = SessionManager()
        
        # Platform state
        self.running = False
        self.current_session = None
        self.real_time_data = deque(maxlen=10000)
        self.analysis_queue = queue.Queue()
        
        # Configuration
        self.config = self.load_configuration()
        
        logger.info(f"HackRF Enhanced Platform v{self.version} initialized")
    
    def load_configuration(self):
        """Load platform configuration"""
        default_config = {
            'device': {
                'auto_detect': True,
                'preferred_sample_rate': 2000000,
                'default_gain': 20,
                'frequency_correction': 0
            },
            'analysis': {
                'ai_enhancement': True,
                'real_time_processing': True,
                'threat_detection': True,
                'protocol_analysis': True
            },
            'security': {
                'authorized_frequencies': [
                    [2400e6, 2485e6],  # WiFi 2.4GHz
                    [5150e6, 5850e6],  # WiFi 5GHz
                    [433e6, 434e6],    # ISM 433MHz
                    [915e6, 916e6]     # ISM 915MHz
                ],
                'threat_thresholds': {
                    'power_anomaly': -30,
                    'frequency_violation': True,
                    'jamming_detection': True
                }
            },
            'gui': {
                'theme': 'dark',
                'update_interval': 100,
                'max_plot_points': 1000
            }
        }
        
        config_file = Path('hackrf_config.json')
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                logger.warning(f"Could not load config: {e}")
        
        return default_config
    
    def save_configuration(self):
        """Save current configuration"""
        try:
            with open('hackrf_config.json', 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save config: {e}")

class HackRFDeviceManager:
    """Advanced device management with multiple device support"""
    
    def __init__(self):
        self.devices = {}
        self.active_device = None
        self.device_capabilities = {}
        
    def detect_devices(self):
        """Detect connected HackRF devices"""
        logger.info("Detecting HackRF devices...")
        detected = {}
        
        try:
            # Check for HackRF devices
            result = subprocess.run(['hackrf_info'], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                device_info = self.parse_device_info(result.stdout)
                device_id = device_info.get('serial', 'unknown')
                detected[device_id] = device_info
                logger.info(f"Detected HackRF: {device_id}")
            
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            logger.warning(f"Device detection failed: {e}")
        
        self.devices = detected
        return detected
    
    def parse_device_info(self, output):
        """Parse hackrf_info output"""
        info = {}
        for line in output.split('\n'):
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower().replace(' ', '_')
                value = value.strip()
                info[key] = value
        return info
    
    def select_device(self, device_id):
        """Select active device"""
        if device_id in self.devices:
            self.active_device = device_id
            logger.info(f"Selected device: {device_id}")
            return True
        return False
    
    def get_device_capabilities(self, device_id=None):
        """Get device capabilities"""
        if device_id is None:
            device_id = self.active_device
        
        if device_id not in self.device_capabilities:
            # Default HackRF One capabilities
            self.device_capabilities[device_id] = {
                'frequency_range': [1e6, 6e9],
                'sample_rates': [2e6, 4e6, 8e6, 10e6, 12.5e6, 16e6, 20e6],
                'max_gain_tx': 47,
                'max_gain_rx': 40,
                'antenna_power': True,
                'duplex': False
            }
        
        return self.device_capabilities[device_id]

class EnhancedSpectrumAnalyzer:
    """Advanced spectrum analysis with AI enhancement"""
    
    def __init__(self):
        self.fft_size = 8192
        self.overlap = 0.5
        self.window = 'hann'
        self.averaging = 10
        self.peak_detection = True
        self.waterfall_data = deque(maxlen=1000)
        
    def analyze_spectrum(self, data, sample_rate, center_freq):
        """Perform enhanced spectrum analysis"""
        try:
            # Convert to complex if needed
            if data.dtype == np.uint8:
                data = data.astype(np.float32)
                data = (data - 127.5) / 127.5
                data = data[::2] + 1j * data[1::2]
            
            # Windowing
            window = np.hanning(len(data))
            windowed_data = data * window
            
            # FFT
            fft_data = np.fft.fftshift(np.fft.fft(windowed_data, self.fft_size))
            
            # Power spectrum
            power_spectrum = 20 * np.log10(np.abs(fft_data) + 1e-12)
            
            # Frequency bins
            freqs = np.fft.fftshift(np.fft.fftfreq(self.fft_size, 1/sample_rate))
            freqs += center_freq
            
            # Peak detection
            peaks = self.detect_peaks(power_spectrum) if self.peak_detection else []
            
            # Update waterfall
            self.waterfall_data.append(power_spectrum)
            
            return {
                'frequencies': freqs,
                'power': power_spectrum,
                'peaks': peaks,
                'timestamp': time.time(),
                'center_freq': center_freq,
                'sample_rate': sample_rate
            }
            
        except Exception as e:
            logger.error(f"Spectrum analysis error: {e}")
            return None
    
    def detect_peaks(self, power_spectrum, threshold=-60, min_distance=10):
        """Detect spectral peaks"""
        peaks = []
        
        try:
            # Simple peak detection
            for i in range(min_distance, len(power_spectrum) - min_distance):
                if (power_spectrum[i] > threshold and
                    power_spectrum[i] > power_spectrum[i-1] and
                    power_spectrum[i] > power_spectrum[i+1]):
                    
                    # Check minimum distance
                    too_close = False
                    for peak_idx, _ in peaks:
                        if abs(i - peak_idx) < min_distance:
                            too_close = True
                            break
                    
                    if not too_close:
                        peaks.append((i, power_spectrum[i]))
            
        except Exception as e:
            logger.error(f"Peak detection error: {e}")
        
        return peaks

class AISignalProcessor:
    """AI-enhanced signal processing and analysis"""
    
    def __init__(self):
        self.signal_classifier = SignalClassifier()
        self.anomaly_detector = AnomalyDetector()
        self.pattern_recognizer = PatternRecognizer()
        
    def process_signal(self, spectrum_data):
        """Process signal with AI enhancement"""
        if not spectrum_data:
            return None
        
        try:
            analysis = {
                'timestamp': spectrum_data['timestamp'],
                'classification': self.signal_classifier.classify(spectrum_data),
                'anomalies': self.anomaly_detector.detect(spectrum_data),
                'patterns': self.pattern_recognizer.recognize(spectrum_data),
                'statistics': self.compute_statistics(spectrum_data)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"AI signal processing error: {e}")
            return None
    
    def compute_statistics(self, spectrum_data):
        """Compute spectral statistics"""
        power = spectrum_data['power']
        return {
            'mean_power': np.mean(power),
            'max_power': np.max(power),
            'min_power': np.min(power),
            'std_power': np.std(power),
            'bandwidth': self.estimate_bandwidth(power),
            'spectral_centroid': self.compute_spectral_centroid(spectrum_data)
        }
    
    def estimate_bandwidth(self, power, threshold=-70):
        """Estimate signal bandwidth"""
        above_threshold = power > threshold
        if np.any(above_threshold):
            indices = np.where(above_threshold)[0]
            return len(indices)
        return 0
    
    def compute_spectral_centroid(self, spectrum_data):
        """Compute spectral centroid"""
        freqs = spectrum_data['frequencies']
        power = 10**(spectrum_data['power']/10)  # Convert from dB
        
        if np.sum(power) > 0:
            centroid = np.sum(freqs * power) / np.sum(power)
            return centroid
        return 0

class SignalClassifier:
    """Signal classification engine"""
    
    def __init__(self):
        self.signal_types = {
            'wifi': {
                'frequency_ranges': [(2400e6, 2485e6), (5150e6, 5850e6)],
                'bandwidth': [20e6, 40e6, 80e6],
                'characteristics': ['ofdm', 'bursty']
            },
            'bluetooth': {
                'frequency_ranges': [(2400e6, 2485e6)],
                'bandwidth': [1e6],
                'characteristics': ['fhss', 'short_duration']
            },
            'zigbee': {
                'frequency_ranges': [(2400e6, 2485e6), (915e6, 916e6)],
                'bandwidth': [2e6],
                'characteristics': ['dsss', 'low_power']
            },
            'cellular': {
                'frequency_ranges': [(850e6, 900e6), (1800e6, 1900e6)],
                'bandwidth': [200e3, 1.4e6, 3e6, 5e6, 10e6, 15e6, 20e6],
                'characteristics': ['continuous', 'high_power']
            }
        }
    
    def classify(self, spectrum_data):
        """Classify signal type"""
        classifications = []
        
        center_freq = spectrum_data['center_freq']
        peaks = spectrum_data.get('peaks', [])
        
        for signal_type, properties in self.signal_types.items():
            confidence = self.calculate_confidence(spectrum_data, properties)
            if confidence > 0.5:
                classifications.append({
                    'type': signal_type,
                    'confidence': confidence,
                    'properties': properties
                })
        
        return sorted(classifications, key=lambda x: x['confidence'], reverse=True)
    
    def calculate_confidence(self, spectrum_data, properties):
        """Calculate classification confidence"""
        confidence = 0.0
        
        center_freq = spectrum_data['center_freq']
        
        # Check frequency range
        for freq_range in properties['frequency_ranges']:
            if freq_range[0] <= center_freq <= freq_range[1]:
                confidence += 0.4
                break
        
        # Check bandwidth (simplified)
        if spectrum_data.get('statistics'):
            estimated_bw = spectrum_data['statistics'].get('bandwidth', 0)
            for bw in properties['bandwidth']:
                if abs(estimated_bw - bw) < bw * 0.2:  # 20% tolerance
                    confidence += 0.3
                    break
        
        # Additional characteristics would be checked here
        confidence += 0.3  # Placeholder for other characteristics
        
        return min(confidence, 1.0)

class AnomalyDetector:
    """Detect anomalous signals"""
    
    def __init__(self):
        self.baseline_power = -70  # dBm
        self.power_threshold = 20  # dB above baseline
        self.history = deque(maxlen=100)
        
    def detect(self, spectrum_data):
        """Detect anomalies in spectrum data"""
        anomalies = []
        
        power = spectrum_data['power']
        max_power = np.max(power)
        
        # Store in history
        self.history.append(max_power)
        
        # Power anomaly detection
        if max_power > self.baseline_power + self.power_threshold:
            anomalies.append({
                'type': 'high_power',
                'severity': 'medium',
                'value': max_power,
                'threshold': self.baseline_power + self.power_threshold,
                'description': f'Unusually high power signal: {max_power:.1f} dBm'
            })
        
        # Frequency violation detection
        center_freq = spectrum_data['center_freq']
        if self.is_restricted_frequency(center_freq):
            anomalies.append({
                'type': 'restricted_frequency',
                'severity': 'high',
                'frequency': center_freq,
                'description': f'Signal in restricted frequency: {center_freq/1e6:.3f} MHz'
            })
        
        # Sudden power changes
        if len(self.history) > 10:
            recent_avg = np.mean(list(self.history)[-10:])
            older_avg = np.mean(list(self.history)[-20:-10]) if len(self.history) > 20 else recent_avg
            
            if abs(recent_avg - older_avg) > 15:  # 15 dB change
                anomalies.append({
                    'type': 'power_change',
                    'severity': 'low',
                    'change': recent_avg - older_avg,
                    'description': f'Power change detected: {recent_avg - older_avg:.1f} dB'
                })
        
        return anomalies
    
    def is_restricted_frequency(self, frequency):
        """Check if frequency is in restricted range"""
        # Example restricted ranges (emergency services, etc.)
        restricted_ranges = [
            (450e6, 470e6),   # Emergency services
            (806e6, 824e6),   # Public safety
            (851e6, 869e6),   # Cellular uplink
        ]
        
        for start, end in restricted_ranges:
            if start <= frequency <= end:
                return True
        return False

class PatternRecognizer:
    """Recognize signal patterns"""
    
    def __init__(self):
        self.patterns = {
            'burst': self.detect_burst_pattern,
            'continuous': self.detect_continuous_pattern,
            'periodic': self.detect_periodic_pattern,
            'frequency_hopping': self.detect_fh_pattern
        }
    
    def recognize(self, spectrum_data):
        """Recognize patterns in spectrum data"""
        recognized_patterns = []
        
        for pattern_name, detector in self.patterns.items():
            try:
                result = detector(spectrum_data)
                if result:
                    recognized_patterns.append({
                        'pattern': pattern_name,
                        'confidence': result.get('confidence', 0.5),
                        'details': result
                    })
            except Exception as e:
                logger.error(f"Pattern recognition error for {pattern_name}: {e}")
        
        return recognized_patterns
    
    def detect_burst_pattern(self, spectrum_data):
        """Detect burst transmission patterns"""
        power = spectrum_data['power']
        max_power = np.max(power)
        mean_power = np.mean(power)
        
        if max_power - mean_power > 20:  # 20 dB above average
            return {
                'confidence': 0.8,
                'peak_power': max_power,
                'average_power': mean_power,
                'dynamic_range': max_power - mean_power
            }
        return None
    
    def detect_continuous_pattern(self, spectrum_data):
        """Detect continuous transmission patterns"""
        power = spectrum_data['power']
        std_power = np.std(power)
        
        if std_power < 5:  # Low variation indicates continuous signal
            return {
                'confidence': 0.7,
                'stability': 5 - std_power,
                'power_variation': std_power
            }
        return None
    
    def detect_periodic_pattern(self, spectrum_data):
        """Detect periodic patterns"""
        # This would analyze temporal patterns across multiple spectrum captures
        # For now, return a placeholder
        return None
    
    def detect_fh_pattern(self, spectrum_data):
        """Detect frequency hopping patterns"""
        # This would analyze frequency changes over time
        # For now, return a placeholder
        return None

class AdvancedSecurityEngine:
    """Advanced security analysis and threat detection"""
    
    def __init__(self):
        self.threat_database = ThreatDatabase()
        self.rogue_detector = RogueDeviceDetector()
        self.jamming_detector = JammingDetector()
        
    def analyze_security(self, spectrum_data, ai_analysis):
        """Perform comprehensive security analysis"""
        security_report = {
            'timestamp': spectrum_data['timestamp'],
            'threat_level': 'low',
            'threats': [],
            'recommendations': []
        }
        
        # Check for known threats
        threats = self.threat_database.check_threats(spectrum_data)
        security_report['threats'].extend(threats)
        
        # Rogue device detection
        rogue_devices = self.rogue_detector.detect(spectrum_data, ai_analysis)
        security_report['threats'].extend(rogue_devices)
        
        # Jamming detection
        jamming_threats = self.jamming_detector.detect(spectrum_data)
        security_report['threats'].extend(jamming_threats)
        
        # Determine overall threat level
        if any(t['severity'] == 'critical' for t in security_report['threats']):
            security_report['threat_level'] = 'critical'
        elif any(t['severity'] == 'high' for t in security_report['threats']):
            security_report['threat_level'] = 'high'
        elif any(t['severity'] == 'medium' for t in security_report['threats']):
            security_report['threat_level'] = 'medium'
        
        # Generate recommendations
        security_report['recommendations'] = self.generate_recommendations(security_report['threats'])
        
        return security_report
    
    def generate_recommendations(self, threats):
        """Generate security recommendations"""
        recommendations = []
        
        for threat in threats:
            threat_type = threat.get('type', '')
            
            if threat_type == 'rogue_ap':
                recommendations.append("Investigate unauthorized access point - verify legitimacy")
            elif threat_type == 'jamming':
                recommendations.append("Potential jamming detected - check for interference source")
            elif threat_type == 'high_power':
                recommendations.append("High power transmission detected - verify authorization")
            elif threat_type == 'restricted_frequency':
                recommendations.append("Transmission in restricted frequency - report to authorities")
        
        return list(set(recommendations))  # Remove duplicates

class ThreatDatabase:
    """Database of known threat signatures"""
    
    def __init__(self):
        self.threat_signatures = {
            'wifi_deauth': {
                'frequency': 2.4e9,
                'pattern': 'deauth_frame',
                'severity': 'medium'
            },
            'bluetooth_attack': {
                'frequency': 2.4e9,
                'pattern': 'bt_exploit',
                'severity': 'medium'
            },
            'cellular_imsi': {
                'frequency': [850e6, 1900e6],
                'pattern': 'imsi_catcher',
                'severity': 'critical'
            }
        }
    
    def check_threats(self, spectrum_data):
        """Check spectrum data against threat database"""
        threats = []
        
        # This would implement sophisticated threat signature matching
        # For now, return empty list
        
        return threats

class RogueDeviceDetector:
    """Detect rogue/unauthorized devices"""
    
    def __init__(self):
        self.known_devices = set()
        self.whitelist = set()
        
    def detect(self, spectrum_data, ai_analysis):
        """Detect rogue devices"""
        rogue_devices = []
        
        # Analyze AI classification results
        if ai_analysis and 'classification' in ai_analysis:
            for classification in ai_analysis['classification']:
                if classification['confidence'] > 0.8:
                    device_signature = self.generate_device_signature(spectrum_data, classification)
                    
                    if device_signature not in self.known_devices and device_signature not in self.whitelist:
                        rogue_devices.append({
                            'type': 'unknown_device',
                            'severity': 'medium',
                            'device_type': classification['type'],
                            'confidence': classification['confidence'],
                            'signature': device_signature[:16],  # Truncated for display
                            'description': f"Unknown {classification['type']} device detected"
                        })
                        
                        # Add to known devices
                        self.known_devices.add(device_signature)
        
        return rogue_devices
    
    def generate_device_signature(self, spectrum_data, classification):
        """Generate unique device signature"""
        signature_data = {
            'frequency': spectrum_data['center_freq'],
            'type': classification['type'],
            'power_profile': np.mean(spectrum_data['power'])
        }
        
        signature_str = json.dumps(signature_data, sort_keys=True)
        return hashlib.md5(signature_str.encode()).hexdigest()

class JammingDetector:
    """Detect jamming attempts"""
    
    def __init__(self):
        self.baseline_noise = -100  # dBm
        self.jamming_threshold = 20  # dB above baseline
        
    def detect(self, spectrum_data):
        """Detect jamming signals"""
        jamming_threats = []
        
        power = spectrum_data['power']
        max_power = np.max(power)
        power_bandwidth = np.sum(power > self.baseline_noise + 10)
        
        # Wideband jamming detection
        if power_bandwidth > len(power) * 0.8:  # 80% of spectrum active
            jamming_threats.append({
                'type': 'wideband_jamming',
                'severity': 'high',
                'bandwidth_affected': power_bandwidth,
                'max_power': max_power,
                'description': 'Potential wideband jamming detected'
            })
        
        # High power jamming
        if max_power > self.baseline_noise + self.jamming_threshold:
            jamming_threats.append({
                'type': 'high_power_jamming',
                'severity': 'medium',
                'power': max_power,
                'threshold': self.baseline_noise + self.jamming_threshold,
                'description': f'High power signal may indicate jamming: {max_power:.1f} dBm'
            })
        
        return jamming_threats

class ProtocolAnalyzer:
    """Advanced protocol analysis"""
    
    def __init__(self):
        self.protocol_decoders = {
            'wifi': WiFiDecoder(),
            'bluetooth': BluetoothDecoder(),
            'zigbee': ZigBeeDecoder(),
            'cellular': CellularDecoder()
        }
    
    def analyze_protocols(self, spectrum_data, ai_analysis):
        """Analyze detected protocols"""
        protocol_analysis = {}
        
        if ai_analysis and 'classification' in ai_analysis:
            for classification in ai_analysis['classification']:
                protocol_type = classification['type']
                
                if protocol_type in self.protocol_decoders:
                    decoder = self.protocol_decoders[protocol_type]
                    analysis = decoder.decode(spectrum_data, classification)
                    
                    if analysis:
                        protocol_analysis[protocol_type] = analysis
        
        return protocol_analysis

class WiFiDecoder:
    """WiFi protocol decoder"""
    
    def decode(self, spectrum_data, classification):
        """Decode WiFi signals"""
        return {
            'channel': self.estimate_wifi_channel(spectrum_data['center_freq']),
            'estimated_bandwidth': '20 MHz',  # Default assumption
            'signal_strength': np.max(spectrum_data['power']),
            'analysis': 'WiFi signal detected - monitor for security issues'
        }
    
    def estimate_wifi_channel(self, frequency):
        """Estimate WiFi channel from frequency"""
        if 2400e6 <= frequency <= 2485e6:
            # 2.4 GHz WiFi
            channel = int((frequency - 2412e6) / 5e6) + 1
            return f"2.4GHz Channel {channel}"
        elif 5150e6 <= frequency <= 5850e6:
            # 5 GHz WiFi
            channel = int((frequency - 5000e6) / 5e6)
            return f"5GHz Channel {channel}"
        return "Unknown"

class BluetoothDecoder:
    """Bluetooth protocol decoder"""
    
    def decode(self, spectrum_data, classification):
        """Decode Bluetooth signals"""
        return {
            'frequency_band': '2.4 GHz ISM',
            'estimated_type': 'Bluetooth Classic/LE',
            'signal_strength': np.max(spectrum_data['power']),
            'analysis': 'Bluetooth signal detected - check for unauthorized devices'
        }

class ZigBeeDecoder:
    """ZigBee protocol decoder"""
    
    def decode(self, spectrum_data, classification):
        """Decode ZigBee signals"""
        return {
            'channel': self.estimate_zigbee_channel(spectrum_data['center_freq']),
            'estimated_bandwidth': '2 MHz',
            'signal_strength': np.max(spectrum_data['power']),
            'analysis': 'ZigBee/IoT signal detected - verify device authorization'
        }
    
    def estimate_zigbee_channel(self, frequency):
        """Estimate ZigBee channel"""
        if 2400e6 <= frequency <= 2485e6:
            channel = int((frequency - 2405e6) / 5e6) + 11
            return f"802.15.4 Channel {channel}"
        return "Unknown"

class CellularDecoder:
    """Cellular protocol decoder"""
    
    def decode(self, spectrum_data, classification):
        """Decode cellular signals"""
        return {
            'band': self.estimate_cellular_band(spectrum_data['center_freq']),
            'technology': 'LTE/5G',
            'signal_strength': np.max(spectrum_data['power']),
            'analysis': 'Cellular signal detected - monitor for IMSI catchers'
        }
    
    def estimate_cellular_band(self, frequency):
        """Estimate cellular band"""
        if 850e6 <= frequency <= 900e6:
            return "Cellular Band 5/8"
        elif 1800e6 <= frequency <= 1900e6:
            return "Cellular Band 3/2"
        return "Unknown cellular band"

class HackRFDatabase:
    """Database for storing analysis results and configurations"""
    
    def __init__(self, db_path='hackrf_platform.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database schema"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        duration INTEGER,
                        frequency_range TEXT,
                        notes TEXT
                    )
                ''')
                
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS spectrum_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id INTEGER,
                        timestamp TEXT,
                        center_freq REAL,
                        sample_rate REAL,
                        max_power REAL,
                        data_blob BLOB,
                        FOREIGN KEY (session_id) REFERENCES sessions (id)
                    )
                ''')
                
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS threats (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id INTEGER,
                        timestamp TEXT,
                        threat_type TEXT,
                        severity TEXT,
                        frequency REAL,
                        description TEXT,
                        FOREIGN KEY (session_id) REFERENCES sessions (id)
                    )
                ''')
                
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS device_signatures (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        signature TEXT UNIQUE,
                        device_type TEXT,
                        first_seen TEXT,
                        last_seen TEXT,
                        is_whitelisted BOOLEAN DEFAULT FALSE
                    )
                ''')
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
    
    def create_session(self, frequency_range, notes=""):
        """Create new analysis session"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    INSERT INTO sessions (timestamp, frequency_range, notes)
                    VALUES (?, ?, ?)
                ''', (datetime.now().isoformat(), frequency_range, notes))
                
                session_id = cursor.lastrowid
                conn.commit()
                return session_id
                
        except Exception as e:
            logger.error(f"Session creation error: {e}")
            return None
    
    def save_spectrum_data(self, session_id, spectrum_data):
        """Save spectrum analysis data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Serialize spectrum data
                data_blob = json.dumps({
                    'frequencies': spectrum_data['frequencies'].tolist(),
                    'power': spectrum_data['power'].tolist(),
                    'peaks': spectrum_data.get('peaks', [])
                }).encode()
                
                conn.execute('''
                    INSERT INTO spectrum_data 
                    (session_id, timestamp, center_freq, sample_rate, max_power, data_blob)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    session_id,
                    datetime.now().isoformat(),
                    spectrum_data['center_freq'],
                    spectrum_data['sample_rate'],
                    np.max(spectrum_data['power']),
                    data_blob
                ))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Spectrum data save error: {e}")
    
    def save_threat(self, session_id, threat):
        """Save detected threat"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    INSERT INTO threats 
                    (session_id, timestamp, threat_type, severity, frequency, description)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    session_id,
                    datetime.now().isoformat(),
                    threat.get('type', 'unknown'),
                    threat.get('severity', 'low'),
                    threat.get('frequency', 0),
                    threat.get('description', '')
                ))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Threat save error: {e}")

class SessionManager:
    """Manage analysis sessions"""
    
    def __init__(self):
        self.current_session = None
        self.session_start_time = None
        
    def start_session(self, database, frequency_range, notes=""):
        """Start new analysis session"""
        self.current_session = database.create_session(frequency_range, notes)
        self.session_start_time = time.time()
        logger.info(f"Started session {self.current_session}")
        return self.current_session
    
    def end_session(self, database):
        """End current session"""
        if self.current_session and self.session_start_time:
            duration = int(time.time() - self.session_start_time)
            
            try:
                with sqlite3.connect(database.db_path) as conn:
                    conn.execute('''
                        UPDATE sessions SET duration = ? WHERE id = ?
                    ''', (duration, self.current_session))
                    conn.commit()
                    
            except Exception as e:
                logger.error(f"Session end error: {e}")
            
            logger.info(f"Ended session {self.current_session}, duration: {duration}s")
            self.current_session = None
            self.session_start_time = None

def main():
    """Main function"""
    print("=" * 70)
    print("HackRF Enhanced Platform v2.0.0")
    print("Advanced SDR Management System")
    print("For authorized security testing and research only")
    print("=" * 70)
    
    try:
        platform = HackRFEnhancedPlatform()
        
        # Initialize components
        devices = platform.device_manager.detect_devices()
        
        if devices:
            print(f"Detected {len(devices)} HackRF device(s)")
            for device_id, info in devices.items():
                print(f"  Device: {device_id}")
                print(f"    Firmware: {info.get('firmware_version', 'Unknown')}")
        else:
            print("No HackRF devices detected")
            print("Platform running in simulation mode")
        
        # Start GUI if available
        try:
            from hackrf_enhanced_gui import HackRFEnhancedGUI
            root = tk.Tk()
            app = HackRFEnhancedGUI(root, platform)
            root.mainloop()
        except ImportError:
            print("GUI not available, running in CLI mode")
            
    except KeyboardInterrupt:
        print("\nShutdown requested by user")
    except Exception as e:
        logger.error(f"Platform error: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()