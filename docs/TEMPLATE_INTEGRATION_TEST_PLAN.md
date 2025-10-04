# 🧪 Template Integration Testing Plan

## 🎯 Test Objective
Verify the complete Template Integration feature workflow from template selection to results viewing.

## 🖥️ Prerequisites
✅ Django server running on port 8000
✅ Vite dev server running on port 5173
✅ At least one entity in database
✅ Search templates seeded in database

## 📋 Test Cases

### Test Case 1: Navigate to Templates Tab ⭐ CRITICAL
**Steps:**
1. Open browser to `http://localhost:5173`
2. Login if required
3. Navigate to Entities list
4. Click on any entity
5. Look for the tabs at the top
6. Click on `🎯 Templates` tab

**Expected Results:**
- ✅ Templates tab is visible (6th tab)
- ✅ Tab has 🎯 icon
- ✅ Tab content loads without errors
- ✅ Component renders properly

**Pass/Fail:** ⬜

---

### Test Case 2: View Template List ⭐ CRITICAL
**Steps:**
1. From Templates tab
2. Observe the template cards displayed

**Expected Results:**
- ✅ Templates filtered by entity type show
- ✅ Header shows count: "X templates available for [entity_type]"
- ✅ Templates displayed in 2-column grid
- ✅ Each template card shows:
  - Template name
  - Description
  - Risk level badge (colored)
  - Category badge
  - Original template query (gray background)
  - Generated query (blue background)
  - Usage tips (yellow box, if available)
  - Expected results text (if available)
  - Execute Search button

**Pass/Fail:** ⬜

**Screenshot Location:** _____________________

---

### Test Case 3: Verify Query Generation ⭐ CRITICAL
**Steps:**
1. Look at a template card
2. Compare "Template:" section with "Generated Query:" section
3. Verify placeholders are replaced

**Example:**
```
Template: site:{domain} "contact"
Entity: Acme Corp (website: https://acme.com)
Generated: site:acme.com "contact"
```

**Expected Results:**
- ✅ {name} replaced with entity name
- ✅ {domain} replaced with domain from website
- ✅ {location} replaced with entity location
- ✅ {industry} replaced with entity industry
- ✅ No placeholders remain in generated query
- ✅ Generated query looks valid

**Pass/Fail:** ⬜

---

### Test Case 4: Risk Level Badges ⭐ MEDIUM
**Steps:**
1. Look at risk level badges on different templates
2. Check colors and icons

**Expected Results:**
- ✅ LOW: Green background, ✓ icon
- ✅ MEDIUM: Yellow background, ⚠ icon
- ✅ HIGH: Orange background, ⚠️ icon
- ✅ CRITICAL: Red background, 🔴 icon

**Pass/Fail:** ⬜

---

### Test Case 5: Category Filter (if multiple categories exist) ⭐ MEDIUM
**Steps:**
1. Check if category dropdown appears (top right)
2. If visible, click dropdown
3. Select a category
4. Observe template list

**Expected Results:**
- ✅ Dropdown appears if 2+ categories exist
- ✅ Dropdown shows "All Categories" + category names
- ✅ Selecting category filters templates
- ✅ Template count updates
- ✅ Only templates from selected category show
- ✅ "All Categories" shows all templates again

**Pass/Fail:** ⬜

---

### Test Case 6: Execute Search - Happy Path ⭐⭐ CRITICAL
**Steps:**
1. Click "🔍 Execute Search" button on any template
2. Observe button state
3. Wait for completion
4. Check for success message

**Expected Results:**
- ✅ Button shows loading spinner
- ✅ Button text changes to "Executing..."
- ✅ Button is disabled during execution
- ✅ After ~1-2 seconds, green success message appears
- ✅ Message: "✅ Search session created successfully! Check the Search Results tab to view results."
- ✅ No errors in browser console (F12)

**Pass/Fail:** ⬜

**Console Errors (if any):** _____________________

---

### Test Case 7: Navigate to Search Results Tab ⭐⭐ CRITICAL
**Steps:**
1. After executing search (Test Case 6)
2. Click on `🔍 Search Results` tab

