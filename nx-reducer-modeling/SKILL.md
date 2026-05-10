---
name: nx-reducer-modeling
description: >
  NX Open Python automation for spur gear reducer modeling. Use this skill when the user mentions NX modeling, reducer parts (shafts, gears, housings, end caps), NX Open Python scripting, or wants to automate CAD part creation. Covers the full workflow: parameter extraction from design specs, structure type selection, script writing with proven APIs (two-step Boolean, Cylinder/Block/Boolean builders), pre-run checklists, and memory/task list updates. Includes verified API reference and pitfall documentation from real NX2312 headless modeling experience.
---

# NX Reducer Modeling

Automated NX part modeling for two-stage spur gear reducers via NX Open Python scripts.

## When to Use

Trigger this skill whenever the user:
- Mentions modeling any reducer part (shaft, gear, housing, end cap, attachment)
- Asks to "build", "create", or "model" a mechanical part in NX
- References their design specification document
- Wants to automate CAD part creation
- Asks about NX Open Python API capabilities

## Environment

Configure these paths for your setup:

- **NX Version**: Siemens NX 2312 (adjust for your version)
- **Python**: Your conda/venv Python with NX Open access
- **NX Open DLL**: `<NX-install-dir>/NXBIN`
- **Run command**:
  ```bash
  export PATH="<NX-install-dir>/NXBIN:$PATH"
  export PYTHONPATH="<NX-install-dir>/NXBIN/python"
  <python-env>/python script.py
  ```
- **Memory system**: L1/L2/L3 layered markdown files with a MEMORY.md routing index
- **Output directory**: Where .prt files and task list are saved
- **Design spec**: Path to the design specification .docx file

## Core Workflow

Follow this 9-step process for every part:

### Step 1: Read Design Spec

Extract key parameters from the design specification document. Use python-docx or zipfile to parse the .docx file. The spec contains tables (Table 5-7 for shafts, Table 3-4 for gears, Table 11 for housing).

### Step 2: Determine Structure Type

| Part Type | Sub-types |
|-----------|-----------|
| Shaft | Stepped shaft (7-segment, 5-segment) / Gear shaft (pinion integral) |
| Gear | Solid type (da < 120mm, 3 steps) / Web type (腹板式, da > 120mm, 6 steps) |
| End Cap | Through cap (透盖, with shaft bore) / Blind cap (闷盖, solid) |
| Housing | Lower (箱座) / Upper (箱盖) — complex, may need GUI assist |

### Step 3: Read Relevant Memory

Before writing code, load from your memory directory:
- `ug-nx.md` — verified APIs, pitfall lessons, Boolean rules
- `reducer-project.md` — current project parameters and progress

**Key rules to internalize:**
- Point3d requires ALL float arguments (never int)
- Two-step Boolean: Create independent body → BooleanBuilder (never one-step Subtract)
- No chamfers in script (UF labels cause warnings; user does in GUI)
- No gear teeth in script (NX GC Toolkit handles involute profiles; user does in GUI)
- `SetTwoDiagonalPoints` creates axis-aligned boxes — cannot rotate via coordinate math
- For holes: "flange first, drill, then unite" pattern to avoid "tool outside target"

### Step 4: Write the Script

