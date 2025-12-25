# Environment Variables Configuration Guide

## 🎯 Quick Start Checklist

Before deploying to Vercel, complete these steps in order:

- [ ] **Step 1**: Create Neon Database (5 minutes)
- [ ] **Step 2**: Generate Secret Key (1 minute)
- [ ] **Step 3**: Add Variables to Vercel (3 minutes)
- [ ] **Step 4**: Redeploy Application (2 minutes)

**Total Time**: ~10 minutes

---

## 📋 Step-by-Step Guide

### Step 1: Create Neon Database (PostgreSQL)

**Why**: Your app needs a database to store tasks and users in production.

**Instructions**:

1. **Go to Neon Console**
   - Visit: [https://console.neon.tech](https://console.neon.tech)
   - Click **"Sign Up"** or **"Login"**
   - Use GitHub/Google for quick signup (free tier available)

2. **Create New Project**
   - Click **"Create Project"** button
   - **Project Name**: `todo-evolution` (or any name)
   - **Region**: Choose closest to you (e.g., US East, Europe West)
   - **PostgreSQL Version**: Keep default (latest)
   - Click **"Create Project"**

3. **Get Connection String**
   - After creation, you'll see **"Connection Details"** panel
   - Look for a dropdown/selector that says **"Connection string"** or **"Connect"**
   
   **Finding the Pooled Connection**:
   
   **Method 1 - Connection Details Panel**:
   - In the connection string box, look for a **dropdown** or **tabs** near the connection string
   - You might see options like:
     - "Direct connection" 
     - "Pooled connection" ← **SELECT THIS**
     - "Session pooler"
   - Click on **"Pooled connection"** or **"Session pooler"**
   
   **Method 2 - Dashboard**:
   - Go to your project dashboard
   - Click on **"Connection Details"** or **"Connect"** button
   - Look for **"Pooler"** or **"Connection pooling"** toggle/tab
   - Enable or select **"Pooled"** option
   
   **Method 3 - Connection String Format**:
   - The pooled connection string typically includes `-pooler` in the hostname
   - Example: `ep-cool-name-12345-pooler.us-east-2.aws.neon.tech`
   - Notice the `-pooler` suffix in the hostname
   
   **Visual Indicators**:
   - ❌ **AVOID**: Direct connection (no `-pooler` in hostname)
   - ✅ **USE**: Pooled connection (has `-pooler` in hostname)
   - The port might also differ (Pooled often uses port 5432 or 6543)
   
4. **Copy the Connection String**
   - Click **"Copy"** button
   - It looks like this:
   ```
   postgresql://neondb_owner:AbCdEf123456@ep-cool-name-12345.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
   - **Save this** - you'll need it in Step 3

**Troubleshooting**:
- If database shows "Paused", click "Resume" (free tier auto-pauses)
- Make sure connection string ends with `?sslmode=require`

---

### Step 2: Generate Secret Key

**Why**: This key secures your JWT (JSON Web Token) authentication system.

**What are JWT tokens?**
- When users log in, your app creates a special encrypted token (like a digital key)
- This token proves the user is authenticated without storing passwords
- The `BETTER_AUTH_SECRET` is used to encrypt/decrypt these tokens
- **If someone gets this secret, they can impersonate any user!** 🔐

**Security Requirements**:
- ✅ Must be at least 32 characters long
- ✅ Must be completely random (unpredictable)
- ✅ Must be different for production vs development
- ❌ Never share or commit to public repositories

---

**Instructions**:

1. **Open Terminal/PowerShell**
   - Windows: Press `Win + R`, type `cmd` or `powershell`, press Enter
   - Mac/Linux: Open Terminal

2. **Run This Command** (Recommended - works if you have Node.js installed):
   ```bash
   node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
   ```

3. **Copy the Output**
   - You'll get something like: `Kx8vN2mP9qR5sT7uV1wX3yZ4aB6cD8eF0gH2iJ4kL6m=`
   - **Save this** - you'll need it in Step 3

**Alternative Methods**:

**If you have OpenSSL** (Mac/Linux, or Windows with Git Bash):
```bash
openssl rand -base64 32
```

**If you have PowerShell** (Windows):
```powershell
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Minimum 0 -Maximum 256 }))
```

**⚠️ Security Note**: Never use online generators for production secrets! Generate locally to keep your secret truly secret.

---

### Step 3: Add Environment Variables to Vercel

**Why**: Vercel needs these to connect to your database and secure your app.

**Instructions**:

1. **Go to Your Vercel Project**
   - Visit: [https://vercel.com/dashboard](https://vercel.com/dashboard)
   - Click on your project (e.g., `2nd-hackathon-shafqat`)

2. **Open Settings**
   - Click **"Settings"** tab at the top
   - Click **"Environment Variables"** in the left sidebar

3. **Add Variable #1: DATABASE_URL**
   
   > [!CAUTION]
   > **CRITICAL: CLEAN YOUR VALUES BEFORE PASTING**
   > Vercel takes everything you paste **literally**. 
   > - ❌ **NO `psql` prefix**: Do not include the word `psql` or the space after it.
   > - ❌ **NO QUOTES**: Do not include `'` single quotes or `"` double quotes.
   > - ❌ **NO BACKTICKS**: Do not include `` ` `` backticks.
   > - ✅ **CORRECT**: Start directly with `postgresql://...`
   
   - Click **"Add New"** button
   - **Name**: `DATABASE_URL`
   - **Value**: Paste your Neon connection string (clean, no quotes!)
   - **Environment**: Check all three boxes:
     - ✅ Production
     - ✅ Preview
     - ✅ Development
   - Click **"Save"**

