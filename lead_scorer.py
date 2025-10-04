"""
Lead Scoring Algorithm for Caprae Capital AI-Readiness Challenge

This module implements an AI-powered lead scoring system that evaluates leads
based on multiple factors to help sales teams prioritize their outreach efforts.
"""

import re
from typing import Dict, List, Any
import math

class LeadScorer:
    """
    Advanced lead scoring system that evaluates leads based on:
    - Company characteristics (size, revenue, industry)
    - Contact completeness and quality
    - Engagement potential
    - Data quality indicators
    """
    
    def __init__(self):
        # Industry scoring weights (higher = more valuable for B2B sales)
        self.industry_weights = {
            'Technology': 0.9,
            'SaaS': 0.95,
            'Software': 0.9,
            'Fintech': 0.85,
            'Healthcare': 0.8,
            'Manufacturing': 0.7,
            'Retail': 0.6,
            'Real Estate': 0.5,
            'Education': 0.6,
            'Consulting': 0.7,
            'Other': 0.5
        }
        
        # Company size scoring (revenue potential)
        self.size_weights = {
            '1-10': 0.3,
            '11-50': 0.5,
            '51-200': 0.7,
            '201-500': 0.8,
            '500+': 0.9
        }
        
        # Revenue scoring
        self.revenue_weights = {
            '0-1M': 0.2,
            '1M-5M': 0.4,
            '5M-10M': 0.6,
            '10M-50M': 0.8,
            '50M-100M': 0.9,
            '100M+': 1.0
        }
    
    def calculate_score(self, lead: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate comprehensive lead score based on multiple factors
        
        Args:
            lead: Dictionary containing lead information
            
        Returns:
            Dictionary with score breakdown and recommendations
        """
        scores = {}
        
        # Company Score (40% weight)
        company_score = self._calculate_company_score(lead)
        scores['company'] = company_score
        
        # Contact Quality Score (30% weight)
        contact_score = self._calculate_contact_score(lead)
        scores['contact'] = contact_score
        
        # Data Completeness Score (20% weight)
        completeness_score = self._calculate_completeness_score(lead)
        scores['completeness'] = completeness_score
        
        # Engagement Potential Score (10% weight)
        engagement_score = self._calculate_engagement_score(lead)
        scores['engagement'] = engagement_score
        
        # Calculate weighted total score
        total_score = (
            company_score * 0.4 +
            contact_score * 0.3 +
            completeness_score * 0.2 +
            engagement_score * 0.1
        )
        
        # Round to 2 decimal places
        total_score = round(total_score, 2)
        
        # Determine priority level
        priority_level = self._determine_priority_level(total_score)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(lead, scores)
        
        return {
            'total_score': total_score,
            'breakdown': scores,
            'priority_level': priority_level,
            'recommendations': recommendations
        }
    
    def _calculate_company_score(self, lead: Dict[str, Any]) -> float:
        """Calculate company-related score"""
        score = 0.0
        
        # Industry scoring
        industry = lead.get('industry', '').lower()
        industry_score = 0.5  # default
        
        for key, weight in self.industry_weights.items():
            if key.lower() in industry:
                industry_score = weight
                break
        
        score += industry_score * 40
        
        # Company size scoring
        company_size = lead.get('company_size', '')
        size_score = self.size_weights.get(company_size, 0.5)
        score += size_score * 30
        
        # Revenue scoring
        revenue = lead.get('revenue', '')
        revenue_score = self.revenue_weights.get(revenue, 0.5)
        score += revenue_score * 30
        
        return min(score, 100.0)
    
    def _calculate_contact_score(self, lead: Dict[str, Any]) -> float:
        """Calculate contact quality score"""
        score = 0.0
        
        # Email quality
        email = lead.get('email', '')
        if email:
            if self._is_valid_email(email):
                score += 30
                # Bonus for professional email domains
                if any(domain in email.lower() for domain in ['gmail.com', 'yahoo.com']):
                    score += 5  # Personal email, slightly lower
                else:
                    score += 15  # Corporate email, higher value
            else:
                score += 5  # Invalid email, minimal points
        
        # Phone quality
        phone = lead.get('phone', '')
        if phone and self._is_valid_phone(phone):
            score += 20
        
        # LinkedIn presence
        linkedin = lead.get('linkedin', '')
        if linkedin and 'linkedin.com' in linkedin.lower():
            score += 20
        
        # Contact name quality
        contact_name = lead.get('contact_name', '')
        if contact_name and len(contact_name.split()) >= 2:
            score += 15
        elif contact_name:
            score += 10
        
        # Website presence
        website = lead.get('website', '')
        if website and self._is_valid_url(website):
            score += 15
        
        return min(score, 100.0)
    
    def _calculate_completeness_score(self, lead: Dict[str, Any]) -> float:
        """Calculate data completeness score"""
        required_fields = ['company_name', 'contact_name', 'email', 'phone', 'industry']
        optional_fields = ['website', 'linkedin', 'company_size', 'revenue']
        
        total_fields = len(required_fields) + len(optional_fields)
        filled_fields = 0
        
        # Count required fields
        for field in required_fields:
            if lead.get(field) and str(lead.get(field)).strip():
                filled_fields += 1
        
        # Count optional fields (weighted less)
        for field in optional_fields:
            if lead.get(field) and str(lead.get(field)).strip():
                filled_fields += 0.5
        
        return (filled_fields / total_fields) * 100
    
    def _calculate_engagement_score(self, lead: Dict[str, Any]) -> float:
        """Calculate engagement potential score"""
        score = 0.0
        
        # Company name quality (professional sounding)
        company_name = lead.get('company_name', '').lower()
        professional_indicators = ['inc', 'corp', 'llc', 'ltd', 'solutions', 'systems', 'technologies', 'group']
        
        if any(indicator in company_name for indicator in professional_indicators):
            score += 30
        
        # Industry growth potential
        industry = lead.get('industry', '').lower()
        high_growth_industries = ['technology', 'saas', 'software', 'fintech', 'ai', 'machine learning']
        
        if any(industry_keyword in industry for industry_keyword in high_growth_industries):
            score += 40
        
        # Company size indicates growth stage
        company_size = lead.get('company_size', '')
        if company_size in ['51-200', '201-500']:  # Sweet spot for B2B sales
            score += 30
        
        return min(score, 100.0)
    
    def _determine_priority_level(self, score: float) -> str:
        """Determine priority level based on score"""
        if score >= 80:
            return 'High'
        elif score >= 60:
            return 'Medium'
        else:
            return 'Low'
    
    def _generate_recommendations(self, lead: Dict[str, Any], scores: Dict[str, float]) -> List[str]:
        """Generate actionable recommendations for the lead"""
        recommendations = []
        
        # Company recommendations
        if scores['company'] < 60:
            recommendations.append("Consider targeting companies in high-growth industries like Technology or SaaS")
        
        # Contact recommendations
        if scores['contact'] < 50:
            if not lead.get('email') or not self._is_valid_email(lead.get('email', '')):
                recommendations.append("Verify and update email address for better contact quality")
            if not lead.get('phone') or not self._is_valid_phone(lead.get('phone', '')):
                recommendations.append("Add valid phone number to improve contact score")
            if not lead.get('linkedin'):
                recommendations.append("Find and add LinkedIn profile for better engagement")
        
        # Completeness recommendations
        if scores['completeness'] < 70:
            missing_fields = []
            for field in ['company_size', 'revenue', 'website']:
                if not lead.get(field):
                    missing_fields.append(field.replace('_', ' ').title())
            
            if missing_fields:
                recommendations.append(f"Complete missing information: {', '.join(missing_fields)}")
        
        # Engagement recommendations
        if scores['engagement'] < 50:
            recommendations.append("This lead may require more nurturing before direct outreach")
        
        # High-value lead recommendations
        if scores['company'] >= 80 and scores['contact'] >= 70:
            recommendations.append("High-value lead - prioritize for immediate outreach")
        
        return recommendations
    
    def _is_valid_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def _is_valid_phone(self, phone: str) -> bool:
        """Validate phone number format"""
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone)
        # Check if it has 10-15 digits (international format)
        return 10 <= len(digits_only) <= 15
    
    def _is_valid_url(self, url: str) -> bool:
        """Validate URL format"""
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return bool(re.match(pattern, url))
