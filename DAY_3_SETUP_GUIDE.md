# DAY 3: LOCAL ENVIRONMENT SETUP & FIRST COMMIT

## ✅ DAY 3 CHECKLIST

This checklist will guide you through setting up the local development environment and making your first Git commit.

---

## PART 1: ENVIRONMENT CONFIGURATION

### Step 1: Create .env File
```bash
# Navigate to project root
cd "c:\Users\Krishna Bhardwaj\OneDrive\Desktop\Zetheta Int\Behavioural Portfolio optimizer"

# Copy template
copy .env.example .env

# Edit .env with your local values
# (Open in VS Code)
```

### Step 2: Configure .env Values

Edit `.env` and update these critical values:

```env
# Database (PostgreSQL via Docker)
DATABASE_URL=postgresql://zetheta_user:zetheta_password@localhost:5432/behavioral_portfolio
DATABASE_USER=zetheta_user
DATABASE_PASSWORD=zetheta_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=behavioral_portfolio

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_ENV=development
DEBUG=True

# Security (CHANGE in production!)
SECRET_KEY=dev-secret-key-change-in-production-12345-67890
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Redis Cache
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Keep other values as defaults for now
```

### Step 3: Verify .env Not Tracked

Verify `.gitignore` includes `.env`:
```bash
# Should show in .gitignore:
# .env
# .env.local
# .env.*.local
```

✅ **Do NOT commit .env file!**

---

## PART 2: DOCKER SETUP & TESTING

### Step 1: Start Docker Services

```bash
# From project root:
docker-compose up -d

# Should show:
# ✓ postgres (database)
# ✓ redis (cache)
# ✓ backend (FastAPI)
# ✓ ml_service (ML server)
# ✓ frontend (React)
# ✓ prometheus (monitoring)
# ✓ grafana (dashboards)
```

### Step 2: Check Services Status

```bash
# List running containers
docker-compose ps

# Expected output:
# NAME                    STATUS
# behavioral_portfolio_db RUNNING
# behavioral_portfolio_cache RUNNING
# behavioral_portfolio_api RUNNING
# behavioral_portfolio_ml RUNNING
# behavioral_portfolio_web RUNNING
# behavioral_portfolio_prometheus RUNNING
# behavioral_portfolio_grafana RUNNING
```

### Step 3: Initialize Database

```bash
# Open backend container shell
docker-compose exec backend bash

# Inside container, initialize database:
python -c "from database import init_db; init_db()"

# Should output:
# Database initialized successfully!

# Exit container
exit
```

### Step 4: Health Checks

Run these tests to verify everything works:

#### Test 1: API Health Check
```bash
curl http://localhost:8000/health

# Expected response:
# {
#   "status": "healthy",
#   "service": "Behavioral Portfolio Optimizer",
#   "version": "1.0.0",
#   "confidential": true
# }
```

#### Test 2: API Docs
```
Open in browser: http://localhost:8000/docs

Should show:
- Swagger UI with all endpoints
- /health GET
- /api/users/register POST
- /api/optimization/optimize POST
- /api/bias/analyze POST
- /api/bias/detect-trade-bias POST
- /api/portfolio/{portfolio_id} GET
```

#### Test 3: Frontend
```
Open in browser: http://localhost:3000

Should show:
- React app loading
- Might see placeholder or "Cannot connect to API" (expected for now)
```

#### Test 4: Prometheus Metrics
```
Open in browser: http://localhost:9090

Should show:
- Prometheus dashboard
- Status: "Up"
```

#### Test 5: Grafana Dashboards
```
Open in browser: http://localhost:3001

Should show:
- Grafana login page
- Default username: admin
- Default password: admin
```

#### Test 6: Database Connection
```bash
# Connect to PostgreSQL in Docker
docker-compose exec postgres psql -U zetheta_user -d behavioral_portfolio

# Inside psql:
\dt  # List tables

# Should show:
# user_profiles
# portfolios
# positions
# behavioral_events
# bias_scores
# recommendations
# backtest_results
# market_data
# sentiment_data

\q  # Exit psql
```

