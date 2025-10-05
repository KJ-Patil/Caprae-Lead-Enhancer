# Caprae Lead Enhancer
## AI-Powered Lead Scoring and Validation System

A sophisticated lead generation enhancement tool built for the Caprae Capital AI-Readiness Challenge. This application provides AI-powered lead scoring, data validation, and prioritization to help sales teams maximize their conversion rates.


## 🚀 Features

### Core Capabilities
- **AI Lead Scoring**: Advanced algorithm that scores leads based on company characteristics, contact quality, and engagement potential
- **Data Validation**: Comprehensive validation of emails, phone numbers, and company data with quality scoring
- **Priority Ranking**: Automatically categorizes leads as High, Medium, or Low priority for focused outreach
- **Data Enrichment**: Standardizes and cleans lead data for better accuracy
- **Export Functionality**: Export processed leads to CSV for integration with CRM systems

### Technical Features
- **Real-time Processing**: Instant lead scoring and validation
- **Responsive Design**: Modern, mobile-friendly interface
- **RESTful API**: Clean API endpoints for integration
- **Data Quality Metrics**: Comprehensive scoring for data completeness and accuracy
- **Duplicate Detection**: Identifies and handles potential duplicate leads

## 🛠 Installation & Setup

See `HOW_TO_RUN.md` for step-by-step instructions.

## 🔧 API Endpoints

- POST `/api/score-leads` – score and analyze leads
- POST `/api/validate-data` – validate lead data quality
- POST `/api/export` – export leads to CSV format
- GET `/api/sample-data` – sample lead data for testing

## 📊 Scoring Algorithm

- Company (40%), Contact (30%), Completeness (20%), Engagement (10%)
- Industry, size, revenue weighting; email/phone/linkedin checks; data completeness; growth signals

## 🎯 Assessment Alignment
- Business value: prioritizes high-impact leads and usable insights
- Technical rigor: validation, enrichment, deterministic scoring, export
- UX: clean flows, sample data, CSV upload, clear feedback
- Communication: docs, scripts, summary, checklist

## 📨 Submission
- Follow `SUBMISSION_CHECKLIST.md` to prepare the GitHub link, video (1–2 min), and email to `Partners@capraecapital.com` with subject: `Developer Intern - Handbook Submission - [Your Name]`.

## 📝 Repository Structure
```
/ (project root)
├── app.py
├── data_validator.py
├── lead_scorer.py
├── requirements.txt
├── templates/
├── static/
├── sample_leads.csv
├── README.md
├── HOW_TO_RUN.md
├── PROJECT_SUMMARY.md
```

## 📄 License
This project is proprietary and confidential. Built for Caprae Capital Partners.
