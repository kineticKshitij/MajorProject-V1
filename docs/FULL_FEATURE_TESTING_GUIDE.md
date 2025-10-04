# 🧪 Full Feature Testing Guide

**Date:** October 4, 2025  
**Testing Type:** Comprehensive Feature Testing  
**Framework Version:** 80% Complete  
**Status:** 🔄 In Progress

---

## 📋 Testing Checklist

### ✅ Pre-Testing Setup
- [ ] Backend server running on http://127.0.0.1:8000
- [ ] Frontend server running on http://localhost:5173
- [ ] Database has 9 test entities
- [ ] User logged in as "Major"
- [ ] Browser DevTools console open (F12)

---

## 🧪 Test Suite 1: Entity System - CRUD Operations

### Test 1.1: List Entities
**URL:** http://localhost:5173/entities  
**Expected:**
- [ ] Page loads without errors
- [ ] Shows "Total Entities: 9" (or current count)
- [ ] Displays entity cards with names, types, icons
- [ ] Each card shows confidence level
- [ ] "New Entity" button visible

**Test Steps:**
1. Navigate to /entities
2. Count visible entity cards
3. Check console for errors
4. Verify entity type icons display correctly

**✅ Pass Criteria:** All 9 test entities visible, no console errors

---

### Test 1.2: View Entity Details
**Test Entity:** TechCorp Industries  
**Expected:**
- [ ] Clicking entity navigates to /entities/{UUID}
- [ ] URL shows UUID (not NaN or undefined)
- [ ] Entity details load (name, type, description)
- [ ] Confidence level badge displays
- [ ] Tabs visible: Overview, Attributes, Relationships, Notes, Graph
- [ ] No "Entity Not Found" error

**Test Steps:**
1. Click on "TechCorp Industries" entity
2. Verify URL contains UUID: `/entities/6d3c39b3-...`
3. Check all entity details load
4. Switch between tabs
5. Check console for errors

**✅ Pass Criteria:** Entity details load, UUID in URL, all tabs accessible

---

### Test 1.3: Edit Entity
**Expected:**
- [ ] "Edit" button visible on entity detail page
- [ ] Clicking "Edit" navigates to /entities/{UUID}/edit
- [ ] Form loads with existing entity data
- [ ] All fields editable (name, type, description, confidence)
- [ ] Entity types dropdown loads (not "entityTypes.map" error)
- [ ] "Save" button works
- [ ] Redirects to entity detail after save

**Test Steps:**
1. From entity detail page, click "Edit"
2. Verify form loads with data
3. Change description
4. Click "Save"
5. Verify changes persist

**✅ Pass Criteria:** Edit form works, data persists, no errors

---

### Test 1.4: Create New Entity
**Expected:**
- [ ] "New Entity" button works
- [ ] Form loads with empty fields
- [ ] Entity types dropdown populates
- [ ] All fields are fillable
- [ ] Validation works (required fields)
- [ ] Entity created successfully
- [ ] Redirects to new entity detail

**Test Steps:**
1. Click "New Entity" from entities list
2. Fill in form:
   - Name: "Test Company XYZ"
   - Type: "Company"
   - Description: "Test entity for QA"
   - Confidence: "high"
3. Click "Create"
4. Verify new entity appears in list

**✅ Pass Criteria:** New entity created, appears in list

---

### Test 1.5: Delete Entity
**Expected:**
- [ ] "Delete" button visible
- [ ] Confirmation dialog appears
- [ ] Entity deleted from database
- [ ] Redirects to entities list
- [ ] Entity no longer appears in list

**Test Steps:**
1. Navigate to test entity created in 1.4
2. Click "Delete"
3. Confirm deletion
4. Verify entity removed from list

**✅ Pass Criteria:** Entity deleted successfully

---

## 🧪 Test Suite 2: Entity Attributes

### Test 2.1: View Attributes
**Test Entity:** TechCorp Industries (has 4 attributes)  
**Expected:**
- [ ] "Attributes" tab shows attributes list
- [ ] All 4 attributes visible:
  - Employee Count: 5000
  - Annual Revenue: $500M
  - Stock Symbol: TECH
  - CEO: John Smith
- [ ] Each attribute shows key, value, value_type
- [ ] "Add Attribute" button visible

