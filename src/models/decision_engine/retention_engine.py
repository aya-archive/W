# A.U.R.A Retention Engine
# Rule-based decision engine for client retention strategies

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class RetentionEngine:
    """Rule-based decision engine for client retention and risk analysis"""
    
    def __init__(self):
        """Initialize the retention engine"""
        self.rules = self._initialize_rules()
        self.thresholds = self._initialize_thresholds()
        self.strategies = self._initialize_strategies()
    
    def _initialize_rules(self) -> Dict[str, Any]:
        """Initialize decision rules for client analysis"""
        return {
            'health_score_rules': {
                'critical': {'min': 0, 'max': 30, 'weight': 0.4, 'action': 'immediate_intervention'},
                'low': {'min': 30, 'max': 50, 'weight': 0.3, 'action': 'proactive_outreach'},
                'medium': {'min': 50, 'max': 70, 'weight': 0.2, 'action': 'monitor_closely'},
                'high': {'min': 70, 'max': 100, 'weight': 0.0, 'action': 'maintain_relationship'}
            },
            'engagement_rules': {
                'low': {'min': 0, 'max': 0.3, 'weight': 0.3, 'action': 'engagement_boost'},
                'medium': {'min': 0.3, 'max': 0.7, 'weight': 0.1, 'action': 'monitor_engagement'},
                'high': {'min': 0.7, 'max': 1.0, 'weight': 0.0, 'action': 'maintain_engagement'}
            },
            'support_rules': {
                'high_volume': {'min': 5, 'max': float('inf'), 'weight': 0.3, 'action': 'support_optimization'},
                'medium_volume': {'min': 2, 'max': 5, 'weight': 0.1, 'action': 'monitor_support'},
                'low_volume': {'min': 0, 'max': 2, 'weight': 0.0, 'action': 'maintain_support'}
            },
            'revenue_rules': {
                'declining': {'threshold': -0.1, 'weight': 0.4, 'action': 'revenue_recovery'},
                'stable': {'threshold': 0.05, 'weight': 0.1, 'action': 'monitor_revenue'},
                'growing': {'threshold': 0.1, 'weight': 0.0, 'action': 'maintain_growth'}
            },
            'nps_rules': {
                'detractor': {'min': 0, 'max': 6, 'weight': 0.3, 'action': 'satisfaction_improvement'},
                'passive': {'min': 7, 'max': 8, 'weight': 0.1, 'action': 'engagement_boost'},
                'promoter': {'min': 9, 'max': 10, 'weight': 0.0, 'action': 'maintain_satisfaction'}
            }
        }
    
    def _initialize_thresholds(self) -> Dict[str, float]:
        """Initialize risk and priority thresholds"""
        return {
            'critical_risk': 0.8,
            'high_risk': 0.6,
            'medium_risk': 0.4,
            'low_risk': 0.2,
            'critical_priority': 0.9,
            'high_priority': 0.7,
            'medium_priority': 0.5
        }
    
    def _initialize_strategies(self) -> Dict[str, Dict[str, Any]]:
        """Initialize retention strategies"""
        return {
            'immediate_intervention': {
                'name': 'Immediate Intervention',
                'description': 'Urgent action required to prevent churn',
                'actions': [
                    'Schedule executive call within 24 hours',
                    'Offer personalized retention package',
                    'Assign dedicated customer success manager',
                    'Provide immediate technical support'
                ],
                'timeline': '24-48 hours',
                'resources': ['Executive team', 'Customer success manager', 'Technical support'],
                'expected_outcome': 'Prevent immediate churn'
            },
            'proactive_outreach': {
                'name': 'Proactive Outreach',
                'description': 'Proactive engagement to improve client health',
                'actions': [
                    'Schedule health check call',
                    'Provide additional training resources',
                    'Offer feature adoption consultation',
                    'Create personalized success plan'
                ],
                'timeline': '1-2 weeks',
                'resources': ['Customer success manager', 'Training team'],
                'expected_outcome': 'Improve health score by 20-30%'
            },
            'engagement_boost': {
                'name': 'Engagement Boost',
                'description': 'Increase client engagement and feature adoption',
                'actions': [
                    'Send personalized feature recommendations',
                    'Schedule product training sessions',
                    'Create engagement campaigns',
                    'Provide usage analytics and insights'
                ],
                'timeline': '2-4 weeks',
                'resources': ['Product team', 'Marketing team'],
                'expected_outcome': 'Increase engagement by 40-50%'
            },
            'support_optimization': {
                'name': 'Support Optimization',
                'description': 'Address underlying issues causing high support volume',
                'actions': [
                    'Conduct support ticket analysis',
                    'Provide proactive issue resolution',
                    'Offer additional training on problem areas',
                    'Implement preventive measures'
                ],
                'timeline': '1-3 weeks',
                'resources': ['Support team', 'Technical team'],
                'expected_outcome': 'Reduce support tickets by 50%'
            },
            'revenue_recovery': {
                'name': 'Revenue Recovery',
                'description': 'Address declining revenue trends',
                'actions': [
                    'Analyze revenue decline causes',
                    'Offer value demonstration sessions',
                    'Provide ROI analysis and case studies',
                    'Create retention incentives'
                ],
                'timeline': '2-4 weeks',
                'resources': ['Sales team', 'Customer success manager'],
                'expected_outcome': 'Stabilize or improve revenue trends'
            }
        }
    
    def analyze_client_risk(self, client_data: pd.Series) -> Dict[str, Any]:
        """
        Analyze individual client risk using rule-based engine
        
        Args:
            client_data: Client data series
            
        Returns:
            Risk analysis results
        """
        try:
            # Extract client attributes
            health_score = client_data.get('current_health_score', 65)
            engagement_score = client_data.get('engagement_score', 0.6)
            support_tickets = client_data.get('support_tickets_30d', 0)
            nps_score = client_data.get('nps_score', 7)
            revenue_growth = client_data.get('revenue_growth_90d', 0)
            
            # Calculate risk factors
            risk_factors = self._calculate_risk_factors(
                health_score, engagement_score, support_tickets, nps_score, revenue_growth
            )
            
            # Calculate composite risk score
            composite_risk_score = sum(risk_factors.values())
            
            # Determine risk level
            risk_level = self._determine_risk_level(composite_risk_score)
            
            # Calculate priority
            priority = self._calculate_priority(composite_risk_score, client_data)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(risk_factors, client_data)
            
            return {
                'risk_level': risk_level,
                'composite_risk_score': composite_risk_score,
                'risk_factors': risk_factors,
                'priority': priority,
                'recommendations': recommendations,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Client risk analysis failed: {e}")
            return {
                'risk_level': 'Unknown',
                'composite_risk_score': 0.0,
                'risk_factors': {},
                'priority': 'Medium',
                'recommendations': [],
                'error': str(e)
            }
    
    def _calculate_risk_factors(self, health_score: float, engagement_score: float, 
                               support_tickets: int, nps_score: int, revenue_growth: float) -> Dict[str, float]:
        """Calculate individual risk factors"""
        risk_factors = {}
        
        # Health score factor
        for level, rule in self.rules['health_score_rules'].items():
            if rule['min'] <= health_score < rule['max']:
                risk_factors['health_score'] = rule['weight']
                break
        
        # Engagement factor
        for level, rule in self.rules['engagement_rules'].items():
            if rule['min'] <= engagement_score < rule['max']:
                risk_factors['engagement'] = rule['weight']
                break
        
        # Support tickets factor
        for level, rule in self.rules['support_rules'].items():
            if rule['min'] <= support_tickets < rule['max']:
                risk_factors['support_tickets'] = rule['weight']
                break
        
        # NPS factor
        for level, rule in self.rules['nps_rules'].items():
            if rule['min'] <= nps_score < rule['max']:
                risk_factors['nps_score'] = rule['weight']
                break
        
        # Revenue growth factor
        if revenue_growth < self.rules['revenue_rules']['declining']['threshold']:
            risk_factors['revenue_decline'] = self.rules['revenue_rules']['declining']['weight']
        elif revenue_growth < self.rules['revenue_rules']['stable']['threshold']:
            risk_factors['revenue_stable'] = self.rules['revenue_rules']['stable']['weight']
        else:
            risk_factors['revenue_growth'] = self.rules['revenue_rules']['growing']['weight']
        
        return risk_factors
    
    def _determine_risk_level(self, risk_score: float) -> str:
        """Determine risk level based on composite score"""
        if risk_score >= self.thresholds['critical_risk']:
            return 'Critical'
        elif risk_score >= self.thresholds['high_risk']:
            return 'High'
        elif risk_score >= self.thresholds['medium_risk']:
            return 'Medium'
        elif risk_score >= self.thresholds['low_risk']:
            return 'Low'
        else:
            return 'Very Low'
    
    def _calculate_priority(self, risk_score: float, client_data: pd.Series) -> str:
        """Calculate action priority based on risk and client value"""
        # Base priority from risk score
        if risk_score >= self.thresholds['critical_priority']:
            base_priority = 'Critical'
        elif risk_score >= self.thresholds['high_priority']:
            base_priority = 'High'
        elif risk_score >= self.thresholds['medium_priority']:
            base_priority = 'Medium'
        else:
            base_priority = 'Low'
        
        # Adjust based on client value
        client_value = client_data.get('total_lifetime_revenue', 0)
        if client_value > 100000:  # High-value client
            if base_priority == 'Medium':
                base_priority = 'High'
            elif base_priority == 'Low':
                base_priority = 'Medium'
        
        return base_priority
    
    def _generate_recommendations(self, risk_factors: Dict[str, float], client_data: pd.Series) -> List[Dict[str, Any]]:
        """Generate retention recommendations based on risk factors"""
        recommendations = []
        
        # Sort risk factors by weight (highest first)
        sorted_factors = sorted(risk_factors.items(), key=lambda x: x[1], reverse=True)
        
        for factor, weight in sorted_factors:
            if weight > 0.2:  # Only consider significant risk factors
                strategy_key = self._get_strategy_for_factor(factor)
                if strategy_key in self.strategies:
                    strategy = self.strategies[strategy_key].copy()
                    strategy['trigger_factor'] = factor
                    strategy['risk_weight'] = weight
                    recommendations.append(strategy)
        
        # If no specific recommendations, provide general monitoring
        if not recommendations:
            recommendations.append({
                'name': 'General Monitoring',
                'description': 'Continue monitoring client health and engagement',
                'actions': ['Regular health check calls', 'Monitor usage patterns'],
                'timeline': 'Ongoing',
                'resources': ['Customer success manager'],
                'expected_outcome': 'Maintain current health level'
            })
        
        return recommendations
    
    def _get_strategy_for_factor(self, factor: str) -> str:
        """Map risk factors to appropriate strategies"""
        factor_strategy_map = {
            'health_score': 'proactive_outreach',
            'engagement': 'engagement_boost',
            'support_tickets': 'support_optimization',
            'revenue_decline': 'revenue_recovery',
            'nps_score': 'satisfaction_improvement'
        }
        
        return factor_strategy_map.get(factor, 'proactive_outreach')
    
    def process_batch_analysis(self, client_data: pd.DataFrame) -> pd.DataFrame:
        """
        Process batch of clients for risk analysis
        
        Args:
            client_data: DataFrame with client data
            
        Returns:
            DataFrame with analysis results
        """
        try:
            results = []
            
            for idx, client in client_data.iterrows():
                # Analyze individual client
                analysis = self.analyze_client_risk(client)
                
                # Create result record
                result = {
                    'customer_id': client.get('customer_id', f'CUST_{idx:04d}'),
                    'name': client.get('name', f'Client {idx}'),
                    'risk_level': analysis.get('risk_level', 'Unknown'),
                    'risk_score': analysis.get('composite_risk_score', 0.0),
                    'priority': analysis.get('priority', 'Medium'),
                    'health_score': client.get('current_health_score', 0),
                    'engagement_score': client.get('engagement_score', 0.0),
                    'recommendations_count': len(analysis.get('recommendations', [])),
                    'analysis_timestamp': analysis.get('analysis_timestamp', datetime.now().isoformat())
                }
                
                results.append(result)
            
            return pd.DataFrame(results)
            
        except Exception as e:
            logger.error(f"Batch analysis failed: {e}")
            return pd.DataFrame()
    
    def get_analysis_summary(self, analysis_results: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate summary of batch analysis results
        
        Args:
            analysis_results: Batch analysis results DataFrame
            
        Returns:
            Analysis summary
        """
        try:
            if analysis_results.empty:
                return {"error": "No analysis results to summarize"}
            
            # Calculate summary statistics
            total_clients = len(analysis_results)
            high_risk_clients = len(analysis_results[analysis_results['risk_level'].isin(['High', 'Critical'])])
            critical_priority = len(analysis_results[analysis_results['priority'] == 'Critical'])
            avg_risk_score = analysis_results['risk_score'].mean()
            
            # Risk distribution
            risk_distribution = analysis_results['risk_level'].value_counts().to_dict()
            priority_distribution = analysis_results['priority'].value_counts().to_dict()
            
            # Generate insights
            insights = self._generate_analysis_insights(analysis_results)
            
            return {
                'total_clients': total_clients,
                'high_risk_clients': high_risk_clients,
                'critical_priority_clients': critical_priority,
                'average_risk_score': avg_risk_score,
                'risk_distribution': risk_distribution,
                'priority_distribution': priority_distribution,
                'insights': insights
            }
            
        except Exception as e:
            logger.error(f"Analysis summary generation failed: {e}")
            return {"error": f"Error generating summary: {e}"}
    
    def _generate_analysis_insights(self, results: pd.DataFrame) -> List[str]:
        """Generate insights from analysis results"""
        insights = []
        
        high_risk_count = len(results[results['risk_level'].isin(['High', 'Critical'])])
        if high_risk_count > 0:
            insights.append(f"{high_risk_count} clients require immediate attention")
        
        avg_risk = results['risk_score'].mean()
        if avg_risk > 0.6:
            insights.append("Overall client health is concerning - consider proactive retention strategies")
        elif avg_risk < 0.3:
            insights.append("Client health is generally good - focus on growth and expansion")
        
        critical_count = len(results[results['priority'] == 'Critical'])
        if critical_count > 0:
            insights.append(f"{critical_count} clients need critical priority intervention")
        
        # Segment-specific insights
        if 'client_segment' in results.columns:
            segment_risks = results.groupby('client_segment')['risk_score'].mean()
            highest_risk_segment = segment_risks.idxmax()
            insights.append(f"Highest risk segment: {highest_risk_segment} (avg risk: {segment_risks[highest_risk_segment]:.2f})")
        
        return insights
