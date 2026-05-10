# nx-modeling-skills

Claude Code Skills for mechanical CAD automation — developed through real-world reducer modeling on Siemens NX 2312.

## Skills

### `nx-reducer-modeling`
NX Open Python automation for spur gear reducer part modeling. Covers shafts, gears, end caps, and housing with a proven 9-step workflow: parameter extraction → structure selection → script writing with verified APIs → pre-run checklist → execution → verification → task/memory updates.

**When to use:** NX modeling, reducer parts, CAD automation, NX Open scripting.

### `cad-vision`
AI vision model analysis of 3D CAD screenshots. Uses Claude vision models (Haiku/Sonnet) to analyze three-view drawings, detect shape issues, and compare models against design specs.

**When to use:** CAD screenshot analysis, three-view comparison, shape verification, spatial understanding.

## Installation

Copy the skill folders to your Claude Code skills directory:
```
~/.claude/skills/nx-reducer-modeling/
~/.claude/skills/cad-vision/
```

Or install via:
```
/plugin install nx-reducer-modeling@<path>
/plugin install cad-vision@<path>
```

## Background

These skills capture the workflow and lessons learned from building a complete two-stage spur gear reducer (展开式二级直齿圆柱齿轮减速器) with NX2312:

- **Parameters**: F=2450N, v=1.25m/s, D=350mm, motor Y132M1-6 (4kW, 960r/min)
- **Center distances**: a1=129mm, a2=159mm, total ratio i=14.074
- **Parts modeled**: 12+ .prt files (3 shafts, 3 gears, 6 end caps, 2 housings, 6 attachments)
- **Key discovery**: NX Open Python in headless NX2312 has severe limitations — only Cylinder, Block, and Boolean builders work reliably; Sketch/Extrude/Shell/EdgeBlend are broken or incomplete

## Key Technical Lessons

1. **Two-step Boolean is mandatory**: `BooleanOption.Subtract` silently fails. Always create independent body → BooleanBuilder.
2. **Point3d requires float**: Passing int causes cryptic errors.
3. **Headless NX2312 limits**: Extrude section integration broken, EdgeBlend memory-violates, Draft angle unsettable.
4. **Blind coordinate stacking fails for complex parts**: Cylinders+blocks work for rotational parts (shafts, gears) but not for cast housings.

## File Structure

```
nx-modeling/
├── README.md
├── nx-reducer-modeling/
│   ├── SKILL.md                          # Main skill instructions
│   └── references/
│       ├── api-reference.md              # Verified/unusable NX Open API list
│       └── part-templates.md             # Step-by-step per part type
└── cad-vision/
    ├── SKILL.md                          # Main skill instructions
    └── references/
        └── vision-api.md                 # Vision API and model reference
```

## Companion

Pair with [AgentMemory](https://github.com/BH2S/AgentMemory) for persistent cross-session memory management.
