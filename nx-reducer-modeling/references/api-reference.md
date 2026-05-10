# NX Open API Reference (NX2312, headless, 2026-05-10)

## Verified Working APIs

### Basic Geometry
| API | Method | Notes |
|-----|--------|-------|
| CreateCylinderBuilder | cyl(dia, height, origin, direction) | Create/Unite/Subtract via BooleanBuilder |
| CreateBlockFeatureBuilder | SetOriginAndLengths(x,y,z,lx,ly,lz) | Also SetTwoDiagonalPoints (axis-aligned!) |
| CreateBooleanBuilder | bool_op(target, tool, operation) | FBT.Unite / FBT.Subtract |

### File Operations
| API | Method | Notes |
|-----|--------|-------|
| Part.NewDisplay | Create from template | Returns Part or None |
| Part.SaveAs | Save with new path | Overwrites if exists |
| Part.Open | Open existing part | Returns (Part, PartLoadStatus) |

### Sketch System
| API | Status | Notes |
|-----|--------|-------|
| Sketches.CreateNewSketchInPlaceBuilder(Sketch.Null) | OK | Creates and activates sketch |
| wp.Curves.CreateLine(Point3d, Point3d) | OK | Draw line in sketch context |
| sketch.AddGeometry(curve, InferConstraintsOption) | OK | Add curve to sketch (single object, not list) |
| sketch.Activate/Deactivate | OK | Must activate before drawing |

### Chamfer
| API | Status | Notes |
|-----|--------|-------|
| UF.Modeling.CreateChamfer(subtype, offset1, offset2, theta, [edge.Tag]) | OK | subtype=1 symmetric. Has label warnings. |
| CreateChamferBuilder | Builder exists | SmartCollector=None in headless, can't select edges |

### Assembly
| API | Status | Notes |
|-----|--------|-------|
| AddComponents([parts], Point3d, Matrix3x3, layer, name, count, fixed) | OK | 7-arg signature cracked |
| Component.ReferenceSet / Unblank / IsBlanked | OK | Visibility control |
| CreateConstraint | Exists | Signature not yet cracked for NX2312 |

### Pattern
| API | Status | Notes |
|-----|--------|-------|
| CreatePatternFeatureBuilder | Exists | FeatureList.Add(Feature) + Commit OK |
| PatternEnum | Read-only | Can't set Circular/Linear in headless |

### Edge Blend (Verified by Claude D, not yet replicated by Claude A)
| API | Status | Notes |
|-----|--------|-------|
| ScRuleFactory.CreateRuleEdgeDumb([edge]) | OK | Creates edge selection rule |
| ScCollector.AddRules([rule]) | OK | Adds rules to collector |
| CreateEdgeBlendBuilder | OK | AddChainset(ScCollector, radius_str) |
| Commit | OK | Verified by Claude D |

## Verified UNUSABLE APIs (headless NX2312)

| API | Failure Mode |
|-----|-------------|
| CreateExtrudeBuilder | Section.AddToSection rejects all curve types |
| CreateHollowBuilder/ShellBuilder | Builder doesn't exist |
| CreateHoleBuilder/HolePackageBuilder | Commit fails ("tool outside target" / "position not found") |
| CreateBossBuilder/RibBuilder | Builder doesn't exist |
| CreateDraftBuilder | No "Angle" attribute, can't set draft angle |
| UF.Modl.CreateExtruded2 | Array dimension mismatch for all direction/limits combos |
| SmartCollector | Always None in headless |

## Boolean Type Enums (DO NOT MIX)

```python
# For feature builders (CreateCylinderBuilder, CreateBlockFeatureBuilder):
GeometricUtilities.BooleanOperation.BooleanType
  .Create   — create standalone body
  .Unite    — unite with target (requires SetTargetBodies)
  .Subtract — subtract from target (requires SetTargetBodies)

# For BooleanBuilder (CreateBooleanBuilder):
Features.Feature.BooleanType
  .Unite    — add tool to target
  .Subtract — remove tool from target
```

## Key Constants

```python
# Direction vectors
X = NXOpen.Vector3d(1., 0., 0.)
Y = NXOpen.Vector3d(0., 1., 0.)
Z = NXOpen.Vector3d(0., 0., 1.)
DOWN = NXOpen.Vector3d(0., 0., -1.)

# UF FeatureSigns for extrude (academic, extrude not working)
UF.Modl.FeatureSigns.NULLSIGN = 0
UF.Modl.FeatureSigns.NO_BOOLEAN = 4
UF.Modl.FeatureSigns.UNITE = 6
UF.Modl.FeatureSigns.SUBTRACT = 7
```

## GB/T 1095 Keyway Depths (Quick Reference)

| Shaft d | b×h | t1 (shaft) | t2 (hub) |
|---------|-----|------------|----------|
| 18 | 6×6 | 3.5 | 2.8 |
| 30 | 10×8 | 5.0 | 3.3 |
| 34 | 10×8 | 5.0 | 3.3 |
| 45 | 14×9 | 5.5 | 3.8 |
| 59 | 18×11 | 7.0 | 4.3 |
