# 🚀 **Complete Fresh Start: Episteme with Django + Next.js + PostgreSQL**

## 📋 **Project Overview**

Build Episteme - an educational platform that critiques Linear Regression against modern ML models (Random Forest, XGBoost) with Socratic learning prompts.

**Tech Stack:**

- **Backend**: Django 4.2 + Django REST Framework + PostgreSQL
- **Frontend**: Next.js 14 + TypeScript + TailwindCSS + Framer Motion
- **ML**: scikit-learn, XGBoost, pandas, numpy
- **Database**: PostgreSQL 15
- **Deployment**: Docker + GitHub Actions (optional)

---

## 🏗️ **Phase 1: Project Setup**

### **1.1 Create Project Directory**

```bash
# Create main project folder
mkdir -p ~/Projects/episteme
cd ~/Projects/episteme

# Create project structure
mkdir -p {backend,frontend,docs,scripts,infra}
```

### **1.2 Initialize Git Repository**

```bash
git init
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/
*.egg-info/
dist/
build/

# Django
*.log
local_settings.py
db.sqlite3
media/
staticfiles/

# Next.js
.next/
out/
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# Environment
.env
.env.local
.env.production
.env.development

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF

git add .
git commit -m "Initial commit: Project structure"
```

---

## 🐍 **Phase 2: Django Backend Setup**

### **2.1 Install Python 3.10 (Critical for ML libraries)**

```bash
# Add deadsnakes repository (for Python 3.10)
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# Install Python 3.10 and dev tools
sudo apt install python3.10 python3.10-venv python3.10-dev python3-pip -y

# Verify installation
python3.10 --version  # Should show Python 3.10.x
```

### **2.2 Create Virtual Environment**

```bash
cd ~/Projects/episteme/backend

# Create virtual environment with Python 3.10
python3.10 -m venv venv

# Activate it
source venv/bin/activate

# Verify Python version
python --version  # Should show Python 3.10.x

# Upgrade pip and core tools
pip install --upgrade pip setuptools wheel
```

### **2.3 Create Requirements Files**

**backend/requirements/base.txt

```txt
# Core Django
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
django-environ==0.11.2

# Database
psycopg2-binary==2.9.9

# ML & Data Science
numpy==1.23.5
pandas==2.1.3
scikit-learn==1.3.2
xgboost==2.0.2
joblib==1.3.2

# Utilities
python-decouple==3.8
gunicorn==21.2.0
whitenoise==6.6.0
```

**backend/requirements/development.txt

```txt
-r base.txt

# Development tools
django-debug-toolbar==4.2.0
ipython==8.17.2
pytest==7.4.3
pytest-django==4.7.0
pytest-cov==4.1.0
factory-boy==3.3.0
```

**backend/requirements/production.txt

```txt
-r base.txt

# Production optimizations
redis==5.0.1
django-redis==5.4.0
sentry-sdk==1.39.1
```

### **2.4 Install Dependencies

```bash
cd ~/Projects/episteme/backend
source venv/bin/activate

# Create requirements directory
mkdir -p requirements

# Move requirement files
mv base.txt requirements/
mv development.txt requirements/
mv production.txt requirements/

# Install development dependencies
pip install -r requirements/development.txt
```

### **2.5 Create Django Project with Modular Structure**

```bash
cd ~/Projects/episteme/backend

# Create Django project
django-admin startproject config .

# Create necessary directories
mkdir -p apps
mkdir -p apps/{core,api,datasets,models_app,socratic}
mkdir -p {static,media,logs,scripts}
mkdir -p config/settings

# Create __init__.py files
touch apps/__init__.py
touch apps/core/__init__.py
touch apps/api/__init__.py
touch apps/datasets/__init__.py
touch apps/models_app/__init__.py
touch apps/socratic/__init__.py
touch config/settings/__init__.py

# Create Django apps
cd apps
python ../manage.py startapp core
python ../manage.py startapp api
python ../manage.py startapp datasets
python ../manage.py startapp models_app
python ../manage.py startapp socratic
cd ..
```