**Expected Results:**
- ✅ Tab switches to Search Results
- ✅ New search session appears at top of list
- ✅ Session shows:
  - Template name
  - Status badge (PENDING or COMPLETED)
  - Executed query in code block
  - Metadata (user, timestamp)
  - Result count badge (e.g., "5 results")

**Pass/Fail:** ⬜

**Screenshot Location:** _____________________

---

### Test Case 8: View Session Details (Collapsible) ⭐⭐ CRITICAL
**Steps:**
1. From Search Results tab
2. Click on a completed search session card
3. Observe expansion
4. Click again to collapse

**Expected Results:**
- ✅ Session expands on first click
- ✅ Shows "Search Results (X)" section
- ✅ Individual results displayed with:
  - Title (clickable link)
  - URL
  - Snippet/description
  - Position number
  - Relevance score
  - Verification status (checkmark if verified)
  - Notes (if any)
- ✅ Session collapses on second click
- ✅ Smooth animation

**Pass/Fail:** ⬜

---

### Test Case 9: Session Status Indicators ⭐ MEDIUM
**Steps:**
1. Look at session status badges
2. Check colors

**Expected Results:**
- ✅ PENDING: Yellow badge "⏳ Search is pending execution"
- ✅ RUNNING: Blue badge with loading message
- ✅ COMPLETED: Green badge
- ✅ FAILED: Red badge "❌ Search failed"

**Pass/Fail:** ⬜

---

### Test Case 10: Click Search Result Link ⭐ MEDIUM
**Steps:**
1. Expand a completed session (Test Case 8)
2. Click on a result title link

**Expected Results:**
- ✅ Opens in new browser tab
- ✅ URL matches the result URL
- ✅ Link opens successfully

**Pass/Fail:** ⬜

---

### Test Case 11: Execute Multiple Templates ⭐ HIGH
**Steps:**
1. Go back to Templates tab
2. Execute 2-3 different templates
3. Go to Search Results tab
4. Observe session list

**Expected Results:**
- ✅ All executed templates appear as separate sessions
- ✅ Sessions ordered by most recent first
- ✅ Each session independent and collapsible
- ✅ Can expand/collapse any session
- ✅ No interference between sessions

**Pass/Fail:** ⬜

---

### Test Case 12: Empty State (No Sessions Yet) ⭐ LOW
**Steps:**
1. Test with fresh entity (no searches executed)
2. Navigate to Search Results tab

**Expected Results:**
- ✅ Shows empty state message
- ✅ Icon displayed (🔍 or similar)
- ✅ Message: "No search sessions yet"
- ✅ Helpful text: "Go to Templates tab to execute searches"

**Pass/Fail:** ⬜

---

### Test Case 13: Template with Different Entity Types ⭐ HIGH
**Steps:**
1. Navigate to different entity types:
   - Person entity
   - Company entity
   - Website entity (if available)
2. Check Templates tab for each

**Expected Results:**
- ✅ Templates filtered by entity type
- ✅ Company entity shows company templates
- ✅ Person entity shows person templates
- ✅ Queries generate correctly for each type
- ✅ Different placeholders work: {name}, {domain}, {location}, etc.

**Pass/Fail:** ⬜

---

### Test Case 14: No Templates Available ⭐ LOW
**Steps:**
1. Test with entity type that has no templates
2. Navigate to Templates tab

**Expected Results:**
- ✅ Shows empty state
- ✅ Icon: 🔍
- ✅ Message: "No Templates Available"
- ✅ Helpful text explaining why

**Pass/Fail:** ⬜

---

### Test Case 15: Error Handling ⭐ MEDIUM
**Steps:**
1. Disconnect internet or stop Django server
2. Try to execute search
3. Observe error handling

**Expected Results:**
- ✅ Red error message appears
- ✅ Message: "❌ Failed to execute search. Please try again."
- ✅ Button re-enables after error
- ✅ Can retry
- ✅ No crash or white screen

**Pass/Fail:** ⬜

---

### Test Case 16: Loading States ⭐ MEDIUM
**Steps:**
1. Navigate to Templates tab
2. Observe initial load
3. Navigate to Search Results tab
4. Observe session list load

**Expected Results:**
- ✅ Loading spinner shows while fetching templates
- ✅ Loading spinner shows while fetching sessions
- ✅ Smooth transition from loading to content
- ✅ No flickering or layout shifts

