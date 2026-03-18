# 🚀 **Complete Production Deployment Guide for Episteme**

## 📦 **Part 1: Virtual Environment Setup & Backend Configuration**

### **Step 1: Python Virtual Environment Setup**

```bash
# Navigate to project root
cd episteme

# Create virtual environment in backend directory
python -m venv backend/venv

# Activate virtual environment (Windows)
backend\venv\Scripts\activate

# Activate virtual environment (Mac/Linux)
source backend/venv/bin/activate

# Verify activation (should show path with venv)
which python
# or on Windows: where python

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
cd backend
pip install -r requirements.txt

# Verify installations
pip list
```

### **Step 2: Fixed Logo SVG (React Compatible)**

The SVG had issues with React compatibility. Here's the fixed version:

```tsx
// frontend/src/components/Logo.tsx
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

## 🎨 **Part 2: Enhanced Visual Design (Gold/Yellow Focus)**

### **Updated Theme with Gold Emphasis**

```tsx
// frontend/src/styles/theme.ts
import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  palette: {
    primary: {
      main: '#0a1929', // Navy
      light: '#1a2b3c',
      dark: '#051020',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#ffb347', // Warm Gold
      light: '#ffc97c',
      dark: '#e69100',
      contrastText: '#0a1929',
    },
    accent: {
      gold: '#ffd700', // Bright Gold
      amber: '#ffc107',
      honey: '#fbbf24',
    },
    background: {
      default: '#ffffff',
      paper: '#f8fafc',
      goldLight: '#fff9e6',
    },
    text: {
      primary: '#0a1929',
      secondary: '#4a5568',
      gold: '#b8860b',
    },
  },
  typography: {
    fontFamily: '"Inter", "Lato", "Helvetica", "Arial", sans-serif',
    h1: {
      fontFamily: '"Lato", sans-serif',
      fontWeight: 700,
      letterSpacing: '-0.02em',
    },
    h2: {
      fontFamily: '"Lato", sans-serif',
      fontWeight: 600,
    },
    button: {
      fontWeight: 600,
      textTransform: 'none',
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          padding: '10px 24px',
          transition: 'all 0.3s ease',
        },
        containedSecondary: {
          background: 'linear-gradient(45deg, #ffb347 30%, #ffd700 90%)',
          color: '#0a1929',
          '&:hover': {
            background: 'linear-gradient(45deg, #ffd700 30%, #ffb347 90%)',
            transform: 'translateY(-2px)',
            boxShadow: '0 8px 16px rgba(255, 180, 71, 0.3)',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          border: '1px solid #e2e8f0',
          transition: 'all 0.3s ease',
          '&:hover': {
            borderColor: '#ffb347',
            boxShadow: '0 12px 24px -8px rgba(255, 180, 71, 0.15)',
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 6,
        },
        colorSecondary: {
          background: 'linear-gradient(135deg, #ffb347 0%, #ffd700 100%)',
          color: '#0a1929',
          fontWeight: 600,
        },
      },
    },
  },
});

// Add custom CSS variables for gold gradients
export const goldGradients = {
  primary: 'linear-gradient(135deg, #ffb347 0%, #ffd700 100%)',
  hover: 'linear-gradient(135deg, #ffd700 0%, #ffb347 100%)',
  subtle: 'linear-gradient(135deg, #fff9e6 0%, #fff3d6 100%)',
  glow: '0 0 20px rgba(255, 180, 71, 0.3)',
};
```

### **Enhanced Home Page with Gold Accents**

```tsx
// frontend/src/pages/Home.tsx (enhanced version)
import React from 'react';
import {
  Box,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  Container,
  Chip,
  useTheme,
} from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import AutoGraphIcon from '@mui/icons-material/AutoGraph';
import PsychologyIcon from '@mui/icons-material/Psychology';
import CompareArrowsIcon from '@mui/icons-material/CompareArrows';
import SchoolIcon from '@mui/icons-material/School';
import EmojiObjectsIcon from '@mui/icons-material/EmojiObjects';
import { goldGradients } from '../styles/theme';

