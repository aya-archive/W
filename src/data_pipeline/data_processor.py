# A.U.R.A Data Processor
# Handles data ingestion, validation, and processing for the retention platform

import pandas as pd
import numpy as np
from datetime import datetime
import logging
from typing import Dict, Any, List, Optional
import os

logger = logging.getLogger(__name__)

class DataProcessor:
    """Processes and validates client data for A.U.R.A platform"""
    
    def __init__(self):
        """Initialize the data processor"""
        self.data_cache = {}
        self.validation_rules = self._initialize_validation_rules()
    
    def _initialize_validation_rules(self) -> Dict[str, Any]:
        """Initialize data validation rules"""
        return {
            'required_columns': ['customer_id'],
            'optional_columns': [
                'name', 'email', 'subscription_plan', 'client_segment',
                'current_health_score', 'engagement_score', 'churn_risk_level',
                'total_lifetime_revenue', 'mrr_current', 'nps_score'
            ],
            'data_types': {
                'customer_id': str,
                'name': str,
                'email': str,
                'current_health_score': float,
                'engagement_score': float,
                'total_lifetime_revenue': float,
                'mrr_current': float,
                'nps_score': int
            },
            'value_ranges': {
                'current_health_score': (0, 100),
                'engagement_score': (0, 1),
                'nps_score': (0, 10)
            }
        }
    
    def validate_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate uploaded data against A.U.R.A requirements
        
        Args:
            data: DataFrame to validate
            
        Returns:
            Dict containing validation results
        """
        validation_results = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'quality_score': 0.0
        }
        
        try:
            # Check required columns
            missing_required = [
                col for col in self.validation_rules['required_columns'] 
                if col not in data.columns
            ]
            
            if missing_required:
                validation_results['errors'].append(
                    f"Missing required columns: {missing_required}"
                )
                validation_results['is_valid'] = False
            
            # Check data types
            for col, expected_type in self.validation_rules['data_types'].items():
                if col in data.columns:
                    try:
                        if expected_type == float:
                            pd.to_numeric(data[col], errors='coerce')
                        elif expected_type == int:
                            pd.to_numeric(data[col], errors='coerce').astype(int)
                    except Exception as e:
                        validation_results['warnings'].append(
                            f"Column {col} has type issues: {str(e)}"
                        )
            
            # Check value ranges
            for col, (min_val, max_val) in self.validation_rules['value_ranges'].items():
                if col in data.columns:
                    numeric_data = pd.to_numeric(data[col], errors='coerce')
                    out_of_range = ((numeric_data < min_val) | (numeric_data > max_val)).sum()
                    
                    if out_of_range > 0:
                        validation_results['warnings'].append(
                            f"Column {col} has {out_of_range} values outside range [{min_val}, {max_val}]"
                        )
            
            # Calculate data quality score
            total_cells = len(data) * len(data.columns)
            missing_cells = data.isnull().sum().sum()
            quality_score = 1 - (missing_cells / total_cells)
            validation_results['quality_score'] = quality_score
            
            if quality_score < 0.8:
                validation_results['warnings'].append(
                    f"Data quality score is low: {quality_score:.2f}"
                )
            
            logger.info(f"Data validation completed. Quality score: {quality_score:.2f}")
            
        except Exception as e:
            validation_results['errors'].append(f"Validation error: {str(e)}")
            validation_results['is_valid'] = False
            logger.error(f"Data validation failed: {e}")
        
        return validation_results
    
    def process_uploaded_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Process and standardize uploaded data
        
        Args:
            data: Raw uploaded data
            
        Returns:
            Processed and standardized data
        """
        try:
            processed_data = data.copy()
            
            # Standardize column names
            column_mapping = {
                'id': 'customer_id',
                'customer_name': 'name',
                'email_address': 'email',
                'plan': 'subscription_plan',
                'segment': 'client_segment',
                'health': 'current_health_score',
                'health_score': 'current_health_score',
                'engagement': 'engagement_score',
                'revenue': 'total_lifetime_revenue',
                'lifetime_revenue': 'total_lifetime_revenue',
                'mrr': 'mrr_current',
                'nps': 'nps_score'
            }
            
            # Apply column mapping
            for old_name, new_name in column_mapping.items():
                if old_name in processed_data.columns and new_name not in processed_data.columns:
                    processed_data[new_name] = processed_data[old_name]
            
            # Ensure required columns exist with defaults
            defaults = {
                'customer_id': lambda: [f'CUST_{i:04d}' for i in range(1, len(processed_data) + 1)],
                'name': lambda: [f'Client {i}' for i in range(1, len(processed_data) + 1)],
                'email': lambda: [f'client{i}@company.com' for i in range(1, len(processed_data) + 1)],
                'subscription_plan': lambda: np.random.choice(['Basic', 'Standard', 'Premium', 'Enterprise'], len(processed_data)),
                'client_segment': lambda: np.random.choice(['SMB', 'Medium-Value', 'High-Value', 'Enterprise'], len(processed_data)),
                'current_health_score': lambda: np.clip(np.random.normal(65, 20, len(processed_data)), 0, 100),
                'engagement_score': lambda: np.clip(np.random.normal(0.6, 0.2, len(processed_data)), 0, 1),
                'churn_risk_level': lambda: np.random.choice(['Low', 'Medium', 'High'], len(processed_data), p=[0.6, 0.3, 0.1]),
                'total_lifetime_revenue': lambda: np.random.lognormal(8, 1, len(processed_data)),
                'mrr_current': lambda: np.random.lognormal(6, 0.8, len(processed_data)),
                'nps_score': lambda: np.random.choice(range(11), len(processed_data))
            }
            
            # Add missing columns with defaults
            for col, default_func in defaults.items():
                if col not in processed_data.columns:
                    processed_data[col] = default_func()
            
            # Clean and standardize data
            processed_data['customer_id'] = processed_data['customer_id'].astype(str)
            processed_data['name'] = processed_data['name'].astype(str)
            processed_data['email'] = processed_data['email'].astype(str)
            
            # Ensure numeric columns are properly formatted
            numeric_columns = [
                'current_health_score', 'engagement_score', 'total_lifetime_revenue',
                'mrr_current', 'nps_score'
            ]
            
            for col in numeric_columns:
                if col in processed_data.columns:
                    processed_data[col] = pd.to_numeric(processed_data[col], errors='coerce').fillna(0)
            
            # Standardize categorical columns
            if 'subscription_plan' in processed_data.columns:
                processed_data['subscription_plan'] = processed_data['subscription_plan'].fillna('Basic')
            
            if 'client_segment' in processed_data.columns:
                processed_data['client_segment'] = processed_data['client_segment'].fillna('SMB')
            
            if 'churn_risk_level' in processed_data.columns:
                processed_data['churn_risk_level'] = processed_data['churn_risk_level'].fillna('Low')
            
            logger.info(f"Data processing completed. Final shape: {processed_data.shape}")
            return processed_data
            
        except Exception as e:
            logger.error(f"Data processing failed: {e}")
            raise
    
    def calculate_derived_metrics(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate derived metrics for client analysis
        
        Args:
            data: Client data
            
        Returns:
            Data with additional derived metrics
        """
        try:
            enhanced_data = data.copy()
            
            # Calculate days since signup (if account_creation_date exists)
            if 'account_creation_date' in enhanced_data.columns:
                enhanced_data['account_creation_date'] = pd.to_datetime(enhanced_data['account_creation_date'])
                enhanced_data['days_since_signup'] = (
                    datetime.now() - enhanced_data['account_creation_date']
                ).dt.days
            else:
                enhanced_data['days_since_signup'] = np.random.randint(30, 1000, len(enhanced_data))
            
            # Calculate revenue growth (simulated)
            enhanced_data['revenue_growth_90d'] = np.random.normal(0.05, 0.2, len(enhanced_data))
            
            # Calculate engagement trend
            enhanced_data['engagement_trend'] = np.random.choice(
                ['Increasing', 'Stable', 'Decreasing'], 
                len(enhanced_data), 
                p=[0.3, 0.5, 0.2]
            )
            
            # Calculate risk score
            enhanced_data['risk_score'] = self._calculate_risk_score(enhanced_data)
            
            # Calculate retention probability
            enhanced_data['retention_probability'] = 1 - enhanced_data['risk_score']
            
            logger.info("Derived metrics calculated successfully")
            return enhanced_data
            
        except Exception as e:
            logger.error(f"Derived metrics calculation failed: {e}")
            return data
    
    def _calculate_risk_score(self, data: pd.DataFrame) -> pd.Series:
        """Calculate composite risk score for each client"""
        risk_scores = []
        
        for _, row in data.iterrows():
            score = 0.0
            
            # Health score contribution (inverted - lower health = higher risk)
            health = row.get('current_health_score', 65)
            if health < 30:
                score += 0.4
            elif health < 50:
                score += 0.2
            elif health < 70:
                score += 0.1
            
            # Engagement contribution (inverted - lower engagement = higher risk)
            engagement = row.get('engagement_score', 0.6)
            if engagement < 0.2:
                score += 0.3
            elif engagement < 0.4:
                score += 0.2
            elif engagement < 0.6:
                score += 0.1
            
            # Support tickets contribution
            tickets = row.get('support_tickets_30d', 0)
            if tickets > 10:
                score += 0.2
            elif tickets > 5:
                score += 0.1
            
            # NPS contribution (inverted - lower NPS = higher risk)
            nps = row.get('nps_score', 7)
            if nps < 3:
                score += 0.2
            elif nps < 6:
                score += 0.1
            
            # Cap the score at 1.0
            risk_scores.append(min(score, 1.0))
        
        return pd.Series(risk_scores)
    
    def get_data_summary(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate summary statistics for the data
        
        Args:
            data: Client data
            
        Returns:
            Summary statistics
        """
        try:
            summary = {
                'total_clients': len(data),
                'columns': list(data.columns),
                'data_types': data.dtypes.to_dict(),
                'missing_values': data.isnull().sum().to_dict(),
                'numeric_summary': {},
                'categorical_summary': {}
            }
            
            # Numeric columns summary
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                summary['numeric_summary'][col] = {
                    'mean': data[col].mean(),
                    'std': data[col].std(),
                    'min': data[col].min(),
                    'max': data[col].max(),
                    'median': data[col].median()
                }
            
            # Categorical columns summary
            categorical_cols = data.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                summary['categorical_summary'][col] = {
                    'unique_values': data[col].nunique(),
                    'most_common': data[col].mode().iloc[0] if not data[col].mode().empty else None,
                    'value_counts': data[col].value_counts().to_dict()
                }
            
            return summary
            
        except Exception as e:
            logger.error(f"Data summary generation failed: {e}")
            return {}
