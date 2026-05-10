---
name: memory-system
description: >
  Build and maintain a layered memory system for complex engineering projects. Use when starting a new multi-session project, when the user mentions "记忆", "memory", "记住这个", "lessons learned", or when you need to persist knowledge across sessions. Covers L1/L2/L3 file architecture, routing table design, when-to-save rules, split thresholds, and self-evolution mechanics. NOT for one-shot tasks or simple Q&A.
---

# Memory System for Complex Projects

A layered markdown memory system that gives any AI persistent context across sessions. Designed for engineering projects where details accumulate fast and wrong context is worse than no context.

## Why This Exists

Without memory, every new session starts blind. With memory done wrong, stale data misleads. This system optimizes for two things: **retrieval speed** (hit the right file in ≤2 steps) and **accuracy** (stale information self-destructs).

## Architecture: L1 → L2 → L3

```
L1 (always hot, <50 lines total)
  ├── MEMORY.md     — routing index + trigger words
  └── user-profile.md — environment, preferences, constraints

L2 (domain-triggered, loaded on keyword match)
  ├── conventions.md    — coding standards, build commands
  ├── lessons.md        — pitfall index, routes to L3
  └── project-status.md — current state, what's done/pending

L3 (deep reference, loaded on specific need)
  ├── lessons-tools.md      — tool-specific pitfalls
  ├── lessons-api.md        — API-specific discoveries
  └── component-specs.md    — detailed parameters per component
```

**Principle**: L1 is tiny (always loaded). L2 loads on keyword match. L3 loads only when L2 routes to it. Total context cost per task: L1 + 1-2 L2 files (~100 lines max).

## Building the Routing Table (MEMORY.md)

This is the single most important file. If routing fails, the whole system fails.

### Trigger Word Design

```markdown
用户消息包含...                          → 加载文件
  "编译"/"build"/"MSBuild"               → conventions.md
  "错误"/"教训"/"坑"                      → lessons.md
  "API"/"NX Open"/"UF"                   → lessons-api.md
  "进度"/"状态"/"还剩"                    → project-status.md
```

**Rules for trigger words**:
- Redundant is better than missing (list synonyms: "编译, build, MSBuild, cmake")
- Match the user's language, not documentation jargon
- If unsure whether to load, LOAD — cost of extra 30 lines << cost of missing context

### Semantic Matching (keyword misses)

When no keyword hits, use this table:
| Topic | Should Load | Why |
|-------|------------|-----|
| Any mention of IDE, editor, toolchain | user-profile.md | Environment paths |
| Creating/modifying project files | conventions.md | Build system rules |
| Python environment, pip, conda | user-profile.md | Python paths |

## What to Save vs What Not to Save

### SAVE (write to memory)

1. **Verified approaches**: User confirmed "对，就这样" → pattern worth reusing
2. **Corrections**: User said "不对" → record why and what's correct
3. **Explicit preferences**: User said "以后都这样"
4. **Non-obvious constraints**: "this tool version doesn't support X"
5. **Pitfalls with solutions**: "doing X caused Y, fixed by Z"
6. **Project state changes**: feature went from planned → done

### DON'T SAVE (don't pollute memory)

- Code details (read the code instead)
- One-time bug fixes (no reusable lesson)
- File path lists (use Glob/ls)
- Current session temp progress (use Task tool)
- Obvious general programming knowledge

## Memory Lifecycle

```
Create → Use → Update/Correct → [Stale] → Delete or Archive
```

**Critical rule**: Stale memory is WORSE than no memory. If a memory claims "file X exists at path Y" or "API Z doesn't work", verify before acting. If memory conflicts with current reality, trust reality and UPDATE the memory.

## Split Thresholds

When an L2 file shows these signals, split out an L3:
- File exceeds ~50 lines (loading cost too high)
- Two or more independently describable sub-topics (semantic impurity)
- Content only needed in rare scenarios (wasted context)

**How to split**: Move the sub-topic to a new L3 file, add a routing entry in the L2 parent, update MEMORY.md trigger table.

## When to Update

- **Immediately**: After a correction ("别这样" → write lesson now)
- **Task complete**: Update project status, mark done items
- **Stale found**: Old memory conflicts with current code → fix immediately
- **User requests**: "记住这个"
- **Split check**: Every time you write a memory file, check: >50 lines? ≥2 sub-topics? → split now, don't wait

## Self-Evolution

The memory system's architecture is itself a memory. Track:
- New/deleted/merged domain files → update MEMORY.md routing
- Trigger word misses → adjust keywords
- Files never loaded → archive or delete
- Cross-domain tasks failing → create scene templates (pre-defined multi-file load recipes)

## Known Weak Points (Monitor These)

1. **Routing failure**: Most common failure mode — AI skips routing protocol and acts on stale memory. Mitigation: make routing a HARD step at the start of every response.
2. **L1 bloat**: MEMORY.md grows beyond 30 lines → split to L2 files, keep L1 as pure routing.
3. **No priority marking**: Hard constraints (must compile) mixed with soft preferences (header-only style). Future: `[硬]`/`[软]` tags.
4. **No expiration**: Version-dependent lessons don't auto-stale. Future: timestamps + review triggers.
5. **Cross-domain recipes undefined**: "new feature implementation" should trigger specific multi-file loads. Future: scene templates.

## Learning from Others' Memory Systems

When you encounter another memory strategy (downloaded skill, open-source project, shared by a colleague), don't blindly adopt or dismiss it. Run this protocol:

### Step 1: Diff the Architecture
| Question | Our System | Their System | Verdict |
|----------|-----------|-------------|---------|
| How many layers? | L1/L2/L3 | ? | |
| How does routing work? | Keyword + semantic table | ? | |
| What triggers a save? | 6 rules | ? | |
| Split threshold? | >50 lines or ≥2 topics | ? | |
| How is staleness handled? | Manual verify | ? | |

### Step 2: Extract the Insight
Ask: what problem did THEY encounter that led to this design choice?
- If they have an expiration mechanism → they got burned by stale data
- If they use YAML frontmatter → they needed structured metadata
- If they separate "hard" vs "soft" rules → they had a compliance incident

The feature itself is less important than the PROBLEM it solves. Only adopt if we share that problem.

### Step 3: Adapt, Don't Copy
Merge rules:
- **Same problem, better solution** → replace ours
- **Problem we don't have** → skip (don't add complexity we don't need)
- **Problem we've had but didn't solve** → adopt with our terminology
- **Incompatible with our workflow** → note in "future ideas" but don't force-fit

### Step 4: Test Before Committing
- Run the merged system on 3 real tasks
- Check: did it load faster? miss fewer triggers? prevent any mistakes?
- If no measurable improvement → revert. Complexity without benefit is waste.

### Step 5: Document the Evolution
In MEMORY.md, keep an "Architecture Changelog":
```markdown
## 架构演进
- 2026-05-10: 从 @someone's-system 引入过期检查机制, 适配为时间戳+半月验证
- 2026-05-09: 初始 L1/L2/L3 架构
```
This prevents forgetting WHY a feature exists and makes future pruning easier.

### Red Flags (Don't Adopt)
- "We do X because it's best practice" — no: ask what problem X solved for THEM
- Over-engineered routing (regex, NLP, vector search) — simple keyword tables work
- Multi-megabyte context dumps — defeats the purpose of layered loading
- "Just remember everything" — noise kills signal