const Home: React.FC = () => {
  const theme = useTheme();

  return (
    <Box>
      {/* Hero Section with Gold Gradient */}
      <Box
        sx={{
          textAlign: 'center',
          py: { xs: 4, md: 8 },
          px: 2,
          background: 'radial-gradient(circle at top right, #fff9e6 0%, #ffffff 100%)',
          borderRadius: '0 0 60px 60px',
          position: 'relative',
          overflow: 'hidden',
          '&::before': {
            content: '""',
            position: 'absolute',
            top: -100,
            right: -100,
            width: 300,
            height: 300,
            background: goldGradients.primary,
            opacity: 0.1,
            borderRadius: '50%',
          },
        }}
      >
        <Chip
          icon={<SchoolIcon />}
          label="Academic Critique Engine"
          color="secondary"
          sx={{ mb: 3, px: 2, py: 1, fontSize: '1rem' }}
        />
        
        <Typography
          variant="h1"
          sx={{
            fontSize: { xs: '2.5rem', md: '4rem' },
            fontWeight: 800,
            mb: 2,
            background: goldGradients.primary,
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
          }}
        >
          AI frees students to reflect,
          <br />
          <span style={{ color: '#0a1929', WebkitTextFillColor: '#0a1929' }}>
            not aggregate.
          </span>
        </Typography>
        
        <Typography
          variant="h5"
          sx={{
            color: '#4b5563',
            maxWidth: '800px',
            mx: 'auto',
            mb: 4,
            fontWeight: 400,
          }}
        >
          Episteme critiques Linear Regression against modern ML models,
          embedding Socratic learning prompts for deeper understanding.
        </Typography>

        <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
          <Button
            component={RouterLink}
            to="/demo"
            variant="contained"
            size="large"
            sx={{
              bgcolor: '#0a1929',
              '&:hover': { 
                bgcolor: '#0f2a44',
                boxShadow: goldGradients.glow,
              },
              px: 4,
              py: 1.5,
            }}
          >
            Try the Demo
          </Button>
          <Button
            component={RouterLink}
            to="/socratic"
            variant="contained"
            color="secondary"
            size="large"
            sx={{
              px: 4,
              py: 1.5,
            }}
          >
            Explore Prompts
          </Button>
        </Box>

        {/* Animated Gold Bar */}
        <Box
          sx={{
            width: '100px',
            height: '4px',
            background: goldGradients.primary,
            mx: 'auto',
            mt: 6,
            borderRadius: '2px',
            animation: 'pulse 2s infinite',
            '@keyframes pulse': {
              '0%': { width: '100px', opacity: 1 },
              '50%': { width: '200px', opacity: 0.7 },
              '100%': { width: '100px', opacity: 1 },
            },
          }}
        />
      </Box>

      {/* Mission Statement with Gold Border */}
      <Container maxWidth="md" sx={{ my: 8 }}>
        <Card 
          sx={{ 
            bgcolor: '#f8f9fa', 
            p: 4,
            borderLeft: '6px solid',
            borderImage: goldGradients.primary,
            borderImageSlice: 1,
          }}
        >
          <Typography 
            variant="body1" 
            sx={{ 
              fontSize: '1.2rem', 
              fontStyle: 'italic',
              color: '#0a1929',
              display: 'flex',
              alignItems: 'center',
              gap: 2,
            }}
          >
            <EmojiObjectsIcon sx={{ color: '#ffb347', fontSize: 40 }} />
            "Linear regression is theoretically neat but limited in human systems. 
            Salary ≠ education alone; housing ≠ rooms alone. AI helps us review knowledge 
            instead of wasting time aggregating content."
          </Typography>
        </Card>
      </Container>

      {/* Features Grid with Gold Hover Effects */}
      <Container maxWidth="lg" sx={{ my: 8 }}>
        <Typography 
          variant="h2" 
          align="center" 
          gutterBottom
          sx={{
            background: goldGradients.primary,
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            mb: 4,
          }}
        >
          Why Episteme?
        </Typography>
        
        <Grid container spacing={4}>
          {[
            {
              icon: <AutoGraphIcon sx={{ fontSize: 40 }} />,
              title: 'Academic Critique',
              desc: 'Compare Linear Regression against Random Forest and XGBoost.',
              gradient: 'linear-gradient(135deg, #ffb34720 0%, #ffd70020 100%)',
            },
            {
              icon: <PsychologyIcon sx={{ fontSize: 40 }} />,
              title: 'Socratic Learning',
              desc: 'Reflect on guiding questions about social factors and model choices.',
              gradient: 'linear-gradient(135deg, #ffd70020 0%, #ffb34720 100%)',
            },
            {
              icon: <CompareArrowsIcon sx={{ fontSize: 40 }} />,
              title: 'Real Data',
              desc: 'Boston Housing, World Bank, and Kaggle datasets show real patterns.',
              gradient: 'linear-gradient(135deg, #ffb34720 0%, #ffd70020 100%)',
            },
          ].map((feature, index) => (
            <Grid item xs={12} md={4} key={index}>
              <Card 
                sx={{ 
                  height: '100%',
                  position: 'relative',
                  overflow: 'hidden',
                  '&::after': {
                    content: '""',
                    position: 'absolute',
                    bottom: 0,
                    left: 0,
                    right: 0,
                    height: '4px',
                    background: goldGradients.primary,
                    transform: 'scaleX(0)',
                    transition: 'transform 0.3s ease',
                  },
                  '&:hover::after': {
                    transform: 'scaleX(1)',
                  },
                }}
              >
                <CardContent>
                  <Box
                    sx={{
                      width: 60,
                      height: 60,
                      borderRadius: '12px',
                      background: feature.gradient,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      mb: 2,
                      color: '#ffb347',
                    }}
                  >
                    {feature.icon}
                  </Box>
                  <Typography variant="h5" gutterBottom>
                    {feature.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {feature.desc}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
};

export default Home;
```

## 🔧 **Part 3: Production-Ready Error Logging System**

### **Backend Logging Configuration**

```python
# backend/src/utils/logger.py
import logging
import logging.handlers
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
import traceback

# Create logs directory if it doesn't exist
LOG_DIR = Path(__file__).parent.parent.parent / 'logs'
ERROR_LOG_DIR = LOG_DIR / 'error'
ACCESS_LOG_DIR = LOG_DIR / 'access'
MODEL_LOG_DIR = LOG_DIR / 'model'

for dir_path in [LOG_DIR, ERROR_LOG_DIR, ACCESS_LOG_DIR, MODEL_LOG_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'message': record.getMessage(),
        }
        
        if hasattr(record, 'request_id'):
            log_obj['request_id'] = record.request_id
            
        if record.exc_info:
            log_obj['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': traceback.format_exception(*record.exc_info)
            }
            
        if hasattr(record, 'extra_data'):
            log_obj['extra'] = record.extra_data
            
        return json.dumps(log_obj)

def setup_logging(app_name: str = "episteme"):
    """Configure logging for the application"""
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Error logger
    error_handler = logging.handlers.RotatingFileHandler(
        ERROR_LOG_DIR / f'{app_name}_error.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(JSONFormatter())
    
    # Access logger
    access_handler = logging.handlers.RotatingFileHandler(
        ACCESS_LOG_DIR / f'{app_name}_access.log',
        maxBytes=10485760,
        backupCount=5
    )
    access_handler.setLevel(logging.INFO)
    access_handler.setFormatter(JSONFormatter())
    
    # Model logger
    model_handler = logging.handlers.RotatingFileHandler(
        MODEL_LOG_DIR / f'{app_name}_model.log',
        maxBytes=10485760,
        backupCount=5
    )
    model_handler.setLevel(logging.INFO)
    model_handler.setFormatter(JSONFormatter())
    
    # Console handler for development
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if os.getenv('ENV') == 'development' else logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    
    root_logger.addHandler(error_handler)
    root_logger.addHandler(access_handler)
    root_logger.addHandler(model_handler)
    root_logger.addHandler(console_handler)
    
    return root_logger

# Create logger instance
logger = setup_logging()

class LoggerMixin:
    """Mixin to add logging capabilities to classes"""
    
    @property
    def logger(self):
        name = '.'.join([self.__class__.__module__, self.__class__.__name__])
        return logging.getLogger(name)
```

### **Error Tracking Middleware**

```python
# backend/src/api/middleware/error_tracking.py
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import time
import uuid
from typing import Callable
from ...utils.logger import logger
import functools

async def error_tracking_middleware(request: Request, call_next: Callable):
    """Middleware to track errors and request performance"""
    
    # Generate request ID
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    # Add request ID to logger
    old_factory = logging.getLogRecordFactory()
    
    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.request_id = request_id
        return record
    
    logging.setLogRecordFactory(record_factory)
    
    # Track request timing
    start_time = time.time()
    
    try:
        response = await call_next(request)
        
        # Log successful request
        process_time = time.time() - start_time
        logger.info(
            f"Request completed",
            extra={
                'request_id': request_id,
                'method': request.method,
                'path': request.url.path,
                'status_code': response.status_code,
                'process_time': process_time
            }
        )
        
        response.headers['X-Request-ID'] = request_id
        return response
        
    except Exception as e:
        # Log error
        process_time = time.time() - start_time
        logger.error(
            f"Request failed: {str(e)}",
            exc_info=True,
            extra={
                'request_id': request_id,
                'method': request.method,
                'path': request.url.path,
                'process_time': process_time,
                'error_type': type(e).__name__
            }
        )
        
        # Return error response
        return JSONResponse(
            status_code=500,
            content={
                'error': 'Internal server error',
                'request_id': request_id,
                'message': str(e) if os.getenv('ENV') == 'development' else 'An error occurred'
            }
        )
```

## 📋 **Part 4: Comprehensive Feature Checklist with Verification**

### **Feature Verification Script**

```python
# backend/scripts/verify_features.py
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
```

## 🚢 **Part 5: CI/CD Pipeline Configuration**

### **GitHub Actions Workflow**

```yaml
# .github/workflows/deploy.yml
name: Deploy Episteme to Production

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

env:
  PYTHON_VERSION: '3.11'
  NODE_VERSION: '18'

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          
      - name: Cache Python dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('backend/requirements/*.txt') }}
          
      - name: Install dependencies
        run: |
          cd backend
          python -m pip install --upgrade pip
          pip install -r requirements/base.txt
          pip install -r requirements/test.txt
          
      - name: Run backend tests
        run: |
          cd backend
          pytest tests/ -v --cov=src --cov-report=xml
          
      - name: Run security scan
        run: |
          cd backend
          pip install bandit
          bandit -r src/ -f json -o bandit-report.json
          
      - name: Upload test coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml
          flags: backend

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          
      - name: Cache Node modules
        uses: actions/cache@v3
        with:
          path: ~/.npm
          key: ${{ runner.os }}-node-${{ hashFiles('frontend/package-lock.json') }}
          
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
          
      - name: Run linting
        run: |
          cd frontend
          npm run lint
          
      - name: Run type check
        run: |
          cd frontend
          npm run type-check
          
      - name: Run tests
        run: |
          cd frontend
          npm test -- --coverage
          
      - name: Build frontend
        run: |
          cd frontend
          npm run build
          
      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: frontend-build
          path: frontend/dist

  security-scan:
    runs-on: ubuntu-latest
    needs: [test-backend, test-frontend]
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
          
      - name: Upload Trivy results to GitHub Security tab
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
          
      - name: Run Dependency Check
        run: |
          cd backend
          pip install safety
          safety check -r requirements/base.txt --json > safety-report.json

  deploy-backend:
    runs-on: ubuntu-latest
    needs: [test-backend, security-scan]
    if: github.ref == 'refs/heads/main'
    environment: production
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
          
      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
        
      - name: Build, tag, and push image to Amazon ECR
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: episteme-backend
          IMAGE_TAG: ${{ github.sha }}
        run: |
          cd backend
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          
      - name: Deploy to ECS
        run: |
          aws ecs update-service --cluster episteme-cluster --service episteme-backend --force-new-deployment

  deploy-frontend:
    runs-on: ubuntu-latest
    needs: [test-frontend, security-scan]
    if: github.ref == 'refs/heads/main'
    environment: production
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Download build artifacts
        uses: actions/download-artifact@v3
        with:
          name: frontend-build
          path: frontend/dist
          
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
          vercel-args: '--prod'
```

## 🔒 **Part 6: Security Hardening**

### **Security Middleware**

```python
# backend/src/api/middleware/security.py
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
import hashlib
import hmac
import time
from typing import Optional
import jwt
from ...core.config import settings

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

class SecurityMiddleware:
    """Security enhancements middleware"""
    
    def __init__(self, app):
        self.app = app
        
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
            
        request = Request(scope, receive)
        
        # Add security headers
        headers = [
            (b"content-type", b"application/json"),
            (b"x-content-type-options", b"nosniff"),
            (b"x-frame-options", b"DENY"),
            (b"x-xss-protection", b"1; mode=block"),
            (b"strict-transport-security", b"max-age=31536000; includeSubDomains"),
            (b"referrer-policy", b"strict-origin-when-cross-origin"),
        ]
        
        # Add CORS headers if needed
        origin = request.headers.get("origin")
        if origin and origin in settings.ALLOWED_ORIGINS:
            headers.append((b"access-control-allow-origin", origin.encode()))
            
        # Continue with request
        await self.app(scope, receive, send)

# API Key authentication
class APIKeyAuth(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        
        if not credentials:
            raise HTTPException(status_code=403, detail="Invalid authorization")
            
        if credentials.scheme != "Bearer":
            raise HTTPException(status_code=403, detail="Invalid authentication scheme")
            
        if not self.verify_api_key(credentials.credentials):
            raise HTTPException(status_code=403, detail="Invalid API key")
            
        return credentials
        
    def verify_api_key(self, api_key: str) -> bool:
        # Verify API key against stored keys
        return api_key in settings.API_KEYS

# Request signing
def sign_request(payload: dict, secret: str) -> str:
    """Sign request payload for integrity"""
    message = json.dumps(payload, sort_keys=True).encode()
    signature = hmac.new(
        secret.encode(),
        message,
        hashlib.sha256
    ).hexdigest()
    return signature

def verify_signature(payload: dict, signature: str, secret: str) -> bool:
    """Verify request signature"""
    expected = sign_request(payload, secret)
    return hmac.compare_digest(signature, expected)

# Input sanitization
def sanitize_input(data: any) -> any:
    """Sanitize input to prevent injection"""
    if isinstance(data, str):
        # Remove any potentially dangerous characters
        dangerous = ['<', '>', '&', '"', "'", ';', '`', '$', '{', '}']
        for char in dangerous:
            data = data.replace(char, f"&#{ord(char)};")
        return data
    elif isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_input(item) for item in data]
    else:
        return data
```

## 📦 **Part 7: Docker Configuration**

### **Backend Dockerfile**

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements/prod.txt requirements.txt

# Install dependencies
RUN pip install --user --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY src/ ./src/
COPY scripts/ ./scripts/

# Create non-root user
RUN useradd -m -u 1000 episteme && \
    chown -R episteme:episteme /app

USER episteme

# Update PATH
ENV PATH=/root/.local/bin:$PATH

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Run application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Docker Compose for Local Development**

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: 
      context: ./backend
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    environment:
      - ENV=development
      - DATABASE_URL=postgresql://postgres:password@db:5432/episteme
      - REDIS_URL=redis://redis:6379
    volumes:
      - ./backend:/app
      - /app/__pycache__
      - ./logs:/app/logs
    depends_on:
      - db
      - redis
    networks:
      - episteme-network

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    ports:
      - "5173:5173"
    environment:
      - VITE_API_URL=http://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules
    depends_on:
      - backend
    networks:
      - episteme-network

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=episteme
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - episteme-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - episteme-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend
    networks:
      - episteme-network

volumes:
  postgres_data:
  redis_data:

networks:
  episteme-network:
    driver: bridge
```

## 🌐 **Part 8: Production Hosting Guide**

### **Option A: AWS ECS with Fargate**

```bash
# 1. Create ECR repositories
aws ecr create-repository --repository-name episteme-backend
aws ecr create-repository --repository-name episteme-frontend

# 2. Build and push images
docker build -t episteme-backend ./backend
docker tag episteme-backend:latest $AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/episteme-backend:latest
docker push $AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/episteme-backend:latest

# 3. Create ECS cluster
aws ecs create-cluster --cluster-name episteme-cluster

# 4. Register task definitions
aws ecs register-task-definition --cli-input-json file://task-definitions/backend.json
aws ecs register-task-definition --cli-input-json file://task-definitions/frontend.json

# 5. Create services
aws ecs create-service --cluster episteme-cluster --service-name episteme-backend --task-definition episteme-backend --desired-count 2 --launch-type FARGATE
aws ecs create-service --cluster episteme-cluster --service-name episteme-frontend --task-definition episteme-frontend --desired-count 2 --launch-type FARGATE

# 6. Set up Application Load Balancer
aws elbv2 create-load-balancer --name episteme-alb --subnets subnet-abc123 subnet-def456 --security-groups sg-789xyz

# 7. Configure auto-scaling
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --scalable-dimension ecs:service:DesiredCount \
  --resource-id service/episteme-cluster/episteme-backend \
  --min-capacity 2 \
  --max-capacity 10
```

### **Option B: Render.com (Simpler)**

```yaml
# render.yaml (updated with enhanced configuration)
services:
  - type: web
    name: episteme-backend
    runtime: python
    repo: https://github.com/yourusername/episteme
    plan: starter
    region: oregon
    buildCommand: |
      cd backend
      pip install -r requirements/prod.txt
    startCommand: |
      cd backend
      uvicorn src.main:app --host 0.0.0.0 --port $PORT --workers 4
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
      - key: ALLOWED_ORIGINS
        value: https://episteme-frontend.onrender.com,https://episteme.app
    healthCheckPath: /health
    autoDeploy: true
    disk:
      name: episteme-data
      mountPath: /app/logs
      sizeGB: 10

  - type: web
    name: episteme-frontend
    runtime: static
    repo: https://github.com/yourusername/episteme
    plan: starter
    region: oregon
    buildCommand: |
      cd frontend
      npm ci
      npm run build
    staticPublishPath: ./frontend/dist
    envVars:
      - key: VITE_API_URL
        value: https://episteme-backend.onrender.com
    headers:
      - path: /*
        name: X-Frame-Options
        value: DENY
      - path: /*
        name: X-Content-Type-Options
        value: nosniff
      - path: /*
        name: Strict-Transport-Security
        value: max-age=31536000; includeSubDomains

  - type: redis
    name: episteme-redis
    plan: free
    region: oregon
    maxmemoryPolicy: allkeys-lru
```

## ✅ **Quick Start Checklist**

### **Initial Setup**

- [ ] Clone repository: `git clone https://github.com/yourusername/episteme.git`
- [ ] Create Python venv: `python -m venv backend/venv`
- [ ] Activate venv: `source backend/venv/bin/activate` (Mac/Linux) or `backend\venv\Scripts\activate` (Windows)
- [ ] Install backend deps: `cd backend && pip install -r requirements/dev.txt`
- [ ] Install frontend deps: `cd frontend && npm install`

### **Development**

- [ ] Start backend: `cd backend && uvicorn src.main:app --reload`
- [ ] Start frontend: `cd frontend && npm run dev`
- [ ] Run verification: `python backend/scripts/verify_features.py`
- [ ] Check logs: `tail -f backend/logs/error/*.log`

### **Production Deployment**

- [ ] Set environment variables in `.env.production`
- [ ] Run security scan: `bandit -r backend/src/`
- [ ] Build frontend: `cd frontend && npm run build`
- [ ] Deploy using Render CLI: `render deploy`
- [ ] Verify deployment: `curl https://your-app.com/health`

## 🎯 **Key Improvements Made**

1. **Virtual Environment**: Proper Python venv setup in backend/
2. **Fixed SVG**: React-compatible logo component
3. **Enhanced Visuals**: Gold-focused design with gradients and animations
4. **Error Logging**: Comprehensive logging system with rotation
5. **CI/CD Ready**: GitHub Actions workflow with testing and security scanning
6. **Security**: Rate limiting, API keys, request signing, input sanitization
7. **Docker**: Multi-stage builds for production optimization
8. **Scalability**: Auto-scaling configuration for AWS
9. **Monitoring**: Health checks and logging infrastructure
10. **Verification**: Automated feature testing script

This setup provides a production-ready, secure, and scalable deployment for Episteme with comprehensive error tracking and monitoring capabilities.