Use this template skeleton:
```python
import NXOpen, os, math
SAVE = r"G:\作业\建模\result_OUTPUT_DIR\part_name.prt"
FBT = NXOpen.Features.Feature.BooleanType  # for BooleanBuilder
BO = NXOpen.GeometricUtilities.BooleanOperation.BooleanType  # for feature builders

def cyl(wp, d, h, origin, direction):
    """Create standalone cylinder body (no Boolean)."""
    c = wp.Features.CreateCylinderBuilder(None)
    c.Diameter.RightHandSide = str(d)
    c.Height.RightHandSide = str(h)
    c.Direction = direction; c.Origin = origin
    c.BooleanOption.Type = BO.Create
    f = c.Commit(); b = f.GetBodies()[0]; c.Destroy()
    return b

def blk(wp, x, y, z, lx, ly, lz):
    """Create standalone block body (no Boolean)."""
    b = wp.Features.CreateBlockFeatureBuilder(None)
    b.SetOriginAndLengths(NXOpen.Point3d(x, y, z), str(lx), str(ly), str(lz))
    b.BooleanOption.Type = BO.Create
    f = b.Commit(); r = f.GetBodies()[0]; b.Destroy()
    return r

def bool_op(wp, target, tool, operation):
    """Two-step Boolean: Create independent body → BooleanBuilder."""
    bb = wp.Features.CreateBooleanBuilder(None)
    bb.Operation = operation; bb.Target = target; bb.Tool = tool
    f = bb.Commit(); r = f.GetBodies()[0]; bb.Destroy()
    return r

def main():
    s = NXOpen.Session.GetSession()
    wp = s.Parts.NewDisplay("model-plain-1-mm-template.prt",
                            NXOpen.Part.Units.Millimeters)
    if not wp: return
    # ... build geometry ...
    out_dir = os.path.dirname(SAVE)
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    if os.path.exists(SAVE): os.remove(SAVE)
    wp.SaveAs(SAVE)
    print(f"Saved: {SAVE}")

if __name__ == "__main__":
    main()
```

### Step 5: Pre-Run Checklist

Verify before executing:
- [ ] All coordinates are float (`.0` suffix for round numbers)
- [ ] Two-step Boolean pattern used throughout (not one-step)
- [ ] No chamfer code (UF creates label warnings)
- [ ] No gear tooth code (user does via GC Toolkit)
- [ ] Assembly interfaces match (bore diameter = shaft diameter, keyway = GB/T 1095 for given shaft d)
- [ ] Flange holes drilled BEFORE uniting flange to body
- [ ] Save path exists or can be created

### Step 6: Run

Execute via bash with the command shown in Environment section. NX must be running. Watch for:
- `NXOpen.NXException: Tool body completely outside target body` → tool doesn't overlap target
- `Expecting double type, found int` → you used int where float needed
- `No overload matches` → wrong argument types

See `references/api-reference.md` for detailed API documentation.

### Step 7: Verify Against Spec

After successful run, verify key parameters against the design spec:
- Shafts: segment diameters and lengths
- Gears: da, df, B, bore diameter
- End caps: flange OD, fit diameter, bolt PCD

### Step 8: Update Task List

Edit `your-output-directory/建模任务清单.txt`:
- Change `[ ]` to `[X]` for completed part
- Add file name and script name
- Update progress summary counts

### Step 9: Update Memory

Edit `your-memory-directory/reducer-project.md` and `ug-nx.md`:
- Update completion status
- Add any new lessons learned
- Flag any API discoveries (both successes and failures)

## Workflow Templates by Part Type

See `references/part-templates.md` for detailed step-by-step workflows for each part type.

## Validated APIs

Read `references/api-reference.md` for the complete verified/unverified API list.

## Key Pitfalls — Read Before Writing Any Code

Each pitfall cost hours. The WHY matters more than the rule.

### 1. One-Step Boolean SILENTLY Fails
`BooleanOption.Subtract` + `SetTargetBodies` → Commit returns OK. But material was NOT removed — the tool body protrudes from the surface. **Rule**: Always two-step (Create independent body → BooleanBuilder). **Symptom**: "Lumpy" model, unexpected protrusions, file too large.

### 2. Point3d Rejects int
`Point3d(0, 0, 0)` with Python ints → cryptic error. **Why**: NX bindings require strict float. **Rule**: Every coordinate must be `0.` not `0`.

### 3. SetTwoDiagonalPoints = Axis-Aligned Forever
Trig-rotated corner positions still produce world-aligned boxes. The rotation math does nothing. **Rule**: For angled features, use cylinders along axis at correct radial position. **Symptom**: Parts look twisted.

### 4. UF Chamfer → Label Warnings
Geometry correct, but NX can't name the feature. **Rule**: Skip chamfers in scripts, user adds via GUI.

### 5. Flange Holes: Drill Before Unite
Drilling already-united flange → "Tool body completely outside target body". **Rule**: Drill standalone flange, then unite to body.

### 6. Headless NX2312 Limits
EdgeBlend crashes, Draft unsettable, Shell/Hole/Extrude unavailable. Accept these limits — don't waste hours re-probing.
