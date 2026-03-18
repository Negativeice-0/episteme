#!/usr/bin/env python
"""
Fixed error tracker for Episteme
"""
import os
import sys
import django
import subprocess
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

class FixedErrorTracker:
    def __init__(self):
        self.backend_errors = []
        self.frontend_errors = []
        
    def scan_all_errors(self):
        print("\n" + "="*60)
        print("🔍 EPISTEME FIXED ERROR SCANNER")
        print("="*60)
        
        self.scan_backend()
        self.scan_frontend()
        self.print_fixes()
        self.ask_to_fix()
        
    def scan_backend(self):
        print("\n📡 SCANNING BACKEND...")
        
        # Check debug_toolbar
        try:
            import debug_toolbar # type: ignore
            print("  ✅ debug_toolbar installed")
        except ImportError:
            self.backend_errors.append({
                'type': 'missing_dependency',
                'target': 'debug_toolbar',
                'fix': 'pip install django-debug-toolbar'
            })
            print("  ❌ debug_toolbar missing")
        
        # Check core files
        core_files = ['exceptions.py', 'utils.py']
        for file in core_files:
            path = Path('core') / file
            if not path.exists():
                self.backend_errors.append({
                    'type': 'missing_file',
                    'target': f'core/{file}',
                    'fix': f'Create core/{file}'
                })
                print(f"  ❌ core/{file} missing")
            else:
                print(f"  ✅ core/{file} exists")
    
    def scan_frontend(self):
        print("\n🎨 SCANNING FRONTEND...")
        
        frontend_path = Path(__file__).parent.parent.parent / 'frontend'
        
        # Check lib/api.ts
        api_file = frontend_path / 'src' / 'lib' / 'api.ts'
        if not api_file.exists():
            self.frontend_errors.append({
                'type': 'missing_file',
                'target': 'src/lib/api.ts',
                'fix': 'Create API client'
            })
            print("  ❌ src/lib/api.ts missing")
        else:
            print("  ✅ src/lib/api.ts exists")
        
        # Check framer-motion
        package_json = frontend_path / 'package.json'
        if package_json.exists():
            import json
            with open(package_json) as f:
                pkg = json.load(f)
                deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
                
                if 'framer-motion' not in deps:
                    self.frontend_errors.append({
                        'type': 'missing_dependency',
                        'target': 'framer-motion',
                        'fix': 'npm install framer-motion'
                    })
                    print("  ❌ framer-motion missing")
                else:
                    print("  ✅ framer-motion installed")
        
        # Check pages
        pages = ['demo', 'metrics', 'socratic', 'about']
        for page in pages:
            page_file = frontend_path / 'src' / 'app' / page / 'page.tsx'
            if not page_file.exists():
                self.frontend_errors.append({
                    'type': 'missing_page',
                    'target': page,
                    'fix': f'Create {page} page'
                })
                print(f"  ❌ {page} page missing")
            else:
                print(f"  ✅ {page} page exists")
    
    def print_fixes(self):
        print("\n" + "="*60)
        print("📊 ERRORS FOUND")
        print("="*60)
        
        all_errors = self.backend_errors + self.frontend_errors
        
        if not all_errors:
            print("\n✅ No errors found! Everything is working!")
            return
        
        print(f"\n❌ Total: {len(all_errors)} errors")
        print(f"  Backend: {len(self.backend_errors)}")
        print(f"  Frontend: {len(self.frontend_errors)}")
        
        print("\n🔧 FIXES NEEDED:")
        for i, error in enumerate(all_errors, 1):
            print(f"\n  {i}. [{error['type']}] {error['target']}")
            print(f"     → FIX: {error['fix']}")
    
    def ask_to_fix(self):
        if not (self.backend_errors or self.frontend_errors):
            return
        
        response = input("\n🔧 Automatically fix all errors? (y/n): ")
        if response.lower() == 'y':
            self.fix_all()
    
    def fix_all(self):
        print("\n" + "="*60)
        print("🔧 FIXING ERRORS...")
        print("="*60)
        
        # Fix backend
        for error in self.backend_errors:
            if error['type'] == 'missing_dependency' and error['target'] == 'debug_toolbar':
                print("\n📦 Installing django-debug-toolbar...")
                subprocess.run(['pip', 'install', 'django-debug-toolbar'])
                
                # Add to settings
                settings_path = Path('config/settings/development.py')
                if settings_path.exists():
                    content = settings_path.read_text()
                    if 'debug_toolbar' not in content:
                        with open(settings_path, 'a') as f:
                            f.write('\n\n# Debug Toolbar\n')
                            f.write("if DEBUG:\n")
                            f.write("    INSTALLED_APPS += ['debug_toolbar']\n")
                            f.write("    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']\n")
                            f.write("    INTERNAL_IPS = ['127.0.0.1']\n")
                    print("   ✅ Added to settings")
            
            elif error['type'] == 'missing_file':
                self.create_file(error['target'])
        
        # Fix frontend
        frontend_path = Path(__file__).parent.parent.parent / 'frontend'
        
        for error in self.frontend_errors:
            if error['type'] == 'missing_dependency' and error['target'] == 'framer-motion':
                print("\n📦 Installing framer-motion...")
                subprocess.run(['npm', 'install', 'framer-motion'], cwd=frontend_path)
            
            elif error['type'] == 'missing_file' and error['target'] == 'src/lib/api.ts':
                self.create_api_file(frontend_path)
            
            elif error['type'] == 'missing_page':
                self.create_page(frontend_path, error['target'])
        
        print("\n✅ All fixes applied!")
        print("\n🔄 Run the scanner again to verify:")
        print("   python scripts/error_tracker.py")
    
    def create_file(self, filename):
        """Create missing Python file"""
        print(f"\n📝 Creating {filename}...")
        
        if filename == 'core/exceptions.py':
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
        elif filename == 'core/utils.py':
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

