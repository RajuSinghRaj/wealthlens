# © 2025 Raju Singh Rajpurohit. All rights reserved.
import sys
import os
import json

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from calculations import calculate_investment

def handler(request):
    """Vercel serverless function handler"""
    
    # Handle CORS
    headers = {
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }
    
    # Handle preflight
    if request.method == 'OPTIONS':
        return ('', 204, headers)
    
    # GET /api
    if request.method == 'GET' and request.path == '/api':
        return (json.dumps({
            "app": "WealthLens",
            "status": "running"
        }), 200, headers)
    
    # POST /api/calculate
    if request.method == 'POST' and request.path == '/api/calculate':
        try:
            data = json.loads(request.body.decode('utf-8'))
            
            sip = calculate_investment(
                monthly_amount=float(data.get("monthly_amount", 0)),
                years=int(data.get("years", 0)),
                annual_return=float(data.get("expected_return", 0)),
                step_up_percent=float(data.get("step_up_percent", 0)),
                expense_ratio=float(data.get("expense_ratio", 0)),
                exit_load=float(data.get("exit_load", 0)),
                tax_percentage=float(data.get("tax_percentage", 0)),
                inflation_percentage=float(data.get("inflation_percentage", 0)),
                pause_months=int(data.get("pause_months", 0))
            )
            
            return (json.dumps({"sip": sip}), 200, headers)
        
        except Exception as e:
            return (json.dumps({"error": str(e)}), 500, headers)
    
    # 404
    return (json.dumps({"error": "NOT_FOUND"}), 404, headers)
