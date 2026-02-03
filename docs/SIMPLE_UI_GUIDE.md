# Simple ERP UI Guide

## Philosophy
**Keep it basic. ERP is for work, not for show.**

- Black background (#000000)
- White text (#e5e5e5)
- Red accents (#d00000)
- No fancy animations
- No colored backgrounds
- Fast and functional

## What We Fixed

### Before
- ❌ Inconsistent colors across pages
- ❌ White backgrounds with colored gradients
- ❌ Blue, green, purple, yellow buttons everywhere
- ❌ Complex CSS with multiple files
- ❌ Glassmorphism effects
- ❌ Shadows and animations

### After
- ✅ Pure black background everywhere
- ✅ All buttons are red
- ✅ Simple borders, no shadows
- ✅ One CSS file (`simple-erp.css`)
- ✅ Clean and fast
- ✅ Easy to maintain

## Files Changed

1. **base.html** - Simplified CSS variables and Tailwind config
2. **simple-erp.css** - One file to rule them all

## How It Works

The `simple-erp.css` file uses `!important` to override ALL Tailwind classes:
- Forces black backgrounds
- Forces white text
- Forces red buttons
- Removes all colored backgrounds
- Removes shadows and gradients

## No Changes Needed to Templates

All your existing HTML templates work as-is. The CSS overrides everything automatically.

## Color Scheme

```
Background:  #000000 (pure black)
Surface:     #0a0a0a (very dark gray)
Border:      #1a1a1a (dark gray)
Text:        #e5e5e5 (light gray)
Text Muted:  #a3a3a3 (medium gray)
Accent:      #d00000 (red)
```

## Status Colors (Kept for Meaning)

- Green: Success/Active (#16a34a)
- Red: Error/Danger (#ef4444)
- Yellow: Warning/Pending (#eab308)
- Blue: Info (#3b82f6)

These are only used for status badges and text, NOT backgrounds.

## Maintenance

To change the theme:
1. Edit `simple-erp.css`
2. Change color values
3. Refresh browser
4. Done!

No need to touch 50+ HTML templates.

## Performance

- One CSS file: ~5KB
- No JavaScript for styling
- Fast page loads
- No build process needed

## Future

If you need to add new pages:
- Just write normal HTML
- Use Tailwind classes as usual
- CSS will override automatically
- Everything stays consistent
