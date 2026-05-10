# Vision API Reference

## Script Location
`<vision-script-path>/vision.sh` — Calls Right Code API (Claude models)

## Usage
```bash
bash <vision-script-path>/vision.sh <image_path> [model_name]
```

## Available Models

| Model | Input $/Mtok | Output $/Mtok | Best For |
|-------|-------------|---------------|----------|
| claude-haiku-4-5 | $0.30 | $1.50 | Quick shape checks, cheap (~3000 images/元) |
| claude-sonnet-4-20250514 | $0.90 | $4.50 | General CAD analysis |
| claude-sonnet-4-5 | $0.90 | $4.50 | Dimension reading |
| claude-sonnet-4-6 | $0.90 | $4.50 | Detailed comparisons (~380 images/元) |

Default: `claude-haiku-4-5` (cheapest, good enough for shape checks)

## API Platform

- Platform: Right Code (right.codes)
- Endpoint: `https://www.right.codes/claude-aws/v1/messages`
- Channel multiplier: ×0.30 (actual cost 30% of Anthropic list price)
- Format: Anthropic Messages API

## Prompting Tips for CAD Analysis

When calling vision API, ask specific questions:
- "What is the overall shape? Rectangular block? Cylinder? Complex casting?"
- "Are there any features protruding at unexpected angles?"
- "Count the visible bolt holes. Are they evenly spaced?"
- "Compare the proportions: is the width about 2x the height?"
- "Do you see any gaps or discontinuities in the surface?"

## Integration with NX Open

For automated screenshot capture (WORK IN PROGRESS):
```python
# UF.Disp.CreateImage — signature identified but headless execution fails
# Workaround: user takes manual screenshot in NX
# Future: explore NXOpen.Gateway.ImageCaptureManager
```
