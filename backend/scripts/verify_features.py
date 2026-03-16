#!/usr/bin/env python
"""
Episteme Feature Verification Script
Run this to verify all features are working correctly
"""

import asyncio
import aiohttp
import json
from datetime import datetime
from pathlib import Path
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class EpistemeVerifier:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.results = {
            'timestamp': datetime.utcnow().isoformat(),
            'tests': [],
            'passed': 0,
            'failed': 0,
            'warnings': 0
        }
        
    async def verify_endpoint(self, session, name, method, endpoint, expected_status=200, **kwargs):
        """Verify a single endpoint"""
        test_result = {
            'name': name,
            'endpoint': endpoint,
            'status': 'pending',
            'errors': [],
            'warnings': []
        }
        
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method.upper() == 'GET':
                async with session.get(url, **kwargs) as response:
                    await self._process_response(response, test_result, expected_status)
            elif method.upper() == 'POST':
                async with session.post(url, **kwargs) as response:
                    await self._process_response(response, test_result, expected_status)
                    
        except Exception as e:
            test_result['status'] = 'failed'
            test_result['errors'].append(str(e))
            
        self.results['tests'].append(test_result)
        if test_result['status'] == 'passed':
            self.results['passed'] += 1
        elif test_result['status'] == 'failed':
            self.results['failed'] += 1
        else:
            self.results['warnings'] += 1
            
    async def _process_response(self, response, test_result, expected_status):
        """Process response and validate"""
        test_result['status_code'] = response.status
        
        if response.status == expected_status:
            try:
                data = await response.json()
                test_result['data_sample'] = str(data)[:200] + '...' if len(str(data)) > 200 else str(data)
                test_result['status'] = 'passed'
            except:
                text = await response.text()
                test_result['data_sample'] = text[:200]
                test_result['status'] = 'passed'
        else:
            test_result['status'] = 'failed'
            test_result['errors'].append(f"Expected {expected_status}, got {response.status}")
            
    async def run_all_verifications(self):
        """Run all verification tests"""
        
        print("\n" + "="*60)
        print("EPISTEME FEATURE VERIFICATION")
        print("="*60)
        
        async with aiohttp.ClientSession() as session:
            # 1. Health Check
            await self.verify_endpoint(
                session, 
                "Health Check", 
                "GET", 
                "/health"
            )
            
            # 2. Datasets List
            await self.verify_endpoint(
                session,
                "Get Datasets List",
                "GET",
                "/datasets"
            )
            
            # 3. Get Housing Dataset Info
            await self.verify_endpoint(
                session,
                "Get Housing Dataset",
                "GET",
                "/dataset/housing"
            )
            
            # 4. Get Education Dataset Info
            await self.verify_endpoint(
                session,
                "Get Education Dataset",
                "GET",
                "/dataset/education"
            )
            
            # 5. Get Salary Dataset Info
            await self.verify_endpoint(
                session,
                "Get Salary Dataset",
                "GET",
                "/dataset/salary"
            )
            
            # 6. Get Metrics
            await self.verify_endpoint(
                session,
                "Get Metrics",
                "GET",
                "/metrics"
            )
            
            # 7. Get Comparison
            await self.verify_endpoint(
                session,
                "Get Comparison",
                "GET",
                "/compare"
            )
            
            # 8. Get Socratic Prompts
            await self.verify_endpoint(
                session,
                "Get Socratic Prompts",
                "GET",
                "/socratic-prompts"
            )
            
            # 9. Test Prediction
            await self.verify_endpoint(
                session,
                "Test Prediction",
                "POST",
                "/predict",
                json={
                    "features": {
                        "CRIM": 0.1,
                        "RM": 6.5,
                        "AGE": 50,
                        "LSTAT": 10,
                        "NOX": 0.5,
                        "DIS": 5,
                        "TAX": 300
                    },
                    "model": "Random Forest"
                }
            )
            
            # 10. Switch Dataset
            await self.verify_endpoint(
                session,
                "Switch Dataset",
                "POST",
                "/switch-dataset/salary"
            )
            
        # Save results
        self.save_results()
        self.print_summary()
        
    def save_results(self):
        """Save verification results to file"""
        results_dir = Path(__file__).parent.parent / 'logs' / 'verification'
        results_dir.mkdir(parents=True, exist_ok=True)
        
        filename = results_dir / f"verification_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
            
        print(f"\n✅ Results saved to: {filename}")
        
    def print_summary(self):
        """Print verification summary"""
        print("\n" + "="*60)
        print("VERIFICATION SUMMARY")
        print("="*60)
        print(f"Total Tests: {len(self.results['tests'])}")
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        print(f"⚠️  Warnings: {self.results['warnings']}")
        print("="*60)
        
        if self.results['failed'] > 0:
            print("\n❌ Failed Tests:")
            for test in self.results['tests']:
                if test['status'] == 'failed':
                    print(f"  - {test['name']}: {test['errors']}")
                    
        if self.results['warnings'] > 0:
            print("\n⚠️  Warnings:")
            for test in self.results['tests']:
                if test['status'] == 'warning':
                    print(f"  - {test['name']}: {test['warnings']}")

async def main():
    verifier = EpistemeVerifier()
    await verifier.run_all_verifications()

if __name__ == "__main__":
    asyncio.run(main())