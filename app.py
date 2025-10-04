"""
Caprae Capital AI-Readiness Challenge
Lead Enhancement Tool - Main Application

This application enhances lead generation by providing:
1. AI-powered lead scoring
2. Data validation and enrichment
3. Lead prioritization and insights
"""

from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import json
from lead_scorer import LeadScorer
from data_validator import DataValidator
import os
from datetime import datetime

app = Flask(__name__)

# Initialize components
lead_scorer = LeadScorer()
data_validator = DataValidator()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/score-leads', methods=['POST'])
def score_leads():
    """API endpoint to score leads"""
    try:
        data = request.get_json()
        leads = data.get('leads', [])
        
        if not leads:
            return jsonify({'error': 'No leads provided'}), 400
        
        # Process and score leads
        scored_leads = []
        for lead in leads:
            # Validate data first
            validated_lead = data_validator.validate_lead(lead)
            
            # Score the lead
            score_data = lead_scorer.calculate_score(validated_lead)
            
            # Combine original data with validation and scoring
            enhanced_lead = {
                **validated_lead,
                'lead_score': score_data['total_score'],
                'score_breakdown': score_data['breakdown'],
                'recommendations': score_data['recommendations'],
                'priority_level': score_data['priority_level']
            }
            
            scored_leads.append(enhanced_lead)
        
        # Sort by score (highest first)
        scored_leads.sort(key=lambda x: x['lead_score'], reverse=True)
        
        return jsonify({
            'success': True,
            'leads': scored_leads,
            'summary': {
                'total_leads': len(scored_leads),
                'high_priority': len([l for l in scored_leads if l['priority_level'] == 'High']),
                'medium_priority': len([l for l in scored_leads if l['priority_level'] == 'Medium']),
                'low_priority': len([l for l in scored_leads if l['priority_level'] == 'Low'])
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/validate-data', methods=['POST'])
def validate_data():
    """API endpoint to validate lead data"""
    try:
        data = request.get_json()
        leads = data.get('leads', [])
        
        validated_leads = []
        for lead in leads:
            validated_lead = data_validator.validate_lead(lead)
            validated_leads.append(validated_lead)
        
        return jsonify({
            'success': True,
            'leads': validated_leads
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export', methods=['POST'])
def export_leads():
    """Export leads to CSV"""
    try:
        data = request.get_json()
        leads = data.get('leads', [])
        
        if not leads:
            return jsonify({'error': 'No leads to export'}), 400
        
        # Create DataFrame
        df = pd.DataFrame(leads)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"enhanced_leads_{timestamp}.csv"
        
        # Save to CSV
        df.to_csv(filename, index=False)
        
        return send_file(filename, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sample-data')
def get_sample_data():
    """Get sample lead data for testing"""
    sample_leads = [
        {
            "company_name": "TechCorp Solutions",
            "contact_name": "John Smith",
            "email": "john.smith@techcorp.com",
            "phone": "+1-555-123-4567",
            "industry": "Technology",
            "company_size": "50-200",
            "revenue": "10M-50M",
            "website": "https://techcorp.com",
            "linkedin": "https://linkedin.com/company/techcorp"
        },
        {
            "company_name": "Global Manufacturing Inc",
            "contact_name": "Sarah Johnson",
            "email": "sarah.j@globalmfg.com",
            "phone": "555-987-6543",
            "industry": "Manufacturing",
            "company_size": "500+",
            "revenue": "100M+",
            "website": "https://globalmfg.com",
            "linkedin": "https://linkedin.com/company/global-manufacturing"
        },
        {
            "company_name": "StartupXYZ",
            "contact_name": "Mike Chen",
            "email": "mike@startupxyz.io",
            "phone": "+1-555-456-7890",
            "industry": "SaaS",
            "company_size": "1-10",
            "revenue": "1M-5M",
            "website": "https://startupxyz.io",
            "linkedin": "https://linkedin.com/company/startupxyz"
        }
    ]
    
    return jsonify({'leads': sample_leads})

if __name__ == '__main__':
    # Create templates and static directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
