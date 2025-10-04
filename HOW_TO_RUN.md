# How to Run Caprae Lead Enhancer
## Quick Start Guide

---

## 🚀 Prerequisites

Before running the application, ensure you have the following installed:

### Required Software
- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** (Python package installer) - Usually comes with Python
- **Git** (optional) - [Download Git](https://git-scm.com/downloads)

### System Requirements
- **Operating System:** Windows, macOS, or Linux
- **RAM:** Minimum 4GB (8GB recommended)
- **Storage:** At least 500MB free space
- **Internet:** Required for initial package installation

---

## 📥 Installation Steps

### Step 1: Download/Clone the Project

**Option A: If you have the project files**
- Ensure all project files are in a single directory
- Navigate to the project directory in your terminal/command prompt

**Option B: If cloning from repository**
```bash
git clone <repository-url>
cd caprae-lead-enhancer
```

### Step 2: Verify Python Installation

Open your terminal/command prompt and check Python version:

```bash
python --version
# Should show Python 3.8 or higher

pip --version
# Should show pip version
```

**If Python is not installed:**
1. Go to [python.org](https://www.python.org/downloads/)
2. Download the latest Python version
3. **Important:** Check "Add Python to PATH" during installation
4. Restart your terminal after installation

### Step 3: Install Dependencies

Navigate to the project directory and install required packages:

```bash
# Install all required packages
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed Flask-2.2.5 Jinja2-3.1.6 MarkupSafe-3.0.3 Werkzeug-3.1.3 beautifulsoup4-4.14.2 certifi-2025.8.3 charset_normalizer-3.4.3 click-8.3.0 colorama-6.0.0 dnspython-2.8.0 email-validator-2.3.0 fuzzywuzzy-0.18.0 idna-3.10 itsdangerous-2.2.0 numpy-2.3.3 pandas-2.3.3 phonenumbers-9.0.15 python-Levenshtein-0.27.1 python-dateutil-2.9.0.post0 pytz-2025.2 rapidfuzz-3.14.1 requests-2.32.5 six-1.17.0 soupsieve-2.8 typing-extensions-4.15.0 tzdata-2025.2 urllib3-2.5.0
```

---

## 🏃‍♂️ Running the Application

### Method 1: Direct Python Execution

```bash
python app.py
```

**Expected output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.31.182:5000
Press CTRL+C to quit
 * Debugger is active!
 * Debugger PIN: 805-152-069
```

### Method 2: Using Python Module

```bash
python -m flask run
```

### Method 3: Using Virtual Environment (Recommended)

**Create virtual environment:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

---

## 🌐 Accessing the Application

### Web Interface
1. **Open your web browser**
2. **Navigate to:** `http://localhost:5000`
3. **Alternative URLs:**
   - `http://127.0.0.1:5000`
   - `http://0.0.0.0:5000`

### What You'll See
- **Hero Section:** Application introduction and features
- **Lead Input Form:** Add leads manually
- **Sample Data Button:** Load test data
- **Processing Section:** Score and analyze leads
- **Results Dashboard:** View scored leads and analytics

---

## 🧪 Testing the Application

### Test 1: Load Sample Data
1. Click **"Try Sample Data"** button
2. Verify that 3 sample leads are loaded
3. Click **"Process & Score Leads"**
4. Review the results dashboard

### Test 2: Add Manual Lead
1. Fill out the lead form with:
   - Company Name: "Test Corp"
   - Contact Name: "John Doe"
   - Email: "john@test.com"
   - Phone: "555-123-4567"
   - Industry: "Technology"
2. Click **"Add Lead"**
3. Click **"Process & Score Leads"**
4. Review the scoring results

### Test 3: API Testing

**Test Sample Data API:**
```bash
curl http://localhost:5000/api/sample-data
```

**Test Lead Scoring API:**
```bash
curl -X POST http://localhost:5000/api/score-leads \
  -H "Content-Type: application/json" \
  -d '{"leads":[{"company_name":"Test Corp","contact_name":"John Doe","email":"john@test.com","phone":"555-123-4567","industry":"Technology"}]}'
```

**PowerShell (Windows):**
```powershell
# Test sample data
Invoke-WebRequest -Uri "http://localhost:5000/api/sample-data" -Method GET

# Test lead scoring
$body = @{leads=@(@{company_name="Test Corp"; contact_name="John Doe"; email="john@test.com"; phone="555-123-4567"; industry="Technology"})} | ConvertTo-Json -Depth 3
Invoke-WebRequest -Uri "http://localhost:5000/api/score-leads" -Method POST -Body $body -ContentType "application/json"
```

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue 1: "Python is not recognized"
**Solution:**
- Reinstall Python with "Add to PATH" option checked
- Restart terminal/command prompt
- Verify with `python --version`

#### Issue 2: "pip is not recognized"
**Solution:**
```bash
# Try using python -m pip instead
python -m pip install -r requirements.txt
```

#### Issue 3: "Module not found" errors
**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### Issue 4: "Port 5000 already in use"
**Solution:**
```bash
# Kill process using port 5000
# On Windows:
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# On macOS/Linux:
lsof -ti:5000 | xargs kill -9
```

#### Issue 5: "Permission denied" errors
**Solution:**
```bash
# On Windows: Run as Administrator
# On macOS/Linux: Use sudo if necessary
sudo pip install -r requirements.txt
```

#### Issue 6: Application won't start
**Solution:**
1. Check Python version: `python --version`
2. Verify all dependencies: `pip list`
3. Check for syntax errors in code
4. Review terminal output for specific error messages

---

## 📱 Using the Application

### Adding Leads
1. **Fill out the form** with lead information
2. **Required fields:** Company Name, Contact Name, Email, Phone, Industry
3. **Optional fields:** Company Size, Revenue, Website, LinkedIn
4. **Click "Add Lead"** to add to processing queue

### Processing Leads
1. **Add one or more leads** to the queue
2. **Click "Process & Score Leads"** to analyze
3. **Wait for processing** (usually instant)
4. **Review results** in the dashboard

### Understanding Results
- **Lead Score:** Overall score out of 100
- **Priority Level:** High (80+), Medium (60-79), Low (<60)
- **Data Quality:** Completeness percentage
- **Recommendations:** Actionable insights for each lead

### Exporting Data
1. **Process leads** to generate results
2. **Click "Export CSV"** button
3. **Download file** to your computer
4. **Import into CRM** or spreadsheet application

---

## 🛑 Stopping the Application

### Method 1: Keyboard Interrupt
- Press **Ctrl+C** in the terminal where the app is running
- Wait for the process to stop gracefully

### Method 2: Close Terminal
- Close the terminal window
- The application will stop automatically

### Method 3: Task Manager (Windows)
1. Open Task Manager (Ctrl+Shift+Esc)
2. Find "python.exe" process
3. End the process

---

## 🔄 Restarting the Application

### Quick Restart
1. **Stop the application** (Ctrl+C)
2. **Run again:** `python app.py`

### Full Restart (if issues persist)
1. **Stop the application**
2. **Deactivate virtual environment** (if using one)
3. **Reactivate virtual environment**
4. **Reinstall dependencies:** `pip install -r requirements.txt`
5. **Run application:** `python app.py`

---

## 📊 Performance Notes

### Expected Performance
- **Startup time:** 2-5 seconds
- **Lead processing:** <1 second per lead
- **Memory usage:** ~50-100MB
- **Concurrent users:** 10-20 (development server)

### Optimization Tips
- **Close unused browser tabs** to free memory
- **Process leads in batches** of 10-50 for best performance
- **Use sample data** for testing to avoid data entry

---

## 🆘 Getting Help

### If You Encounter Issues
1. **Check this guide** for common solutions
2. **Review terminal output** for error messages
3. **Verify all prerequisites** are installed correctly
4. **Try the troubleshooting steps** above

### Support Information
- **Project:** Caprae Lead Enhancer
- **Version:** 1.0.0
- **Challenge:** Caprae Capital AI-Readiness
- **Documentation:** See README.md for detailed information

---

## ✅ Success Indicators

### Application is Running Correctly When:
- ✅ Terminal shows "Running on http://127.0.0.1:5000"
- ✅ Web browser loads the application interface
- ✅ Sample data loads without errors
- ✅ Lead scoring works and shows results
- ✅ Export functionality works

### Ready for Use When:
- ✅ All features are accessible
- ✅ No error messages in terminal
- ✅ Results display correctly
- ✅ Export generates valid CSV files

---

**🎉 Congratulations! You're ready to use the Caprae Lead Enhancer!**

*For detailed feature documentation, see README.md*
*For project overview, see PROJECT_SUMMARY.md*
