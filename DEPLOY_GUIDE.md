# Discord Auto-Joiner - Deployment Guide

## Step 1: Push Code to GitHub

### Using Replit (Easiest):
1. Click the **Git** icon in the left sidebar
2. Click **"Create a Git repository"**
3. Click **"Connect to GitHub"** and authorize
4. Create/select a repository
5. Click **"Commit & Push"**

### Using Terminal:
```bash
git init
git add .
git commit -m "Discord Auto-Joiner bot"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

## Step 2: Deploy from GitHub

### Option 1: Railway.app (Recommended - Has Free Tier)
1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variable: `TOKEN` = your Discord token
6. Railway will auto-detect Python and deploy

### Option 2: Render.com (Free Tier Available)
1. Go to https://render.com
2. Create new "Background Worker"
3. Connect your GitHub repository
4. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
5. Add environment variable: `TOKEN`
6. Deploy

### Option 3: Replit Deployment (Paid)
1. Click "Deploy" button in Replit
2. Choose "Reserved VM"
3. Deploy directly (no GitHub needed)

### Option 4: Self-Hosted VPS
1. Rent a server (DigitalOcean, AWS, etc.)
2. Clone repo: `git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git`
3. Install Python 3.10+
4. Install dependencies: `pip install -r requirements.txt`
5. Set TOKEN environment variable
6. Run: `python main.py`
7. Use screen/tmux to keep running: `screen -S bot python main.py`

## Important Notes
- **Never commit your TOKEN** to GitHub (it's private!)
- Add TOKEN as environment variable on deployment platform
- The bot needs continuous uptime to stay in voice channel
- Free tiers may have limited uptime (Railway gives 500 hours/month free)

## Files in Your Repository
- `main.py` - Main bot code
- `keep_alive.py` - Flask server for uptime
- `requirements.txt` - Python dependencies
- `pyproject.toml` / `poetry.lock` - Package management
