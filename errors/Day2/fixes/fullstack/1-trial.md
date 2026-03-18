# 🔍 **The Truth: Why the Error Tracker Lied & How to Really Fix It**

The error tracker failed because it only checked if `src/lib/api.ts` exists, but your Next.js can't find it because of **path resolution issues**. Let's manually fix everything step by step.

## 📋 **Current Problems Identified**

### **Frontend Issues:**

1. **`@/lib/api` not found** - Path alias not working
2. **Next.js config warnings** - Deprecated options
3. **Missing API client file** (or in wrong location)

### **Backend Issues:**

Let's check those too.

---

## 🚀 **Step 1: Fix Next.js Configuration**

```bash
cd ~/Projects/episteme/frontend

# Delete the old config
rm next.config.js

# Create new next.config.ts (TypeScript version)
cat > next.config.ts << 'EOF'
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  reactStrictMode: true,
  
  // Modern image configuration (replaces domains)
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**',
      },
    ],
  },
  
  // Remove swcMinify (it's enabled by default in Next.js 15+)
  
  // API rewrites
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'}/:path*`,
      },
    ];
  },
};

export default nextConfig;
EOF
```

---

## 🚀 **Step 2: Fix TypeScript Path Alias**

```bash
# Update tsconfig.json
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
EOF
```

---

## 🚀 **Step 3: Create the API Client in the CORRECT Location**

```bash
# Create the directory if it doesn't exist
mkdir -p src/lib

# Create the API client
cat > src/lib/api.ts << 'EOF'
/**
 * Episteme API Client
 * 
 * This file MUST be at: frontend/src/lib/api.ts
 * And MUST be imported as: import { api } from '@/lib/api'
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// Log the API URL for debugging
console.log('🌐 API Client initialized with base URL:', API_BASE);

export const api = {
  // Health check
  async healthCheck() {
    try {
      const res = await fetch(`${API_BASE}/health/`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (error) {
      console.error('API Health Check Failed:', error);
      throw error;
    }
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
  async predict(data: { features: Record<string, number>; model: string }) {
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

export default api;
EOF

# Create a test page to verify everything
cat > src/app/test-api/page.tsx << 'EOF'
'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';

export default function TestApiPage() {
  const [status, setStatus] = useState('Testing...');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    testConnection();
  }, []);

  const testConnection = async () => {
    try {
      const result = await api.healthCheck();
      setStatus(`✅ Connected! Backend says: ${result.message}`);
    } catch (err) {
      setError(`❌ Failed: ${err instanceof Error ? err.message : 'Unknown error'}`);
      setStatus('Failed');
    }
  };

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">API Test Page</h1>
      <div className="p-4 bg-gray-100 rounded">
        <p className="mb-2">Status: {status}</p>
        {error && <p className="text-red-600">{error}</p>}
        <p className="text-sm text-gray-600 mt-4">
          API URL: {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'}
        </p>
      </div>
    </div>
  );
}
EOF
```

---

## 🚀 **Step 4: Clear Next.js Cache**

```bash
# Kill any running Next.js processes
pkill -f next

# Clear Next.js cache
rm -rf .next
rm -rf node_modules/.cache

# Reinstall dependencies to be safe
rm -rf node_modules
npm install

# Now try running again
npm run dev
```

---

## 🚀 **Step 5: Verify the File Structure**

```bash
# This should show your api.ts file
ls -la src/lib/
# Should output: api.ts

# Check if the file exists in the right place
cat src/lib/api.ts | head -5
# Should show the file content
```

---

## 🚀 **Step 6: Fix Backend Issues (One by One)**

Open a NEW terminal:

```bash
cd ~/Projects/episteme/backend
source venv/bin/activate

# 1. Install debug toolbar
pip install django-debug-toolbar

# 2. Create missing core files
cat > core/exceptions.py << 'EOF'
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        response.data = {
            'error': True,
            'code': response.status_code,
            'message': str(exc),
            'type': exc.__class__.__name__,
        }
    return response
EOF

cat > core/utils.py << 'EOF'
import json
from datetime import datetime

def log_model_training(model_name, metrics, dataset_name):
    print(f"[{datetime.now()}] Model {model_name} trained on {dataset_name}: {metrics}")
EOF

# 3. Update development settings to include debug toolbar
cat >> config/settings/development.py << 'EOF'

# Debug Toolbar Configuration
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']
    
    # For Docker/network access
    import socket
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + '1' for ip in ips]
EOF

# 4. Run migrations and load data
python manage.py makemigrations
python manage.py migrate
python scripts/load_datasets.py
```

---

## 🚀 **Step 7: Test Everything in Order**

### **Terminal 1 - Backend**

```bash
cd ~/Projects/episteme/backend
source venv/bin/activate
python manage.py runserver
```

### **Terminal 2 - Frontend**

```bash
cd ~/Projects/episteme/frontend
npm run dev
```

### **Browser Tests**

```bash
1. **Test API directly**: http://localhost:8000/api/health/
   - Should show: `{"status":"healthy","message":"Episteme API is running"}`

2. **Test frontend API connection**: http://localhost:3000/test-api
   - Should show: ✅ Connected!

3. **Test demo page**: http://localhost:3000/demo
   - Should load without errors

---

## 🚀 **Step 8: If Still Not Working - Nuclear Option**

```bash
cd ~/Projects/episteme/frontend

# Complete reset
rm -rf node_modules .next
rm package-lock.json

# Reinstall everything fresh
npm install
npm install framer-motion @heroicons/react
npm install -D @types/node

# Clear npm cache
npm cache clean --force

# Run with clean slate
npm run dev
```

---

## 📊 **Why Did the Error Tracker Lie?**

The error tracker only checked if the file `src/lib/api.ts` existed. But Next.js couldn't find it because:

1. **Path alias not working** - `@/lib/api` wasn't resolving correctly
2. **Cache issues** - Next.js cached the error state
3. **Config problems** - Deprecated options causing confusion

**The fix**: We manually ensured the file exists in the EXACT right place AND fixed the TypeScript path resolution.

---

## ✅ **After This, You Should Have:**

- ✅ No frontend module errors
- ✅ Backend running with all dependencies
- ✅ API client working
- ✅ All pages loading
- ✅ Test page to verify connections

**Try it now and let me know what happens!** If you still see errors, copy-paste the EXACT error message and I'll fix that specific one.
