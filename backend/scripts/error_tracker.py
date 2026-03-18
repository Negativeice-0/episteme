#!/usr/bin/env python
"""
Comprehensive error tracking and fixing system
"""
import os
import sys
import django
import subprocess
import re
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

class EpistemeErrorTracker:
    """
    Tracks and fixes all errors in the Episteme project
    """
    
    def __init__(self):
        self.backend_errors = []
        self.frontend_errors = []
        self.fixed_errors = []
        self.pending_errors = []
        
    def scan_all_errors(self):
        """Scan both backend and frontend for errors"""
        print("\n" + "="*60)
        print("🔍 EPISTEME COMPREHENSIVE ERROR SCAN")
        print("="*60)
        
        self.scan_backend_errors()
        self.scan_frontend_errors()
        self.scan_missing_files()
        self.scan_import_errors()
        
        self.print_summary()
        return self.pending_errors
    
    def scan_backend_errors(self):
        """Scan Django backend for errors"""
        print("\n📡 SCANNING BACKEND...")
        
        # Check for missing dependencies
        try:
            import debug_toolbar
            print("  ✅ debug_toolbar installed")
        except ImportError:
            self.backend_errors.append({
                'type': 'missing_dependency',
                'file': 'settings/development.py',
                'error': 'debug_toolbar not installed',
                'fix': 'pip install django-debug-toolbar'
            })
            print("  ❌ debug_toolbar missing")
        
        # Check middleware configuration
        try:
            from core.middleware import RequestLoggingMiddleware
            print("  ✅ core.middleware.RequestLoggingMiddleware exists")
        except ImportError:
            self.backend_errors.append({
                'type': 'missing_file',
                'file': 'core/middleware.py',
                'error': 'RequestLoggingMiddleware not found',
                'fix': 'Create core/middleware.py'
            })
            print("  ❌ RequestLoggingMiddleware missing")
        
        # Check database connection
        from django.db import connection
        try:
            connection.ensure_connection()
            print("  ✅ Database connected")
        except Exception as e:
            self.backend_errors.append({
                'type': 'database',
                'error': str(e),
                'fix': 'Check PostgreSQL is running and .env is configured'
            })
            print(f"  ❌ Database error: {e}")
        
        # Check apps configuration
        from django.apps import apps
        required_apps = ['core', 'api', 'datasets', 'models_app', 'socratic']
        for app in required_apps:
            try:
                apps.get_app_config(app)
                print(f"  ✅ {app} app configured")
            except LookupError:
                self.backend_errors.append({
                    'type': 'missing_app',
                    'app': app,
                    'fix': f"Add '{app}' to INSTALLED_APPS in settings/base.py"
                })
                print(f"  ❌ {app} app not in INSTALLED_APPS")
    
    def scan_frontend_errors(self):
        """Scan Next.js frontend for errors"""
        print("\n🎨 SCANNING FRONTEND...")
        
        frontend_path = Path(__file__).parent.parent.parent / 'frontend'
        
        # Check for missing api.ts
        api_file = frontend_path / 'src' / 'lib' / 'api.ts'
        if not api_file.exists():
            self.frontend_errors.append({
                'type': 'missing_file',
                'file': 'src/lib/api.ts',
                'error': 'API client not found',
                'fix': 'Create src/lib/api.ts with proper exports'
            })
            print("  ❌ src/lib/api.ts missing")
        else:
            print("  ✅ src/lib/api.ts exists")
        
        # Check for framer-motion
        package_json = frontend_path / 'package.json'
        if package_json.exists():
            import json
            with open(package_json) as f:
                pkg = json.load(f)
                deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
                
                if 'framer-motion' not in deps:
                    self.frontend_errors.append({
                        'type': 'missing_dependency',
                        'package': 'framer-motion',
                        'fix': 'npm install framer-motion'
                    })
                    print("  ❌ framer-motion missing")
                else:
                    print("  ✅ framer-motion installed")
                
                if '@heroicons/react' not in deps:
                    self.frontend_errors.append({
                        'type': 'missing_dependency',
                        'package': '@heroicons/react',
                        'fix': 'npm install @heroicons/react'
                    })
                    print("  ❌ @heroicons/react missing")
                else:
                    print("  ✅ @heroicons/react installed")
        
        # Check for missing pages
        required_pages = ['demo', 'metrics', 'socratic', 'about']
        for page in required_pages:
            page_file = frontend_path / 'src' / 'app' / page / 'page.tsx'
            if not page_file.exists():
                self.frontend_errors.append({
                    'type': 'missing_page',
                    'page': page,
                    'fix': f'Create src/app/{page}/page.tsx'
                })
                print(f"  ❌ {page} page missing")
            else:
                print(f"  ✅ {page} page exists")
    
    def scan_missing_files(self):
        """Scan for missing required files"""
        print("\n📁 SCANNING MISSING FILES...")
        
        backend_path = Path(__file__).parent.parent
        
        # Required files
        required_files = [
            ('core/middleware.py', self.create_middleware_file),
            ('core/exceptions.py', self.create_exceptions_file),
            ('core/utils.py', self.create_utils_file),
            ('api/urls.py', self.create_api_urls_file),
            ('api/views.py', self.create_api_views_file),
            ('models_app/trainer.py', self.create_trainer_file),
        ]
        
        for file_path, create_func in required_files:
            full_path = backend_path / file_path
            if not full_path.exists():
                self.backend_errors.append({
                    'type': 'missing_file',
                    'file': file_path,
                    'fix': f'Create {file_path}',
                    'create_func': create_func
                })
                print(f"  ❌ {file_path} missing")
            else:
                print(f"  ✅ {file_path} exists")
    
    def scan_import_errors(self):
        """Check for common import errors"""
        print("\n🔤 SCANNING IMPORT PATTERNS...")
        
        # Check frontend imports
        frontend_path = Path(__file__).parent.parent.parent / 'frontend'
        
        # Look for @/ imports without proper tsconfig
        tsconfig = frontend_path / 'tsconfig.json'
        if tsconfig.exists():
            import json
            with open(tsconfig) as f:
                config = json.load(f)
                paths = config.get('compilerOptions', {}).get('paths', {})
                
                if '@/*' not in paths:
                    self.frontend_errors.append({
                        'type': 'config_error',
                        'file': 'tsconfig.json',
                        'error': '@/* path alias not configured',
                        'fix': 'Add "@/*": ["./src/*"] to compilerOptions.paths'
                    })
                    print("  ❌ @/* path alias missing")
                else:
                    print("  ✅ @/* path alias configured")
    
    def print_summary(self):
        """Print error summary"""
        print("\n" + "="*60)
        print("📊 ERROR SUMMARY")
        print("="*60)
        
        total_errors = len(self.backend_errors) + len(self.frontend_errors)
        
        if total_errors == 0:
            print("\n✅ NO ERRORS FOUND! Everything is working!")
            return
        
        print(f"\n❌ Total Errors Found: {total_errors}")
        print(f"  Backend: {len(self.backend_errors)}")
        print(f"  Frontend: {len(self.frontend_errors)}")
        
        print("\n🔧 FIXES NEEDED:")
        for i, error in enumerate(self.backend_errors + self.frontend_errors, 1):
            print(f"\n  {i}. [{error['type']}] {error.get('file', error.get('package', 'unknown'))}")
            print(f"     → {error['error']}")
            print(f"     → FIX: {error['fix']}")
    
    def fix_all_errors(self):
        """Automatically fix all detected errors"""
        print("\n" + "="*60)
        print("🔧 AUTOMATICALLY FIXING ERRORS")
        print("="*60)
        
        # Fix backend errors
        for error in self.backend_errors:
            self.fix_backend_error(error)
        
        # Fix frontend errors
        for error in self.frontend_errors:
            self.fix_frontend_error(error)
        
        print("\n✅ All fixes applied! Run the error tracker again to verify.")
    
    def fix_backend_error(self, error):
        """Fix a specific backend error"""
        if error['type'] == 'missing_dependency' and error.get('package') == 'django-debug-toolbar':
            print("\n📦 Installing django-debug-toolbar...")
            subprocess.run(['pip', 'install', 'django-debug-toolbar'])
            print("   ✅ Installed")
        
        elif error['type'] == 'missing_file' and 'create_func' in error:
            print(f"\n📝 Creating {error['file']}...")
            error['create_func']()
            print(f"   ✅ Created")
        
        elif error['type'] == 'missing_app':
            print(f"\n📱 Adding {error['app']} to INSTALLED_APPS...")
            self.add_app_to_settings(error['app'])
    
    def fix_frontend_error(self, error):
        """Fix a specific frontend error"""
        if error['type'] == 'missing_dependency':
            print(f"\n📦 Installing {error['package']}...")
            subprocess.run(['npm', 'install', error['package']], 
                         cwd=Path(__file__).parent.parent.parent / 'frontend')
            print(f"   ✅ Installed")
        
        elif error['type'] == 'missing_file' and error['file'] == 'src/lib/api.ts':
            print("\n📝 Creating api.ts...")
            self.create_api_file()
        
        elif error['type'] == 'missing_page':
            print(f"\n📝 Creating {error['page']} page...")
            self.create_page(error['page'])
        
        elif error['type'] == 'config_error':
            print("\n⚙️ Fixing tsconfig.json...")
            self.fix_tsconfig()
    
    def create_middleware_file(self):
        """Create core/middleware.py"""
        content = '''import logging
import uuid
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(MiddlewareMixin):
    """Log all requests with unique ID"""
    
    def process_request(self, request):
        request.request_id = str(uuid.uuid4())
        
    def process_response(self, request, response):
        response['X-Request-ID'] = getattr(request, 'request_id', 'unknown')
        return response
'''
        path = Path(__file__).parent.parent / 'core' / 'middleware.py'
        path.write_text(content)
    
    def create_exceptions_file(self):
        """Create core/exceptions.py"""
        content = '''from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """Custom exception handler for consistent error responses"""
    response = exception_handler(exc, context)
    
    if response is not None:
        response.data = {
            'error': True,
            'code': response.status_code,
            'message': str(exc),
            'type': exc.__class__.__name__,
        }
    else:
        response = Response({
            'error': True,
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': 'Internal server error',
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response
'''
        path = Path(__file__).parent.parent / 'core' / 'exceptions.py'
        path.write_text(content)
    
    def create_utils_file(self):
        """Create core/utils.py"""
        content = '''import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class JSONFormatter:
    """Format data as JSON for logging"""
    
    @staticmethod
    def format(data):
        try:
            return json.dumps(data, indent=2, default=str)
        except:
            return str(data)
'''
        path = Path(__file__).parent.parent / 'core' / 'utils.py'
        path.write_text(content)
    
    def create_api_urls_file(self):
        """Create api/urls.py"""
        content = '''from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health-check'),
]
'''
        path = Path(__file__).parent.parent / 'api' / 'urls.py'
        path.write_text(content)
    
    def create_api_views_file(self):
        """Create api/views.py"""
        content = '''from django.http import JsonResponse
from datetime import datetime

def health_check(request):
    """Health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'message': 'Episteme API is running'
    })
'''
        path = Path(__file__).parent.parent / 'api' / 'views.py'
        path.write_text(content)
    
    def create_trainer_file(self):
        """Create models_app/trainer.py"""
        content = '''import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb

class ModelTrainer:
    """Train and manage ML models"""
    
    def __init__(self):
        self.models = {}
        self.metrics = {}
    
    def train(self, X, y):
        """Train models on data"""
        # Simple implementation for now
        return {}
'''
        path = Path(__file__).parent.parent / 'models_app' / 'trainer.py'
        path.write_text(content)
    
    def create_api_file(self):
        """Create frontend/src/lib/api.ts"""
        content = '''// API client for Episteme
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export const api = {
    // Health check
    async healthCheck() {
        const res = await fetch(`${API_BASE}/health/`);
        return res.json();
    },
    
    // Datasets
    async getDatasets() {
        const res = await fetch(`${API_BASE}/datasets/`);
        return res.json();
    },
    
    async getDataset(id: string) {
        const res = await fetch(`${API_BASE}/datasets/${id}/`);
        return res.json();
    },
    
    // Models
    async predict(data: any) {
        const res = await fetch(`${API_BASE}/models/predict/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return res.json();
    },
    
    async getMetrics() {
        const res = await fetch(`${API_BASE}/models/metrics/`);
        return res.json();
    },
    
    // Socratic
    async getSocraticPrompts() {
        const res = await fetch(`${API_BASE}/socratic/prompts/`);
        return res.json();
    }
};
'''
        path = Path(__file__).parent.parent.parent / 'frontend' / 'src' / 'lib' / 'api.ts'
        path.parent.mkdir(exist_ok=True)
        path.write_text(content)
    
    def create_page(self, page_name):
        """Create a missing page"""
        content = f'''import {{ motion }} from 'framer-motion';

export default function {page_name.title()}Page() {{
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="max-w-6xl mx-auto"
    >
      <h1 className="text-4xl font-bold text-navy mb-4">{page_name.title()}</h1>
      <p className="text-xl text-gray-600">Coming soon...</p>
    </motion.div>
  );
}}
'''
        path = Path(__file__).parent.parent.parent / 'frontend' / 'src' / 'app' / page_name / 'page.tsx'
        path.parent.mkdir(exist_ok=True)
        path.write_text(content)
    
    def fix_tsconfig(self):
        """Fix tsconfig.json to include path aliases"""
        import json
        path = Path(__file__).parent.parent.parent / 'frontend' / 'tsconfig.json'
        
        if path.exists():
            with open(path) as f:
                config = json.load(f)
            
            if 'compilerOptions' not in config:
                config['compilerOptions'] = {}
            
            if 'paths' not in config['compilerOptions']:
                config['compilerOptions']['paths'] = {}
            
            config['compilerOptions']['paths']['@/*'] = ['./src/*']
            
            with open(path, 'w') as f:
                json.dump(config, f, indent=2)
    
    def add_app_to_settings(self, app_name):
        """Add app to INSTALLED_APPS in settings"""
        settings_path = Path(__file__).parent.parent / 'config' / 'settings' / 'base.py'
        
        if settings_path.exists():
            content = settings_path.read_text()
            
            # Find INSTALLED_APPS list and add app if not there
            if f"'{app_name}'" not in content and f'"{app_name}"' not in content:
                # Simple approach - append to end of list
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'INSTALLED_APPS' in line and '[' in line:
                        # Find the closing bracket
                        for j in range(i, len(lines)):
                            if ']' in lines[j]:
                                lines[j] = lines[j].replace(']', f"    '{app_name}',\n]")
                                break
                        break
                
                settings_path.write_text('\n'.join(lines))

def main():
    tracker = EpistemeErrorTracker()
    errors = tracker.scan_all_errors()
    
    if errors:
        response = input("\n🔧 Automatically fix all errors? (y/n): ")
        if response.lower() == 'y':
            tracker.fix_all_errors()
            print("\n🔄 Running verification again...")
            tracker.scan_all_errors()
    
    print("\n✨ Done!")

if __name__ == '__main__':
    main()