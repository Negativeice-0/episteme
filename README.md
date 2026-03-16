# Episteme - Academic Critique Engine

**AI frees students to reflect, not aggregate.**

Episteme is a web application that critiques Linear Regression against modern ML models (Random Forest, XGBoost) and embeds Socratic learning prompts. Built for academic adoption, it helps students understand the limitations of linear models in human systems.

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
