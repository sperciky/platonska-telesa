# Step 18 Variants - Enhanced Angle Proof Visualizations

Three different approaches to visualizing the mathematical proof that only 5 Platonic solids can exist.

## Overview

All three variants prove the same mathematical fact using the **angle constraint**:
- Each vertex must connect ≥3 faces (otherwise it's not a 3D solid)
- The sum of angles at a vertex must be **< 360°** (otherwise it's flat or impossible)

---

## 📊 Step 18a: Kruhové měřidlo (Circular Angle Meters)

**File:** `steps/definitions/bonus_why_five_18a.py`

**Visualization:** Side-by-side comparison
- **Left column:** Polygons meeting at a shared vertex (current style from step 17)
- **Right column:** Circular "angle meter" showing how the angles fill 360°
  - Green filled arc: angles used (< 360° = valid ✅)
  - Gray dashed circle: 360° boundary
  - Red overflow: if sum > 360° ❌

**Best for:** Visual learners who need to "see" the angle constraint as a physical limitation.

**Layout:** 9 rows × 2 columns (18 total subplots)

**Key features:**
- Clear visual representation of "angle budget" (360°)
- Shows valid configurations in green, invalid in red
- Displays Platonic solid names for valid cases
- Height: 2000px (tall, scrollable)

---

## 📋 Step 18b: Tabulka (Interactive Table)

**File:** `steps/definitions/bonus_why_five_18b.py`

**Visualization:** Comprehensive data table
- Columns: Polygon | Internal Angle | Count | Sum | Status | Platonic Solid
- Color-coded rows:
  - Green: Valid (< 360°) → forms Platonic solid ✅
  - Red: Invalid (≥ 360°) → flat plane or impossible ❌
- Includes all cases from triangles through higher polygons

**Best for:** Systematic thinkers who prefer organized data and logical progression.

**Layout:** Single interactive table with 15 rows

**Key features:**
- Systematic exploration of all possibilities
- Easy to scan and compare
- Mathematical formulas shown explicitly
- Annotation box explains the proof logic
- Height: 900px (compact)

---

## 🔄 Step 18c: Vývojový diagram (Flow Diagram)

**File:** `steps/definitions/bonus_why_five_18c.py`

**Visualization:** Logical flow chart
- **Top:** Definition and conditions
- **Middle:** Formula for internal angles
- **Main section:** Each polygon type with all possible counts (3, 4, 5, 6)
  - Green boxes: Valid combinations → Platonic solid ✅
  - Red boxes: Invalid combinations ❌
- **Bottom:** Final conclusion

**Best for:** Understanding the **logical progression** of the proof step-by-step.

**Layout:** Vertical flow with arrows connecting boxes

**Key features:**
- Shows the reasoning process
- Arrows guide the reader through the logic
- Each polygon type shown with all test cases
- Clear separation between valid and invalid
- Height: 1200px (medium)

---

## 🎯 Comparison Summary

| Feature | 18a (Circular) | 18b (Table) | 18c (Flow) |
|---------|---------------|-------------|------------|
| **Visual style** | Geometric diagrams | Data table | Flow chart |
| **Best for** | Visual learners | Data analysts | Logical thinkers |
| **Information density** | Medium | High | Medium |
| **Interactivity** | Hover tooltips | Hover tooltips | Hover tooltips |
| **Height** | 2000px (tall) | 900px (compact) | 1200px (medium) |
| **Complexity** | Medium | Low | Low-Medium |
| **Angle visualization** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Systematic coverage** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Logical flow** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🚀 Usage

### Generate animations for all three variants:

```bash
cd new/
python generate_animations.py --steps 18
```

This will create:
- `animations/step_18_Bonus.gif` (variant a)
- `animations/step_18_Bonus.gif` (variant b)
- `animations/step_18_Bonus.gif` (variant c)

**Note:** Since all have step number 18, they may overwrite each other. Generate them separately:

```bash
# Generate each separately
python generate_animations.py --steps 18  # Will generate the last one (18c)
```

Or modify the step numbers in the class metadata to be 18, 19, 20 to avoid conflicts.

---

## 📝 Which One to Use?

**Recommendation:** Include **all three** in your presentation!
- Start with **18c (Flow)** to show the logical proof structure
- Then **18a (Circular)** to visualize the angle constraint
- Finally **18b (Table)** for systematic review

This gives your audience three different "lenses" to understand the proof, ensuring comprehension regardless of learning style.

---

## 🔧 Technical Details

All three steps:
- Inherit from `Step` base class
- Implement `render_plotly_diagram()` returning a `go.Figure`
- Use step number `18` (can be changed to avoid conflicts)
- Category: `'Bonus'`
- Include Czech language descriptions via `get_description()`

The visualizations are **2D plots** (not 3D rotating), so they generate **static GIFs** (2-frame format for compatibility).
