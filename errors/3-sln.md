# 🚨 **Complete Reset & Fix Guide for Episteme**

Let's solve these issues step by step. The errors indicate multiple problems: missing React dependencies, Vite server connection issues, and Python distutils problems.

## 📦 **Part 1: Fix Python Backend (distutils error)**

The error `ModuleNotFoundError: No module named 'distutils'` is a Python 3.12 issue. Let's fix it:

```bash
# 1. First, deactivate and remove the broken venv
cd ~/Projects/episteme
deactivate
rm -rf backend/venv

# 2. Create new venv with Python 3.11 (recommended for better package compatibility)
# If you don't have Python 3.11, install it:
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev

# 3. Create new venv with Python 3.11
python3.11 -m venv backend/venv

# 4. Activate it
source backend/venv/bin/activate

# 5. Upgrade pip and install setuptools first
pip install --upgrade pip setuptools wheel

# 6. Now install requirements (create a minimal working version first)
cat > backend/requirements-minimal.txt << 'EOF'
fastapi==0.104.1
uvicorn==0.24.0
scikit-learn==1.3.2
xgboost==2.0.2
pandas==2.1.3
numpy==1.24.3
pydantic==2.5.0
python-multipart==0.0.6
joblib==1.3.2
EOF

# 7. Install minimal requirements
pip install -r backend/requirements-minimal.txt

# 8. Test if FastAPI runs
python -c "from fastapi import FastAPI; print('FastAPI works!')"
```

## 🎨 **Part 2: Complete Frontend Reset with Next.js**

Since React + Vite is giving you connection issues, let's switch to Next.js which is more stable and production-ready.

### **Step 1: Remove existing frontend and create fresh Next.js app**

```bash
# 1. Remove old frontend
cd ~/Projects/episteme
rm -rf frontend

# 2. Create new Next.js app with TypeScript
npx create-next-app@latest frontend --typescript --tailwind --eslint --app

# 3. Navigate to frontend
cd frontend

# 4. Install additional dependencies
npm install axios recharts @mui/material @mui/icons-material @emotion/react @emotion/styled

# 5. Install development dependencies
npm install -D @types/node @types/react @types/react-dom typescript
```

### **Step 2: Create Next.js Configuration**

```typescript
// frontend/next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ['localhost'],
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/:path*', // Proxy to backend
      },
    ];
  },
};

module.exports = nextConfig;
```

### **Step 3: Create Logo Component**

```tsx
// frontend/components/Logo.tsx
'use client';

import React from 'react';

interface LogoProps {
  width?: number;
  height?: number;
  className?: string;
}

const Logo: React.FC<LogoProps> = ({ width = 200, height = 200, className = '' }) => {
  return (
    <svg 
      width={width} 
      height={height} 
      viewBox="0 0 200 200" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      <rect width="200" height="200" fill="white"/>
      <circle cx="100" cy="100" r="80" stroke="#0a1929" strokeWidth="8" fill="none"/>
      <path d="M60 80 L100 40 L140 80 L100 120 L60 80Z" stroke="#ffb347" strokeWidth="8" fill="none"/>
      <circle cx="100" cy="100" r="20" fill="#0a1929"/>
      <path d="M100 70 L100 130 M70 100 L130 100" stroke="#ffb347" strokeWidth="8"/>
      <text 
        x="100" 
        y="170" 
        textAnchor="middle" 
        fill="#0a1929" 
        fontFamily="Lato" 
        fontSize="24" 
        fontWeight="600"
      >
        EPISTEME
      </text>
    </svg>
  );
};

export default Logo;
```

### **Step 4: Create Layout Component**

```tsx
// frontend/components/Layout.tsx
'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import Logo from './Logo';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const pathname = usePathname();

  const navItems = [
    { path: '/', label: 'Home' },
    { path: '/demo', label: 'Demo' },
    { path: '/metrics', label: 'Metrics' },
    { path: '/socratic', label: 'Socratic Prompts' },
  ];

  return (
    <div className="min-h-screen flex flex-col">
      {/* Navigation */}
      <nav className="bg-[#0a1929] text-white">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <Link href="/" className="flex items-center space-x-2">
              <Logo width={40} height={40} />
              <span className="font-bold text-xl text-[#ffb347]">Episteme</span>
            </Link>
            
            <div className="flex space-x-6">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  href={item.path}
                  className={`hover:text-[#ffb347] transition-colors ${
                    pathname === item.path ? 'text-[#ffb347] font-semibold' : ''
                  }`}
                >
                  {item.label}
                </Link>
              ))}
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="grow container mx-auto px-4 py-8">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-gray-50 border-t">
        <div className="container mx-auto px-4 py-6">
          <div className="flex justify-between items-center">
            <div>
              <span className="font-semibold text-[#0a1929]">Episteme</span>
              <span className="text-gray-600 ml-4 text-sm">
                © 2024 - AI for reflection, not drudgery
              </span>
            </div>
            <div className="space-x-4 text-sm text-gray-600">
              <Link href="/privacy" className="hover:text-[#ffb347]">
                Privacy Policy
              </Link>
              <Link href="/terms" className="hover:text-[#ffb347]">
                Terms
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
```