**Test Steps:**
1. Navigate to TechCorp Industries
2. Click "Attributes" tab
3. Count visible attributes
4. Verify attribute data displays correctly

**✅ Pass Criteria:** 4 attributes visible, data correct

---

### Test 2.2: Add Attribute
**Expected:**
- [ ] "Add Attribute" button works
- [ ] Form appears (inline or modal)
- [ ] Fields: key, value, value_type
- [ ] Attribute saves successfully
- [ ] New attribute appears in list

**Test Steps:**
1. Click "Add Attribute"
2. Fill in:
   - Key: "Founded"
   - Value: "2010"
   - Value Type: "text"
3. Save attribute
4. Verify it appears in list

**✅ Pass Criteria:** Attribute created and visible

---

### Test 2.3: Edit Attribute
**Expected:**
- [ ] Edit button/icon visible per attribute
- [ ] Edit form loads with existing data
- [ ] Changes save successfully
- [ ] Updated value displays

**Test Steps:**
1. Click edit on "Founded" attribute
2. Change value to "2011"
3. Save
4. Verify change persists

**✅ Pass Criteria:** Attribute updated successfully

---

### Test 2.4: Delete Attribute
**Expected:**
- [ ] Delete button/icon visible
- [ ] Confirmation appears
- [ ] Attribute deleted
- [ ] No longer appears in list

**Test Steps:**
1. Click delete on "Founded" attribute
2. Confirm deletion
3. Verify removed from list

**✅ Pass Criteria:** Attribute deleted

---

## 🧪 Test Suite 3: Entity Relationships

### Test 3.1: View Relationships
**Test Entity:** Dr. Sarah Chen (has 1 relationship)  
**Expected:**
- [ ] "Relationships" tab shows relationships
- [ ] Shows: Dr. Sarah Chen → Employee at → TechCorp Industries
- [ ] Confidence level displayed
- [ ] Related entity is clickable link
- [ ] "Add Relationship" button visible

**Test Steps:**
1. Navigate to Dr. Sarah Chen entity
2. Click "Relationships" tab
3. Verify relationship displays
4. Click on related entity link

**✅ Pass Criteria:** 1 relationship visible, link works

---

### Test 3.2: Add Relationship
**Expected:**
- [ ] "Add Relationship" button works
- [ ] Form shows:
   - Related entity dropdown/search
   - Relationship type field
   - Confidence level selector
- [ ] Relationship saves
- [ ] Appears in both entities' relationship lists

**Test Steps:**
1. From Dr. Sarah Chen, click "Add Relationship"
2. Select related entity: "Metropolitan University"
3. Type: "Alumni"
4. Confidence: "high"
5. Save
6. Verify appears in both entities

**✅ Pass Criteria:** Relationship created bidirectionally

---

### Test 3.3: Delete Relationship
**Expected:**
- [ ] Delete button visible
- [ ] Confirmation appears
- [ ] Relationship removed from both entities

**Test Steps:**
1. Delete "Alumni" relationship
2. Confirm
3. Check both entities

**✅ Pass Criteria:** Relationship deleted from both sides

---

## 🧪 Test Suite 4: Entity Notes

### Test 4.1: View Notes
**Expected:**
- [ ] "Notes" tab visible
- [ ] Notes list displays (may be empty)
- [ ] "Add Note" button visible
- [ ] Notes show content, timestamp, author

**Test Steps:**
1. Navigate to any entity
2. Click "Notes" tab
3. Check note display format

**✅ Pass Criteria:** Notes section accessible

---

### Test 4.2: Add Note
**Expected:**
- [ ] "Add Note" button works
- [ ] Text area appears
- [ ] Note saves
- [ ] Appears in notes list with timestamp

**Test Steps:**
1. Click "Add Note"
2. Enter: "Testing note functionality - QA session"
3. Save
4. Verify note appears

**✅ Pass Criteria:** Note created successfully

---

### Test 4.3: Edit Note
**Expected:**
- [ ] Edit button visible per note
- [ ] Note content editable
- [ ] Changes save
- [ ] Updated content displays

**Test Steps:**
1. Click edit on test note
2. Modify text
3. Save
4. Verify change

**✅ Pass Criteria:** Note edited successfully

---

