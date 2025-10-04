# Button Troubleshooting Guide
## Caprae Lead Enhancer

---

## 🔧 Fixed Issues

### ✅ "Try Sample Data" Button
**Problem:** Button was not working due to missing event listeners
**Solution:** Added proper event listener setup in JavaScript
**Status:** ✅ FIXED

### ✅ "Upload Your Leads" Button  
**Problem:** CSV upload functionality was not implemented
**Solution:** Added complete CSV upload and parsing functionality
**Status:** ✅ FIXED

---

## 🚀 How to Test the Buttons

### Test 1: Sample Data Button
1. **Open the application** in your browser: `http://localhost:5000`
2. **Click "Try Sample Data"** button in the hero section
3. **Expected result:** 
   - 3 sample leads should be loaded
   - Lead count should show "3"
   - Leads should appear in the list below
   - Success alert should appear

### Test 2: CSV Upload Button
1. **Click "Upload Your Leads"** button in the hero section
2. **Select the sample CSV file** (`sample_leads.csv` in the project directory)
3. **Expected result:**
   - 5 leads should be loaded from the CSV
   - Lead count should show "5" (or total if you had existing leads)
   - Leads should appear in the list
   - Success alert should show "Successfully loaded 5 leads from CSV"

---

## 📁 Sample CSV File

A sample CSV file (`sample_leads.csv`) has been created with the following structure:

```csv
company_name,contact_name,email,phone,industry,company_size,revenue,website,linkedin
TechCorp Solutions,John Smith,john.smith@techcorp.com,+1-555-123-4567,Technology,50-200,10M-50M,https://techcorp.com,https://linkedin.com/company/techcorp
Global Manufacturing Inc,Sarah Johnson,sarah.j@globalmfg.com,555-987-6543,Manufacturing,500+,100M+,https://globalmfg.com,https://linkedin.com/company/global-manufacturing
StartupXYZ,Mike Chen,mike@startupxyz.io,+1-555-456-7890,SaaS,1-10,1M-5M,https://startupxyz.io,https://linkedin.com/company/startupxyz
DataFlow Systems,Jennifer Lee,jennifer@dataflow.com,555-234-5678,Technology,51-200,5M-10M,https://dataflow.com,https://linkedin.com/company/dataflow
CloudTech Inc,Robert Wilson,robert@cloudtech.net,555-345-6789,Software,201-500,50M-100M,https://cloudtech.net,https://linkedin.com/company/cloudtech
```

---

## 🔍 Technical Details

### What Was Fixed

#### 1. Event Listener Setup
**Before:**
```javascript
// Buttons had onclick attributes but no proper event listeners
<button onclick="loadSampleData()">Try Sample Data</button>
```

**After:**
```javascript
// Proper event listener setup
function setupButtonHandlers() {
    const sampleDataBtn = document.getElementById('sampleDataBtn');
    if (sampleDataBtn) {
        sampleDataBtn.addEventListener('click', loadSampleData);
    }
}
```

#### 2. CSV Upload Implementation
**Added:**
- Hidden file input for CSV selection
- CSV parsing function with flexible column mapping
- File validation (CSV format only)
- Error handling for malformed files
- Success feedback to user

#### 3. Column Mapping
The CSV parser automatically maps common column names:
- `company_name` → company, company name, business name
- `contact_name` → contact name, name, contact, full name
- `email` → email, email address, e-mail
- `phone` → phone, phone number, telephone, mobile
- `industry` → industry, sector, business type
- And more...

---

## 🐛 If Buttons Still Don't Work

### Check 1: Browser Console
1. **Open browser developer tools** (F12)
2. **Go to Console tab**
3. **Look for JavaScript errors**
4. **Common issues:**
   - `Uncaught TypeError: Cannot read property 'addEventListener' of null`
   - `Uncaught ReferenceError: function is not defined`

### Check 2: Network Tab
1. **Open browser developer tools** (F12)
2. **Go to Network tab**
3. **Click the buttons**
4. **Look for failed requests** (red entries)
5. **Check if API calls are being made**

### Check 3: Application Status
1. **Verify the application is running:**
   ```bash
   python app.py
   ```
2. **Check terminal output for errors**
3. **Verify port 5000 is accessible**

### Check 4: File Permissions
1. **Ensure CSV file is readable**
2. **Check if file is in the correct location**
3. **Try with different CSV files**

---

## 🔄 Restart Instructions

If buttons still don't work after the fixes:

### Method 1: Hard Refresh
1. **Press Ctrl+F5** (or Cmd+Shift+R on Mac)
2. **Clear browser cache**
3. **Try again**

### Method 2: Restart Application
1. **Stop the application** (Ctrl+C in terminal)
2. **Restart:**
   ```bash
   python app.py
   ```
3. **Refresh browser**

### Method 3: Clear Browser Data
1. **Open browser settings**
2. **Clear browsing data**
3. **Select "Cached images and files"
4. **Clear data and refresh**

---

## ✅ Success Indicators

### Sample Data Button Working When:
- ✅ Clicking loads 3 sample leads
- ✅ Lead count updates to show "3"
- ✅ Leads appear in the list
- ✅ Success alert appears
- ✅ No console errors

### CSV Upload Button Working When:
- ✅ Clicking opens file dialog
- ✅ CSV file selection works
- ✅ Leads are loaded from CSV
- ✅ Lead count updates correctly
- ✅ Success alert shows correct count
- ✅ No console errors

---

## 📞 Support

If you're still experiencing issues:

1. **Check the browser console** for specific error messages
2. **Verify the application is running** without errors
3. **Try the sample CSV file** provided
4. **Test with different browsers** (Chrome, Firefox, Edge)

The buttons should now work correctly with both sample data loading and CSV file upload functionality!

---

**Last Updated:** October 4, 2025  
**Status:** ✅ All Issues Fixed