### **2.6 Configuration Files**

**backend/.env

```bash
# Django Settings
SECRET_KEY=django-insecure-your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=episteme
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

**backend/config/settings/base.py

```python
import os
from pathlib import Path
from environ import Env

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Environment variables
env = Env()
Env.read_env(os.path.join(BASE_DIR, '.env'))

# Security
SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'corsheaders',
    
    # Local apps
    'apps.core',
    'apps.api',
    'apps.datasets',
    'apps.models_app',
    'apps.socratic',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.core.middleware.RequestLoggingMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])
CORS_ALLOW_CREDENTIALS = True

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer' if DEBUG else 'rest_framework.renderers.JSONRenderer',
    ],
    'EXCEPTION_HANDLER': 'apps.core.exceptions.custom_exception_handler',
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'maxBytes': 10485760,
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}
```

**backend/config/settings/development.py

```python
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Use SQLite for quick development (optional)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']
```

**backend/config/settings/production.py

```python
from .base import *

DEBUG = False
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['episteme.app', 'api.episteme.app'])

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CORS
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=['https://episteme.app'])

# REST Framework - disable browsable API
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = ['rest_framework.renderers.JSONRenderer']
```

**backend/config/urls.py

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
```

**backend/config/wsgi.py** and **backend/config/asgi.py** remain as generated.

### **2.7 Create manage.py wrapper

```bash
cat > manage.py << 'EOF'
#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
EOF

chmod +x manage.py
```

---

## 🐘 **Phase 3: PostgreSQL Setup**

### **3.1 Install PostgreSQL

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Check status
sudo systemctl status postgresql
```

### **3.2 Create Database and User

```bash
# Switch to postgres user
sudo -u postgres psql

# In psql prompt:
CREATE DATABASE episteme;
CREATE USER postgres WITH PASSWORD 'postgres';
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE episteme TO postgres;
\q
```

### **3.3 Test Connection

```bash
# Test connection
psql -h localhost -U postgres -d episteme -W
# Password: postgres
\q
```

---

## ⚛️ **Phase 4: Next.js Frontend Setup**

### **4.1 Install Node.js

```bash
# Install Node.js 18.x (LTS)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Verify
node --version
npm --version
```

### **4.2 Create Next.js Application

```bash
cd ~/Projects/episteme

# Create Next.js app with all options
npx create-next-app@latest frontend \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*"

cd frontend
```

### **4.3 Install Frontend Dependencies

```bash
cd ~/Projects/episteme/frontend

# Core dependencies
npm install axios react-query zustand

# UI and animations
npm install framer-motion react-intersection-observer
npm install @heroicons/react
npm install react-hot-toast

# Charts and data visualization
npm install recharts d3 @types/d3

# Forms
npm install react-hook-form zod @hookform/resolvers

# Date handling
npm install date-fns

# Development dependencies
npm install -D @types/node @types/react @types/react-dom
npm install -D prettier eslint-config-prettier
```

### **4.4 Update package.json scripts

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "format": "prettier --write \"**/*.{js,jsx,ts,tsx,json,css,md}\""
  }
}
```

### **4.5 Configure Next.js

```javascript
// frontend/next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ['localhost', 'api.episteme.app'],
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.NEXT_PUBLIC_API_URL + '/:path*',
      },
    ];
  },
  // Experimental features for better performance
  experimental: {
    optimizeCss: true,
    scrollRestoration: true,
  },
};

module.exports = nextConfig;
```

### **4.6 Environment Variables

```bash
# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_APP_NAME=Episteme
NEXT_PUBLIC_APP_VERSION=1.0.0
```

### **4.7 Tailwind Configuration

```javascript
// frontend/tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        navy: '#0a1929',
        gold: '#ffb347',
        'gold-light': '#ffd700',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'slide-up': 'slideUp 0.5s ease-out',
        'fade-in': 'fadeIn 0.8s ease-in',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: 0 },
          '100%': { transform: 'translateY(0)', opacity: 1 },
        },
        fadeIn: {
          '0%': { opacity: 0 },
          '100%': { opacity: 1 },
        },
      },
      backgroundImage: {
        'gold-gradient': 'linear-gradient(135deg, #ffb347 0%, #ffd700 100%)',
        'navy-gradient': 'linear-gradient(135deg, #0a1929 0%, #1a2b3c 100%)',
      },
    },
  },
  plugins: [],
};
```