### Test 4.4: Delete Note
**Expected:**
- [ ] Delete button visible
- [ ] Note deleted
- [ ] Removed from list

**Test Steps:**
1. Delete test note
2. Verify removal

**✅ Pass Criteria:** Note deleted

---

## 🧪 Test Suite 5: Google Dorks System

### Test 5.1: List Dorks
**URL:** http://localhost:5173/dorks  
**Expected:**
- [ ] Page loads without errors
- [ ] Dorks displayed in grid/list
- [ ] Each dork shows:
   - Title
   - Query snippet
   - Category badge
   - Risk level badge
   - Difficulty badge
- [ ] Search bar visible
- [ ] Category filter visible

**Test Steps:**
1. Navigate to /dorks
2. Scroll through dork list
3. Check badge displays
4. Verify no console errors

**✅ Pass Criteria:** Dorks list loads, badges display correctly

---

### Test 5.2: View Dork Details
**Test Dork:** SSH Private Keys (ID: 20 or first dork)  
**Expected:**
- [ ] Clicking dork navigates to /dorks/{id}
- [ ] Dork details load:
   - Title
   - Full query
   - Description
   - Category, Risk, Difficulty badges
   - Example usage
   - Notes
   - Usage count
   - Execution count
- [ ] "Execute" button visible
- [ ] "Bookmark" button visible

**Test Steps:**
1. Click on any dork
2. Verify all details display
3. Check badges render correctly
4. Verify no TypeError for difficulty

**✅ Pass Criteria:** Dork details load, no difficulty error

---

### Test 5.3: Execute Dork
**Expected:**
- [ ] "Execute" button clickable
- [ ] Opens Google search in new tab
- [ ] execution_count increments
- [ ] No 500 error
- [ ] No AttributeError

**Test Steps:**
1. From dork detail page, click "Execute"
2. Verify Google search opens
3. Check execution_count increased
4. Check backend logs for errors

**Test Steps (Verify Count):**
```bash
python manage.py shell -c "from googledorks.models import GoogleDork; d = GoogleDork.objects.get(id=20); print(f'Execution count: {d.execution_count}')"
```

**✅ Pass Criteria:** Execution works, count increments, no errors

---

### Test 5.4: Bookmark Dork
**Expected:**
- [ ] Bookmark button toggles
- [ ] Bookmarked state persists
- [ ] Bookmarked dorks filterable

**Test Steps:**
1. Click bookmark button
2. Refresh page
3. Verify bookmark state saved
4. Check bookmarks filter

**✅ Pass Criteria:** Bookmark functionality works

---

### Test 5.5: Search Dorks
**Expected:**
- [ ] Search bar functional
- [ ] Results filter as you type
- [ ] Searches title, query, description
- [ ] No results message if nothing found

**Test Steps:**
1. Enter "SSH" in search
2. Verify results filter
3. Clear search
4. Verify all dorks return

**✅ Pass Criteria:** Search works correctly

---

### Test 5.6: Filter by Category
**Expected:**
- [ ] Category filter dropdown works
- [ ] Filters dorks by selected category
- [ ] "All" option shows all dorks

**Test Steps:**
1. Select category from filter
2. Verify only category dorks show
3. Select "All"
4. Verify all dorks return

**✅ Pass Criteria:** Category filter works

---

## 🧪 Test Suite 6: Entity Templates

### Test 6.1: View Templates
**URL:** http://localhost:5173/templates  
**Expected:**
- [ ] Templates page loads
- [ ] Template list displays
- [ ] Each template shows name, type, field count
- [ ] "Create from Template" button visible

**Test Steps:**
1. Navigate to /templates
2. View available templates
3. Check template details

**✅ Pass Criteria:** Templates accessible

---

### Test 6.2: Create Entity from Template
**Expected:**
- [ ] "Create from Template" works
- [ ] Form pre-fills with template data
- [ ] Fields editable
- [ ] Entity created successfully
- [ ] Template attributes applied

**Test Steps:**
1. Select a template
2. Click "Create from Template"
3. Fill in entity-specific data
4. Create entity
5. Verify template attributes applied

**✅ Pass Criteria:** Template-based entity creation works

---

## 🧪 Test Suite 7: Search and Filter

### Test 7.1: Entity Search
**Expected:**
- [ ] Search bar on entities page
- [ ] Real-time filtering
- [ ] Searches entity names, descriptions
- [ ] Case-insensitive

