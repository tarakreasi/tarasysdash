# Mockup vs Implementation Gap Analysis

## Visual Differences Identified

### 1. Background & Atmosphere ❌
**Mockup**: Subtle scanline effect overlay  
**Current**: Plain dark background

**Fix Needed**:
```css
/* Add scanline overlay */
.scanline {
  background: linear-gradient(to bottom,
    rgba(255, 255, 255, 0),
    rgba(255, 255, 255, 0) 50%,
    rgba(0, 0, 0, 0.1) 50%,
    rgba(0, 0, 0, 0.1));
  background-size: 100% 4px;
  pointer-events: none;
}
```

### 2. Metric Cards Progress Bars ❌
**Mockup**: Very thin (h-1), clean bars  
**Current**: Same thickness but could be refined

**Mockup Code**:
```html
<div class="w-full bg-slate-800 h-1 mt-2 rounded-full overflow-hidden">
  <div class="bg-primary h-full w-[45%]" style="box-shadow: 0 0 8px #25d1f4"></div>
</div>
```

**Status**: Already implemented ✅

### 3. Icon Opacity ❌  
**Mockup**: Icons at 100% opacity by default, glow on hover  
**Current**: Icons at 50% opacity, brighten to 100% on hover

**Fix Needed**: Remove opacity-50, add glow effect
```css
/* Mockup style */
.material-symbols-outlined.text-primary {
  opacity: 100; /* not 50 */
}

group-hover:opacity-100 → group-hover:drop-shadow-[0_0_5px_currentColor]
```

### 4. Card Styling Details ⚠️
**Mockup**:
- `rounded-xl` (0.75rem)
- `shadow-lg`
- Hover: `hover:border-primary/50`

**Current**:
- `rounded-lg` (0.5rem) - NEEDS UPDATE
- No shadow-lg - NEEDS ADDITION
- Hover working ✅

### 5. Typography Weights & Spacing ⚠️
**Mockup**: More compact, tighter leading  
**Current**: Roomier spacing

**Specific Fixes**:
```css
/* Mockup values */
.metric-value {
  leading: none; /* ✅ already done */
  tracking: tight; /* need to add */
}

.uppercase-label {
  tracking: wider; /* ✅ already done */
}
```

### 6. Charts - CRITICAL GAP ❌
**Mockup**: SVG charts with glowing stroke  
**Current**: Empty chart containers

**Mockup Chart Style**:
```html
<path 
  stroke="#25d1f4" 
  stroke-width="2" 
  style="filter: drop-shadow(0 0 4px #25d1f4);"
  vector-effect="non-scaling-stroke"
/>
```

**Fix**: Add glow filter to ECharts configuration

### 7. Rack Headers ⚠️
**Mockup**: More subtle divider lines  
**Current**: Bright border-color

**Fix Needed**:
```css
/* Change from */
border-color: #283639

/* To */
border-color: rgba(148, 163, 184, 0.1) /* slate-400/10 */
```

### 8. System Status Glow ⚠️
**Mockup**: Green with shadow  
**Current**: Green with pulse animation

**Mockup Style**:
```html
<span class="w-2 h-2 bg-green-500 rounded-full shadow-[0_0_5px_#22c55e]"></span>
```

**Status**: Implemented but could enhance glow

## Priority Fixes

### High Impact (Do First):
1. ✅ Add scanline overlay effect
2. ✅ Change card border-radius to `rounded-xl`
3. ✅ Add `shadow-lg` to cards
4. ✅ Fix icon opacity (remove opacity-50)
5. ✅ Add chart glow effects

### Medium Impact:
6. Enhance rack header subtlety
7. Add tighter `tracking-tight` to metrics
8. Reduce card padding slightly

### Low Impact (Polish):
9. Fine-tune hover transitions
10. Adjust specific color values