### **4.8 Global Styles

```css
/* frontend/src/app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --navy: #0a1929;
    --gold: #ffb347;
    --gold-light: #ffd700;
  }

  * {
    @apply border-border;
  }

  body {
    @apply bg-white text-gray-900 antialiased;
  }

  h1, h2, h3, h4, h5, h6 {
    @apply font-bold text-navy;
  }
}

@layer components {
  .gold-gradient {
    @apply bg-gradient-to-r from-gold to-gold-light;
  }
  
  .gold-text {
    @apply bg-gradient-to-r from-gold to-gold-light bg-clip-text text-transparent;
  }
  
  .card-hover {
    @apply transition-all duration-300 hover:shadow-xl hover:-translate-y-1;
  }
}
```

### **4.9 Create Folder Structure

```bash
cd ~/Projects/episteme/frontend/src

# Create directory structure
mkdir -p components/{layout,ui,features}
mkdir -p hooks
mkdir -p lib
mkdir -p services
mkdir -p store
mkdir -p types
mkdir -p utils
mkdir -p app/(routes)/{demo,metrics,socratic,about}
mkdir -p styles
mkdir -p public/images

# Create barrel files
touch components/index.ts
touch hooks/index.ts
touch lib/index.ts
touch services/index.ts
touch store/index.ts
touch types/index.ts
touch utils/index.ts
```

---

## 🔗 **Phase 5: Backend-Frontend Integration**

### **5.1 Create API Service Layer**

**frontend/src/types/index.ts

```typescript
export interface Dataset {
  id: string;
  name: string;
  description: string;
  features: string[];
  target: string;
  feature_descriptions: Record<string, string>;
  units: string;
  n_samples: number;
  n_features: number;
}

export interface PredictionRequest {
  features: Record<string, number>;
  model: 'Linear Regression' | 'Random Forest' | 'XGBoost';
}

export interface PredictionResponse {
  prediction: number;
  model: string;
  dataset: string;
  units: string;
}

export interface ModelMetrics {
  r2: number;
  rmse: number;
  mae: number;
  feature_importance?: Record<string, number>;
}

export interface ComparisonResponse {
  metrics: Record<string, ModelMetrics>;
  best_model: string;
  models: string[];
  note: string;
}

export interface SocraticPrompt {
  id: number;
  question: string;
  context: string;
  reflection: string;
  order: number;
}

export interface Reflection {
  id: number;
  prompt: number;
  content: string;
  session_id: string;
  created_at: string;
}
```

**frontend/src/lib/api.ts

