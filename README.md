# Episteme - Academic Critique Engine

**AI frees students to reflect, not aggregate.**

Episteme is a web application that critiques Linear Regression against modern ML models (Random Forest, XGBoost) and embeds Socratic learning prompts. Built for academic adoption, it helps students understand the limitations of linear models in human systems.

Super user is lsetga and school admission number.

## 🎯 Mission

Linear regression is theoretically neat but limited in human systems. Salary ≠ education alone; housing ≠ rooms alone. AI helps us review knowledge instead of wasting time aggregating content.

## ✨ Features

- **Model Comparison**: Real-time comparison of Linear Regression vs Random Forest vs XGBoost
- **Interactive Demo**: Adjust housing features and see predictions from all models
- **Socratic Prompts**: Guiding questions for deeper reflection
- **Real Datasets**: Boston Housing, World Bank education vs income, Kaggle salary data
- **Academic Critique**: Educational commentary on model limitations and strengths

## 🚀 Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload


# 📋 **Session Summary: Episteme Development Journey**

## 🎯 **What We Accomplished**

### **1. The Python 3.12 + distutils Saga**
- **Issue**: Python 3.12 removed `distutils`, causing all ML libraries (numpy, scikit-learn, xgboost) to fail installation
- **Solution**: Added deadsnakes PPA repository to get Python 3.10
  ```bash
  sudo add-apt-repository ppa:deadsnakes/ppa
  sudo apt update
  sudo apt install python3.10 python3.10-venv python3.10-dev
  ```
  
- **Root Cause**: Only Python ≤3.11 has full compatibility with the current ML ecosystem
- **Lesson Learned**: Always check library compatibility before jumping to latest Python version

### **2. Framework Evolution**

- **Initial Attempt**: FastAPI with complex modular structure
  - ✅ Great for APIs
  - ❌ Required manual setup for everything (auth, admin, DB)
  - ❌ Package conflicts with Python 3.12
  
- **Final Choice**: Django REST Framework
  - ✅ Built-in admin panel (free CRUD!)
  - ✅ ORM with automatic migrations
  - ✅ Authentication & permissions out-of-the-box
  - ✅ Battle-tested security
  - ✅ Perfect for full-stack applications
  - ✅ Same amazing modular structure maintained

### **3. Backend Architecture (Maintained)**

```merm
backend/
├── apps/                    # Modular app structure preserved
│   ├── core/                # Middleware, exceptions, utils
│   ├── api/                 # Main API router
│   ├── datasets/            # Dataset management with ML-ready data
│   ├── models_app/          # LinearRegression, RF, XGBoost
│   └── socratic/            # Learning prompts & reflections
├── config/                  # Environment-specific settings
├── logs/                    # Structured logging
└── scripts/                 # Initialization & training scripts
```

### **4. Data & ML Pipeline**

- **Three Datasets**: Housing, Education vs Income, Salary (all with non-linear patterns)
- **Three Models**: Linear Regression (R²~0.72), Random Forest (R²~0.85), XGBoost (R²~0.87)
- **Auto-training**: Models train on first request or via management commands
- **Feature**: Model comparison with educational commentary

### **5. Socratic Learning System**

- **6 Initial Prompts** with guided reflections
- **Reflection storage** (anonymous sessions)
- **Random prompt** endpoint for variety
- Educational context for each ML concept

---

## 🚀 **Next Phase: Mind-Blowing Frontend + Backend Integration**

Now that the backend is rock-solid with Django, let's create a frontend that will make educators and students go "WOW!"

### **🎨 Visual Vision**

```typescript
// frontend/styles/theme.ts - Enhanced with animations
export const theme = {
  colors: {
    navy: '#0a1929',
    gold: '#ffb347',
    goldLight: '#ffd700',
    goldGradient: 'linear-gradient(135deg, #ffb347 0%, #ffd700 100%)',
    navyGradient: 'linear-gradient(135deg, #0a1929 0%, #1a2b3c 100%)',
  },
  animations: {
    float: 'float 6s ease-in-out infinite',
    pulse: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
    slideUp: 'slideUp 0.5s ease-out',
    fadeIn: 'fadeIn 0.8s ease-in',
    gradientShift: 'gradientShift 3s ease infinite',
  }
}
```

### **📱 Pages to Build**

#### **1. Landing Page (Already Started)**

- Animated gold particles in background
- Floating 3D model comparison visualization
- Typewriter effect for mission statement
- Interactive hero section with CTA

