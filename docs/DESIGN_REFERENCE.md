# Dashboard Mockup Design Reference

**Source**: `docs/sprint/dashboard.html`  
**Analysis Date**: 2026-01-01  
**Purpose**: UI Polish guidelines for Phase 2 implementation

---

## Design Aesthetic: **Technical Cyberpunk/DevOps**

The mockup showcases a professional monitoring dashboard with a futuristic, high-tech aesthetic suitable for 24/7 operations centers.

---

## Color System

### Background Palette
```css
--bg-primary: #101f22;      /* Deep dark teal - main background */
--bg-surface: #16262a;      /* Slightly lighter - cards/surfaces */
--border-default: #283639;  /* Subtle borders for separation */
```

### Accent Colors
```css
--primary-cyan: #25d1f4;    /* Neon cyan - CTAs, active states, links */
--success-green: #10b981;   /* Pulsing green - "SYSTEM ONLINE" */
--warning-gold: #fbbf24;    /* Amber - high CPU/temp warnings */
--error-red: #ef4444;       /* Soft red - offline/critical states */
--secondary-purple: #a78bfa; /* Purple - secondary data visualization */
```

### Typography Colors
```css
--text-primary: #ffffff;     /* White - headings, important data */
--text-secondary: #cbd5e1;   /* Slate-300 - body text, labels */
--text-tertiary: #94a3b8;    /* Slate-400 - inactive nav, metadata */
```

---

## Typography

### Font Family
**Primary**: `Space Grotesk` - Modern geometric sans-serif  
**Fallback**: `system-ui, -apple-system, sans-serif`

### Hierarchy
```css
/* Navigation */
.nav-link {
  font-size: 0.875rem;      /* 14px */
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Section Headers (Rack IDs) */
.section-header {
  font-size: 1rem;          /* 16px */
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

/* Data Values */
.metric-value {
  font-family: monospace;   /* Tabular numbers */
  font-size: 2rem;          /* 32px for large metrics */
  font-weight: 700;
}

/* Logs/Terminal */
.log-entry {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;       /* 12px */
}
```

---

## Component Styles

### Cards
```css
.card {
  background: #16262a;
  border: 1px solid #283639;
  border-radius: 0.5rem;    /* 8px */
  padding: 1rem;            /* 16px */
  box-shadow: none;         /* Avoid heavy shadows */
}

/* Hover State */
.card:hover {
  border-color: #25d1f4;
  transform: translateY(-2px);
  transition: all 0.2s ease;
}
```

### Status Indicators
```css
/* Pulsing Online Dot */
.status-online {
  width: 0.5rem;
  height: 0.5rem;
  background: #10b981;
  border-radius: 50%;
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
```

### Buttons
```css
/* Primary CTA */
.btn-primary {
  background: #25d1f4;
  color: #000000;           /* Black text for max contrast */
  font-weight: 700;
  padding: 0.5rem 1.5rem;
  border-radius: 0.375rem;  /* 6px */
  border: none;
}

.btn-primary:hover {
  background: #22c4e8;
  box-shadow: 0 0 20px rgba(37, 209, 244, 0.4);
}
```

### Navigation
```css
.nav-active {
  border-bottom: 2px solid #25d1f4;
  color: #25d1f4;
}

.nav-inactive {
  color: #94a3b8;
  border-bottom: 2px solid transparent;
}

.nav-inactive:hover {
  color: #cbd5e1;
}
```

---

## Data Visualization

### Charts (ECharts Configuration)
```javascript
const chartTheme = {
  backgroundColor: 'transparent',
  textStyle: {
    color: '#cbd5e1',
    fontFamily: 'Space Grotesk'
  },
  grid: {
    borderColor: '#283639',
    borderWidth: 1
  },
  // Glowing line effect
  lineStyle: {
    width: 2,
    shadowColor: 'rgba(37, 209, 244, 0.5)',
    shadowBlur: 10
  },
  areaStyle: {
    color: {
      type: 'linear',
      x: 0, y: 0, x2: 0, y2: 1,
      colorStops: [
        { offset: 0, color: 'rgba(37, 209, 244, 0.3)' },
        { offset: 1, color: 'rgba(37, 209, 244, 0.05)' }
      ]
    }
  }
}
```

### Terminal/Logs Section
```css
.terminal {
  background: #0a0f11;
  border: 1px solid #283639;
  border-radius: 0.5rem;
  padding: 1rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  max-height: 300px;
  overflow-y: auto;
}

/* Log Level Colors */
.log-error { color: #ef4444; }
.log-warn { color: #fbbf24; }
.log-info { color: #25d1f4; }
.log-debug { color: #94a3b8; }
```

---

## Layout Patterns

### Dashboard Structure
- **Main Area**: 75% width (left side)
- **Sidebar**: 25% width (right side, sticky)
- **Spacing**: Consistent 1rem (16px) gaps between sections

### Responsive Breakpoints
```css
@media (max-width: 1024px) {
  /* Stack sidebar below main content */
  .dashboard-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  /* Mobile: Single column, hamburger menu */
  .nav-links {
    display: none; /* Show hamburger instead */
  }
}
```

---

## Animations & Micro-interactions

### Subtle Transitions
```css
* {
  transition: color 0.2s ease,
              border-color 0.2s ease,
              background-color 0.2s ease,
              transform 0.2s ease;
}
```

### Status Badge Glow
```css
.badge-online {
  box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
  animation: glow 2s ease-in-out infinite;
}

@keyframes glow {
  0%, 100% { box-shadow: 0 0 10px rgba(16, 185, 129, 0.5); }
  50% { box-shadow: 0 0 20px rgba(16, 185, 129, 0.8); }
}
```

---

## Implementation Status (Sprint 15)

### ✅ Completed
1. **Color Palette**: Cyberpunk teal backgrounds and neon accents fully integrated.
2. **Typography**: `Space Grotesk` and mono fonts active.
3. **Glowing Charts**: ECharts config now includes glow effects and gradients.
4. **Pulsing Indicators**: Real-time status badges with pulsing animations.
5. **Terminal Logs**: Visual log display implemented at bottom of panel.
6. **Responsive Layout**: Modular components with breakdown for mobile/sidebar.
7. **Micro-interactions**: Subtle hover state transitions on all cards.

---

## Screenshot Reference

![Mockup Terminal Section](/home/twantoro/.gemini/antigravity/brain/ac97332c-07e2-4090-a55d-41610b48c0cc/dashboard_terminal_logs_1767274870240.png)

![Full Mockup Recording](/home/twantoro/.gemini/antigravity/brain/ac97332c-07e2-4090-a55d-41610b48c0cc/mockup_analysis_1767274798457.webp)
