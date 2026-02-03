"""
Settings Routes - Theme and Application Settings
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.settings import AppSettings, UserSettings

bp = Blueprint('settings', __name__, url_prefix='/settings')

# Theme presets
THEME_PRESETS = {
    'red': {
        'name': 'Red (Industrial)',
        'primary': '#d00000',
        'primary_hover': '#a80c06',
        'primary_light': '#ff0000',
        'description': 'Bold and industrial - perfect for manufacturing'
    },
    'blue': {
        'name': 'Blue (Professional)',
        'primary': '#0066cc',
        'primary_hover': '#0052a3',
        'primary_light': '#3399ff',
        'description': 'Professional and corporate'
    },
    'green': {
        'name': 'Green (Growth)',
        'primary': '#059669',
        'primary_hover': '#047857',
        'primary_light': '#10b981',
        'description': 'Fresh and growth-oriented'
    },
    'purple': {
        'name': 'Purple (Modern)',
        'primary': '#7c3aed',
        'primary_hover': '#6d28d9',
        'primary_light': '#8b5cf6',
        'description': 'Modern and creative'
    },
    'orange': {
        'name': 'Orange (Energetic)',
        'primary': '#ea580c',
        'primary_hover': '#c2410c',
        'primary_light': '#f97316',
        'description': 'Energetic and warm'
    },
    'teal': {
        'name': 'Teal (Balanced)',
        'primary': '#0d9488',
        'primary_hover': '#0f766e',
        'primary_light': '#14b8a6',
        'description': 'Calm and balanced'
    },
    'pink': {
        'name': 'Pink (Creative)',
        'primary': '#db2777',
        'primary_hover': '#be185d',
        'primary_light': '#ec4899',
        'description': 'Creative and vibrant'
    },
    'indigo': {
        'name': 'Indigo (Trust)',
        'primary': '#4f46e5',
        'primary_hover': '#4338ca',
        'primary_light': '#6366f1',
        'description': 'Trustworthy and stable'
    }
}


@bp.route('/')
@login_required
def index():
    """Settings dashboard"""
    return redirect(url_for('settings.theme'))


@bp.route('/theme', methods=['GET', 'POST'])
@login_required
def theme():
    """Theme settings page"""
    if request.method == 'POST':
        try:
            theme_preset = request.form.get('theme_preset')
            apply_to = request.form.get('apply_to', 'user')  # 'user' or 'company'
            
            print(f"DEBUG: Received theme_preset={theme_preset}, apply_to={apply_to}")  # Debug log
            
            if not theme_preset:
                flash('Please select a theme!', 'error')
                return redirect(url_for('settings.theme'))
            
            if theme_preset not in THEME_PRESETS:
                flash(f'Invalid theme selected: {theme_preset}', 'error')
                return redirect(url_for('settings.theme'))
            
            theme_data = THEME_PRESETS[theme_preset]
            
            if apply_to == 'company' and current_user.role == 'admin':
                # Apply to entire company (all users)
                AppSettings.set(
                    'theme_preset',
                    theme_preset,
                    setting_type='string',
                    description='Company-wide theme preset',
                    user_id=current_user.id
                )
                AppSettings.set('theme_primary', theme_data['primary'], user_id=current_user.id)
                AppSettings.set('theme_primary_hover', theme_data['primary_hover'], user_id=current_user.id)
                AppSettings.set('theme_primary_light', theme_data['primary_light'], user_id=current_user.id)
                
                flash(f'✅ Theme "{theme_data["name"]}" applied company-wide!', 'success')
            else:
                # Apply to current user only
                UserSettings.set(current_user.id, 'theme_preset', theme_preset)
                UserSettings.set(current_user.id, 'theme_primary', theme_data['primary'])
                UserSettings.set(current_user.id, 'theme_primary_hover', theme_data['primary_hover'])
                UserSettings.set(current_user.id, 'theme_primary_light', theme_data['primary_light'])
                
                flash(f'✅ Theme "{theme_data["name"]}" applied to your account!', 'success')
            
            print(f"DEBUG: Theme saved successfully")  # Debug log
            return redirect(url_for('settings.theme'))
            
        except Exception as e:
            db.session.rollback()
            print(f"DEBUG ERROR: {str(e)}")  # Debug log
            import traceback
            traceback.print_exc()
            flash(f'❌ Error saving theme: {str(e)}', 'error')
            return redirect(url_for('settings.theme'))
    
    # Get current theme
    user_theme = UserSettings.get(current_user.id, 'theme_preset')
    company_theme = AppSettings.get('theme_preset', 'red')
    
    current_theme = user_theme or company_theme
    
    print(f"DEBUG: Current theme={current_theme}, user_theme={user_theme}, company_theme={company_theme}")  # Debug log
    
    return render_template(
        'settings/theme.html',
        theme_presets=THEME_PRESETS,
        current_theme=current_theme,
        is_admin=current_user.role == 'admin'
    )


@bp.route('/theme/preview/<preset>')
@login_required
def preview_theme(preset):
    """Preview theme colors (AJAX endpoint)"""
    if preset not in THEME_PRESETS:
        return jsonify({'error': 'Invalid theme'}), 400
    
    return jsonify(THEME_PRESETS[preset])


@bp.route('/theme/reset', methods=['POST'])
@login_required
def reset_theme():
    """Reset theme to default"""
    try:
        # Delete user theme settings
        UserSettings.query.filter_by(
            user_id=current_user.id,
            setting_key='theme_preset'
        ).delete()
        UserSettings.query.filter_by(
            user_id=current_user.id,
            setting_key='theme_primary'
        ).delete()
        UserSettings.query.filter_by(
            user_id=current_user.id,
            setting_key='theme_primary_hover'
        ).delete()
        UserSettings.query.filter_by(
            user_id=current_user.id,
            setting_key='theme_primary_light'
        ).delete()
        
        db.session.commit()
        flash('Theme reset to company default!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error resetting theme: {str(e)}', 'error')
    
    return redirect(url_for('settings.theme'))


def get_active_theme(user_id):
    """
    Get active theme for a user
    Returns theme colors dict
    """
    # Check user-specific theme first
    user_theme = UserSettings.get(user_id, 'theme_preset')
    
    if user_theme and user_theme in THEME_PRESETS:
        return THEME_PRESETS[user_theme]
    
    # Fall back to company theme
    company_theme = AppSettings.get('theme_preset', 'red')
    
    if company_theme in THEME_PRESETS:
        return THEME_PRESETS[company_theme]
    
    # Default to red
    return THEME_PRESETS['red']
