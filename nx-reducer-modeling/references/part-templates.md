# Part Modeling Templates

## Solid Gear (实心式, da < 120mm)

3 steps:
```
1. Solid cylinder ∅da × B (毛坯)
2. Subtract bore cylinder ∅d_bore × B (轮毂孔)
3. Subtract keyway block b×(t2+1.5)×B (键槽, 矩形块)
```
- After script: user adds gear teeth via NX GC Toolkit (齿轮建模→圆柱齿轮)
- After script: user adds Edge Blend R=b/2 to keyway ends

## Web Gear (腹板式, da 120-500mm)

6 steps:
```
1. Solid cylinder ∅da × B (毛坯)
2. Subtract bore cylinder ∅d_bore × B (轮毂孔)
3. Create left gap ring: ∅RIM_ID - ∅D_hub, length = (B-c)/2
4. Create right gap ring: same, positioned at other end
5. Subtract lightening holes: n×∅d0 at PCD=(D_hub+RIM_ID)/2
6. Subtract keyway block b×(t2+1.5)×B
```
Where:
- δ = 2.5m (rim thickness)
- RIM_ID = df - 2δ
- D_hub = d_bore × 1.6
- c = 0.3B (web thickness)
- d0 ≈ 25-35mm, n = 4-6

## Stepped Shaft (阶梯轴)

N segments, each a cylinder united along X:
```
1. Cylinder seg1: ∅d1 × l1 at origin
2. For i=2..N: Cylinder seg_i: ∅di × li at X=∑(l1..li-1), Unite
3. Keyway: Block + 2 Cylinders for round ends, Subtract
4. Center holes: Cylinder ∅5×8 at both ends, Subtract
5. Chamfer: skip (GUI manual, UF has label warnings)
```

## Gear Shaft (齿轮轴, da ≈ shaft diameter)

Same as stepped shaft, but the gear segment is integral:
- Gear segment is part of the cylinder chain (same Unite pattern)
- After script: user adds gear teeth via NX GC Toolkit
- Gear section stays as da-diameter cylinder for assembly reference

## End Cap (轴承端盖)

Both through and blind caps:
```
1. Flange cylinder: ∅D_flange × t_flange
2. Fit boss cylinder: ∅D_fit × t_fit at X=t_flange, Unite
3. Bolt holes: N×∅d_bolt through flange, Subtract
4. (Through cap only): Central bore ∅(shaft_d+1) through all, Subtract
```
Where:
- D_flange ≈ bearing_OD × 1.6
- D_fit = bearing_OD (fits into housing bore)
- Bolt PCD ≈ bearing_OD + 16~20mm
- t_fit ≈ 0.7 × bearing_width
- d_bolt = 8.5 (M8 clearance)
