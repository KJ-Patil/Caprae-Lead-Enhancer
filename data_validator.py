"""
Data Validation and Enrichment Module for Caprae Capital AI-Readiness Challenge

This module provides comprehensive data validation, cleaning, and enrichment
capabilities for lead generation data.
"""

import re
import phonenumbers
from email_validator import validate_email, EmailNotValidError
from typing import Dict, Any, List, Tuple
from fuzzywuzzy import fuzz, process

class DataValidator:
    """
    Comprehensive data validation and enrichment system that:
    - Validates email addresses and phone numbers
    - Cleans and standardizes data formats
    - Detects and handles duplicates
    - Enriches missing information where possible
    """
    
    def __init__(self):
        # Common industry mappings for standardization
        self.industry_mappings = {
            'tech': 'Technology',
            'software': 'Software',
            'saas': 'SaaS',
            'fintech': 'Fintech',
            'healthcare': 'Healthcare',
            'manufacturing': 'Manufacturing',
            'retail': 'Retail',
            'real estate': 'Real Estate',
            'education': 'Education',
            'consulting': 'Consulting'
        }
        
        # Company size standardization
        self.size_mappings = {
            'startup': '1-10',
            'small': '11-50',
            'medium': '51-200',
            'large': '201-500',
            'enterprise': '500+'
        }
    
    def validate_lead(self, lead: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive lead validation and enrichment
        
        Args:
            lead: Raw lead data dictionary
            
        Returns:
            Validated and enriched lead data
        """
        validated_lead = lead.copy()
        
        # Validate and clean each field
        email_data = self._validate_email(lead.get('email', ''))
        validated_lead['email'] = email_data['value'] if isinstance(email_data, dict) else email_data
        
        phone_data = self._validate_phone(lead.get('phone', ''))
        validated_lead['phone'] = phone_data['value'] if isinstance(phone_data, dict) else phone_data
        validated_lead['company_name'] = self._clean_company_name(lead.get('company_name', ''))
        validated_lead['contact_name'] = self._clean_contact_name(lead.get('contact_name', ''))
        validated_lead['industry'] = self._standardize_industry(lead.get('industry', ''))
        validated_lead['company_size'] = self._standardize_company_size(lead.get('company_size', ''))
        validated_lead['revenue'] = self._standardize_revenue(lead.get('revenue', ''))
        website_data = self._validate_url(lead.get('website', ''))
        validated_lead['website'] = website_data['value'] if isinstance(website_data, dict) else website_data
        
        linkedin_data = self._validate_linkedin(lead.get('linkedin', ''))
        validated_lead['linkedin'] = linkedin_data['value'] if isinstance(linkedin_data, dict) else linkedin_data
        
        # Add validation flags
        validated_lead['validation_flags'] = self._get_validation_flags(validated_lead)
        
        # Add data quality score
        validated_lead['data_quality_score'] = self._calculate_data_quality_score(validated_lead)
        
        return validated_lead
    
    def _validate_email(self, email: str) -> Dict[str, Any]:
        """Validate and enrich email data"""
        if not email or not email.strip():
            return {
                'value': '',
                'is_valid': False,
                'deliverability': 'unknown',
                'suggestions': ['Email address is required']
            }
        
        email = email.strip().lower()
        
        try:
            # Validate email format
            valid = validate_email(email)
            email = valid.email
            
            # Check deliverability indicators
            deliverability = self._assess_email_deliverability(email)
            
            return {
                'value': email,
                'is_valid': True,
                'deliverability': deliverability,
                'suggestions': []
            }
            
        except EmailNotValidError as e:
            suggestions = []
            if '@' not in email:
                suggestions.append('Email must contain @ symbol')
            if '.' not in email.split('@')[-1] if '@' in email else True:
                suggestions.append('Email must have valid domain')
            
            return {
                'value': email,
                'is_valid': False,
                'deliverability': 'invalid',
                'suggestions': suggestions
            }
    
    def _validate_phone(self, phone: str) -> Dict[str, Any]:
        """Validate and standardize phone number"""
        if not phone or not phone.strip():
            return {
                'value': '',
                'is_valid': False,
                'formatted': '',
                'country_code': '',
                'suggestions': ['Phone number is required']
            }
        
        phone = phone.strip()
        
        try:
            # Parse phone number
            parsed = phonenumbers.parse(phone, None)
            
            if phonenumbers.is_valid_number(parsed):
                formatted = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
                country_code = str(parsed.country_code)
                
                return {
                    'value': phone,
                    'is_valid': True,
                    'formatted': formatted,
                    'country_code': country_code,
                    'suggestions': []
                }
            else:
                return {
                    'value': phone,
                    'is_valid': False,
                    'formatted': '',
                    'country_code': '',
                    'suggestions': ['Invalid phone number format']
                }
                
        except phonenumbers.NumberParseException:
            # Try to clean and reformat
            cleaned = re.sub(r'[^\d+]', '', phone)
            if len(cleaned) >= 10:
                return {
                    'value': phone,
                    'is_valid': True,
                    'formatted': cleaned,
                    'country_code': '',
                    'suggestions': ['Phone number may need country code']
                }
            else:
                return {
                    'value': phone,
                    'is_valid': False,
                    'formatted': '',
                    'country_code': '',
                    'suggestions': ['Phone number too short or invalid format']
                }
    
    def _clean_company_name(self, name: str) -> str:
        """Clean and standardize company name"""
        if not name:
            return ''
        
        # Remove extra whitespace and standardize
        name = ' '.join(name.split())
        
        # Remove common suffixes that might be inconsistent
        suffixes_to_remove = [' inc', ' inc.', ' llc', ' llc.', ' corp', ' corp.', ' ltd', ' ltd.']
        for suffix in suffixes_to_remove:
            if name.lower().endswith(suffix):
                name = name[:-len(suffix)]
                break
        
        return name.strip()
    
    def _clean_contact_name(self, name: str) -> str:
        """Clean and standardize contact name"""
        if not name:
            return ''
        
        # Remove extra whitespace and standardize
        name = ' '.join(name.split())
        
        # Capitalize properly
        name_parts = name.split()
        capitalized_parts = []
        for part in name_parts:
            if part.upper() in ['JR', 'SR', 'III', 'IV', 'V']:
                capitalized_parts.append(part.upper())
            else:
                capitalized_parts.append(part.capitalize())
        
        return ' '.join(capitalized_parts)
    
    def _standardize_industry(self, industry: str) -> str:
        """Standardize industry classification"""
        if not industry:
            return 'Other'
        
        industry_lower = industry.lower().strip()
        
        # Direct mapping
        for key, value in self.industry_mappings.items():
            if key in industry_lower:
                return value
        
        # Fuzzy matching for close matches
        best_match = process.extractOne(industry_lower, list(self.industry_mappings.keys()))
        if best_match and best_match[1] >= 80:  # 80% similarity threshold
            return self.industry_mappings[best_match[0]]
        
        return industry.title()
    
    def _standardize_company_size(self, size: str) -> str:
        """Standardize company size classification"""
        if not size:
            return ''
        
        size_lower = size.lower().strip()
        
        # Direct mapping
        for key, value in self.size_mappings.items():
            if key in size_lower:
                return value
        
        # Try to extract numbers
        numbers = re.findall(r'\d+', size)
        if numbers:
            num_employees = int(numbers[0])
            if num_employees <= 10:
                return '1-10'
            elif num_employees <= 50:
                return '11-50'
            elif num_employees <= 200:
                return '51-200'
            elif num_employees <= 500:
                return '201-500'
            else:
                return '500+'
        
        return size
    
    def _standardize_revenue(self, revenue: str) -> str:
        """Standardize revenue classification"""
        if not revenue:
            return ''
        
        revenue_lower = revenue.lower().strip()
        
        # Extract numbers and convert to standard format
        numbers = re.findall(r'[\d.]+', revenue_lower)
        if numbers:
            try:
                value = float(numbers[0])
                if 'k' in revenue_lower or 'thousand' in revenue_lower:
                    value *= 1000
                elif 'm' in revenue_lower or 'million' in revenue_lower:
                    value *= 1000000
                elif 'b' in revenue_lower or 'billion' in revenue_lower:
                    value *= 1000000000
                
                # Categorize
                if value < 1000000:
                    return '0-1M'
                elif value < 5000000:
                    return '1M-5M'
                elif value < 10000000:
                    return '5M-10M'
                elif value < 50000000:
                    return '10M-50M'
                elif value < 100000000:
                    return '50M-100M'
                else:
                    return '100M+'
            except ValueError:
                pass
        
        return revenue
    
    def _validate_url(self, url: str) -> Dict[str, Any]:
        """Validate and clean URL"""
        if not url or not url.strip():
            return {
                'value': '',
                'is_valid': False,
                'suggestions': ['Website URL is recommended']
            }
        
        url = url.strip()
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Basic URL validation
        url_pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        if re.match(url_pattern, url):
            return {
                'value': url,
                'is_valid': True,
                'suggestions': []
            }
        else:
            return {
                'value': url,
                'is_valid': False,
                'suggestions': ['Invalid URL format']
            }
    
    def _validate_linkedin(self, linkedin: str) -> Dict[str, Any]:
        """Validate LinkedIn URL"""
        if not linkedin or not linkedin.strip():
            return {
                'value': '',
                'is_valid': False,
                'suggestions': ['LinkedIn profile is recommended']
            }
        
        linkedin = linkedin.strip()
        
        # Add protocol if missing
        if not linkedin.startswith(('http://', 'https://')):
            linkedin = 'https://' + linkedin
        
        # Check if it's a LinkedIn URL
        if 'linkedin.com' in linkedin.lower():
            return {
                'value': linkedin,
                'is_valid': True,
                'suggestions': []
            }
        else:
            return {
                'value': linkedin,
                'is_valid': False,
                'suggestions': ['Must be a valid LinkedIn URL']
            }
    
    def _get_validation_flags(self, lead: Dict[str, Any]) -> Dict[str, bool]:
        """Get validation flags for the lead"""
        flags = {}
        
        # Email validation
        email = lead.get('email', '')
        flags['has_valid_email'] = bool(email) and '@' in str(email)
        
        # Phone validation
        phone = lead.get('phone', '')
        flags['has_valid_phone'] = bool(phone) and len(str(phone).replace(' ', '').replace('-', '').replace('(', '').replace(')', '')) >= 10
        
        # Required fields
        flags['has_company_name'] = bool(lead.get('company_name'))
        flags['has_contact_name'] = bool(lead.get('contact_name'))
        flags['has_industry'] = bool(lead.get('industry'))
        
        # Optional fields
        flags['has_website'] = bool(lead.get('website'))
        flags['has_linkedin'] = bool(lead.get('linkedin'))
        flags['has_company_size'] = bool(lead.get('company_size'))
        flags['has_revenue'] = bool(lead.get('revenue'))
        
        return flags
    
    def _calculate_data_quality_score(self, lead: Dict[str, Any]) -> float:
        """Calculate overall data quality score"""
        flags = lead.get('validation_flags', {})
        
        # Weight different fields
        weights = {
            'has_valid_email': 0.25,
            'has_valid_phone': 0.20,
            'has_company_name': 0.15,
            'has_contact_name': 0.15,
            'has_industry': 0.10,
            'has_website': 0.05,
            'has_linkedin': 0.05,
            'has_company_size': 0.03,
            'has_revenue': 0.02
        }
        
        score = 0.0
        for flag, weight in weights.items():
            if flags.get(flag, False):
                score += weight
        
        return round(score * 100, 2)
    
    def _assess_email_deliverability(self, email: str) -> str:
        """Assess email deliverability based on domain and format"""
        domain = email.split('@')[-1].lower()
        
        # High deliverability domains
        high_deliverability = ['gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com']
        
        # Corporate domains (usually higher deliverability)
        corporate_indicators = ['.com', '.org', '.net', '.edu', '.gov']
        
        if domain in high_deliverability:
            return 'high'
        elif any(indicator in domain for indicator in corporate_indicators):
            return 'medium'
        else:
            return 'low'
    
    def detect_duplicates(self, leads: List[Dict[str, Any]], threshold: float = 0.85) -> List[Dict[str, Any]]:
        """
        Detect potential duplicate leads using fuzzy matching
        
        Args:
            leads: List of lead dictionaries
            threshold: Similarity threshold for duplicate detection
            
        Returns:
            List of duplicate groups
        """
        duplicates = []
        processed = set()
        
        for i, lead1 in enumerate(leads):
            if i in processed:
                continue
                
            duplicate_group = [lead1]
            
            for j, lead2 in enumerate(leads[i+1:], i+1):
                if j in processed:
                    continue
                
                # Compare company names
                company1 = lead1.get('company_name', '').lower()
                company2 = lead2.get('company_name', '').lower()
                
                if company1 and company2:
                    similarity = fuzz.ratio(company1, company2) / 100.0
                    
                    if similarity >= threshold:
                        duplicate_group.append(lead2)
                        processed.add(j)
            
            if len(duplicate_group) > 1:
                duplicates.append({
                    'group': duplicate_group,
                    'similarity_score': similarity,
                    'recommended_lead': self._select_best_lead(duplicate_group)
                })
                processed.add(i)
        
        return duplicates
    
    def _select_best_lead(self, leads: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Select the best lead from a duplicate group"""
        # Score each lead based on data completeness and quality
        best_lead = leads[0]
        best_score = 0
        
        for lead in leads:
            score = 0
            
            # Count filled fields
            for field in ['email', 'phone', 'website', 'linkedin', 'company_size', 'revenue']:
                if lead.get(field):
                    score += 1
            
            # Bonus for valid email
            email_data = lead.get('email', {})
            if isinstance(email_data, dict) and email_data.get('is_valid'):
                score += 2
            
            if score > best_score:
                best_score = score
                best_lead = lead
        
        return best_lead