---

## PART 3: VERIFY CODE IMPORTS

Test that Python modules can be imported:

```bash
# From project root
docker-compose exec backend python

# In Python interpreter:
from database import UserProfile, Portfolio, Position
print("✓ Database models imported")

from behavioral_analyzer import BehavioralAnalyzer
print("✓ Behavioral analyzer imported")

from portfolio_optimizer import BehavioralPortfolioOptimizer
print("✓ Portfolio optimizer imported")

from main import app
print("✓ FastAPI app imported")

exit()  # Exit Python
```

---

## PART 4: GIT REPOSITORY SETUP

### Step 1: Initialize Git Repository

```bash
# From project root
git init

# Check status
git status

# Should show all untracked files
```

### Step 2: Create .gitignore (Already Done!)

Verify `.gitignore` is in place:
```bash
# Should already exist, verify with:
ls .gitignore

# Should include:
# - .env files
# - __pycache__/
# - node_modules/
# - .pytest_cache/
# - *.pyc
# - .vscode/
# - etc.
```

### Step 3: Create GitHub Private Repository

**CRITICAL: MUST BE PRIVATE!**

1. Go to https://github.com/new
2. Enter repository name: `zetheta-behavioral-portfolio-[yourname]`
3. **Select: PRIVATE** (NOT Public!)
4. Add README: No (we have one)
5. Add .gitignore: No (we have one)
6. Add license: None (Proprietary)
7. Click "Create repository"

### Step 4: Connect Local to GitHub

```bash
# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/zetheta-behavioral-portfolio-[yourname].git

# Verify remote added
git remote -v

# Should show:
# origin  https://github.com/YOUR_USERNAME/zetheta-behavioral-portfolio-[yourname].git (fetch)
# origin  https://github.com/YOUR_USERNAME/zetheta-behavioral-portfolio-[yourname].git (push)
```

### Step 5: Make First Commit

```bash
# Stage all files
git add .

# Verify what will be committed
git status

# Should NOT include:
# - .env
# - __pycache__/
# - node_modules/
# - .pytest_cache/

# Make first commit
git commit -m "Initial project setup - Behavioral Portfolio Optimizer (Day 1 completion)"

# Verify commit
git log --oneline
# Should show your commit
```

### Step 6: Push to GitHub

```bash
# Create main branch and push
git branch -M main
git push -u origin main

# Verify on GitHub
# Open: https://github.com/YOUR_USERNAME/zetheta-behavioral-portfolio-[yourname]
# Should show:
# - All project files
# - README.md
# - Last commit: "Initial project setup..."
```

### Step 7: Configure GitHub Security

**MUST DO THIS!**

1. Go to repository Settings
2. → Branches
3. → Add rule → "main"
   - Require pull request reviews: 1
   - Dismiss stale reviews: Yes
   - Require status checks: Yes (when available)
4. → General
   - Disable: Forking
   - Disable: Discussions
5. → Security & Analysis
   - Enable: Dependabot alerts
   - Enable: Secret scanning

---

## PART 5: DAILY VERIFICATION

Create a verification script to test everything:

```bash
# Create: verify_setup.sh (or .bat on Windows)

#!/bin/bash

echo "🔍 Verifying Behavioral Portfolio Optimizer Setup"
echo "=================================================="

# Check 1: Docker running
echo -n "1. Docker services... "
if docker-compose ps | grep -q "running"; then
    echo "✓"
else
    echo "✗ Docker services not running"
fi

# Check 2: API health
echo -n "2. API health check... "
if curl -s http://localhost:8000/health | grep -q "healthy"; then
    echo "✓"
else
    echo "✗ API not responding"
fi

# Check 3: Database
echo -n "3. Database connection... "
if docker-compose exec -T postgres pg_isready; then
    echo "✓"
else
    echo "✗ Database not responding"
fi

# Check 4: Python imports
echo -n "4. Python modules... "
if docker-compose exec -T backend python -c "from database import UserProfile; from behavioral_analyzer import BehavioralAnalyzer; from portfolio_optimizer import BehavioralPortfolioOptimizer" 2>/dev/null; then
    echo "✓"
else
    echo "✗ Python imports failed"
fi

# Check 5: Git status
echo -n "5. Git repository... "
if git log --oneline 2>/dev/null | head -1 | grep -q "Initial"; then
    echo "✓"
else
    echo "✗ Git repository not configured"
fi

echo "=================================================="
echo "✓ All checks complete!"
```

