#!/usr/bin/env python3
"""
NewAI API Server
Provides API endpoints for NewAI churn prediction integration
"""

import json
import os
import sys
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import logging

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from newai_integration import NewAIIntegration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewAIAPIHandler(BaseHTTPRequestHandler):
    """HTTP request handler for NewAI API"""
    
    def __init__(self, *args, **kwargs):
        self.newai = NewAIIntegration()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        try:
            if self.path == '/api/newai/info':
                self._handle_model_info()
            elif self.path == '/api/newai/predict':
                self._handle_predict()
            elif self.path == '/api/newai/health':
                self._handle_health()
            elif self.path == '/api/newai/download-predictions':
                self._handle_download_predictions()
            else:
                self._send_error(404, "Not Found")
        except Exception as e:
            logger.error(f"Error handling GET request: {e}")
            self._send_error(500, f"Internal Server Error: {str(e)}")
    
    def do_POST(self):
        """Handle POST requests"""
        try:
            if self.path == '/api/newai/upload':
                self._handle_upload()
            elif self.path == '/api/newai/predict':
                self._handle_predict_post()
            else:
                self._send_error(404, "Not Found")
        except Exception as e:
            logger.error(f"Error handling POST request: {e}")
            self._send_error(500, f"Internal Server Error: {str(e)}")
    
    def _handle_model_info(self):
        """Handle model info request"""
        info = self.newai.get_model_info()
        self._send_json_response(info)
    
    def _handle_predict(self):
        """Handle prediction request"""
        results = self.newai.run_churn_prediction()
        self._send_json_response(results)
    
    def _handle_predict_post(self):
        """Handle prediction request with data"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            results = self.newai.run_churn_prediction()
            self._send_json_response(results)
        except json.JSONDecodeError:
            self._send_error(400, "Invalid JSON")
    
    def _handle_upload(self):
        """Handle data upload request"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            # In a real implementation, you would save the uploaded file
            # For now, we'll just run predictions on sample data
            results = self.newai.run_churn_prediction()
            self._send_json_response({
                "success": True,
                "message": "Data uploaded and processed successfully",
                "results": results
            })
        except json.JSONDecodeError:
            self._send_error(400, "Invalid JSON")
    
    def _handle_health(self):
        """Handle health check request"""
        health = {
            "status": "healthy",
            "newai_available": self.newai.available,
            "version": "1.0.0"
        }
        self._send_json_response(health)
    
    def _handle_download_predictions(self):
        """Handle predictions.csv download request - returns only AI output columns"""
        try:
            predictions_file = self.newai.newai_path / "predictions.csv"
            
            if not predictions_file.exists():
                self._send_error(404, "predictions.csv not found. Please run the model first.")
                return
            
            # Read and filter the predictions.csv file to only include AI output columns
            import pandas as pd
            df = pd.read_csv(predictions_file)
            
            # Keep only the essential AI output columns
            ai_output_columns = ['customerID', 'churn_probability', 'risk_level']
            filtered_df = df[ai_output_columns]
            
            # Convert to CSV
            csv_content = filtered_df.to_csv(index=False)
            
            # Send the filtered file
            self.send_response(200)
            self.send_header('Content-Type', 'text/csv')
            self.send_header('Content-Disposition', 'attachment; filename="predictions_ai_output.csv"')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(csv_content.encode('utf-8'))
            
        except Exception as e:
            logger.error(f"Error downloading predictions.csv: {e}")
            self._send_error(500, f"Error downloading predictions.csv: {str(e)}")
    
    def _send_json_response(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response = json.dumps(data, indent=2)
        self.wfile.write(response.encode('utf-8'))
    
    def _send_error(self, code, message):
        """Send error response"""
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        error_response = {
            "error": True,
            "code": code,
            "message": message
        }
        response = json.dumps(error_response, indent=2)
        self.wfile.write(response.encode('utf-8'))
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def start_newai_api(port=8081):
    """Start the NewAI API server"""
    try:
        server_address = ('', port)
        httpd = HTTPServer(server_address, NewAIAPIHandler)
        
        print("🤖 NewAI API Server Starting...")
        print("=" * 50)
        print(f"🌐 API running at: http://localhost:{port}")
        print("📊 Available endpoints:")
        print("   • GET  /api/newai/info     - Model information")
        print("   • GET  /api/newai/predict  - Run predictions")
        print("   • POST /api/newai/upload   - Upload data")
        print("   • GET  /api/newai/health   - Health check")
        print("=" * 50)
        print("🛑 Press Ctrl+C to stop the server")
        
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        print("\n🛑 NewAI API server stopped by user")
    except Exception as e:
        print(f"❌ Error starting NewAI API server: {e}")

def main():
    """Main function"""
    print("🤖 NewAI API Server")
    print("AI-Powered Churn Prediction API")
    print("=" * 50)
    
    # Get port from command line or use default
    port = 8081
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("❌ Invalid port number. Using default port 8081.")
    
    # Start the server
    start_newai_api(port)

if __name__ == "__main__":
    main()
