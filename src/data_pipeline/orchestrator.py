# A.U.R.A Data Pipeline Orchestrator
# Orchestrates the complete data pipeline from Bronze to Gold layer

import pandas as pd
import numpy as np
import os
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class DataPipelineOrchestrator:
    """Orchestrates the complete A.U.R.A data pipeline."""
    
    def __init__(self):
        """Initialize the pipeline orchestrator."""
        self.bronze_path = "data/bronze"
        self.silver_path = "data/silver"
        self.gold_path = "data/gold"
        self.pipeline_stats = {}
        
        # Ensure directories exist
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure all pipeline directories exist."""
        directories = [self.bronze_path, self.silver_path, self.gold_path]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Ensured directory exists: {directory}")
    
    def run_complete_pipeline(self) -> Dict[str, Any]:
        """
        Run the complete data pipeline from Bronze to Gold.
        
        Returns:
            Dict[str, Any]: Pipeline execution results
        """
        try:
            start_time = datetime.now()
            logger.info("Starting A.U.R.A data pipeline execution")
            
            # Initialize results
            results = {
                'overall_success': True,
                'errors': [],
                'warnings': [],
                'statistics': {},
                'duration': 0
            }
            
            # Bronze Layer - Raw data ingestion
            bronze_result = self._process_bronze_layer()
            results['statistics']['bronze_records'] = bronze_result.get('record_count', 0)
            if bronze_result.get('errors'):
                results['errors'].extend(bronze_result['errors'])
            
            # Silver Layer - Cleaned and standardized data
            silver_result = self._process_silver_layer()
            results['statistics']['silver_records'] = silver_result.get('record_count', 0)
            if silver_result.get('errors'):
                results['errors'].extend(silver_result['errors'])
            
            # Gold Layer - Business-ready analytics data
            gold_result = self._process_gold_layer()
            results['statistics']['gold_records'] = gold_result.get('record_count', 0)
            if gold_result.get('errors'):
                results['errors'].extend(gold_result['errors'])
            
            # Calculate duration
            end_time = datetime.now()
            results['duration'] = (end_time - start_time).total_seconds()
            
            # Determine overall success
            if results['errors']:
                results['overall_success'] = False
                results['warnings'].append(f"Pipeline completed with {len(results['errors'])} errors")
            else:
                results['warnings'].append("Pipeline completed successfully")
            
            logger.info(f"Pipeline execution completed in {results['duration']:.2f} seconds")
            return results
            
        except Exception as e:
            logger.error(f"Pipeline execution failed: {e}")
            return {
                'overall_success': False,
                'errors': [str(e)],
                'warnings': [],
                'statistics': {},
                'duration': 0
            }
    
    def _process_bronze_layer(self) -> Dict[str, Any]:
        """
        Process Bronze layer - raw data ingestion.
        
        Returns:
            Dict[str, Any]: Bronze layer processing results
        """
        try:
            logger.info("Processing Bronze layer - raw data ingestion")
            
            # Generate sample raw data (in real implementation, this would load from external sources)
            raw_data = self._generate_sample_raw_data()
            
            # Save to Bronze layer
            bronze_file = os.path.join(self.bronze_path, "raw_customer_data.csv")
            raw_data.to_csv(bronze_file, index=False)
            
            logger.info(f"Bronze layer data saved to {bronze_file}")
            
            return {
                'success': True,
                'record_count': len(raw_data),
                'file_path': bronze_file,
                'errors': []
            }
            
        except Exception as e:
            logger.error(f"Bronze layer processing failed: {e}")
            return {
                'success': False,
                'record_count': 0,
                'errors': [str(e)]
            }
    
    def _process_silver_layer(self) -> Dict[str, Any]:
        """
        Process Silver layer - cleaned and standardized data.
        
        Returns:
            Dict[str, Any]: Silver layer processing results
        """
        try:
            logger.info("Processing Silver layer - data cleaning and standardization")
            
            # Load Bronze data
            bronze_file = os.path.join(self.bronze_path, "raw_customer_data.csv")
            if not os.path.exists(bronze_file):
                # Generate sample data if Bronze file doesn't exist
                bronze_data = self._generate_sample_raw_data()
            else:
                bronze_data = pd.read_csv(bronze_file)
            
            # Clean and standardize data
            silver_data = self._clean_and_standardize_data(bronze_data)
            
            # Save to Silver layer
            silver_file = os.path.join(self.silver_path, "cleaned_customer_data.csv")
            silver_data.to_csv(silver_file, index=False)
            
            logger.info(f"Silver layer data saved to {silver_file}")
            
            return {
                'success': True,
                'record_count': len(silver_data),
                'file_path': silver_file,
                'errors': []
            }
            
        except Exception as e:
            logger.error(f"Silver layer processing failed: {e}")
            return {
                'success': False,
                'record_count': 0,
                'errors': [str(e)]
            }
    
    def _process_gold_layer(self) -> Dict[str, Any]:
        """
        Process Gold layer - business-ready analytics data.
        
        Returns:
            Dict[str, Any]: Gold layer processing results
        """
        try:
            logger.info("Processing Gold layer - business analytics data")
            
            # Load Silver data
            silver_file = os.path.join(self.silver_path, "cleaned_customer_data.csv")
            if not os.path.exists(silver_file):
                # Generate sample data if Silver file doesn't exist
                silver_data = self._generate_sample_cleaned_data()
            else:
                silver_data = pd.read_csv(silver_file)
            
            # Create customer 360 view
            gold_data = self._create_customer_360_view(silver_data)
            
            # Save to Gold layer
            gold_file = os.path.join(self.gold_path, "customer_360.csv")
            gold_data.to_csv(gold_file, index=False)
            
            logger.info(f"Gold layer data saved to {gold_file}")
            
            return {
                'success': True,
                'record_count': len(gold_data),
                'file_path': gold_file,
                'errors': []
            }
            
        except Exception as e:
            logger.error(f"Gold layer processing failed: {e}")
            return {
                'success': False,
                'record_count': 0,
                'errors': [str(e)]
            }
    
    def _generate_sample_raw_data(self) -> pd.DataFrame:
        """Generate sample raw data for Bronze layer."""
        np.random.seed(42)
        n_customers = 500
        
        # Generate raw, unprocessed data
        raw_data = pd.DataFrame({
            'id': [f'CUST_{i:04d}' for i in range(1, n_customers + 1)],
            'customer_name': [f'Customer {i}' for i in range(1, n_customers + 1)],
            'email_address': [f'customer{i}@example.com' for i in range(1, n_customers + 1)],
            'plan': np.random.choice(['Basic', 'Standard', 'Premium', 'Enterprise'], n_customers, p=[0.3, 0.4, 0.2, 0.1]),
            'revenue': np.random.lognormal(8, 1, n_customers),
            'health': np.clip(np.random.normal(60, 20, n_customers), 0, 100),
            'engagement': np.random.uniform(0, 1, n_customers),
            'risk': np.random.choice(['Low', 'Medium', 'High'], n_customers, p=[0.6, 0.3, 0.1]),
            'segment': np.random.choice(['SMB', 'Medium-Value', 'High-Value'], n_customers, p=[0.5, 0.3, 0.2]),
            'last_activity_days': np.random.randint(1, 90, n_customers),
            'support_tickets': np.random.poisson(3, n_customers),
            'created_date': pd.date_range('2020-01-01', periods=n_customers, freq='D').strftime('%Y-%m-%d')
        })
        
        return raw_data
    
    def _clean_and_standardize_data(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize raw data for Silver layer."""
        # Create a copy
        cleaned_data = raw_data.copy()
        
        # Standardize column names
        column_mapping = {
            'id': 'customer_id',
            'customer_name': 'name',
            'email_address': 'email',
            'plan': 'subscription_plan',
            'revenue': 'total_lifetime_revenue',
            'health': 'current_health_score',
            'engagement': 'engagement_score',
            'risk': 'churn_risk_level',
            'last_activity_days': 'days_since_last_engagement',
            'support_tickets': 'total_support_tickets_lifetime'
        }
        
        # Apply column mapping
        for old_name, new_name in column_mapping.items():
            if old_name in cleaned_data.columns:
                cleaned_data[new_name] = cleaned_data[old_name]
        
        # Clean data types
        cleaned_data['customer_id'] = cleaned_data['customer_id'].astype(str)
        cleaned_data['name'] = cleaned_data['name'].astype(str)
        cleaned_data['email'] = cleaned_data['email'].astype(str)
        
        # Ensure numeric columns are properly formatted
        numeric_columns = ['total_lifetime_revenue', 'current_health_score', 'engagement_score', 
                          'days_since_last_engagement', 'total_support_tickets_lifetime']
        
        for col in numeric_columns:
            if col in cleaned_data.columns:
                cleaned_data[col] = pd.to_numeric(cleaned_data[col], errors='coerce').fillna(0)
        
        # Handle missing values
        cleaned_data['subscription_plan'] = cleaned_data['subscription_plan'].fillna('Basic')
        cleaned_data['churn_risk_level'] = cleaned_data['churn_risk_level'].fillna('Low')
        cleaned_data['segment'] = cleaned_data['segment'].fillna('SMB')
        
        return cleaned_data
    
    def _generate_sample_cleaned_data(self) -> pd.DataFrame:
        """Generate sample cleaned data for Silver layer."""
        np.random.seed(42)
        n_customers = 500
        
        cleaned_data = pd.DataFrame({
            'customer_id': [f'CUST_{i:04d}' for i in range(1, n_customers + 1)],
            'name': [f'Customer {i}' for i in range(1, n_customers + 1)],
            'email': [f'customer{i}@example.com' for i in range(1, n_customers + 1)],
            'subscription_plan': np.random.choice(['Basic', 'Standard', 'Premium', 'Enterprise'], n_customers, p=[0.3, 0.4, 0.2, 0.1]),
            'total_lifetime_revenue': np.random.lognormal(8, 1, n_customers),
            'current_health_score': np.clip(np.random.normal(60, 20, n_customers), 0, 100),
            'engagement_score': np.random.uniform(0, 1, n_customers),
            'churn_risk_level': np.random.choice(['Low', 'Medium', 'High'], n_customers, p=[0.6, 0.3, 0.1]),
            'segment': np.random.choice(['SMB', 'Medium-Value', 'High-Value'], n_customers, p=[0.5, 0.3, 0.2]),
            'days_since_last_engagement': np.random.randint(1, 90, n_customers),
            'total_support_tickets_lifetime': np.random.poisson(3, n_customers)
        })
        
        return cleaned_data
    
    def _create_customer_360_view(self, cleaned_data: pd.DataFrame) -> pd.DataFrame:
        """Create customer 360 view for Gold layer."""
        # Create a copy
        gold_data = cleaned_data.copy()
        
        # Add calculated fields
        gold_data['customer_lifetime_days'] = np.random.randint(30, 1000, len(gold_data))
        gold_data['monthly_revenue'] = gold_data['total_lifetime_revenue'] / (gold_data['customer_lifetime_days'] / 30)
        gold_data['risk_score'] = self._calculate_risk_scores(gold_data)
        gold_data['retention_probability'] = self._calculate_retention_probability(gold_data)
        gold_data['upsell_potential'] = self._calculate_upsell_potential(gold_data)
        
        # Add data quality flags
        gold_data['data_quality_score'] = self._calculate_data_quality_score(gold_data)
        gold_data['last_updated'] = datetime.now().isoformat()
        
        return gold_data
    
    def _calculate_risk_scores(self, data: pd.DataFrame) -> pd.Series:
        """Calculate composite risk scores."""
        risk_scores = []
        
        for _, row in data.iterrows():
            score = 0
            
            # Health score contribution
            health = row.get('current_health_score', 50)
            if health < 30:
                score += 0.3
            elif health < 50:
                score += 0.2
            
            # Engagement contribution
            engagement = row.get('engagement_score', 0.5)
            if engagement < 0.3:
                score += 0.2
            
            # Churn risk contribution
            churn_risk = row.get('churn_risk_level', 'Medium')
            if churn_risk == 'High':
                score += 0.4
            elif churn_risk == 'Medium':
                score += 0.2
            
            # Days since engagement contribution
            days = row.get('days_since_last_engagement', 30)
            if days > 60:
                score += 0.1
            
            risk_scores.append(min(score, 1.0))
        
        return pd.Series(risk_scores)
    
    def _calculate_retention_probability(self, data: pd.DataFrame) -> pd.Series:
        """Calculate retention probability."""
        # Simple model based on risk score
        risk_scores = self._calculate_risk_scores(data)
        retention_prob = 1 - risk_scores
        return retention_prob.clip(0, 1)
    
    def _calculate_upsell_potential(self, data: pd.DataFrame) -> pd.Series:
        """Calculate upsell potential."""
        potential = []
        
        for _, row in data.iterrows():
            score = 0
            
            # High health score increases potential
            health = row.get('current_health_score', 50)
            if health > 80:
                score += 0.3
            elif health > 60:
                score += 0.2
            
            # High engagement increases potential
            engagement = row.get('engagement_score', 0.5)
            if engagement > 0.7:
                score += 0.3
            elif engagement > 0.5:
                score += 0.2
            
            # Revenue level affects potential
            revenue = row.get('total_lifetime_revenue', 0)
            if revenue > 20000:
                score += 0.2
            elif revenue > 10000:
                score += 0.1
            
            potential.append(min(score, 1.0))
        
        return pd.Series(potential)
    
    def _calculate_data_quality_score(self, data: pd.DataFrame) -> pd.Series:
        """Calculate data quality scores."""
        quality_scores = []
        
        for _, row in data.iterrows():
            score = 1.0
            
            # Penalize missing values
            missing_count = row.isnull().sum()
            score -= missing_count * 0.1
            
            # Penalize invalid values
            if row.get('current_health_score', 0) < 0 or row.get('current_health_score', 0) > 100:
                score -= 0.2
            
            if row.get('engagement_score', 0) < 0 or row.get('engagement_score', 0) > 1:
                score -= 0.2
            
            quality_scores.append(max(score, 0.0))
        
        return pd.Series(quality_scores)