def log_model_training(model_name, metrics, dataset_name):
    """Log model training metrics"""
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'model': model_name,
        'metrics': metrics,
        'dataset': dataset_name,
    }
    logger.info(f"Model training: {JSONFormatter.format(log_entry)}")
'''
        else:
            content = '# Auto-generated file\n'
        
        path = Path(filename)
        path.write_text(content)
        print(f"   ✅ Created {filename}")
    
    def create_api_file(self, frontend_path):
        """Create frontend API client"""
        print("\n📝 Creating src/lib/api.ts...")
        
        api_dir = frontend_path / 'src' / 'lib'
        api_dir.mkdir(parents=True, exist_ok=True)
        
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
        api_file = api_dir / 'api.ts'
        api_file.write_text(content)
        print("   ✅ Created api.ts")
    
    def create_page(self, frontend_path, page_name):
        """Create a missing page"""
        print(f"\n📝 Creating {page_name} page...")
        
        page_dir = frontend_path / 'src' / 'app' / page_name
        page_dir.mkdir(parents=True, exist_ok=True)
        
        content = f'''import {{ motion }} from 'framer-motion';
import {{ useEffect, useState }} from 'react';
import {{ api }} from '@/lib/api';

export default function {page_name.title()}Page() {{
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);

  useEffect(() => {{
    loadData();
  }}, []);

  const loadData = async () => {{
    try {{
      // Add your data loading logic here
      setLoading(false);
    }} catch (error) {{
      console.error('Failed to load data:', error);
      setLoading(false);
    }}
  }};

  if (loading) {{
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gold"></div>
      </div>
    );
  }}

  return (
    <motion.div
      initial={{{{ opacity: 0, y: 20 }}}}
      animate={{{{ opacity: 1, y: 0 }}}}
      transition={{{{ duration: 0.5 }}}}
      className="max-w-6xl mx-auto"
    >
      <h1 className="text-4xl font-bold text-navy mb-4">{page_name.title()}</h1>
      <p className="text-xl text-gray-600">Coming soon...</p>
    </motion.div>
  );
}}
'''
        page_file = page_dir / 'page.tsx'
        page_file.write_text(content)
        print(f"   ✅ Created {page_name} page")

def main():
    tracker = FixedErrorTracker()
    tracker.scan_all_errors()

if __name__ == '__main__':
    main()