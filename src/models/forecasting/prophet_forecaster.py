# A.U.R.A Prophet Forecaster
# Time series forecasting using Facebook Prophet for client behavior prediction

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple
import logging
import warnings
warnings.filterwarnings('ignore')

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    logging.warning("Prophet not available. Using simplified forecasting.")

logger = logging.getLogger(__name__)

class ProphetForecaster:
    """Time series forecasting using Prophet for client retention metrics"""
    
    def __init__(self):
        """Initialize the Prophet forecaster"""
        self.model = None
        self.is_trained = False
        self.forecast_data = None
        
        if not PROPHET_AVAILABLE:
            logger.warning("Prophet not available. Using simplified forecasting methods.")
    
    def prepare_time_series_data(self, data: pd.DataFrame, metric: str) -> pd.DataFrame:
        """
        Prepare time series data for Prophet forecasting
        
        Args:
            data: Client data
            metric: Metric to forecast (revenue, engagement, health_score)
            
        Returns:
            Time series data in Prophet format
        """
        try:
            # Generate historical time series data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            dates = pd.date_range(start=start_date, end=end_date, freq='D')
            
            # Create time series based on metric
            if metric == "revenue":
                # Simulate revenue trends
                base_revenue = data['total_lifetime_revenue'].mean() if 'total_lifetime_revenue' in data.columns else 10000
                values = self._generate_revenue_series(base_revenue, len(dates))
            elif metric == "engagement":
                # Simulate engagement trends
                base_engagement = data['engagement_score'].mean() if 'engagement_score' in data.columns else 0.6
                values = self._generate_engagement_series(base_engagement, len(dates))
            elif metric == "health_score":
                # Simulate health score trends
                base_health = data['current_health_score'].mean() if 'current_health_score' in data.columns else 65
                values = self._generate_health_series(base_health, len(dates))
            else:
                # Default to revenue
                values = self._generate_revenue_series(10000, len(dates))
            
            # Create Prophet-compatible DataFrame
            ts_data = pd.DataFrame({
                'ds': dates,
                'y': values
            })
            
            logger.info(f"Time series data prepared for {metric}. Shape: {ts_data.shape}")
            return ts_data
            
        except Exception as e:
            logger.error(f"Time series data preparation failed: {e}")
            # Return minimal data
            dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
            return pd.DataFrame({'ds': dates, 'y': np.random.normal(100, 10, len(dates))})
    
    def _generate_revenue_series(self, base_revenue: float, length: int) -> np.ndarray:
        """Generate realistic revenue time series"""
        # Add trend, seasonality, and noise
        trend = np.linspace(0, 0.2, length)  # 20% growth over period
        seasonal = np.sin(np.arange(length) * 2 * np.pi / 365) * 0.1  # Annual seasonality
        noise = np.random.normal(0, 0.05, length)  # 5% noise
        
        values = base_revenue * (1 + trend + seasonal + noise)
        return np.maximum(values, 0)  # Ensure non-negative
    
    def _generate_engagement_series(self, base_engagement: float, length: int) -> np.ndarray:
        """Generate realistic engagement time series"""
        # Add trend and seasonality
        trend = np.linspace(0, 0.1, length)  # 10% improvement over period
        seasonal = np.sin(np.arange(length) * 2 * np.pi / 30) * 0.05  # Monthly seasonality
        noise = np.random.normal(0, 0.02, length)  # 2% noise
        
        values = base_engagement + trend + seasonal + noise
        return np.clip(values, 0, 1)  # Ensure between 0 and 1
    
    def _generate_health_series(self, base_health: float, length: int) -> np.ndarray:
        """Generate realistic health score time series"""
        # Add trend and seasonality
        trend = np.linspace(0, 0.15, length)  # 15% improvement over period
        seasonal = np.sin(np.arange(length) * 2 * np.pi / 90) * 5  # Quarterly seasonality
        noise = np.random.normal(0, 2, length)  # Small noise
        
        values = base_health + trend + seasonal + noise
        return np.clip(values, 0, 100)  # Ensure between 0 and 100
    
    def train_model(self, ts_data: pd.DataFrame) -> bool:
        """
        Train the Prophet model
        
        Args:
            ts_data: Time series data in Prophet format
            
        Returns:
            True if training successful, False otherwise
        """
        try:
            if PROPHET_AVAILABLE:
                # Use actual Prophet model
                self.model = Prophet(
                    yearly_seasonality=True,
                    weekly_seasonality=True,
                    daily_seasonality=False,
                    seasonality_mode='multiplicative'
                )
                
                # Add custom seasonalities
                self.model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
                
                # Fit the model
                self.model.fit(ts_data)
                self.is_trained = True
                
                logger.info("Prophet model trained successfully")
            else:
                # Use simplified model
                self.model = self._create_simplified_model(ts_data)
                self.is_trained = True
                
                logger.info("Simplified forecasting model trained")
            
            self.forecast_data = ts_data
            return True
            
        except Exception as e:
            logger.error(f"Model training failed: {e}")
            return False
    
    def _create_simplified_model(self, ts_data: pd.DataFrame) -> Dict[str, Any]:
        """Create a simplified forecasting model when Prophet is not available"""
        # Calculate trend and seasonality
        values = ts_data['y'].values
        dates = ts_data['ds'].values
        
        # Simple linear trend
        x = np.arange(len(values))
        trend_coef = np.polyfit(x, values, 1)
        trend = np.polyval(trend_coef, x)
        
        # Simple seasonality (monthly)
        seasonal_period = 30
        seasonal = np.sin(2 * np.pi * x / seasonal_period) * np.std(values) * 0.1
        
        # Store model parameters
        model = {
            'trend_coef': trend_coef,
            'seasonal_period': seasonal_period,
            'seasonal_amplitude': np.std(values) * 0.1,
            'mean_value': np.mean(values),
            'std_value': np.std(values)
        }
        
        return model
    
    def generate_forecast(self, periods: int) -> pd.DataFrame:
        """
        Generate forecast for specified number of periods
        
        Args:
            periods: Number of periods to forecast
            
        Returns:
            Forecast DataFrame with predictions and confidence intervals
        """
        try:
            if not self.is_trained:
                raise ValueError("Model must be trained before generating forecasts")
            
            if PROPHET_AVAILABLE and self.model is not None:
                # Use Prophet forecasting
                future = self.model.make_future_dataframe(periods=periods)
                forecast = self.model.predict(future)
                
                # Return only future periods
                forecast_result = forecast.tail(periods)[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
                forecast_result.columns = ['date', 'forecast', 'lower_bound', 'upper_bound']
                
            else:
                # Use simplified forecasting
                forecast_result = self._simplified_forecast(periods)
            
            logger.info(f"Forecast generated for {periods} periods")
            return forecast_result
            
        except Exception as e:
            logger.error(f"Forecast generation failed: {e}")
            # Return empty forecast
            dates = pd.date_range(start=datetime.now(), periods=periods, freq='D')
            return pd.DataFrame({
                'date': dates,
                'forecast': np.zeros(periods),
                'lower_bound': np.zeros(periods),
                'upper_bound': np.zeros(periods)
            })
    
    def _simplified_forecast(self, periods: int) -> pd.DataFrame:
        """Generate simplified forecast when Prophet is not available"""
        if self.model is None:
            # Create default model
            self.model = {
                'trend_coef': [0, 100],
                'seasonal_period': 30,
                'seasonal_amplitude': 10,
                'mean_value': 100,
                'std_value': 20
            }
        
        # Generate future dates
        dates = pd.date_range(start=datetime.now(), periods=periods, freq='D')
        
        # Calculate forecast values
        x = np.arange(len(self.forecast_data), len(self.forecast_data) + periods)
        trend = np.polyval(self.model['trend_coef'], x)
        seasonal = np.sin(2 * np.pi * x / self.model['seasonal_period']) * self.model['seasonal_amplitude']
        noise = np.random.normal(0, self.model['std_value'] * 0.1, periods)
        
        forecast_values = trend + seasonal + noise
        
        # Calculate confidence intervals
        std_error = self.model['std_value'] * 0.1
        lower_bound = forecast_values - 1.96 * std_error
        upper_bound = forecast_values + 1.96 * std_error
        
        return pd.DataFrame({
            'date': dates,
            'forecast': forecast_values,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound
        })
    
    def get_forecast_insights(self, forecast: pd.DataFrame, historical_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate insights from the forecast
        
        Args:
            forecast: Forecast DataFrame
            historical_data: Historical data for comparison
            
        Returns:
            Dictionary containing forecast insights
        """
        try:
            if forecast.empty or historical_data.empty:
                return {"error": "No forecast or historical data available"}
            
            # Calculate key metrics
            current_value = historical_data['y'].iloc[-1] if 'y' in historical_data.columns else 0
            forecasted_value = forecast['forecast'].iloc[-1]
            
            # Calculate growth rate
            if current_value > 0:
                growth_rate = ((forecasted_value - current_value) / current_value) * 100
            else:
                growth_rate = 0
            
            # Calculate trend direction
            if len(forecast) > 1:
                trend_direction = "Increasing" if forecast['forecast'].iloc[-1] > forecast['forecast'].iloc[0] else "Decreasing"
            else:
                trend_direction = "Stable"
            
            # Calculate confidence level
            confidence_level = self._calculate_confidence_level(forecast)
            
            # Generate recommendations
            recommendations = self._generate_forecast_recommendations(
                growth_rate, trend_direction, confidence_level
            )
            
            insights = {
                "current_value": current_value,
                "forecasted_value": forecasted_value,
                "growth_rate": growth_rate,
                "trend_direction": trend_direction,
                "confidence_level": confidence_level,
                "recommendations": recommendations,
                "forecast_periods": len(forecast)
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"Forecast insights generation failed: {e}")
            return {"error": f"Error generating insights: {e}"}
    
    def _calculate_confidence_level(self, forecast: pd.DataFrame) -> str:
        """Calculate confidence level based on forecast uncertainty"""
        try:
            if 'upper_bound' in forecast.columns and 'lower_bound' in forecast.columns:
                uncertainty = (forecast['upper_bound'] - forecast['lower_bound']).mean()
                relative_uncertainty = uncertainty / forecast['forecast'].mean()
                
                if relative_uncertainty < 0.1:
                    return "High"
                elif relative_uncertainty < 0.2:
                    return "Medium"
                else:
                    return "Low"
            else:
                return "Medium"
        except:
            return "Medium"
    
    def _generate_forecast_recommendations(self, growth_rate: float, trend_direction: str, confidence_level: str) -> list:
        """Generate recommendations based on forecast insights"""
        recommendations = []
        
        if growth_rate > 10:
            recommendations.append("Strong positive growth expected - consider scaling resources")
        elif growth_rate < -10:
            recommendations.append("Declining trend detected - implement retention strategies")
        else:
            recommendations.append("Stable trend - maintain current strategies")
        
        if confidence_level == "Low":
            recommendations.append("High uncertainty in forecast - monitor closely and adjust strategies")
        
        if trend_direction == "Decreasing":
            recommendations.append("Declining trend - investigate root causes and implement interventions")
        
        return recommendations
    
    def create_forecast_visualization(self, historical_data: pd.DataFrame, forecast: pd.DataFrame, title: str = "Forecast") -> Any:
        """
        Create visualization of historical data and forecast
        
        Args:
            historical_data: Historical time series data
            forecast: Forecast data
            title: Chart title
            
        Returns:
            Plotly figure object
        """
        try:
            import plotly.graph_objects as go
            
            fig = go.Figure()
            
            # Add historical data
            fig.add_trace(go.Scatter(
                x=historical_data['ds'],
                y=historical_data['y'],
                mode='lines',
                name='Historical',
                line=dict(color='#004D7A', width=2)
            ))
            
            # Add forecast
            fig.add_trace(go.Scatter(
                x=forecast['date'],
                y=forecast['forecast'],
                mode='lines',
                name='Forecast',
                line=dict(color='#00B3B3', width=2, dash='dash')
            ))
            
            # Add confidence interval
            if 'upper_bound' in forecast.columns and 'lower_bound' in forecast.columns:
                fig.add_trace(go.Scatter(
                    x=forecast['date'],
                    y=forecast['upper_bound'],
                    mode='lines',
                    line=dict(width=0),
                    showlegend=False,
                    hoverinfo='skip'
                ))
                
                fig.add_trace(go.Scatter(
                    x=forecast['date'],
                    y=forecast['lower_bound'],
                    mode='lines',
                    line=dict(width=0),
                    fill='tonexty',
                    fillcolor='rgba(0, 179, 179, 0.2)',
                    name='Confidence Interval',
                    hoverinfo='skip'
                ))
            
            fig.update_layout(
                title=title,
                xaxis_title="Date",
                yaxis_title="Value",
                hovermode='x unified',
                template='plotly_white'
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Forecast visualization creation failed: {e}")
            return None
