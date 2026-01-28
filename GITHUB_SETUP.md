# 🚀 GitHub Upload Guide

This guide will help you upload the PSL Data Science Project to GitHub.

## Prerequisites

- GitHub account (https://github.com)
- Git installed on your computer
- Your GitHub username: **Muhamma-Farooq-13**

## Step 1: Create a New Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `psl-project` (or any name you prefer)
3. Description: `Comprehensive Machine Learning Project for Pakistan Super League Dataset (2016-2024)`
4. Set to **Public** (for open-source)
5. **Do NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 2: Initialize Git Locally

Open PowerShell in the project directory and run:

```bash
# Navigate to project directory
cd e:\psl

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Complete MLOps project structure with comprehensive documentation, testing, and deployment support"

# Verify status
git status
```

## Step 3: Connect to GitHub

```bash
# Add remote repository (replace YOUR_REPO_URL with the URL from GitHub)
git remote add origin https://github.com/Muhamma-Farooq-13/psl-project.git

# Verify remote
git remote -v
```

## Step 4: Push to GitHub

```bash
# Push to main branch
git branch -M main
git push -u origin main

# This will prompt for authentication:
# - Username: Muhamma-Farooq-13
# - Password: Your GitHub personal access token (or password)
```

## Setting Up GitHub Authentication (Recommended)

### Using Personal Access Token (Recommended)

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Click "Generate new token"
3. Select scopes: `repo`, `workflow`
4. Copy the token
5. When prompted for password during `git push`, use the token

### Using SSH (Advanced)

```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "mfarooqshafee333@gmail.com"

# Add to ssh-agent
ssh-add ~/.ssh/id_ed25519

# Add public key to GitHub Settings → SSH and GPG keys
cat ~/.ssh/id_ed25519.pub

# Change remote URL to use SSH
git remote set-url origin git@github.com:Muhamma-Farooq-13/psl-project.git
```

## Step 5: Verify Upload

After pushing, verify on GitHub:
1. Visit https://github.com/Muhamma-Farooq-13/psl-project
2. You should see all your files and folders
3. Check that:
   - ✅ All source code is there
   - ✅ Documentation files are visible
   - ✅ .gitignore is working (large model files not showing)
   - ✅ README.md displays properly

## Step 6: Add Badges (Optional)

Edit README.md to add repository status badges:

```markdown
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Muhamma-Farooq-13/psl-project)](https://github.com/Muhamma-Farooq-13/psl-project/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/Muhamma-Farooq-13/psl-project)](https://github.com/Muhamma-Farooq-13/psl-project/issues)
```

## Step 7: Configure Repository Settings

On GitHub:

1. **Branch Protection** (Optional)
   - Settings → Branches → Add rule
   - Require pull request reviews before merging
   - Require status checks to pass

2. **Enable Issues** (Already enabled)
   - Settings → Features → Issues ✅

3. **Enable Discussions** (Optional)
   - Settings → Features → Discussions ✅

4. **Add Topics** (For discoverability)
   - Edit repository details
   - Add: `machine-learning`, `mlops`, `flask`, `docker`, `cricket`

## Regular Git Workflow

After initial upload, use these commands for updates:

```bash
# Check status
git status

# Stage changes
git add .

# Commit changes
git commit -m "Descriptive message about changes"

# Push to GitHub
git push origin main

# Pull latest changes (if working with others)
git pull origin main
```

## Common Commands

```bash
# View commit history
git log --oneline

# Check remote URL
git remote -v

# Create a new branch
git checkout -b feature/your-feature

# Switch branches
git checkout main

# Delete local branch
git branch -d feature/your-feature

# View all branches
git branch -a
```

## Troubleshooting

### "fatal: not a git repository"
```bash
# Make sure you're in the project directory
cd e:\psl
git init
```

### Authentication failed
```bash
# Use personal access token instead of password
# Or set up SSH key as described above
```

### Large files error
```bash
# Don't commit .pkl, .h5, or other model files
# They should be in .gitignore (already configured)
# Use git-lfs for large files if needed
```

### Want to remove a file from history
```bash
# Remove file from tracking (don't delete it)
git rm --cached filename

# Commit the change
git commit -m "Remove large file from tracking"
```

## Repository Structure on GitHub

Your GitHub repository will have:

```
psl-project/
├── README.md              # Main documentation
├── src/                   # Source code
├── tests/                 # Test suite
├── notebooks/             # Jupyter notebooks
├── data/                  # Data directory
├── models/                # (empty on GitHub, use .gitkeep)
├── requirements.txt       # Dependencies
├── Dockerfile             # Docker configuration
├── .github/               # GitHub workflows and templates
└── [other files]          # Configuration and documentation
```

## After Upload

### Next Steps:

1. **Add GitHub Actions** - Already configured in `.github/workflows/ci-cd.yml`
2. **Enable GitHub Pages** - For documentation hosting (optional)
3. **Add Collaborators** - Settings → Collaborators
4. **Set up Releases** - GitHub → Releases (when publishing versions)
5. **Add Project Board** - For tracking issues and features
6. **Configure Webhooks** - For CI/CD integration

## Sharing Your Project

Once uploaded:

1. **Share the link**: https://github.com/Muhamma-Farooq-13/psl-project
2. **Add to your portfolio**
3. **Share on social media**
4. **Link in your resume/CV**

## Privacy & Licensing

✅ **License**: MIT License (already included)
✅ **Code of Conduct**: Included
✅ **Security Policy**: Included
✅ **Contributing Guidelines**: Included

## Support Resources

- GitHub Help: https://help.github.com
- Git Documentation: https://git-scm.com/doc
- GitHub Guides: https://guides.github.com

---

## ✅ Quick Checklist

Before pushing to GitHub:

- [ ] All files are in `e:\psl` directory
- [ ] `git status` shows all files ready
- [ ] Created repository on GitHub
- [ ] Remote URL configured
- [ ] Authentication set up
- [ ] Initial commit ready
- [ ] Ready to push with `git push -u origin main`

---

**Your project is ready for GitHub upload!** 🎉

For any questions, refer to the Git/GitHub documentation or contact: mfarooqshafee333@gmail.com
