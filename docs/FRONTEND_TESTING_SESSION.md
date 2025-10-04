# 🧪 Frontend Testing - Live Session

**Date:** October 4, 2025  
**Time Started:** Now  
**Frontend Status:** ✅ Running on http://localhost:5173  
**Backend Status:** ✅ Running on http://127.0.0.1:8000

---

## ✅ Pre-Test Verification

- [x] Frontend server running: http://localhost:5173 ✅
- [x] Backend server running: http://127.0.0.1:8000 ✅
- [x] Database has test data: 9 entities ✅
- [x] All serializers fixed ✅
- [x] User: Major (logged in)

---

## 🎯 Critical Test Plan (5 Minutes)

### Test 1: Entity Listing Page ⏳
**URL:** http://localhost:5173/entities

**Steps:**
1. Open browser to http://localhost:5173/entities
2. Press F12 to open DevTools Console
3. Check the page

**Expected Results:**
- [ ] Page loads without errors
- [ ] See "Entities" or similar header
- [ ] See entity cards/list
- [ ] Count shows ~9 entities
- [ ] Console shows 0 errors (no red text)

**Actual Results:**
Status: ⬜ Not Tested Yet
Entities Visible: _____
Console Errors: _____
Screenshot: _____

---

### Test 2: Entity Detail - UUID Bug Verification ⚠️ CRITICAL
**This is the most important test!**

**Steps:**
1. From entities page, click on **"TechCorp Industries"** (or any entity)
2. **Look at the URL in the address bar**
3. Check the page content

**Expected Results:**
- [ ] URL format: `http://localhost:5173/entities/4486af3d-85c9-4bf3-93df-69f97a2b026e`
- [ ] URL contains a UUID (long string like above)
- [ ] **NOT** `http://localhost:5173/entities/NaN` ❌
- [ ] **NOT** `http://localhost:5173/entities/undefined` ❌
- [ ] Page shows entity details:
  - [ ] Entity name
  - [ ] Entity type
  - [ ] Description
  - [ ] Tabs: Overview, Attributes, Relationships, Notes, Graph
- [ ] No "Entity Not Found" error
- [ ] Console: 0 errors

**Actual Results:**
Status: ⬜ Not Tested Yet
URL: _____________________
UUID Present: [ ] Yes [ ] No
Page Loaded: [ ] Yes [ ] No
Console Errors: _____

**⚠️ If URL shows NaN:** UUID bug NOT fixed - report immediately!  
**✅ If URL shows UUID:** Bug IS fixed - proceed with testing!

---

### Test 3: Entity Edit Form ⏳
**Steps:**
1. From entity detail page, click **"Edit"** button
2. Wait for form to load

**Expected Results:**
- [ ] URL: `http://localhost:5173/entities/{UUID}/edit`
- [ ] Form loads with entity data:
  - [ ] Name field populated
  - [ ] Entity type dropdown shows current type
  - [ ] Description populated
  - [ ] Other fields populated
- [ ] Entity types dropdown **loads successfully**
- [ ] **NO** "entityTypes.map is not a function" error
- [ ] Console: 0 errors

**Actual Results:**
Status: ⬜ Not Tested Yet
Form Loaded: [ ] Yes [ ] No
Entity Types Loaded: [ ] Yes [ ] No
Console Errors: _____

**⚠️ If "entityTypes.map" error:** Pagination bug NOT fixed!  
**✅ If dropdown loads:** Bug IS fixed!

---

### Test 4: Create New Entity ⏳
**Steps:**
1. Go to entities page
2. Click **"New Entity"** or "+ Add Entity" button
3. Check the form

**Expected Results:**
- [ ] Form opens/loads
- [ ] Entity types dropdown **populates**
- [ ] Can select entity type
- [ ] All fields editable
- [ ] **NO** "entityTypes.map is not a function" error
- [ ] Console: 0 errors

**Test Create:**
1. Fill in form:
   - Name: "Test Entity QA"
   - Type: "Company"
   - Description: "Created during testing"
2. Click "Create" or "Save"