```typescript
import axios, { AxiosError, AxiosInstance } from 'axios';
import {
  Dataset,
  PredictionRequest,
  PredictionResponse,
  ComparisonResponse,
  SocraticPrompt,
  Reflection,
  ModelMetrics,
} from '@/types';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response) {
          // Server responded with error
          console.error('API Error:', error.response.data);
          throw error.response.data;
        } else if (error.request) {
          // Request made but no response
          console.error('Network Error:', error.request);
          throw new Error('Network error - is the backend running?');
        } else {
          // Something else happened
          console.error('Error:', error.message);
          throw error;
        }
      }
    );
  }

  // Health check
  async healthCheck() {
    const response = await this.client.get('/health/');
    return response.data;
  }

  // Datasets
  async getDatasets() {
    const response = await this.client.get('/datasets/');
    return response.data;
  }

  async getDataset(id: string): Promise<Dataset> {
    const response = await this.client.get(`/datasets/${id}/`);
    return response.data;
  }

  async getCurrentDataset() {
    const response = await this.client.get('/datasets/current/');
    return response.data;
  }

  async switchDataset(datasetId: string) {
    const response = await this.client.post('/datasets/switch/', { dataset_id: datasetId });
    return response.data;
  }

  // Models
  async predict(request: PredictionRequest): Promise<PredictionResponse> {
    const response = await this.client.post('/models/predict/', request);
    return response.data;
  }

  async getMetrics(): Promise<Record<string, ModelMetrics>> {
    const response = await this.client.get('/models/metrics/');
    return response.data;
  }

  async compareModels(): Promise<ComparisonResponse> {
    const response = await this.client.get('/models/compare/');
    return response.data;
  }

  async retrainModels(datasetId?: string) {
    const response = await this.client.post('/models/retrain/', { dataset_id: datasetId });
    return response.data;
  }

  // Socratic
  async getPrompts(): Promise<SocraticPrompt[]> {
    const response = await this.client.get('/socratic/prompts/');
    return response.data;
  }

  async getRandomPrompt(): Promise<SocraticPrompt> {
    const response = await this.client.get('/socratic/prompts/random/');
    return response.data;
  }

  async saveReflection(promptId: number, content: string, sessionId: string): Promise<Reflection> {
    const response = await this.client.post(`/socratic/prompts/${promptId}/reflect/`, {
      content,
      session_id: sessionId,
    });
    return response.data;
  }
}

export const api = new ApiClient();
```

### **5.2 Create Store with Zustand**

**frontend/src/store/useEpistemeStore.ts

```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { api } from '@/lib/api';
import { Dataset, ModelMetrics, SocraticPrompt } from '@/types';

interface EpistemeState {
  // State
  currentDataset: string | null;
  datasets: Dataset[];
  metrics: Record<string, ModelMetrics> | null;
  prompts: SocraticPrompt[];
  selectedModel: 'Linear Regression' | 'Random Forest' | 'XGBoost';
  isLoading: boolean;
  error: string | null;
  sessionId: string;

  // Actions
  setSelectedModel: (model: 'Linear Regression' | 'Random Forest' | 'XGBoost') => void;
  loadDatasets: () => Promise<void>;
  loadMetrics: () => Promise<void>;
  loadPrompts: () => Promise<void>;
  switchDataset: (datasetId: string) => Promise<void>;
  predict: (features: Record<string, number>) => Promise<number>;
  clearError: () => void;
}

export const useEpistemeStore = create<EpistemeState>()(
  persist(
    (set, get) => ({
      // Initial state
      currentDataset: null,
      datasets: [],
      metrics: null,
      prompts: [],
      selectedModel: 'Random Forest',
      isLoading: false,
      error: null,
      sessionId: Math.random().toString(36).substring(7),

      // Actions
      setSelectedModel: (model) => set({ selectedModel: model }),

      loadDatasets: async () => {
        set({ isLoading: true, error: null });
        try {
          const datasets = await api.getDatasets();
          set({ datasets, isLoading: false });
        } catch (error) {
          set({ error: 'Failed to load datasets', isLoading: false });
        }
      },

      loadMetrics: async () => {
        set({ isLoading: true, error: null });
        try {
          const metrics = await api.getMetrics();
          set({ metrics, isLoading: false });
        } catch (error) {
          set({ error: 'Failed to load metrics', isLoading: false });
        }
      },

      loadPrompts: async () => {
        set({ isLoading: true, error: null });
        try {
          const prompts = await api.getPrompts();
          set({ prompts, isLoading: false });
        } catch (error) {
          set({ error: 'Failed to load prompts', isLoading: false });
        }
      },

      switchDataset: async (datasetId) => {
        set({ isLoading: true, error: null });
        try {
          await api.switchDataset(datasetId);
          set({ currentDataset: datasetId, isLoading: false });
          // Reload metrics for new dataset
          await get().loadMetrics();
        } catch (error) {
          set({ error: 'Failed to switch dataset', isLoading: false });
        }
      },

      predict: async (features) => {
        set({ isLoading: true, error: null });
        try {
          const response = await api.predict({
            features,
            model: get().selectedModel,
          });
          set({ isLoading: false });
          return response.prediction;
        } catch (error) {
          set({ error: 'Prediction failed', isLoading: false });
          throw error;
        }
      },

      clearError: () => set({ error: null }),
    }),
    {
      name: 'episteme-storage',
      partialize: (state) => ({
        selectedModel: state.selectedModel,
        sessionId: state.sessionId,
      }),
    }
  )
);
```