**Test Steps:**
1. Go to /entities
2. Search "TechCorp"
3. Verify results
4. Search "healthcare"
5. Verify results

**✅ Pass Criteria:** Entity search works

---

### Test 7.2: Entity Type Filter
**Expected:**
- [ ] Type filter dropdown
- [ ] Filters by Company, Person, Organization, etc.
- [ ] "All Types" shows all entities

**Test Steps:**
1. Select "Company" filter
2. Verify only companies show (3 entities)
3. Select "Person"
4. Verify only persons show (2 entities)

**✅ Pass Criteria:** Type filter works correctly

---

### Test 7.3: Confidence Level Filter
**Expected:**
- [ ] Confidence filter available
- [ ] Filters by high/medium/low
- [ ] Multiple selections work

**Test Steps:**
1. Filter by "High" confidence
2. Verify results
3. Filter by "Medium"
4. Verify results

**✅ Pass Criteria:** Confidence filter works

---

## 🧪 Test Suite 8: Graph Visualization

### Test 8.1: View Relationship Graph
**Test Entity:** TechCorp Industries  
**Expected:**
- [ ] "Graph" tab visible (🕸️ icon)
- [ ] Graph renders without errors
- [ ] Shows entity node
- [ ] Shows related entities
- [ ] Shows relationship edges with labels
- [ ] Zoom/pan controls work

**Test Steps:**
1. Navigate to TechCorp Industries
2. Click "Graph" tab
3. Wait for graph to render
4. Verify nodes display:
   - TechCorp Industries (center)
   - Dr. Sarah Chen (connected)
   - Open Source Foundation (connected)
5. Verify edge labels show relationship types
6. Test zoom in/out
7. Test pan/drag

**✅ Pass Criteria:** Graph renders, shows relationships, interactive

---

### Test 8.2: Click Node Navigation
**Expected:**
- [ ] Clicking node navigates to that entity
- [ ] Node hover shows tooltip
- [ ] Node colors indicate entity type

**Test Steps:**
1. Hover over Dr. Sarah Chen node
2. Verify tooltip appears
3. Click node
4. Verify navigates to Sarah Chen entity

**✅ Pass Criteria:** Node interactions work

---

## 🧪 Test Suite 9: Bug Fix Verification

### Test 9.1: UUID Handling
**Bug Fixed:** Entity URLs showing /entities/NaN  
**Test:**
- [ ] Navigate to any entity
- [ ] URL shows UUID (e.g., /entities/6d3c39b3-5429-4614-87af-17b07a96c30a)
- [ ] NOT /entities/NaN
- [ ] Entity details load
- [ ] Edit entity URL also shows UUID

**✅ Pass Criteria:** No NaN URLs, UUIDs work everywhere

---

### Test 9.2: Entity Types Pagination
**Bug Fixed:** entityTypes.map is not a function  
**Test:**
- [ ] Create new entity
- [ ] Entity types dropdown loads
- [ ] No console error "entityTypes.map is not a function"
- [ ] Can select entity type

**✅ Pass Criteria:** Entity types load correctly

---

### Test 9.3: Execution Count Field
**Bug Fixed:** AttributeError on execution_count  
**Test:**
- [ ] Execute any dork
- [ ] No 500 error
- [ ] No AttributeError in backend logs
- [ ] Execution count visible in dork details

**Terminal Test:**
```bash
python manage.py shell -c "from googledorks.models import GoogleDork; d = GoogleDork.objects.first(); print(f'Has execution_count: {hasattr(d, \"execution_count\")}'); print(f'Value: {d.execution_count}')"
```

**✅ Pass Criteria:** execution_count exists and works

---

### Test 9.4: Difficulty Null Check
**Bug Fixed:** Cannot read properties of undefined (reading 'toLowerCase')  
**Test:**
- [ ] View dork with undefined difficulty
- [ ] No TypeError in console
- [ ] Difficulty badge shows default (gray)

**✅ Pass Criteria:** No difficulty errors

---

### Test 9.5: Serializer Fields
**Bug Fixed:** execution_count not in Meta.fields  
**Test:**
- [ ] View any dork detail page
- [ ] No 500 error
- [ ] Dork data serializes correctly