Run it with:
```bash
bash verify_setup.sh
```

---

## PART 6: TROUBLESHOOTING

### Problem: Docker services won't start
```bash
# Check Docker is running
docker ps

# If no output, start Docker Desktop

# Check logs
docker-compose logs backend

# Rebuild containers
docker-compose build --no-cache
docker-compose up -d
```

### Problem: API returns error
```bash
# Check backend logs
docker-compose logs backend

# Restart backend
docker-compose restart backend

# Reinitialize database
docker-compose exec backend python -c "from database import init_db; init_db()"
```

### Problem: Database connection refused
```bash
# Check PostgreSQL is running
docker-compose ps | grep postgres

# Check port 5432 is available
netstat -an | findstr :5432  # Windows
lsof -i :5432                 # Mac/Linux

# Restart database
docker-compose restart postgres
```

### Problem: Python imports fail
```bash
# Reinstall requirements
docker-compose exec backend pip install -r requirements.txt

# Check Python version
docker-compose exec backend python --version
# Should be 3.10+

# Test individual imports
docker-compose exec backend python -c "import fastapi; print(fastapi.__version__)"
```

### Problem: Can't push to GitHub
```bash
# Verify remote configured
git remote -v

# Check credentials
git config --global user.email "your-email@example.com"
git config --global user.name "Your Name"

# Retry push
git push -u origin main

# If 403 error: Check GitHub token in https URL settings
```

---

## PART 7: DAILY STARTUP PROCEDURE

Each day, follow this to start working:

```bash
# 1. Navigate to project
cd "c:\Users\Krishna Bhardwaj\OneDrive\Desktop\Zetheta Int\Behavioural Portfolio optimizer"

# 2. Start Docker
docker-compose up -d

# 3. Verify services
docker-compose ps

# 4. Quick health check
curl http://localhost:8000/health

# 5. Check Git status
git status

# 6. Create feature branch for the day
git checkout -b day-4-data-pipeline
# (adjust day number)

# 7. Start coding!
```

---

## PART 8: DAILY SHUTDOWN PROCEDURE

At end of day:

```bash
# 1. Commit your changes
git add .
git commit -m "Day 4: [What you accomplished]"

# 2. Push to GitHub
git push origin day-4-data-pipeline

# 3. Stop Docker services
docker-compose down

# 4. Verify stopped
docker-compose ps
# Should show nothing running
```

---

## FINAL CHECKLIST

### Day 3 Completion ✓

- [ ] .env file configured from .env.example
- [ ] .env file NOT committed to git
- [ ] Docker Compose started successfully
- [ ] All 7 services running
- [ ] API health check passes
- [ ] Database initialized
- [ ] Python imports work
- [ ] GitHub repository created (PRIVATE)
- [ ] First commit made
- [ ] Pushed to GitHub
- [ ] Branch protection rules configured
- [ ] Verification script works

### System Ready For Development

Once all above checked:
- ✅ Backend ready for Day 4-5 data pipeline
- ✅ Database ready for data storage
- ✅ API ready for endpoint implementation
- ✅ Version control configured
- ✅ Monitoring infrastructure in place

---

## NEXT: DAY 4-5 DATA PIPELINE

Once this is complete, you're ready to:
1. Create `data_collector.py`
2. Implement market data APIs
3. Set up sentiment analysis
4. Create async data pipeline

**You're on track! 🚀**

---

*CONFIDENTIAL - Property of Zetheta Algorithms Private Limited*