---

## 🎨 **Phase 6: Frontend Components**

### **6.1 Layout Components**

**frontend/src/components/layout/Navbar.tsx

```tsx
'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion } from 'framer-motion';
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline';
import { useState } from 'react';

const navItems = [
  { path: '/', label: 'Home' },
  { path: '/demo', label: 'Demo' },
  { path: '/metrics', label: 'Metrics' },
  { path: '/socratic', label: 'Learn' },
];

export const Navbar = () => {
  const pathname = usePathname();
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-navy text-white sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <motion.div
              whileHover={{ rotate: 180 }}
              transition={{ duration: 0.3 }}
              className="w-8 h-8 bg-gold-gradient rounded-lg"
            />
            <span className="font-bold text-xl gold-text">Episteme</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex space-x-6">
            {navItems.map((item) => (
              <Link
                key={item.path}
                href={item.path}
                className={`relative px-3 py-2 transition-colors hover:text-gold ${
                  pathname === item.path ? 'text-gold' : ''
                }`}
              >
                {pathname === item.path && (
                  <motion.div
                    layoutId="activeNav"
                    className="absolute inset-0 bg-gold/20 rounded-lg"
                    transition={{ type: 'spring', bounce: 0.2, duration: 0.6 }}
                  />
                )}
                <span className="relative">{item.label}</span>
              </Link>
            ))}
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden p-2 hover:text-gold transition-colors"
          >
            {isOpen ? (
              <XMarkIcon className="w-6 h-6" />
            ) : (
              <Bars3Icon className="w-6 h-6" />
            )}
          </button>
        </div>

        {/* Mobile Navigation */}
        <motion.div
          initial={false}
          animate={isOpen ? 'open' : 'closed'}
          variants={{
            open: { height: 'auto', opacity: 1 },
            closed: { height: 0, opacity: 0 },
          }}
          className="md:hidden overflow-hidden"
        >
          <div className="py-4 space-y-2">
            {navItems.map((item) => (
              <Link
                key={item.path}
                href={item.path}
                className={`block px-4 py-2 rounded-lg transition-colors ${
                  pathname === item.path
                    ? 'bg-gold/20 text-gold'
                    : 'hover:bg-gold/10'
                }`}
                onClick={() => setIsOpen(false)}
              >
                {item.label}
              </Link>
            ))}
          </div>
        </motion.div>
      </div>
    </nav>
  );
};
```

**frontend/src/components/layout/Footer.tsx

```tsx
'use client';

import Link from 'next/link';

export const Footer = () => {
  return (
    <footer className="bg-gray-50 border-t">
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
          <div className="text-center md:text-left">
            <span className="font-semibold text-navy">Episteme</span>
            <span className="text-gray-600 ml-4 text-sm">
              © 2024 - AI for reflection, not drudgery
            </span>
          </div>
          
          <div className="flex space-x-6 text-sm text-gray-600">
            <Link href="/about" className="hover:text-gold transition-colors">
              About
            </Link>
            <Link href="/privacy" className="hover:text-gold transition-colors">
              Privacy
            </Link>
            <Link href="/terms" className="hover:text-gold transition-colors">
              Terms
            </Link>
            <a
              href="https://github.com/yourusername/episteme"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-gold transition-colors"
            >
              GitHub
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};
```

**frontend/src/components/layout/Layout.tsx

```tsx
'use client';

import { Navbar } from './Navbar';
import { Footer } from './Footer';
import { Toaster } from 'react-hot-toast';

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout = ({ children }: LayoutProps) => {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="grow container mx-auto px-4 py-8">
        {children}
      </main>
      <Footer />
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#0a1929',
            color: '#fff',
          },
          success: {
            iconTheme: {
              primary: '#ffb347',
              secondary: '#0a1929',
            },
          },
        }}
      />
    </div>
  );
};
```