**Expected:**
- [ ] Entity creates successfully
- [ ] Redirects to new entity detail page
- [ ] New entity appears in entities list

**Actual Results:**
Status: ⬜ Not Tested Yet
Dropdown Loaded: [ ] Yes [ ] No
Entity Created: [ ] Yes [ ] No
New Entity ID: _____

---

### Test 5: Dork Execution ⏳
**Steps:**
1. Navigate to: http://localhost:5173/dorks
2. Click on **first dork** in the list
3. Click **"Execute"** button

**Expected Results:**
- [ ] Dork list page loads
- [ ] Dork detail page loads
- [ ] Difficulty badge displays (any color, even gray)
- [ ] **NO** "Cannot read properties of undefined" error for difficulty
- [ ] Execute button is clickable
- [ ] **Clicking Execute opens Google search in new tab**
- [ ] **NO** 500 error
- [ ] **NO** AttributeError in backend console
- [ ] Console: 0 errors

**Actual Results:**
Status: ⬜ Not Tested Yet
Dork List Loaded: [ ] Yes [ ] No
Dork Detail Loaded: [ ] Yes [ ] No
Execute Worked: [ ] Yes [ ] No
Google Opened: [ ] Yes [ ] No
Console Errors: _____

**⚠️ If 500 error:** execution_count bug NOT fixed!  
**✅ If Google opens:** Bug IS fixed!

---

### Test 6: Graph Visualization ⏳
**Steps:**
1. Navigate to TechCorp Industries entity
2. Click **🕸️ "Graph"** tab (or "Relationships Graph")
3. Wait for graph to render

**Expected Results:**
- [ ] Graph tab is clickable
- [ ] Graph renders (shows nodes and lines)
- [ ] Shows entity nodes:
  - [ ] TechCorp Industries (center)
  - [ ] Dr. Sarah Chen (connected)
  - [ ] Open Source Foundation (connected)
- [ ] Lines/edges connect nodes
- [ ] Can zoom in/out (mouse wheel or controls)
- [ ] Can pan/drag graph
- [ ] Clicking node navigates to that entity
- [ ] Console: 0 errors

**Actual Results:**
Status: ⬜ Not Tested Yet
Graph Rendered: [ ] Yes [ ] No
Nodes Visible: _____
Interactive: [ ] Yes [ ] No
Console Errors: _____

---

## 📊 Console Error Check

**Open DevTools Console (F12) and check for errors:**

### Expected: ✅ NO ERRORS
- [ ] No red error messages
- [ ] No "NaN" related errors
- [ ] No "entityTypes.map" errors
- [ ] No "Cannot read properties of undefined"
- [ ] No 401 Unauthorized (after initial login)
- [ ] No 500 Internal Server Errors

### Common Errors to Watch For:
1. ❌ `GET /api/dorks/entities/NaN/ 404` - UUID bug
2. ❌ `entityTypes.map is not a function` - Pagination bug
3. ❌ `Cannot read properties of undefined (reading 'toLowerCase')` - Difficulty bug
4. ❌ `GET /api/dorks/dorks/{id}/execute/ 500` - execution_count bug
5. ❌ `GET /api/dorks/entities/{UUID}/ 500` - Serializer bug

**Actual Console Errors Found:**
```
(Paste any errors here)
```

---

## 🎨 Visual/UI Check

### Navigation
- [ ] Top navigation bar visible
- [ ] Menu items clickable
- [ ] User info/avatar displays
- [ ] Logout button works

### Entities Page
- [ ] Entity cards/list displays nicely
- [ ] Entity type icons show
- [ ] Search bar functional
- [ ] Filters work (if present)
- [ ] Pagination works (if multiple pages)

### Entity Detail Page
- [ ] Layout looks good
- [ ] Tabs are styled properly
- [ ] Information is readable
- [ ] Buttons are styled
- [ ] Colors/badges show correctly

### Forms
- [ ] Input fields styled
- [ ] Dropdowns styled
- [ ] Buttons styled and clickable
- [ ] Form validation shows (if applicable)

