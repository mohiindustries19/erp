# 🔧 Fix GitHub Authentication Issue

## Problem
Git is trying to push using the wrong GitHub account (`QuantalgoGitBackup` instead of `mohiindustries19`).

Error:
```
remote: Permission to mohiindustries19/erp.git denied to QuantalgoGitBackup.
fatal: unable to access 'https://github.com/mohiindustries19/erp.git/': The requested URL returned error: 403
```

---

## ✅ Solution 1: Use GitHub Personal Access Token (Recommended)

### Step 1: Create Personal Access Token
1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name: `Railway Deployment`
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
5. Click **"Generate token"**
6. **COPY THE TOKEN** (you won't see it again!)

### Step 2: Update Git Remote with Token
```powershell
cd d:\OtherRepos\mohierp\mohi-erp

# Remove old remote
git remote remove origin

# Add new remote with token
git remote add origin https://YOUR_TOKEN@github.com/mohiindustries19/erp.git

# Push
git push -u origin main
```

Replace `YOUR_TOKEN` with the token you copied.

---

## ✅ Solution 2: Use GitHub Desktop (Easiest)

### Step 1: Install GitHub Desktop
Download from: https://desktop.github.com/

### Step 2: Sign in with mohiindustries19 account
1. Open GitHub Desktop
2. File → Options → Accounts
3. Sign in with `mohiindustries19` account

### Step 3: Add Repository
1. File → Add Local Repository
2. Choose: `d:\OtherRepos\mohierp\mohi-erp`
3. Click "Add Repository"

### Step 4: Publish
1. Click "Publish repository"
2. Choose repository: `mohiindustries19/erp`
3. Click "Publish"

Done! ✅

---

## ✅ Solution 3: Use SSH Key (Advanced)

### Step 1: Generate SSH Key
```powershell
ssh-keygen -t ed25519 -C "info@mohiindustries.in"
```
Press Enter for all prompts (use default location).

### Step 2: Add SSH Key to GitHub
```powershell
# Copy public key
type ~\.ssh\id_ed25519.pub
```

1. Go to: https://github.com/settings/keys
2. Click **"New SSH key"**
3. Paste the key
4. Click **"Add SSH key"**

### Step 3: Update Git Remote
```powershell
cd d:\OtherRepos\mohierp\mohi-erp

# Remove old remote
git remote remove origin

# Add SSH remote
git remote add origin git@github.com:mohiindustries19/erp.git

# Push
git push -u origin main
```

---

## ✅ Solution 4: Clear Git Credentials (Quick Fix)

### Windows Credential Manager
```powershell
# Open Credential Manager
control /name Microsoft.CredentialManager

# Or use command line
cmdkey /list | findstr github
cmdkey /delete:git:https://github.com
```

Then try pushing again - Git will ask for credentials:
```powershell
git push -u origin main
```

Enter:
- Username: `mohiindustries19`
- Password: Your GitHub Personal Access Token (not your password!)

---

## 🎯 Recommended: Solution 1 (Personal Access Token)

This is the most reliable method for Railway deployment.

### Quick Steps:
1. Create token at: https://github.com/settings/tokens
2. Copy token
3. Run:
```powershell
cd d:\OtherRepos\mohierp\mohi-erp
git remote set-url origin https://YOUR_TOKEN@github.com/mohiindustries19/erp.git
git push -u origin main
```

---

## 🔒 Security Note

**Never commit your Personal Access Token to the repository!**

The token is only used in the git remote URL locally. Railway will connect to GitHub separately using OAuth.

---

## ✅ After Successful Push

Once pushed successfully, continue with Railway deployment:

1. Go to: https://railway.app
2. New Project → Deploy from GitHub
3. Select: `mohiindustries19/erp`
4. Add PostgreSQL
5. Set environment variables
6. Deploy! 🚀

---

## 📞 Need Help?

If you're still having issues:
1. Make sure you're logged into the correct GitHub account in your browser
2. Try GitHub Desktop (easiest solution)
3. Or use Personal Access Token method

**Your repository**: https://github.com/mohiindustries19/erp.git