### **6.2 Home Page**

**frontend/src/app/page.tsx

```tsx
'use client';

import { motion, useScroll, useTransform } from 'framer-motion';
import Link from 'next/link';
import { useRef } from 'react';
import { 
  ChartBarIcon, 
  AcademicCapIcon, 
  ChatBubbleLeftRightIcon 
} from '@heroicons/react/24/outline';

export default function HomePage() {
  const containerRef = useRef(null);
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ['start start', 'end start'],
  });

  const y = useTransform(scrollYProgress, [0, 1], ['0%', '50%']);
  const opacity = useTransform(scrollYProgress, [0, 0.5], [1, 0]);

  return (
    <div ref={containerRef} className="relative">
      {/* Hero Section with Parallax */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        {/* Animated Background */}
        <motion.div
          className="absolute inset-0"
          style={{ y, opacity }}
        >
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_50%,rgba(255,180,71,0.1)_0%,transparent_50%)]" />
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_70%_50%,rgba(10,25,41,0.1)_0%,transparent_50%)]" />
        </motion.div>

        {/* Floating Particles */}
        <div className="absolute inset-0 overflow-hidden">
          {[...Array(20)].map((_, i) => (
            <motion.div
              key={i}
              className="absolute w-2 h-2 bg-gold/20 rounded-full"
              initial={{
                x: Math.random() * window.innerWidth,
                y: Math.random() * window.innerHeight,
              }}
              animate={{
                y: [null, -30, 30, -30],
                x: [null, 30, -30, 30],
              }}
              transition={{
                duration: 10 + Math.random() * 10,
                repeat: Infinity,
                ease: 'linear',
              }}
            />
          ))}
        </div>

        {/* Main Content */}
        <div className="relative z-10 text-center px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <span className="inline-block px-4 py-2 bg-gold/10 text-gold rounded-full font-semibold mb-6">
              Academic Critique Engine
            </span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-5xl md:text-7xl font-bold mb-6"
          >
            <span className="gold-text">AI frees students</span>
            <br />
            <span className="text-navy">to reflect, not aggregate.</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="text-xl text-gray-600 max-w-3xl mx-auto mb-8"
          >
            Episteme critiques Linear Regression against modern ML models,
            embedding Socratic learning prompts for deeper understanding.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="flex gap-4 justify-center"
          >
            <Link
              href="/demo"
              className="px-8 py-3 bg-navy text-white rounded-lg hover:bg-navy/90 transition-all hover:shadow-xl hover:-translate-y-1"
            >
              Try the Demo
            </Link>
            <Link
              href="/socratic"
              className="px-8 py-3 gold-gradient text-navy rounded-lg hover:shadow-xl hover:-translate-y-1 transition-all font-semibold"
            >
              Explore Prompts
            </Link>
          </motion.div>

          {/* Scroll Indicator */}
          <motion.div
            animate={{ y: [0, 10, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="absolute bottom-10 left-1/2 transform -translate-x-1/2"
          >
            <div className="w-6 h-10 border-2 border-navy rounded-full flex justify-center">
              <div className="w-1 h-3 bg-navy rounded-full mt-2" />
            </div>
          </motion.div>
        </div>
      </section>

      {/* Mission Statement */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="max-w-4xl mx-auto"
          >
            <div className="bg-white p-8 md:p-12 rounded-2xl shadow-xl border-l-8 border-gold">
              <AcademicCapIcon className="w-16 h-16 text-gold mb-6" />
              <p className="text-xl md:text-2xl text-navy leading-relaxed italic">
                "Linear regression is theoretically neat but limited in human systems. 
                Salary ≠ education alone; housing ≠ rooms alone. AI helps us review knowledge 
                instead of wasting time aggregating content."
              </p>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">Why Episteme?</h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: ChartBarIcon,
                title: 'Academic Critique',
                desc: 'Compare Linear Regression against Random Forest and XGBoost.',
                delay: 0,
              },
              {
                icon: ChatBubbleLeftRightIcon,
                title: 'Socratic Learning',
                desc: 'Reflect on guiding questions about social factors and model choices.',
                delay: 0.2,
              },
              {
                icon: AcademicCapIcon,
                title: 'Real Data',
                desc: 'Boston Housing, World Bank, and Kaggle datasets show real patterns.',
                delay: 0.4,
              },
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: feature.delay }}
                viewport={{ once: true }}
                whileHover={{ y: -10 }}
                className="bg-white p-8 rounded-xl shadow-lg hover:shadow-2xl transition-all"
              >
                <feature.icon className="w-12 h-12 text-gold mb-4" />
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Model Preview */}
      <section className="py-20 bg-navy text-white">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12 gold-text">
            Model Performance
          </h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { name: 'Linear Regression', r2: 0.72, color: 'from-blue-400 to-blue-600' },
              { name: 'Random Forest', r2: 0.85, color: 'from-gold to-gold-light' },
              { name: 'XGBoost', r2: 0.87, color: 'from-purple-400 to-purple-600' },
            ].map((model, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                whileHover={{ scale: 1.05 }}
                className="bg-white/10 backdrop-blur-lg rounded-xl p-8 text-center"
              >
                <h3 className="text-2xl font-semibold mb-4">{model.name}</h3>
                <motion.div
                  initial={{ width: 0 }}
                  whileInView={{ width: '100%' }}
                  transition={{ duration: 1, delay: 0.5 + index * 0.1 }}
                  className="h-32 flex items-end justify-center"
                >
                  <div
                    className={`w-20 bg-linear-to-t ${model.color} rounded-t-lg`}
                    style={{ height: `${model.r2 * 100}%` }}
                  />
                </motion.div>
                <p className="mt-4 text-2xl font-bold">R² = {model.r2}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
```