---

## ⚡ Performance Check

### Page Load Times (Rough Estimate):
- Entities list page: _____ seconds
- Entity detail page: _____ seconds
- Dork list page: _____ seconds
- Graph visualization: _____ seconds

### Responsiveness:
- [ ] Pages load quickly (< 3 seconds)
- [ ] No long delays
- [ ] Smooth scrolling
- [ ] Smooth interactions

---

## 🔍 Network Tab Check

**Open DevTools → Network tab**

### Check API Calls:
1. **Entities API:**
   ```
   GET /api/dorks/entities/?search=&status=&priority=&page=1
   Status: Should be 200 OK
   Response: Should show entities data
   ```

2. **Entity Detail API:**
   ```
   GET /api/dorks/entities/{UUID}/
   Status: Should be 200 OK (NOT 500!)
   Response: Should show entity details with all fields
   ```

3. **Entity Types API:**
   ```
   GET /api/dorks/entity-types/
   Status: Should be 200 OK
   Response: Should show paginated results with entity types
   ```

4. **Dork Execute API:**
   ```
   POST /api/dorks/dorks/{id}/execute/
   Status: Should be 200 OK (NOT 500!)
   ```

**Actual Results:**
API Calls Status: _____
Any 500 Errors: _____
Any 404 Errors: _____

---

## ✅ Test Results Summary

### Critical Tests (Must Pass):
1. **Entity Detail UUID:** [ ] PASS [ ] FAIL
2. **Entity Types Dropdown:** [ ] PASS [ ] FAIL
3. **Dork Execution:** [ ] PASS [ ] FAIL
4. **No Console Errors:** [ ] PASS [ ] FAIL

### Important Tests:
5. **Graph Visualization:** [ ] PASS [ ] FAIL
6. **Entity Creation:** [ ] PASS [ ] FAIL
7. **Entity Editing:** [ ] PASS [ ] FAIL

### Overall Status:
- [ ] ✅ ALL CRITICAL TESTS PASSED
- [ ] ⚠️ SOME TESTS FAILED
- [ ] ❌ MAJOR ISSUES FOUND

---

## 🐛 Issues Found

### Issue #1:
**Description:** _____
**Location:** _____
**Severity:** [ ] Critical [ ] Major [ ] Minor
**Console Error:** _____
**Screenshot:** _____

### Issue #2:
**Description:** _____
**Location:** _____
**Severity:** [ ] Critical [ ] Major [ ] Minor

---

## 📝 Notes

**General Observations:**
- _____
- _____

**Performance Notes:**
- _____

**UI/UX Notes:**
- _____

**Suggestions:**
- _____

---

## ✨ Final Assessment

**Date Completed:** _____
**Tester:** _____
**Browser:** _____
**Total Test Time:** _____ minutes

**Overall Grade:**
- [ ] 🎉 EXCELLENT - All tests passed, no issues
- [ ] ✅ GOOD - Minor issues only
- [ ] ⚠️ FAIR - Some important issues
- [ ] ❌ POOR - Critical issues found

**Ready for Production:**
- [ ] YES - All critical bugs fixed
- [ ] NO - Issues need fixing

**Recommendation:**
_____

---

## 🚀 Quick Test Commands

### Test Frontend Accessibility:
```powershell
curl http://localhost:5173
```

### Check Backend API:
```powershell
curl http://localhost:8000/api/dorks/entities/
```

### View Database Status:
```powershell
python check_database_status.py
```

---

## 📞 Help

**If you see errors:**
1. Take screenshot of console
2. Copy error message
3. Note which test failed
4. Document in "Issues Found" section
5. Hard refresh browser (Ctrl+Shift+R)
6. Test again

**If everything works:**
1. Check all boxes as PASS ✅
2. Document in Final Assessment
3. Celebrate! 🎉

---

**START TESTING NOW!**

Open: http://localhost:5173/entities

**Remember:** The most critical test is checking if entity URLs show UUIDs or NaN!

---

**Good luck! 🧪🚀**
