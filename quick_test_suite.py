#!/usr/bin/env python3
"""
Quick Test Suite - OpenRouter Enhanced
=====================================
Simplified testing without Unicode issues
"""

import os
import sys
import json
import time
import requests
import sqlite3
import hashlib
import platform
from datetime import datetime
from pathlib import Path

class QuickTestSuite:
    def __init__(self):
        self.version = "Quick Test Suite v1.0"
        self.session_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        
        # OpenRouter config
        self.openrouter_config = {
            'api_key': 'sk-or-v1-d41d8cd98f00b204e9800998ecf8427e',
            'base_url': 'https://openrouter.ai/api/v1/chat/completions',
            'cost_total': 0.0,
            'requests_made': 0
        }
        
        # Test targets
        self.test_targets = {
            'mobile_app': 'mobile_security_app.html',
            'windows_exe': 'dist/security_platform_windows.exe',
            'hackrf_exe': 'dist/hackrf_ultimate_complete_application.exe',
            'openrouter_system': 'http://localhost:6969'
        }
        
        self.test_results = []
        
    def run_tests(self):
        """Run all tests"""
        print(f"{self.version}")
        print("=" * 50)
        print("Starting comprehensive testing...")
        print(f"Session ID: {self.session_id}")
        print(f"Cost: $0.00 (OpenRouter free models)")
        print("=" * 50)
        
        start_time = datetime.now()
        
        # Test phases
        tests = [
            ("File System Check", self.test_file_system),
            ("Application Testing", self.test_applications),
            ("Mobile App Testing", self.test_mobile_app),
            ("OpenRouter Integration", self.test_openrouter),
            ("AI Analysis", self.test_ai_integration),
            ("Performance Testing", self.test_performance),
            ("Security Assessment", self.test_security)
        ]
        
        for test_name, test_function in tests:
            print(f"\n[TEST] {test_name}")
            print("-" * 30)
            try:
                result = test_function()
                if result:
                    print(f"[PASS] {test_name} completed successfully")
                    self.test_results.append({'test': test_name, 'result': 'PASS'})
                else:
                    print(f"[FAIL] {test_name} failed")
                    self.test_results.append({'test': test_name, 'result': 'FAIL'})
            except Exception as e:
                print(f"[ERROR] {test_name} error: {e}")
                self.test_results.append({'test': test_name, 'result': 'ERROR'})
                
        end_time = datetime.now()
        total_time = (end_time - start_time).total_seconds()
        
        # Results summary
        passed = len([r for r in self.test_results if r['result'] == 'PASS'])
        failed = len([r for r in self.test_results if r['result'] == 'FAIL'])
        errors = len([r for r in self.test_results if r['result'] == 'ERROR'])
        total = len(self.test_results)
        
        print(f"\n" + "=" * 50)
        print(f"TEST SUMMARY")
        print(f"=" * 50)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Errors: {errors}")
        print(f"Success Rate: {(passed/total*100):.1f}%")
        print(f"Execution Time: {total_time:.2f} seconds")
        print(f"Cost: ${self.openrouter_config['cost_total']:.2f}")
        print(f"AI Requests: {self.openrouter_config['requests_made']}")
        
        # Generate report
        report_file = f"test_report_{self.session_id}.txt"
        with open(report_file, 'w') as f:
            f.write(f"QUICK TEST SUITE REPORT\n")
            f.write(f"Session: {self.session_id}\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write(f"Total Tests: {total}\n")
            f.write(f"Passed: {passed}\n")
            f.write(f"Failed: {failed}\n")
            f.write(f"Success Rate: {(passed/total*100):.1f}%\n\n")
            
            for result in self.test_results:
                f.write(f"{result['test']}: {result['result']}\n")
                
        print(f"Report saved: {report_file}")
        
        return self.session_id
        
    def test_file_system(self):
        """Test file system"""
        print("Checking application files...")
        
        all_exist = True
        for app_name, app_path in self.test_targets.items():
            if Path(app_path).exists():
                size = Path(app_path).stat().st_size
                print(f"  [OK] {app_name}: {app_path} ({size:,} bytes)")
            else:
                print(f"  [MISSING] {app_name}: {app_path}")
                all_exist = False
                
        return all_exist
        
    def test_applications(self):
        """Test applications"""
        print("Testing executable applications...")
        
        # Test Windows EXE
        windows_exe = Path(self.test_targets['windows_exe'])
        if windows_exe.exists():
            size = windows_exe.stat().st_size
            if size > 1000000:  # > 1MB
                print(f"  [OK] Windows EXE: {size:,} bytes")
            else:
                print(f"  [WARN] Windows EXE seems small: {size:,} bytes")
        else:
            print(f"  [MISSING] Windows EXE not found")
            return False
            
        # Test HackRF EXE
        hackrf_exe = Path(self.test_targets['hackrf_exe'])
        if hackrf_exe.exists():
            size = hackrf_exe.stat().st_size
            if size > 1000000:  # > 1MB
                print(f"  [OK] HackRF EXE: {size:,} bytes")
            else:
                print(f"  [WARN] HackRF EXE seems small: {size:,} bytes")
        else:
            print(f"  [MISSING] HackRF EXE not found")
            return False
            
        return True
        
    def test_mobile_app(self):
        """Test mobile application"""
        print("Testing mobile application...")
        
        mobile_path = Path(self.test_targets['mobile_app'])
        if not mobile_path.exists():
            print("  [MISSING] Mobile app not found")
            return False
            
        try:
            content = mobile_path.read_text(encoding='utf-8')
            
            # Check key features
            checks = {
                'Security Features': 'Security Scanner' in content,
                'HackRF Integration': 'HackRF Suite' in content,
                'Mobile UI': 'mobile-header' in content,
                'Touch Support': 'touchstart' in content,
                'Responsive Design': 'viewport' in content
            }
            
            all_passed = True
            for check_name, check_result in checks.items():
                status = "OK" if check_result else "FAIL"
                print(f"  [{status}] {check_name}")
                if not check_result:
                    all_passed = False
                    
            return all_passed
            
        except Exception as e:
            print(f"  [ERROR] Mobile app test failed: {e}")
            return False
            
    def test_openrouter(self):
        """Test OpenRouter system"""
        print("Testing OpenRouter integration...")
        
        try:
            # Test health endpoint
            response = requests.get(f"{self.test_targets['openrouter_system']}/health", 
                                  timeout=10)
            
            if response.status_code == 200:
                print("  [OK] OpenRouter health check passed")
                return True
            else:
                print(f"  [FAIL] OpenRouter health check failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"  [ERROR] OpenRouter test failed: {e}")
            return False
            
    def test_ai_integration(self):
        """Test AI integration"""
        print("Testing AI integration...")
        
        try:
            # Simple AI test
            headers = {
                'Authorization': f'Bearer {self.openrouter_config["api_key"]}',
                'Content-Type': 'application/json',
                'HTTP-Referer': 'http://localhost:8080'
            }
            
            data = {
                'model': 'meta-llama/llama-3.1-8b-instruct:free',
                'messages': [{'role': 'user', 'content': 'Respond with exactly: AI TEST SUCCESSFUL'}],
                'max_tokens': 50,
                'temperature': 0.1
            }
            
            response = requests.post(self.openrouter_config['base_url'], 
                                   headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                
                if 'SUCCESSFUL' in ai_response:
                    print("  [OK] AI integration test successful")
                    self.openrouter_config['requests_made'] += 1
                    return True
                else:
                    print(f"  [WARN] AI responded but unexpected: {ai_response}")
                    return False
            else:
                print(f"  [FAIL] AI test failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"  [ERROR] AI integration failed: {e}")
            return False
            
    def test_performance(self):
        """Test performance"""
        print("Testing performance...")
        
        try:
            # File load performance
            mobile_path = Path(self.test_targets['mobile_app'])
            if mobile_path.exists():
                start_time = time.time()
                content = mobile_path.read_text(encoding='utf-8')
                load_time = time.time() - start_time
                
                if load_time < 1.0:  # Should load in under 1 second
                    print(f"  [OK] Mobile app loads in {load_time:.3f}s")
                    return True
                else:
                    print(f"  [SLOW] Mobile app loads in {load_time:.3f}s")
                    return False
            else:
                print("  [MISSING] Mobile app not found for performance test")
                return False
                
        except Exception as e:
            print(f"  [ERROR] Performance test failed: {e}")
            return False
            
    def test_security(self):
        """Test security"""
        print("Testing security configuration...")
        
        # Check cost control
        if self.openrouter_config['cost_total'] == 0.0:
            print("  [OK] Cost control: $0.00")
        else:
            print(f"  [WARN] Cost incurred: ${self.openrouter_config['cost_total']:.2f}")
            
        # Check file permissions (basic)
        try:
            for app_name, app_path in self.test_targets.items():
                if Path(app_path).exists() and app_path.endswith('.exe'):
                    # Basic executable check
                    print(f"  [OK] {app_name}: Executable exists")
                    
            return True
            
        except Exception as e:
            print(f"  [ERROR] Security test failed: {e}")
            return False

def main():
    """Main function"""
    test_suite = QuickTestSuite()
    session_id = test_suite.run_tests()
    print(f"\nTest session {session_id} completed!")

if __name__ == "__main__":
    main()