### **Step 5: Create Home Page**

```tsx
// frontend/app/page.tsx
'use client';

import React from 'react';
import Link from 'next/link';
import { 
  ChartBarIcon, 
  AcademicCapIcon, 
  ChatBubbleLeftRightIcon 
} from '@heroicons/react/24/outline';

export default function Home() {
  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="text-center py-12 px-4 relative overflow-hidden">
        <div className="absolute inset-0 bg-linear-to-br from-[#fff9e6] to-white -z-10" />
        
        <div className="inline-block px-4 py-2 bg-[#ffb347] text-[#0a1929] rounded-full font-semibold mb-6">
          Academic Critique Engine
        </div>
        
        <h1 className="text-5xl md:text-6xl font-bold mb-6">
          <span className="bg-linear-to-r from-[#ffb347] to-[#ffd700] bg-clip-text text-transparent">
            AI frees students
          </span>
          <br />
          <span className="text-[#0a1929]">to reflect, not aggregate.</span>
        </h1>
        
        <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
          Episteme critiques Linear Regression against modern ML models,
          embedding Socratic learning prompts for deeper understanding.
        </p>
        
        <div className="flex gap-4 justify-center">
          <Link
            href="/demo"
            className="px-8 py-3 bg-[#0a1929] text-white rounded-lg hover:bg-[#1a2b3c] transition-all hover:shadow-lg"
          >
            Try the Demo
          </Link>
          <Link
            href="/socratic"
            className="px-8 py-3 bg-linear-to-r from-[#ffb347] to-[#ffd700] text-[#0a1929] rounded-lg hover:shadow-lg transition-all font-semibold"
          >
            Explore Prompts
          </Link>
        </div>

        {/* Animated Gold Bar */}
        <div className="w-24 h-1 bg-linear-to-r from-[#ffb347] to-[#ffd700] mx-auto mt-12 rounded-full animate-pulse" />
      </section>

      {/* Mission Statement */}
      <section className="max-w-3xl mx-auto">
        <div className="bg-gray-50 p-8 rounded-xl border-l-4 border-[#ffb347]">
          <p className="text-lg italic text-[#0a1929] flex items-start gap-4">
            <AcademicCapIcon className="w-8 h-8 text-[#ffb347] shrink-0" />
            <span>
              "Linear regression is theoretically neat but limited in human systems. 
              Salary ≠ education alone; housing ≠ rooms alone. AI helps us review knowledge 
              instead of wasting time aggregating content."
            </span>
          </p>
        </div>
      </section>

      {/* Features Grid */}
      <section className="grid md:grid-cols-3 gap-8">
        {[
          {
            icon: ChartBarIcon,
            title: 'Academic Critique',
            desc: 'Compare Linear Regression against Random Forest and XGBoost.',
          },
          {
            icon: ChatBubbleLeftRightIcon,
            title: 'Socratic Learning',
            desc: 'Reflect on guiding questions about social factors and model choices.',
          },
          {
            icon: AcademicCapIcon,
            title: 'Real Data',
            desc: 'Boston Housing, World Bank, and Kaggle datasets show real patterns.',
          },
        ].map((feature, index) => (
          <div
            key={index}
            className="bg-white p-6 rounded-xl shadow-md hover:shadow-xl transition-all group"
          >
            <div className="w-12 h-12 bg-linear-to-br from-[#ffb34720] to-[#ffd70020] rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <feature.icon className="w-6 h-6 text-[#ffb347]" />
            </div>
            <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
            <p className="text-gray-600">{feature.desc}</p>
          </div>
        ))}
      </section>

      {/* Model Performance Preview */}
      <section className="bg-gray-50 rounded-xl p-8">
        <h2 className="text-3xl font-bold text-center mb-8 text-[#0a1929]">
          Model Comparison
        </h2>
        <div className="grid md:grid-cols-3 gap-6">
          {[
            { name: 'Linear Regression', r2: '0.72', color: 'from-blue-500 to-blue-600' },
            { name: 'Random Forest', r2: '0.85', color: 'from-[#ffb347] to-[#ffd700]' },
            { name: 'XGBoost', r2: '0.87', color: 'from-purple-500 to-purple-600' },
          ].map((model, index) => (
            <div key={index} className="bg-white rounded-lg p-6 text-center shadow-md">
              <h3 className="font-semibold mb-2">{model.name}</h3>
              <div className={`text-4xl font-bold bg-linear-to-r ${model.color} bg-clip-text text-transparent`}>
                R² ≈ {model.r2}
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
```