4. **Add Variable #2: BETTER_AUTH_SECRET**
   - Click **"Add New"** button again
   - **Name**: `BETTER_AUTH_SECRET`
   - **Value**: Paste your secret from Step 2
   - **Environment**: Check all three boxes
   - Click **"Save"**

5. **Add Variable #3: NEXT_PUBLIC_BACKEND_URL**
   - Click **"Add New"** button
   - **Name**: `NEXT_PUBLIC_BACKEND_URL`
   - **Value**: `https://YOUR-APP-NAME.vercel.app/api`
   - Replace `YOUR-APP-NAME` with your actual Vercel URL
   - Example: `https://2nd-hackathon-shafqat.vercel.app/api`
   - **IMPORTANT**: Must end with `/api`
   - **Environment**: Check all three boxes
   - Click **"Save"**

6. **Add Variable #4: NEXT_PUBLIC_BETTER_AUTH_URL**
   - Click **"Add New"** button
   - **Name**: `NEXT_PUBLIC_BETTER_AUTH_URL`
   - **Value**: `https://YOUR-APP-NAME.vercel.app`
   - Replace `YOUR-APP-NAME` with your actual Vercel URL
   - Example: `https://2nd-hackathon-shafqat.vercel.app`
   - **IMPORTANT**: NO `/api` at the end
   - **Environment**: Check all three boxes
   - Click **"Save"**

**Verification**:
- You should now see 4 environment variables listed
- Each should have green checkmarks for Production, Preview, Development

---

### Step 4: Redeploy Your Application

**Why**: Vercel needs to rebuild with the new environment variables.

**Instructions**:

1. **Go to Deployments Tab**
   - Click **"Deployments"** at the top of your Vercel project

2. **Find Latest Deployment**
   - You'll see a list of deployments
   - Find the most recent one (top of the list)

3. **Redeploy**
   - Click the **"..."** (three dots) button on the right
   - Click **"Redeploy"**
   - A popup will appear
   - **Optional**: Check **"Use existing Build Cache"** (faster)
   - Click **"Redeploy"** button

4. **Wait for Build**
   - Status will show "Building..."
   - This takes 2-3 minutes
   - Wait until it shows "Ready" with a green checkmark

5. **Verify Deployment**
   - Click **"Visit"** button
   - Your app should now load without errors!

---

## ✅ Verification Steps

After deployment, test these endpoints:

### 1. Test Frontend
- Visit: `https://your-app.vercel.app`
- Should show your landing page
- ✅ **Success**: Page loads with "EVOLVE" heading

### 2. Test Backend Health
- Visit: `https://your-app.vercel.app/api/health`
- Should show: `{"status":"healthy"}`
- ✅ **Success**: JSON response appears

### 3. Test API Documentation
- Visit: `https://your-app.vercel.app/docs`
- Should show Swagger UI with all API endpoints
- ✅ **Success**: Interactive API docs appear

### 4. Test Authentication
- Click "Start the Evolution" on homepage
- Try signing up with email/password
- ✅ **Success**: Can create account and login

### 5. Test CRUD Operations
- After login, go to Dashboard
- Try creating a task
- Try marking it complete
- Try deleting it
- ✅ **Success**: All operations work

---

## 🔧 Troubleshooting

### Issue: "FUNCTION_INVOCATION_FAILED"

**Cause**: Missing or incorrect environment variables

**Solution**:
1. Go to Vercel Settings → Environment Variables
2. Verify all 4 variables are present
3. Check `DATABASE_URL` uses **Pooled** connection (not Direct)
4. Ensure `DATABASE_URL` ends with `?sslmode=require`
5. Redeploy after fixing

---

### Issue: "This Serverless Function has crashed"

**Cause**: Database connection error or missing dependencies

**Solution**:
1. Check Vercel Function Logs:
   - Deployments → Click deployment → View Function Logs
2. Look for error messages
3. Common fixes:
   - Verify Neon database is not paused
   - Check connection string is correct
   - Ensure all Python dependencies in `pyproject.toml`

