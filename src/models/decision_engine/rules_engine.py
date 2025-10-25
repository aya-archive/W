# A.U.R.A Decision Engine Rules Engine
# Rule-based decision engine for customer risk analysis and retention strategies

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class RuleBasedDecisionEngine:
    """Rule-based decision engine for customer risk analysis and retention strategies."""
    
    def __init__(self):
        """Initialize the decision engine with rules and thresholds."""
        self.rules = self._initialize_rules()
        self.thresholds = self._initialize_thresholds()
    
    def _initialize_rules(self) -> Dict[str, Any]:
        """Initialize decision rules for customer analysis."""
        return {
            'health_score_rules': {
                'critical': {'min': 0, 'max': 30, 'weight': 0.3},
                'low': {'min': 30, 'max': 50, 'weight': 0.2},
                'medium': {'min': 50, 'max': 70, 'weight': 0.1},
                'high': {'min': 70, 'max': 100, 'weight': 0.0}
            },
            'engagement_rules': {
                'low': {'min': 0, 'max': 0.3, 'weight': 0.2},
                'medium': {'min': 0.3, 'max': 0.7, 'weight': 0.1},
                'high': {'min': 0.7, 'max': 1.0, 'weight': 0.0}
            },
            'churn_risk_rules': {
                'high': {'weight': 0.4},
                'medium': {'weight': 0.2},
                'low': {'weight': 0.0}
            },
            'days_since_engagement_rules': {
                'critical': {'min': 60, 'weight': 0.1},
                'warning': {'min': 30, 'max': 60, 'weight': 0.05},
                'normal': {'min': 0, 'max': 30, 'weight': 0.0}
            }
        }
    
    def _initialize_thresholds(self) -> Dict[str, float]:
        """Initialize risk thresholds."""
        return {
            'critical_risk': 0.7,
            'high_risk': 0.5,
            'medium_risk': 0.3,
            'low_risk': 0.0
        }
    
    def analyze_customer_risk(self, customer_data: pd.Series) -> Dict[str, Any]:
        """
        Analyze customer risk using rule-based engine.
        
        Args:
            customer_data: Customer data series
            
        Returns:
            Dict[str, Any]: Risk analysis results
        """
        try:
            # Extract customer attributes
            health_score = customer_data.get('current_health_score', 50)
            churn_risk = customer_data.get('churn_risk_level', 'Medium')
            engagement = customer_data.get('engagement_score', 0.5)
            days_since_engagement = customer_data.get('days_since_last_engagement', 30)
            
            # Calculate risk factors
            risk_factors = self._calculate_risk_factors(
                health_score, churn_risk, engagement, days_since_engagement
            )
            
            # Calculate composite risk score
            composite_risk_score = sum(risk_factors.values())
            
            # Determine risk level
            risk_level = self._determine_risk_level(composite_risk_score)
            
            # Calculate confidence
            confidence = self._calculate_confidence(risk_factors)
            
            return {
                'risk_level': risk_level,
                'composite_risk_score': composite_risk_score,
                'risk_factors': risk_factors,
                'confidence': confidence,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing customer risk: {e}")
            return {
                'risk_level': 'Unknown',
                'composite_risk_score': 0.0,
                'risk_factors': {},
                'confidence': 'Low',
                'error': str(e)
            }
    
    def generate_recommendations(self, risk_analysis: Dict[str, Any], 
                               customer_data: pd.Series) -> Dict[str, Any]:
        """
        Generate retention recommendations based on risk analysis.
        
        Args:
            risk_analysis: Risk analysis results
            customer_data: Customer data
            
        Returns:
            Dict[str, Any]: Recommendations and action plan
        """
        try:
            risk_level = risk_analysis.get('risk_level', 'Medium')
            risk_score = risk_analysis.get('composite_risk_score', 0.5)
            
            # Generate recommendations based on risk level
            recommendations = self._get_risk_based_recommendations(risk_level, risk_score)
            
            # Add customer-specific recommendations
            customer_specific = self._get_customer_specific_recommendations(customer_data)
            recommendations['recommended_actions'].extend(customer_specific)
            
            # Determine priority and timeline
            priority = self._determine_priority(risk_level, risk_score)
            timeline = self._determine_timeline(risk_level)
            expected_outcome = self._predict_outcome(risk_level, risk_score)
            
            return {
                'priority': priority,
                'timeline': timeline,
                'expected_outcome': expected_outcome,
                'recommended_actions': recommendations['recommended_actions'],
                'resources_required': recommendations['resources_required'],
                'success_metrics': recommendations['success_metrics']
            }
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return {
                'priority': 'Medium',
                'timeline': '2-4 weeks',
                'expected_outcome': 'Moderate retention probability',
                'recommended_actions': ['Schedule customer success call'],
                'resources_required': ['Customer Success Manager'],
                'error': str(e)
            }
    
    def process_customer_batch(self, customer_data: pd.DataFrame) -> pd.DataFrame:
        """
        Process a batch of customers for risk analysis.
        
        Args:
            customer_data: DataFrame with customer data
            
        Returns:
            pd.DataFrame: Batch analysis results
        """
        try:
            results = []
            
            for idx, customer in customer_data.iterrows():
                # Analyze individual customer
                risk_analysis = self.analyze_customer_risk(customer)
                recommendations = self.generate_recommendations(risk_analysis, customer)
                
                # Create result record
                result = {
                    'customer_id': customer.get('customer_id', f'CUST_{idx:04d}'),
                    'name': customer.get('name', f'Customer {idx}'),
                    'risk_level': risk_analysis.get('risk_level', 'Unknown'),
                    'risk_score': risk_analysis.get('composite_risk_score', 0.0),
                    'health_score': customer.get('current_health_score', 0),
                    'churn_risk': customer.get('churn_risk_level', 'Unknown'),
                    'engagement_score': customer.get('engagement_score', 0.0),
                    'priority': recommendations.get('priority', 'Medium'),
                    'timeline': recommendations.get('timeline', '2-4 weeks'),
                    'recommended_actions_count': len(recommendations.get('recommended_actions', []))
                }
                
                results.append(result)
            
            return pd.DataFrame(results)
            
        except Exception as e:
            logger.error(f"Error processing customer batch: {e}")
            return pd.DataFrame()
    
    def get_decision_summary(self, results: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate summary of batch processing results.
        
        Args:
            results: Batch processing results DataFrame
            
        Returns:
            Dict[str, Any]: Decision summary
        """
        try:
            if results.empty:
                return {"error": "No results to summarize"}
            
            # Calculate summary statistics
            total_customers = len(results)
            high_risk_customers = len(results[results['risk_level'].isin(['High', 'Critical'])])
            critical_priority_customers = len(results[results['priority'] == 'Critical'])
            average_risk_score = results['risk_score'].mean()
            
            # Risk distribution
            risk_distribution = results['risk_level'].value_counts().to_dict()
            priority_distribution = results['priority'].value_counts().to_dict()
            
            # Generate insights
            insights = self._generate_insights(results)
            
            return {
                'total_customers': total_customers,
                'high_risk_customers': high_risk_customers,
                'critical_priority_customers': critical_priority_customers,
                'average_risk_score': average_risk_score,
                'risk_distribution': risk_distribution,
                'priority_distribution': priority_distribution,
                'insights': insights
            }
            
        except Exception as e:
            logger.error(f"Error generating decision summary: {e}")
            return {"error": f"Error generating summary: {e}"}
    
    def _calculate_risk_factors(self, health_score: float, churn_risk: str, 
                               engagement: float, days_since_engagement: int) -> Dict[str, float]:
        """Calculate individual risk factors."""
        risk_factors = {}
        
        # Health score factor
        for level, rule in self.rules['health_score_rules'].items():
            if rule['min'] <= health_score < rule['max']:
                risk_factors['health_score'] = rule['weight']
                break
        
        # Engagement factor
        for level, rule in self.rules['engagement_rules'].items():
            if rule['min'] <= engagement < rule['max']:
                risk_factors['engagement'] = rule['weight']
                break
        
        # Churn risk factor
        risk_factors['churn_risk'] = self.rules['churn_risk_rules'].get(churn_risk.lower(), {}).get('weight', 0.0)
        
        # Days since engagement factor
        if days_since_engagement >= 60:
            risk_factors['days_since_engagement'] = 0.1
        elif days_since_engagement >= 30:
            risk_factors['days_since_engagement'] = 0.05
        else:
            risk_factors['days_since_engagement'] = 0.0
        
        return risk_factors
    
    def _determine_risk_level(self, risk_score: float) -> str:
        """Determine risk level based on composite score."""
        if risk_score >= self.thresholds['critical_risk']:
            return 'Critical'
        elif risk_score >= self.thresholds['high_risk']:
            return 'High'
        elif risk_score >= self.thresholds['medium_risk']:
            return 'Medium'
        else:
            return 'Low'
    
    def _calculate_confidence(self, risk_factors: Dict[str, float]) -> str:
        """Calculate confidence level in risk assessment."""
        total_weight = sum(risk_factors.values())
        if total_weight >= 0.8:
            return 'High'
        elif total_weight >= 0.5:
            return 'Medium'
        else:
            return 'Low'
    
    def _get_risk_based_recommendations(self, risk_level: str, risk_score: float) -> Dict[str, List[str]]:
        """Get recommendations based on risk level."""
        recommendations = {
            'recommended_actions': [],
            'resources_required': [],
            'success_metrics': []
        }
        
        if risk_level == 'Critical':
            recommendations['recommended_actions'] = [
                'Immediate executive escalation',
                'Personal retention call within 24 hours',
                'Custom retention offer with significant discount',
                'Assign dedicated customer success manager'
            ]
            recommendations['resources_required'] = [
                'Senior Customer Success Manager',
                'Executive sponsor',
                'Retention specialist',
                'Marketing team for campaigns'
            ]
            recommendations['success_metrics'] = [
                'Retention rate improvement',
                'Customer satisfaction score',
                'Revenue recovery'
            ]
        elif risk_level == 'High':
            recommendations['recommended_actions'] = [
                'Schedule retention call within 48 hours',
                'Provide personalized retention offer',
                'Assign dedicated account manager',
                'Monitor engagement metrics daily'
            ]
            recommendations['resources_required'] = [
                'Customer Success Manager',
                'Retention specialist',
                'Account manager'
            ]
            recommendations['success_metrics'] = [
                'Engagement score improvement',
                'Health score increase',
                'Retention probability'
            ]
        else:
            recommendations['recommended_actions'] = [
                'Regular check-in calls',
                'Proactive support outreach',
                'Value demonstration sessions'
            ]
            recommendations['resources_required'] = [
                'Customer Success Manager'
            ]
            recommendations['success_metrics'] = [
                'Customer satisfaction',
                'Engagement metrics'
            ]
        
        return recommendations
    
    def _get_customer_specific_recommendations(self, customer_data: pd.Series) -> List[str]:
        """Get customer-specific recommendations."""
        recommendations = []
        
        # Segment-based recommendations
        segment = customer_data.get('segment', 'SMB')
        if segment == 'High-Value':
            recommendations.append('Executive relationship building')
            recommendations.append('Premium support access')
        elif segment == 'Medium-Value':
            recommendations.append('Regular business reviews')
            recommendations.append('Feature adoption training')
        else:  # SMB
            recommendations.append('Self-service resources')
            recommendations.append('Community engagement')
        
        # Plan-based recommendations
        plan = customer_data.get('subscription_plan', 'Basic')
        if plan in ['Premium', 'Enterprise']:
            recommendations.append('Advanced feature training')
            recommendations.append('API integration support')
        
        return recommendations
    
    def _determine_priority(self, risk_level: str, risk_score: float) -> str:
        """Determine action priority."""
        if risk_level in ['Critical', 'High']:
            return 'Critical' if risk_level == 'Critical' else 'High'
        elif risk_level == 'Medium':
            return 'Medium'
        else:
            return 'Low'
    
    def _determine_timeline(self, risk_level: str) -> str:
        """Determine action timeline."""
        if risk_level == 'Critical':
            return 'Immediate (24-48 hours)'
        elif risk_level == 'High':
            return 'Urgent (1-2 weeks)'
        elif risk_level == 'Medium':
            return 'Standard (2-4 weeks)'
        else:
            return 'Routine (1-2 months)'
    
    def _predict_outcome(self, risk_level: str, risk_score: float) -> str:
        """Predict retention outcome."""
        if risk_level == 'Low':
            return 'High retention probability'
        elif risk_level == 'Medium':
            return 'Moderate retention probability'
        elif risk_level == 'High':
            return 'Low retention probability'
        else:  # Critical
            return 'Very low retention probability'
    
    def _generate_insights(self, results: pd.DataFrame) -> List[str]:
        """Generate insights from batch results."""
        insights = []
        
        high_risk_count = len(results[results['risk_level'].isin(['High', 'Critical'])])
        if high_risk_count > 0:
            insights.append(f"{high_risk_count} customers require immediate attention")
        
        avg_risk = results['risk_score'].mean()
        if avg_risk > 0.5:
            insights.append("Overall customer health is concerning - consider proactive retention strategies")
        elif avg_risk < 0.3:
            insights.append("Customer health is generally good - focus on growth and expansion")
        
        critical_count = len(results[results['priority'] == 'Critical'])
        if critical_count > 0:
            insights.append(f"{critical_count} customers need critical priority intervention")
        
        return insights