#### **2. Interactive Demo (PRIORITY)**

- **3D Sliders** for feature inputs (using Three.js)
- **Real-time Prediction** with model switching
- **Visual Comparison** of model predictions
- **Decision Tree Visualization** for Random Forest
- **Feature Importance Charts** with animations

#### **3. Model Metrics Dashboard**

- **Animated Charts** (Recharts + Framer Motion)
- **Radar Charts** comparing model performance
- **Confetti** when switching to better model
- **Interactive Tooltips** with educational notes
- **Model Comparison Cards** with flip animations

#### **4. Socratic Learning Hub**

- **Card Stack** of questions (swipeable)
- **Animated Thought Bubbles** for reflections
- **Progress Tracking** with gold particles
- **Discussion Board** with real-time updates
- **Mind Map Visualization** of concepts

#### **5. Dataset Explorer**

- **3D Data Visualization** (rotating scatter plots)
- **Correlation Heatmaps** with hover effects
- **Data Storytelling** with animated transitions
- **Feature Distribution** with particle effects

### **🔧 Integration Tasks**

#### **API Service (frontend/services/api.ts)**

```typescript
// Complete API integration with error handling
export const api = {
  // Datasets
  getDatasets: () => axios.get('/api/datasets/'),
  getDataset: (id) => axios.get(`/api/datasets/${id}/`),
  switchDataset: (id) => axios.post('/api/datasets/switch/', { dataset_id: id }),
  
  // Models
  predict: (features, model) => axios.post('/api/models/predict/', { features, model }),
  getMetrics: () => axios.get('/api/models/metrics/'),
  compareModels: () => axios.get('/api/models/compare/'),
  
  // Socratic
  getPrompts: () => axios.get('/api/socratic/prompts/'),
  getRandomPrompt: () => axios.get('/api/socratic/prompts/random/'),
  saveReflection: (promptId, content) => 
    axios.post(`/api/socratic/prompts/${promptId}/reflect/`, { content }),
}
```

#### **State Management**

```typescript
// Using Zustand for simplicity + performance
interface EpistemeState {
  currentDataset: string;
  selectedModel: string;
  predictions: Record<string, number>;
  metrics: Metrics;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  setDataset: (id: string) => void;
  setModel: (model: string) => void;
  predict: (features: Features) => Promise<void>;
  refreshMetrics: () => Promise<void>;
}
```

### **✨ Animation Libraries to Add**

```bash
cd frontend
npm install framer-motion three @react-three/fiber @react-three/drei
npm install react-intersection-observer react-parallax-tilt
npm install react-confetti react-type-animation
npm install recharts d3
```

### **🎯 Immediate Next Steps**

1. **Connect frontend to Django API**

   ```typescript
   // Test connection
   const { data } = await axios.get('http://localhost:8000/api/health/');
   ```

2. **Build the Demo page with:**
   - Real-time model switching
   - Animated feature sliders
   - Live prediction updates
   - Visual model comparison

3. **Add educational tooltips** explaining:
   - Why Random Forest beats Linear Regression
   - What R² actually means
   - How XGBoost works (visualized)

4. **Create the Metrics Dashboard** with:
   - Animated number counters
   - Beautiful chart transitions
   - Model performance stories

### **🌟 Bonus Features for "WOW" Factor**

- **Dark/Light mode** toggle with gold accents
- **Share predictions** as beautiful cards
- **Export reflections** as PDF learning journals
- **Voice input** for Socratic reflections
- **AR visualization** of decision trees (web AR)

## 📊 **Timeline Estimate**

| Phase | Features | Time |

| 1 | API Integration + Demo Page | 2-3 hours |
| 2 | Metrics Dashboard + Charts | 2-3 hours |
| 3 | Socratic Hub + Reflections | 2 hours |
| 4 | Dataset Explorer + 3D Viz | 3-4 hours |
| 5 | Polish + Animations | 2 hours |

*Total: ~11-14 hours to mind-blowing completion

---

## 💡 **Key Takeaways**

1. **Python version matters** - ML ecosystem lags behind latest Python
2. **Django > FastAPI for full-stack** when you need admin, auth, and ORM
3. **Modular structure** works beautifully in both frameworks
4. **Educational mission** is preserved: "AI frees students to reflect, not aggregate"
5. **The gold/navy palette** will pop with proper animations

Ready to build the most beautiful educational ML app ever? 🚀✨