**✅ Pass Criteria:** Dorks serialize without errors

---

### Test 9.6: Entity Ownership
**Bug Fixed:** Entities belonged to testuser  
**Test:**
- [ ] Logged in as "Major"
- [ ] Can see all 9 test entities
- [ ] NOT showing "No entities found"

**Terminal Verify:**
```bash
python manage.py shell -c "from googledorks.models_entity import Entity; from django.contrib.auth.models import User; major = User.objects.get(username='Major'); print(f'Major owns {Entity.objects.filter(created_by=major).count()} entities')"
```

**✅ Pass Criteria:** Major owns all test entities

---

### Test 9.7: TypeScript Types
**Bug Fixed:** Missing GoogleDork interface fields  
**Test:**
- [ ] No TypeScript compilation errors
- [ ] Frontend builds without warnings
- [ ] All dork properties accessible

**✅ Pass Criteria:** 0 TypeScript errors

---

## 🧪 Test Suite 10: Performance & UX

### Test 10.1: Page Load Times
**Expected:**
- [ ] Entities page loads < 2 seconds
- [ ] Entity detail loads < 1 second
- [ ] Dorks page loads < 2 seconds
- [ ] Graph renders < 3 seconds

**Test Steps:**
1. Open DevTools Network tab
2. Hard refresh each page
3. Note load times

**✅ Pass Criteria:** Reasonable load times

---

### Test 10.2: Console Errors
**Expected:**
- [ ] 0 console errors on any page
- [ ] 0 console warnings (or only minor ones)

**Test Steps:**
1. Open console (F12)
2. Navigate through all pages
3. Document any errors

**✅ Pass Criteria:** No critical console errors

---

### Test 10.3: Responsive Design
**Expected:**
- [ ] Pages render on mobile (375px)
- [ ] Pages render on tablet (768px)
- [ ] Pages render on desktop (1920px)
- [ ] Navigation accessible on mobile

**Test Steps:**
1. Open DevTools
2. Toggle device toolbar
3. Test different screen sizes

**✅ Pass Criteria:** Responsive layout works

---

### Test 10.4: Browser Compatibility
**Expected:**
- [ ] Works on Chrome/Edge
- [ ] Works on Firefox
- [ ] Works on Safari (if available)

**Test Steps:**
1. Test in each browser
2. Document any issues

**✅ Pass Criteria:** Works in major browsers

---

## 📊 Test Results Summary Template

```markdown
## Test Results: [Date]

### Overall Status: [PASS/FAIL/PARTIAL]

### Test Suites Passed: X/10

### Critical Issues Found: X
1. [Issue description]
2. [Issue description]

### Minor Issues Found: X
1. [Issue description]
2. [Issue description]

### Performance Notes:
- Average page load: X seconds
- Graph render time: X seconds
- API response time: X ms

### Browser Tested:
- [ ] Chrome/Edge
- [ ] Firefox
- [ ] Safari

### Recommendations:
1. [Recommendation]
2. [Recommendation]

### Next Steps:
1. [Action item]
2. [Action item]
```

---

## 🎯 Quick Start Testing

### Fastest Path (15 minutes):
1. ✅ Test Suite 1.1-1.2 (Entity list & detail)
2. ✅ Test Suite 5.1-5.3 (Dorks list, detail, execute)
3. ✅ Test Suite 8.1 (Graph visualization)
4. ✅ Test Suite 9 (All bug fixes)

### Comprehensive Testing (60 minutes):
- Run all 10 test suites in order
- Document results
- Take screenshots of issues
- Create test results report

---

## 📝 Testing Notes

**Test Environment:**
- OS: Windows
- Python: 3.13
- Django: 5.2.6
- Node: [Check version]
- Browser: [Check version]

**Test Data:**
- 9 test entities
- 2 relationships
- 7 attributes
- Multiple dorks in database

**Known Limitations:**
- None (all bugs fixed!)

---

## ✅ Success Criteria

**Testing Complete When:**
1. All 10 test suites executed
2. All bug fixes verified working
3. Test results documented
4. Any issues found are logged
5. Recommendations created

**Framework Ready for 90% When:**
- All tests pass
- No critical issues
- Performance acceptable
- Sub-forms implemented (next feature)

---

**Happy Testing! 🧪🚀**