**Pass/Fail:** ⬜

---

### Test Case 17: UI Responsiveness ⭐ MEDIUM
**Steps:**
1. Resize browser window
2. Test mobile view (DevTools mobile emulation)
3. Check tablet view

**Expected Results:**
- ✅ Desktop: 2-column grid for templates
- ✅ Mobile: 1-column grid (stacked)
- ✅ All text readable
- ✅ Buttons accessible
- ✅ No horizontal scrolling
- ✅ Cards don't overflow

**Pass/Fail:** ⬜

---

### Test Case 18: Browser Console Check ⭐⭐ CRITICAL
**Steps:**
1. Open Browser DevTools (F12)
2. Go to Console tab
3. Perform all actions above
4. Monitor for errors

**Expected Results:**
- ✅ No TypeScript errors
- ✅ No React warnings
- ✅ No API errors (except intentional test)
- ✅ No 404 errors
- ✅ Clean console output

**Pass/Fail:** ⬜

**Errors Found:** _____________________

---

### Test Case 19: API Network Requests ⭐ HIGH
**Steps:**
1. Open DevTools Network tab
2. Execute a search
3. Observe API calls

**Expected Results:**
- ✅ GET `/api/dorks/entity-search-templates/?entity_type=X` - Status 200
- ✅ POST `/api/dorks/entity-search-sessions/` - Status 201
- ✅ GET `/api/dorks/entities/:id/search_sessions/` - Status 200
- ✅ GET `/api/dorks/entity-search-sessions/:id/results/` - Status 200
- ✅ Request payloads correct
- ✅ Response data valid

**Pass/Fail:** ⬜

---

### Test Case 20: Session Metadata Accuracy ⭐ MEDIUM
**Steps:**
1. Execute a search
2. View session in Search Results tab
3. Check metadata

**Expected Results:**
- ✅ Session name: "[Template Name] - [Entity Name]"
- ✅ Shows current user
- ✅ Timestamp accurate (within 1 minute)
- ✅ Result count matches actual results
- ✅ Executed query matches generated query

**Pass/Fail:** ⬜

---

## 📊 Test Summary

**Total Test Cases:** 20
**Critical:** 8
**High:** 3
**Medium:** 8
**Low:** 1

**Passed:** _____ / 20
**Failed:** _____ / 20
**Blocked:** _____ / 20

## ✅ Pass Criteria
- All CRITICAL tests must pass
- At least 90% of HIGH tests must pass
- At least 75% of MEDIUM tests must pass
- No blocking bugs

## 🐛 Bugs Found

### Bug #1
**Title:** _____________________
**Severity:** Critical / High / Medium / Low
**Steps to Reproduce:**
1. 
2. 
3. 

**Expected:** _____________________
**Actual:** _____________________
**Screenshot:** _____________________

---

## 🎯 Quick Test Checklist (5 Minutes)

For rapid verification:
- [ ] Templates tab visible and loads
- [ ] Template cards display properly
- [ ] Query generation works (placeholders replaced)
- [ ] Execute button works
- [ ] Success message appears
- [ ] Search Results tab shows session
- [ ] Session expands/collapses
- [ ] No console errors
- [ ] No visual glitches

## 🚀 Next Steps After Testing

### If All Tests Pass:
1. ✅ Mark Template Integration as COMPLETE
2. 🎉 Celebrate achievement
3. 📋 Choose next feature:
   - Option A: Relationship Visualization
   - Option B: Sub-Forms (Attributes/Relationships/Notes)
   - Option C: Batch Template Execution
   - Option D: Advanced Search Features

### If Tests Fail:
1. 🐛 Document bugs in detail
2. 🔧 Prioritize by severity
3. 💻 Fix critical/high bugs first
4. 🔄 Re-test after fixes

---

**Tester:** _____________________
**Date:** October 3, 2025
**Browser:** Chrome / Firefox / Safari / Edge
**Version:** _____________________
**Test Duration:** _____ minutes

**Overall Result:** ✅ PASS / ❌ FAIL / ⚠️ PARTIAL

**Notes:**
_____________________
_____________________
_____________________
