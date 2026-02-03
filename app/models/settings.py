"""
Application Settings Model
"""
from app import db
from datetime import datetime

class AppSettings(db.Model):
    """Application-wide settings"""
    __tablename__ = 'app_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    setting_key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    setting_value = db.Column(db.Text, nullable=True)
    setting_type = db.Column(db.String(50), default='string')  # string, integer, boolean, json
    description = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    def __repr__(self):
        return f'<AppSettings {self.setting_key}={self.setting_value}>'
    
    @staticmethod
    def get(key, default=None):
        """Get setting value by key"""
        setting = AppSettings.query.filter_by(setting_key=key).first()
        if setting:
            # Type conversion
            if setting.setting_type == 'boolean':
                return setting.setting_value.lower() in ('true', '1', 'yes')
            elif setting.setting_type == 'integer':
                return int(setting.setting_value)
            return setting.setting_value
        return default
    
    @staticmethod
    def set(key, value, setting_type='string', description=None, user_id=None):
        """Set or update setting value"""
        setting = AppSettings.query.filter_by(setting_key=key).first()
        if setting:
            setting.setting_value = str(value)
            setting.setting_type = setting_type
            setting.updated_by = user_id
            if description:
                setting.description = description
        else:
            setting = AppSettings(
                setting_key=key,
                setting_value=str(value),
                setting_type=setting_type,
                description=description,
                updated_by=user_id
            )
            db.session.add(setting)
        db.session.commit()
        return setting


class UserSettings(db.Model):
    """User-specific settings"""
    __tablename__ = 'user_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    setting_key = db.Column(db.String(100), nullable=False)
    setting_value = db.Column(db.Text, nullable=True)
    setting_type = db.Column(db.String(50), default='string')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'setting_key', name='_user_setting_uc'),
    )
    
    def __repr__(self):
        return f'<UserSettings user={self.user_id} {self.setting_key}={self.setting_value}>'
    
    @staticmethod
    def get(user_id, key, default=None):
        """Get user setting value"""
        setting = UserSettings.query.filter_by(user_id=user_id, setting_key=key).first()
        if setting:
            if setting.setting_type == 'boolean':
                return setting.setting_value.lower() in ('true', '1', 'yes')
            elif setting.setting_type == 'integer':
                return int(setting.setting_value)
            return setting.setting_value
        return default
    
    @staticmethod
    def set(user_id, key, value, setting_type='string'):
        """Set or update user setting"""
        setting = UserSettings.query.filter_by(user_id=user_id, setting_key=key).first()
        if setting:
            setting.setting_value = str(value)
            setting.setting_type = setting_type
        else:
            setting = UserSettings(
                user_id=user_id,
                setting_key=key,
                setting_value=str(value),
                setting_type=setting_type
            )
            db.session.add(setting)
        db.session.commit()
        return setting
