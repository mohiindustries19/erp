# Theme System Setup Guide

## Overview
Full-featured theme system with CSS variables + Tailwind CSS integration.

## Features Implemented

### 1. **8 Theme Presets**
- Red (Industrial) - Default
- Blue (Professional)
- Green (Growth)
- Purple (Modern)
- Orange (Energetic)
- Teal (Balanced)
- Pink (Creative)
- Indigo (Trust)

### 2. **Two-Level Theme Application**
- **User Level**: Personal theme preference
- **Company Level**: Company-wide default (Admin only)

### 3. **CSS Variables + Tailwind**
- Dynamic CSS variables injected in base.html
- Tailwind utility classes: `bg-theme-primary`, `text-theme-primary`, `border-theme-primary`
- Works with hover states: `hover:bg-theme-primary-hover`

### 4. **Database Models**
- `AppSettings`: Company-wide settings
- `UserSettings`: User-specific settings

## Setup Instructions

### Step 1: Run Database Migration
```bash
cd mohi-erp
flask db migrate -m "Add theme settings tables"
flask db upgrade
```

### Step 2: Initialize Default Theme (Optional)
```python
from app import create_app, db
from app.models.settings import AppSettings

app = create_app()
with app.app_context():
    AppSettings.set('theme_preset', 'red', description='Default company theme')
    AppSettings.set('theme_primary', '#d00000')
    AppSettings.set('theme_primary_hover', '#a80c06')
    AppSettings.set('theme_primary_light', '#ff0000')
```

### Step 3: Access Settings
- Navigate to **Settings** in the sidebar (bottom section)
- Or go directly to: `http://localhost:5000/settings/theme`

## Usage

### For Users
1. Click **Settings** in sidebar
2. Select a theme preset
3. Choose "My Account Only"
4. Click "Save Theme"

### For Admins
1. Click **Settings** in sidebar
2. Select a theme preset
3. Choose "Entire Company" to apply to all users
4. Click "Save Theme"

### Reset Theme
- Click "Reset to Default" to revert to company theme

## Using Theme Colors in Templates

### Tailwind Classes
```html
<!-- Backgrounds -->
<div class="bg-theme-primary">Primary background</div>
<div class="bg-theme-primary-hover">Hover background</div>
<div class="bg-theme-primary-light">Light background</div>

<!-- Text -->
<p class="text-theme-primary">Primary text</p>

<!-- Borders -->
<div class="border-2 border-theme-primary">Bordered element</div>

<!-- Hover States -->
<button class="bg-theme-primary hover:bg-theme-primary-hover">Button</button>
```

### CSS Variables
```css
.custom-element {
    background-color: var(--theme-primary);
    border-color: var(--theme-primary);
    color: var(--theme-primary);
}

.custom-element:hover {
    background-color: var(--theme-primary-hover);
}
```

## Files Created/Modified

### New Files
- `app/models/settings.py` - Settings models
- `app/routes/settings.py` - Settings routes
- `app/templates/settings/theme.html` - Theme settings page
- `THEME_SYSTEM_SETUP.md` - This guide

### Modified Files
- `app/__init__.py` - Registered settings blueprint, added theme context processor
- `app/models/__init__.py` - Added settings models
- `app/templates/base.html` - Added Settings link, injected CSS variables

## Database Schema

### app_settings
- `id` - Primary key
- `setting_key` - Unique setting identifier
- `setting_value` - Setting value (text)
- `setting_type` - Data type (string, integer, boolean, json)
- `description` - Setting description
- `updated_at` - Last update timestamp
- `updated_by` - User who updated

### user_settings
- `id` - Primary key
- `user_id` - Foreign key to users
- `setting_key` - Setting identifier
- `setting_value` - Setting value (text)
- `setting_type` - Data type
- `updated_at` - Last update timestamp
- Unique constraint on (user_id, setting_key)

## Theme Hierarchy
1. **User Theme** (highest priority) - Personal preference
2. **Company Theme** (fallback) - Company-wide default
3. **System Default** (fallback) - Red theme

## Extending the System

### Add New Theme Preset
Edit `app/routes/settings.py`:
```python
THEME_PRESETS = {
    'custom': {
        'name': 'Custom Theme',
        'primary': '#hexcode',
        'primary_hover': '#hexcode',
        'primary_light': '#hexcode',
        'description': 'Description'
    }
}
```

### Add New Settings
```python
# Company-wide
AppSettings.set('new_setting', 'value', setting_type='string')

# User-specific
UserSettings.set(user_id, 'new_setting', 'value')
```

## Notes
- Theme changes apply immediately (no page refresh needed for most elements)
- Print templates automatically use the active theme
- All existing pages will use the theme colors via CSS variables
- Admins can override user themes by applying company-wide theme

## Support
For issues or questions, contact the development team.