---

## 🚀 **Phase 7: Running the Application**

### **7.1 First Terminal - Backend

```bash
cd ~/Projects/episteme/backend
source venv/bin/activate

# Set Django settings module
export DJANGO_SETTINGS_MODULE=config.settings.development

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load initial data
python scripts/init_data.py

# Run development server
python manage.py runserver
```

### **7.2 Second Terminal - Frontend

```bash
cd ~/Projects/episteme/frontend

# Install dependencies (if not already)
npm install

# Run development server
npm run dev
```

### **7.3 Access Points

```merm
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **API Root**: http://localhost:8000/api/
```

---

## 📦 **Phase 8: Docker Setup (Optional)**

**backend/Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements/production.txt .
RUN pip install --no-cache-dir -r production.txt

# Copy application
COPY . .

# Run
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

**frontend/Dockerfile

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app

COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000
CMD ["node", "server.js"]
```

**docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: episteme
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.production
      - DB_HOST=db
      - DB_NAME=episteme
      - DB_USER=postgres
      - DB_PASSWORD=postgres
    depends_on:
      - db
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000/api
    depends_on:
      - backend

volumes:
  postgres_data:
```

---

## ✅ **Final Checklist**

- [ ] Python 3.10 installed from deadsnakes
- [ ] Virtual environment created and activated
- [ ] Django dependencies installed
- [ ] PostgreSQL installed and running
- [ ] Database created and configured
- [ ] Django project structure created
- [ ] Node.js 18+ installed
- [ ] Next.js app created
- [ ] Frontend dependencies installed
- [ ] Tailwind configured with custom theme
- [ ] API service layer implemented
- [ ] Zustand store created
- [ ] Layout components built
- [ ] Home page with animations
- [ ] Both servers running
- [ ] Connection working

---

## 🎯 **Commands Quick Reference**

```bash
# Backend
cd backend
source venv/bin/activate
python manage.py runserver

# Frontend
cd frontend
npm run dev

# Database
sudo -u postgres psql
\c episteme
\dt

# Git
git add .
git commit -m "message"
git push origin main
```

Your Episteme project is now ready for development! The backend is robust with Django + PostgreSQL, and the frontend is beautiful with Next.js + Tailwind + Framer Motion animations. Time to build those mind-blowing pages! 🚀✨
