# A.U.R.A Configuration Settings
# Centralized configuration management for the A.U.R.A platform

import os
from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AURASettings:
    """Configuration settings for A.U.R.A platform"""
    
    def __init__(self):
        """Initialize A.U.R.A settings"""
        self.app_config = self._load_app_config()
        self.database_config = self._load_database_config()
        self.ai_config = self._load_ai_config()
        self.dashboard_config = self._load_dashboard_config()
        self.notification_config = self._load_notification_config()
    
    def _load_app_config(self) -> Dict[str, Any]:
        """Load application configuration"""
        return {
            'app_name': 'A.U.R.A - Adaptive User Retention Assistant',
            'version': '1.0.0',
            'environment': os.getenv('AURA_ENV', 'development'),
            'debug': os.getenv('AURA_DEBUG', 'False').lower() == 'true',
            'log_level': os.getenv('AURA_LOG_LEVEL', 'INFO'),
            'timezone': os.getenv('AURA_TIMEZONE', 'UTC'),
            'max_file_size': int(os.getenv('AURA_MAX_FILE_SIZE', '10485760')),  # 10MB
            'supported_formats': ['csv', 'xlsx', 'json'],
            'data_refresh_interval': int(os.getenv('AURA_DATA_REFRESH_MINUTES', '60')),
            'session_timeout': int(os.getenv('AURA_SESSION_TIMEOUT_MINUTES', '480')),  # 8 hours
            'max_concurrent_users': int(os.getenv('AURA_MAX_CONCURRENT_USERS', '100'))
        }
    
    def _load_database_config(self) -> Dict[str, Any]:
        """Load database configuration"""
        return {
            'type': os.getenv('AURA_DB_TYPE', 'sqlite'),
            'host': os.getenv('AURA_DB_HOST', 'localhost'),
            'port': int(os.getenv('AURA_DB_PORT', '5432')),
            'name': os.getenv('AURA_DB_NAME', 'aura_db'),
            'user': os.getenv('AURA_DB_USER', 'aura_user'),
            'password': os.getenv('AURA_DB_PASSWORD', ''),
            'connection_pool_size': int(os.getenv('AURA_DB_POOL_SIZE', '10')),
            'connection_timeout': int(os.getenv('AURA_DB_TIMEOUT', '30')),
            'backup_enabled': os.getenv('AURA_DB_BACKUP_ENABLED', 'True').lower() == 'true',
            'backup_frequency': os.getenv('AURA_DB_BACKUP_FREQUENCY', 'daily'),
            'data_retention_days': int(os.getenv('AURA_DB_RETENTION_DAYS', '365'))
        }
    
    def _load_ai_config(self) -> Dict[str, Any]:
        """Load AI/ML configuration"""
        return {
            'prophet_enabled': os.getenv('AURA_PROPHET_ENABLED', 'True').lower() == 'true',
            'prophet_confidence_interval': float(os.getenv('AURA_PROPHET_CONFIDENCE', '0.95')),
            'forecast_periods': int(os.getenv('AURA_FORECAST_PERIODS', '30')),
            'model_retrain_frequency': os.getenv('AURA_MODEL_RETRAIN_FREQUENCY', 'weekly'),
            'risk_threshold_high': float(os.getenv('AURA_RISK_THRESHOLD_HIGH', '0.7')),
            'risk_threshold_medium': float(os.getenv('AURA_RISK_THRESHOLD_MEDIUM', '0.4')),
            'health_score_threshold_low': int(os.getenv('AURA_HEALTH_THRESHOLD_LOW', '50')),
            'health_score_threshold_high': int(os.getenv('AURA_HEALTH_THRESHOLD_HIGH', '80')),
            'engagement_threshold_low': float(os.getenv('AURA_ENGAGEMENT_THRESHOLD_LOW', '0.3')),
            'engagement_threshold_high': float(os.getenv('AURA_ENGAGEMENT_THRESHOLD_HIGH', '0.7')),
            'support_ticket_threshold_high': int(os.getenv('AURA_SUPPORT_THRESHOLD_HIGH', '5')),
            'nps_threshold_detractor': int(os.getenv('AURA_NPS_THRESHOLD_DETRACTOR', '6')),
            'nps_threshold_promoter': int(os.getenv('AURA_NPS_THRESHOLD_PROMOTER', '9')),
            'chatbot_timeout': int(os.getenv('AURA_CHATBOT_TIMEOUT_SECONDS', '30')),
            'chatbot_max_history': int(os.getenv('AURA_CHATBOT_MAX_HISTORY', '50')),
            'model_cache_size': int(os.getenv('AURA_MODEL_CACHE_SIZE', '100'))
        }
    
    def _load_dashboard_config(self) -> Dict[str, Any]:
        """Load dashboard configuration"""
        return {
            'theme': os.getenv('AURA_DASHBOARD_THEME', 'light'),
            'color_scheme': {
                'primary': os.getenv('AURA_COLOR_PRIMARY', '#004D7A'),
                'secondary': os.getenv('AURA_COLOR_SECONDARY', '#00B3B3'),
                'success': os.getenv('AURA_COLOR_SUCCESS', '#4CAF50'),
                'warning': os.getenv('AURA_COLOR_WARNING', '#FF9800'),
                'error': os.getenv('AURA_COLOR_ERROR', '#F44336'),
                'info': os.getenv('AURA_COLOR_INFO', '#2196F3')
            },
            'charts_per_page': int(os.getenv('AURA_CHARTS_PER_PAGE', '6')),
            'default_date_range': os.getenv('AURA_DEFAULT_DATE_RANGE', '90d'),
            'auto_refresh_interval': int(os.getenv('AURA_AUTO_REFRESH_SECONDS', '300')),  # 5 minutes
            'export_formats': ['csv', 'xlsx', 'pdf', 'png'],
            'max_export_records': int(os.getenv('AURA_MAX_EXPORT_RECORDS', '10000')),
            'dashboard_layout': os.getenv('AURA_DASHBOARD_LAYOUT', 'grid'),
            'enable_real_time': os.getenv('AURA_ENABLE_REAL_TIME', 'True').lower() == 'true',
            'enable_notifications': os.getenv('AURA_ENABLE_NOTIFICATIONS', 'True').lower() == 'true'
        }
    
    def _load_notification_config(self) -> Dict[str, Any]:
        """Load notification configuration"""
        return {
            'email_enabled': os.getenv('AURA_EMAIL_ENABLED', 'False').lower() == 'true',
            'email_smtp_host': os.getenv('AURA_EMAIL_SMTP_HOST', ''),
            'email_smtp_port': int(os.getenv('AURA_EMAIL_SMTP_PORT', '587')),
            'email_smtp_user': os.getenv('AURA_EMAIL_SMTP_USER', ''),
            'email_smtp_password': os.getenv('AURA_EMAIL_SMTP_PASSWORD', ''),
            'email_from': os.getenv('AURA_EMAIL_FROM', 'noreply@aura.com'),
            'slack_enabled': os.getenv('AURA_SLACK_ENABLED', 'False').lower() == 'true',
            'slack_webhook_url': os.getenv('AURA_SLACK_WEBHOOK_URL', ''),
            'slack_channel': os.getenv('AURA_SLACK_CHANNEL', '#aura-alerts'),
            'notification_triggers': {
                'high_risk_client': os.getenv('AURA_NOTIFY_HIGH_RISK', 'True').lower() == 'true',
                'low_health_score': os.getenv('AURA_NOTIFY_LOW_HEALTH', 'True').lower() == 'true',
                'high_support_volume': os.getenv('AURA_NOTIFY_HIGH_SUPPORT', 'True').lower() == 'true',
                'system_errors': os.getenv('AURA_NOTIFY_SYSTEM_ERRORS', 'True').lower() == 'true'
            },
            'notification_frequency': os.getenv('AURA_NOTIFICATION_FREQUENCY', 'immediate'),
            'notification_recipients': os.getenv('AURA_NOTIFICATION_RECIPIENTS', '').split(',')
        }
    
    def get_setting(self, category: str, key: str, default: Any = None) -> Any:
        """Get a specific setting value"""
        try:
            config_map = {
                'app': self.app_config,
                'database': self.database_config,
                'ai': self.ai_config,
                'dashboard': self.dashboard_config,
                'notification': self.notification_config
            }
            
            config = config_map.get(category, {})
            return config.get(key, default)
            
        except Exception as e:
            logger.error(f"Error getting setting {category}.{key}: {e}")
            return default
    
    def update_setting(self, category: str, key: str, value: Any) -> bool:
        """Update a specific setting value"""
        try:
            config_map = {
                'app': self.app_config,
                'database': self.database_config,
                'ai': self.ai_config,
                'dashboard': self.dashboard_config,
                'notification': self.notification_config
            }
            
            if category in config_map:
                config_map[category][key] = value
                logger.info(f"Updated setting {category}.{key} = {value}")
                return True
            else:
                logger.error(f"Invalid category: {category}")
                return False
                
        except Exception as e:
            logger.error(f"Error updating setting {category}.{key}: {e}")
            return False
    
    def get_all_settings(self) -> Dict[str, Dict[str, Any]]:
        """Get all configuration settings"""
        return {
            'app': self.app_config,
            'database': self.database_config,
            'ai': self.ai_config,
            'dashboard': self.dashboard_config,
            'notification': self.notification_config
        }
    
    def validate_settings(self) -> Dict[str, List[str]]:
        """Validate all configuration settings"""
        validation_results = {
            'errors': [],
            'warnings': [],
            'info': []
        }
        
        try:
            # Validate app settings
            if not self.app_config.get('app_name'):
                validation_results['errors'].append('App name is required')
            
            if self.app_config.get('max_file_size', 0) <= 0:
                validation_results['errors'].append('Max file size must be positive')
            
            # Validate database settings
            if self.database_config.get('type') not in ['sqlite', 'postgresql', 'mysql']:
                validation_results['errors'].append('Invalid database type')
            
            # Validate AI settings
            if not 0 <= self.ai_config.get('risk_threshold_high', 0) <= 1:
                validation_results['errors'].append('Risk threshold high must be between 0 and 1')
            
            if not 0 <= self.ai_config.get('risk_threshold_medium', 0) <= 1:
                validation_results['errors'].append('Risk threshold medium must be between 0 and 1')
            
            if self.ai_config.get('risk_threshold_high', 0) <= self.ai_config.get('risk_threshold_medium', 0):
                validation_results['warnings'].append('Risk threshold high should be greater than medium')
            
            # Validate dashboard settings
            if self.dashboard_config.get('theme') not in ['light', 'dark']:
                validation_results['warnings'].append('Invalid dashboard theme')
            
            # Validate notification settings
            if self.notification_config.get('email_enabled') and not self.notification_config.get('email_smtp_host'):
                validation_results['warnings'].append('Email enabled but SMTP host not configured')
            
            if self.notification_config.get('slack_enabled') and not self.notification_config.get('slack_webhook_url'):
                validation_results['warnings'].append('Slack enabled but webhook URL not configured')
            
            # Add info messages
            validation_results['info'].append(f"Configuration loaded for {self.app_config.get('app_name', 'A.U.R.A')}")
            validation_results['info'].append(f"Environment: {self.app_config.get('environment', 'unknown')}")
            validation_results['info'].append(f"Debug mode: {self.app_config.get('debug', False)}")
            
        except Exception as e:
            validation_results['errors'].append(f"Configuration validation failed: {e}")
            logger.error(f"Configuration validation error: {e}")
        
        return validation_results
    
    def export_settings(self, file_path: str) -> bool:
        """Export settings to a file"""
        try:
            import json
            
            settings_data = {
                'export_timestamp': datetime.now().isoformat(),
                'settings': self.get_all_settings(),
                'validation': self.validate_settings()
            }
            
            with open(file_path, 'w') as f:
                json.dump(settings_data, f, indent=2, default=str)
            
            logger.info(f"Settings exported to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Settings export failed: {e}")
            return False
    
    def import_settings(self, file_path: str) -> bool:
        """Import settings from a file"""
        try:
            import json
            
            with open(file_path, 'r') as f:
                settings_data = json.load(f)
            
            if 'settings' in settings_data:
                settings = settings_data['settings']
                
                # Update configurations
                if 'app' in settings:
                    self.app_config.update(settings['app'])
                if 'database' in settings:
                    self.database_config.update(settings['database'])
                if 'ai' in settings:
                    self.ai_config.update(settings['ai'])
                if 'dashboard' in settings:
                    self.dashboard_config.update(settings['dashboard'])
                if 'notification' in settings:
                    self.notification_config.update(settings['notification'])
                
                logger.info(f"Settings imported from {file_path}")
                return True
            else:
                logger.error("Invalid settings file format")
                return False
                
        except Exception as e:
            logger.error(f"Settings import failed: {e}")
            return False
    
    def get_environment_info(self) -> Dict[str, Any]:
        """Get environment information"""
        return {
            'python_version': os.sys.version,
            'platform': os.name,
            'working_directory': os.getcwd(),
            'environment_variables': {
                key: value for key, value in os.environ.items() 
                if key.startswith('AURA_')
            },
            'configuration_loaded': datetime.now().isoformat(),
            'settings_validation': self.validate_settings()
        }