---

### Issue: "Failed to connect to database"

**Cause**: Wrong connection string or database paused

**Solution**:
1. Go to Neon Console
2. Check if database shows "Paused" - click "Resume"
3. Verify you copied **Pooled** connection string
4. Test connection string locally:
   ```bash
   psql "your-connection-string-here"
   ```

---

### Issue: API calls return 401 Unauthorized

**Cause**: `BETTER_AUTH_SECRET` mismatch or not set

**Solution**:
1. Verify `BETTER_AUTH_SECRET` is set in Vercel
2. Ensure it's the same value (not "development_secret...")
3. Generate a new secret and update both frontend and backend
4. Redeploy

---

### Issue: CORS errors in browser console

**Cause**: Wrong `NEXT_PUBLIC_BACKEND_URL`

**Solution**:
1. Check `NEXT_PUBLIC_BACKEND_URL` ends with `/api`
2. Verify it matches your Vercel URL exactly
3. Example: `https://2nd-hackathon-shafqat.vercel.app/api`
4. Redeploy after fixing

---

## 📝 Local Development Setup

For testing locally before deploying:

### Backend: `src/backend/.env`
```env
DATABASE_URL="sqlite:///todo.db"
BETTER_AUTH_SECRET="development_secret_only_change_in_prod"
```

### Frontend: `src/frontend/.env.local`
```env
DATABASE_URL="sqlite:///todo.db"
BETTER_AUTH_SECRET="development_secret_only_change_in_prod"
NEXT_PUBLIC_BACKEND_URL="http://127.0.0.1:800"
NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:3000"
```

**Start Backend**:
```bash
cd src/backend
uv run uvicorn main:app --host 0.0.0.0 --port 800 --reload
```

**Start Frontend** (separate terminal):
```bash
cd src/frontend
npm run dev
```

**Access**: http://localhost:3000

---

## 📊 Environment Variables Summary

| Variable | Local Value | Production Value | Where Used |
|----------|-------------|------------------|------------|
| `DATABASE_URL` | `sqlite:///todo.db` | Neon PostgreSQL URL | Backend + Frontend |
| `BETTER_AUTH_SECRET` | `development_secret...` | Generated secret | Backend + Frontend |
| `NEXT_PUBLIC_BACKEND_URL` | `http://127.0.0.1:800` | `https://your-app.vercel.app/api` | Frontend only |
| `NEXT_PUBLIC_BETTER_AUTH_URL` | `http://localhost:3000` | `https://your-app.vercel.app` | Frontend only |

---

## 🎓 Understanding Each Variable

### DATABASE_URL
- **Purpose**: Tells your app where to store data
- **Local**: Uses SQLite (file on your computer)
- **Production**: Uses Neon PostgreSQL (cloud database)
- **Format**: `postgresql://user:pass@host/db?sslmode=require`

### BETTER_AUTH_SECRET
- **Purpose**: Encrypts user login tokens (JWT)
- **Security**: Must be random and secret
- **Length**: At least 32 characters
- **Never**: Share or commit to public repos

### NEXT_PUBLIC_BACKEND_URL
- **Purpose**: Tells frontend where backend API lives
- **Local**: Points to `localhost:800`
- **Production**: Points to Vercel `/api` route
- **Must**: End with `/api` in production

### NEXT_PUBLIC_BETTER_AUTH_URL
- **Purpose**: Tells auth system where your app lives
- **Used for**: Redirects after login/logout
- **Must**: Match your actual domain
- **No**: `/api` suffix on this one

---

## 🚀 Ready to Deploy?

**Final Checklist**:
- [ ] Neon database created and active
- [ ] Connection string copied (Pooled, not Direct)
- [ ] Secret key generated (32+ characters)
- [ ] All 4 variables added to Vercel
- [ ] Variables set for Production, Preview, Development
- [ ] Application redeployed
- [ ] Health endpoint returns `{"status":"healthy"}`
- [ ] Can access `/docs` endpoint
- [ ] Can sign up and login
- [ ] Can create/edit/delete tasks

**If all checked**, your deployment is successful! 🎉

---

## 📞 Need Help?

1. **Check Vercel Logs**: Deployments → Click deployment → View Function Logs
2. **Test Locally First**: Make sure it works on `localhost` before deploying
3. **Verify Environment Variables**: Double-check spelling and values
4. **Check Neon Dashboard**: Ensure database is active (not paused)

---

## 🔐 Security Notes

> **⚠️ IMPORTANT**: Your `.env` files are tracked in Git per your request. Be careful when pushing to public repositories!

**Best Practices**:
- ✅ Use different secrets for local vs production
- ✅ Never share your `BETTER_AUTH_SECRET`
- ✅ Rotate secrets if compromised
- ✅ Use Neon's free tier for testing
- ❌ Don't commit production secrets to public repos
