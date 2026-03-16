# REpo madness

You've identified a real issue. Having separate git repos for frontend and backend is actually **not ideal** for a project like Episteme. Here's the best approach:

## ✅ Recommended: Monorepo Structure

Keep everything in **one root repository** with separate folders:

```merm
episteme/
├── .git/                 # Single git repo at root
├── .gitignore
├── README.md
├── backend/
│   ├── venv/
│   ├── src/
│   ├── requirements.txt
│   └── .gitignore        # Backend-specific ignores
├── frontend/
│   ├── node_modules/
│   ├── app/
│   ├── package.json
│   └── .gitignore        # Frontend-specific ignores
└── docker-compose.yml    # Optional: orchestrate both
```

### 🔧 Fix Your Current Situation

1. **Remove the frontend git repo:**

```bash
cd ~/Projects/episteme/frontend
rm -rf .git
```

2.**Verify root is the only repo:**

```bash
cd ~/Projects/episteme
git status  # Should show files from both frontend and backend
```

3.**Update root .gitignore** to exclude node_modules and venv:

```bash
# episteme/.gitignore
backend/venv/
backend/__pycache__/
backend/*.egg-info/
backend/.env

frontend/node_modules/
frontend/.next/
frontend/out/
frontend/dist/

.DS_Store
*.log
.env.local
```

4.**Commit the structure:**

```bash
cd ~/Projects/episteme
git add .
git commit -m "feat: monorepo structure with backend and frontend"
```

### 📋 Why This Is Better

| Aspect | Monorepo | Separate Repos |
| **Atomic commits** | Both frontend + backend changes in one commit | Hard to sync versions |
| **CI/CD** | Single workflow tests both | Need two workflows |
| **Deployment** | Deploy together reliably | Risk of version mismatch |
| **Documentation** | One README covers everything | Scattered docs |
| **Onboarding** | Clone once, run both | Clone twice, setup twice |

### 🚀 Optional: Docker Compose for Local Dev

Create `episteme/docker-compose.yml` to run both services together:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
    volumes:
      - ./backend:/app

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    volumes:
      - ./frontend:/app
    depends_on:
      - backend
```

Then just run: `docker-compose up`