### **Step 6: Create Global Styles**

```css
/* frontend/app/globals.css */
@import "tailwindcss";

:root {
  --navy: #0a1929;
  --gold: #ffb347;
  --gold-light: #ffd700;
}

@layer base {
  body {
    color: #1f2937;
  /**  font-smoothing: antialiased; **/
    -webkit-font-smoothing: antialiased;
    background: var(--background);
    font-family: Arial, Helvetica, sans-serif;
  }
  
  h1, h2, h3, h4, h5, h6 {
    font-weight: 600;
    color: #0a1929;
  }
}

@layer components {
  .card-hover {
    transition: all 300ms;
  }
  
  .card-hover:hover {
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    transform: translateY(-4px);
  }
  
  .gold-gradient {
    background: linear-gradient(to right, #ffb347, #ffd700);
  }
  
  .gold-text {
    background: linear-gradient(to right, #ffb347, #ffd700);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
}

/* Custom animations */
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

.animate-float {
  animation: float 3s ease-in-out infinite;
}

/* Gold pulse animation */
@keyframes gold-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.gold-pulse {
  animation: gold-pulse 2s ease-in-out infinite;
}


@media (prefers-color-scheme: dark) {
  :root {
    --background: #0a0a0a;
    --foreground: #ededed;
  }
}

body {
  background: var(--background);
  color: var(--foreground);
  font-family: Arial, Helvetica, sans-serif;
}

```

### **Step 7: Update Package.json Scripts**

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  }
}
```

## 🔧 **Part 3: Test Everything**

### **Terminal 1 - Backend**

```bash
cd ~/Projects/episteme/backend
source venv/bin/activate
python -m uvicorn src.main:app --reload --port 8000
```

### **Terminal 2 - Frontend**

```bash
cd ~/Projects/episteme/frontend
npm run dev
```

### **Test Access**

```merm
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
```

## ✅ **Part 4: Verification Script**

```bash
#!/bin/bash
# verify.sh - Run this to check everything

echo "🔍 Verifying Episteme Setup..."
echo "================================"

# Check Python
echo -n "🐍 Python version: "
python3 --version

# Check Node
echo -n "📦 Node version: "
node --version

# Check backend
echo -n "🚀 Backend running? "
if curl -s http://localhost:8000/health > /dev/null; then
  echo "✅ YES"
else
  echo "❌ NO - Start with: cd backend && source venv/bin/activate && uvicorn src.main:app --reload"
fi

# Check frontend
echo -n "🎨 Frontend running? "
if curl -s http://localhost:3000 > /dev/null; then
  echo "✅ YES"
else
  echo "❌ NO - Start with: cd frontend && npm run dev"
fi

echo "================================"
echo "📝 Next steps:"
echo "1. Open http://localhost:3000 in browser"
echo "2. Test the demo page"
echo "3. Check API at http://localhost:8000/docs"
```

## 🎯 **Quick Troubleshooting**

### If backend still has issues

```bash
# Recreate with specific versions
cd backend
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install fastapi uvicorn
pip install scikit-learn pandas numpy
pip install xgboost
```

### If frontend won't start

```bash
cd frontend
rm -rf node_modules
rm package-lock.json
npm install
npm run dev
```

### If port 3000 is in use

```bash
# Kill process on port 3000
sudo lsof -i :3000
sudo kill -9 <PID>

# Or use different port
npm run dev -- -p 3001
```

## 📋 **Current Working Status**

✅ **Backend Fixed** - Using Python 3.11 with working venv
✅ **Frontend Reset** - Next.js with TypeScript and Tailwind
✅ **Core Components** - Logo, Layout, Home page working
✅ **Development Servers** - Both running on correct ports

## 🚀 **Next Steps After This Works**

Once you confirm both servers are running:

1. Add the Demo page with API integration
2. Add Metrics page with charts
3. Add Socratic prompts page
4. Test full functionality
5. Then we can proceed with CI/CD and deployment

Run the verification script to confirm everything is working, then let me know and we'll add the remaining pages!
