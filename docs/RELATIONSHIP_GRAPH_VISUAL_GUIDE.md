# 🕸️ Relationship Graph - Quick Visual Guide

## 📸 What You'll See

### **Graph Tab Location:**
```
Entity Detail Page
┌─────────────────────────────────────────────────────────┐
│ Acme Corporation                            [Edit] [Del]│
├─────────────────────────────────────────────────────────┤
│ 📋 Overview                                              │
│ 🏷️ Attributes (5)                                       │
│ 🔗 Relationships (12)                                    │
│ 📝 Notes (3)                                            │
│ 🎯 Templates                                            │
│ 🕸️ Graph  ← NEW! Click here                            │
│ 🔍 Search Results (8)                                   │
└─────────────────────────────────────────────────────────┘
```

---

## 🎨 Graph Visualization Example

### **Simple Graph (3 entities):**
```
                    Tech Solutions
                   ┌──────────┐
                   │ 🔷       │
          Partner  │          │  Competitor
    ┌──────────────┤          ├────────────┐
    │              └──────────┘            │
    │                                      │
    ↓                                      ↓
┌──────────┐                         ┌──────────┐
│ 🔷       │                         │ 🔷       │
│          │←────── subsidiary ──────┤          │
│Acme Corp │         (Strong)        │Big Corp  │
│ (CENTER) │                         │          │
└──────────┘                         └──────────┘
   BLUE                                 WHITE
```

### **Complex Graph (7 entities):**
```
        Entity A                Entity B
       ┌────────┐              ┌────────┐
       │   🔷   │              │   🔷   │
       └────────┘              └────────┘
            ↓                       ↓
            │ weak                  │ strong
            │ (green)               │ (red, animated)
            ↓                       ↓
    Entity D         ┌──────────────┐         Entity C
   ┌────────┐        │   CURRENT    │        ┌────────┐
   │   🔷   │←───────┤   ENTITY     │───────→│   🔷   │
   └────────┘ medium │    (BLUE)    │ medium └────────┘
    (amber)          │              │  (amber)
                     └──────────────┘
            ↑                       ↑
            │                       │
            │                       │
       ┌────────┐              ┌────────┐
       │   🔷   │              │   🔷   │
       └────────┘              └────────┘
        Entity E                Entity F

Arranged in a circle around the center!
```

---

## 🎯 Interactive Elements

### **1. Entity Nodes:**
```
┌─────────────────────────┐
│ 🔷 Acme Corporation     │  ← Icon + Name
│ Company                 │  ← Entity Type
│ 5 connections           │  ← Relationship Count
└─────────────────────────┘
```

**Node States:**
- 🔵 **Blue Background**: Current entity (center)
- ⬜ **White Background**: Related entity (clickable)
- 🖱️ **Hover**: Shadow increases
- 👆 **Click**: Navigate to entity

### **2. Relationship Edges:**
```
Entity A ──────→ Entity B
         label
```

**Edge Properties:**
- **Arrow**: Shows direction
- **Label**: Relationship type ("subsidiary", "partner", etc.)
- **Color**: Strength indicator
  - 🟢 Green = Weak (1-4)
  - 🟠 Amber = Medium (5-7)
  - 🔴 Red = Strong (8-10)
- **Width**: Thicker = stronger
- **Animation**: Strong edges (8-10) animate

### **3. Info Panel (Top Left):**
```
┌──────────────────────────┐
│ Relationship Graph       │
│                          │
│ Legend:                  │
│ ■ Current Entity         │
│ □ Related Entities       │
│                          │
│ Strength:                │
│ ─ Weak (1-4)            │
│ ─ Medium (5-7)          │
│ ─ Strong (8-10)         │
└──────────────────────────┘
```

### **4. Stats Panel (Top Right):**
```
┌──────────────────────────┐
│ Total Connections: 12    │
│ Outgoing: 7             │
│ Incoming: 5             │
└──────────────────────────┘
```

### **5. Controls (Bottom Left):**
```
┌──────┐
│  +   │  Zoom In
├──────┤
│  -   │  Zoom Out
├──────┤
│  ⊡   │  Fit View
├──────┤
│  🔒  │  Lock/Unlock
└──────┘
```

### **6. Mini Map (Bottom Right):**
```
┌───────────────┐
│ ┌─────────┐   │  ← Viewport indicator
│ │ ●   ●   │   │  ← Entity dots
│ │   ●●●   │   │
│ │ ●   ●   │   │
│ └─────────┘   │
└───────────────┘
```

