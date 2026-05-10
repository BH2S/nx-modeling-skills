---
name: cad-vision
description: >
  Visual analysis of 3D CAD models using AI vision models. Use this skill whenever the user shows you CAD screenshots, wants to compare a model against design specs, needs to verify part shapes, or mentions using vision to understand 3D geometry. Works with NX three-view drawings, isometric views, or any CAD screenshot. Integrates with the vision.sh pipeline for automated image analysis. Use this skill when the user says "看看这个模型", "分析三视图", "截图对比", or references comparing models to drawings.
---

# CAD Vision Analysis

Use AI vision models to "see" and analyze 3D CAD models from screenshots.

## When to Use

- User shares a CAD screenshot and asks if it looks right
- Need to compare a modeled part against design specifications
- Want to understand 3D spatial relationships from 2D views
- Debugging "why does my model look wrong?"
- Verifying assembly fit from visual inspection

## Pipeline

### Step 1: Get the Screenshot

In NX, the user should:
1. Open the part or assembly
2. Create a drawing sheet: File → New → Drawing → A3 or A4
3. Add views: Base View → Front, Top, Right (三视图)
4. Add Isometric view
5. Screenshot the drawing sheet

For simpler checks, a single isometric view screenshot works.

### Step 2: Run Vision Analysis

Use the vision.sh script:
```bash
bash <vision-script-path>/vision.sh <screenshot_path> <model_name>
```

**Model selection by task:**
| Task | Model | Why |
|------|-------|-----|
| Quick shape check | claude-haiku-4-5 | Fast, cheap (~3000 images/元) |
| Dimension reading | claude-sonnet-4-6 | Better OCR for numbers |
| Detailed comparison | claude-sonnet-4-6 | Higher accuracy |

**API details** in `references/vision-api.md`.

### Step 3: Analyze Results

Compare vision output against design spec:

```
Checklist:
□ Overall proportions match expected dimensions
□ Feature positions correct (bearing seats at right Y, bolts at right positions)
□ No geometry protruding where it shouldn't (ribs piercing flanges)
□ Bolt holes present and correctly positioned
□ Bosses and ribs properly sized relative to body
□ No obviously missing features (drain hole, oil level boss, etc.)
```

### Step 4: Report + Fix

Present findings in this format:

```
| Issue | Location | Severity | Fix |
|-------|----------|----------|-----|
| Rib protrudes above flange | Bearing boss rib #3 | High | Reduce rib height by 15mm |
```

Then modify the NX Open Python script coordinates and rebuild.

## Three-View Analysis Protocol

For full spatial understanding, use three orthogonal views:

### Front View (XY Plane)
- Check: shaft center distances, bearing bore alignment
- Verify: overall width and height
- Look for: symmetry issues

### Top View (XZ Plane)
- Check: shaft parallelism, gear overlap
- Verify: housing length, wall thickness
- Look for: bolt hole patterns

### Side View (YZ Plane)
- Check: shaft Z positions, split plane alignment
- Verify: bearing boss protrusion
- Look for: rib depth, flange thickness

## Common Shape Issues Detected by Vision

- **Rib piercing**: Rib extends beyond intended boundary
- **Boss mismatch**: Bearing boss too large/small relative to bore
- **Flange gap**: Flange doesn't cover full perimeter
- **Hole offset**: Bolt hole pattern not centered on flange
- **Proportion error**: Overall part looks "stretched" or "squashed"
- **Missing feature**: Drain hole, lifting lug, inspection window absent