### **7. Instructions (Bottom Right):**
```
┌────────────────────────┐
│ 🖱️ Click node to view  │
│ 🔍 Scroll to zoom      │
│ ✋ Drag to pan         │
└────────────────────────┘
```

---

## 🎬 User Actions

### **Action 1: Zoom In/Out**
```
Mouse Wheel Up    → Zoom In  (+ button)
Mouse Wheel Down  → Zoom Out (- button)
```

### **Action 2: Pan View**
```
Click + Drag Canvas → Move view around
```

### **Action 3: Navigate**
```
Click Entity Node → Go to that entity's detail page
```

### **Action 4: Reposition**
```
Click + Drag Node → Move node (temporary)
```

### **Action 5: Fit View**
```
Click Fit View Button → Center and fit all nodes
```

### **Action 6: Mini Map Navigation**
```
Click area in Mini Map → Jump to that area
```

---

## 🎨 Color Coding System

### **Nodes:**
- 🔵 **Blue (#3b82f6)**: Current entity - you are here
- ⚪ **White (#ffffff)**: Related entity - click to explore
- 🌫️ **Gray (#94a3b8)**: Mini map nodes

### **Edges:**
- 🟢 **Green (#10b981)**: Weak relationship (1-4)
- 🟠 **Amber (#f59e0b)**: Medium relationship (5-7)
- 🔴 **Red (#ef4444)**: Strong relationship (8-10)

### **Backgrounds:**
- ⬜ **Light Gray (#f9fafb)**: Canvas background
- 🟦 **Grid (#e5e7eb)**: Grid pattern

---

## 💡 Pro Tips

1. **Find Important Connections**:
   - Look for red (strong) edges
   - These are your most important relationships

2. **Explore Networks**:
   - Click a related entity
   - See its relationships
   - Build mental map of network

3. **Use Mini Map**:
   - Quickly navigate large graphs
   - See overall structure

4. **Fit View First**:
   - Click fit view button
   - See entire graph at once
   - Then zoom into areas of interest

5. **Read Labels**:
   - Edge labels show relationship types
   - Helps understand connections

---

## 📋 Empty State

If entity has no relationships:
```
┌────────────────────────────────────┐
│                                    │
│            🔗                      │
│                                    │
│    No Relationships Found          │
│                                    │
│  This entity doesn't have any      │
│  relationships yet.                │
│                                    │
│  Add relationships in the          │
│  "Relationships" tab to see        │
│  them visualized here.             │
│                                    │
└────────────────────────────────────┘
```

---

## 🐛 Troubleshooting

### **Graph doesn't show:**
- Check entity has relationships
- Look for error message
- Refresh page

### **Nodes overlap:**
- Zoom in to see details
- Drag nodes to reposition
- Use fit view button

### **Can't click node:**
- Make sure it's not the center (blue) node
- Only white nodes are clickable
- Try clicking the entity name text

### **Performance issues:**
- Reduce zoom level
- Limit to entities with <50 relationships
- Consider filtering (future feature)

---

## 🎯 Testing Checklist

Quick 5-minute test:
- [ ] Navigate to entity with relationships
- [ ] Click 🕸️ Graph tab
- [ ] See center node (blue)
- [ ] See related nodes (white)
- [ ] See edges with labels
- [ ] Check color coding (green/amber/red)
- [ ] Zoom in/out works
- [ ] Pan by dragging works
- [ ] Click related node navigates
- [ ] Mini map visible
- [ ] Info panels visible
- [ ] No console errors

---

## 📊 Example Relationships

### **Common Relationship Types:**
- `parent_company` → Parent organization
- `subsidiary` → Owned company
- `partner` → Business partner
- `competitor` → Market competitor
- `vendor` → Supplier
- `client` → Customer
- `affiliated` → General affiliation
- `acquired_by` → Acquisition
- `merged_with` → Merger
- `invested_in` → Investment

---

## 🌟 Benefits

1. **Visual Intelligence**: See connections at a glance
2. **Quick Navigation**: Click to explore network
3. **Strength Analysis**: Color coding shows importance
4. **Network Mapping**: Understand relationships
5. **Investigation Tool**: Follow connections
6. **Pattern Recognition**: Spot clusters and hubs
7. **Presentation Ready**: Share insights visually

---

## 🎊 Success!

You now have an interactive relationship graph that:
✅ Visualizes entity networks
✅ Shows relationship strength
✅ Enables click navigation
✅ Provides interactive exploration
✅ Displays helpful information
✅ Handles edge cases gracefully

**Enjoy exploring your entity networks! 🕸️✨**
