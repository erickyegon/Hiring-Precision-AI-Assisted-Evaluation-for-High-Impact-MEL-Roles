"""
MEL Manager Job Description and Scoring Criteria
"""

MEL_MANAGER_JOB_DESCRIPTION = """
POSITION: MEL Manager (Monitoring, Evaluation, and Learning)

ROLE OVERVIEW:
The MEL Manager will be responsible for designing, implementing, and managing comprehensive monitoring, evaluation, and learning systems for development programs. This role requires strong analytical skills, experience with data collection and analysis, and the ability to translate findings into actionable recommendations for program improvement.

KEY RESPONSIBILITIES:
1. Design and implement MEL frameworks and systems
2. Develop data collection tools and methodologies
3. Conduct regular monitoring and evaluation activities
4. Analyze program data and prepare comprehensive reports
5. Facilitate learning sessions and knowledge sharing
6. Ensure compliance with donor requirements and standards
7. Build capacity of program staff in MEL practices
8. Manage MEL databases and information systems
9. Coordinate with external evaluators and consultants
10. Support evidence-based decision making

REQUIRED QUALIFICATIONS:
- Master's degree in Development Studies, Statistics, Economics, Social Sciences, or related field
- Minimum 5 years of experience in MEL, research, or program evaluation
- Strong knowledge of MEL frameworks and methodologies
- Experience with quantitative and qualitative data analysis
- Proficiency in statistical software (SPSS, R, Stata, or similar)
- Experience with data visualization tools
- Strong report writing and presentation skills
- Experience working with international development organizations
- Knowledge of donor requirements (USAID, EU, UN, etc.)
- Experience in project management

PREFERRED QUALIFICATIONS:
- PhD in relevant field
- 7+ years of MEL experience
- Experience in East Africa or similar contexts
- Certification in evaluation (AEA, IOCE, etc.)
- Experience with impact evaluation methodologies
- Knowledge of participatory evaluation approaches
- Experience with digital data collection tools
- Multilingual capabilities

TECHNICAL SKILLS:
- Statistical analysis software (SPSS, R, Stata, SAS)
- Data visualization (Tableau, Power BI, Excel)
- Survey design and implementation
- Database management
- GIS and mapping software
- Mobile data collection platforms (KoBo, ODK, SurveyCTO)
- Project management software
- Microsoft Office Suite (advanced Excel)

SOFT SKILLS:
- Strong analytical and critical thinking
- Excellent communication and presentation skills
- Attention to detail and accuracy
- Ability to work under pressure and meet deadlines
- Cultural sensitivity and adaptability
- Team leadership and collaboration
- Problem-solving and innovation
- Stakeholder management
"""

SCORING_CRITERIA = {
    "education": {
        "weight": 20,
        "description": "Educational background and qualifications",
        "scoring_guide": {
            "excellent": "PhD in relevant field (25-30 points)",
            "very_good": "Master's in relevant field (20-24 points)", 
            "good": "Bachelor's in relevant field with additional certifications (15-19 points)",
            "fair": "Bachelor's in relevant field (10-14 points)",
            "poor": "Below bachelor's or irrelevant field (0-9 points)"
        }
    },
    "experience": {
        "weight": 25,
        "description": "MEL and relevant work experience",
        "scoring_guide": {
            "excellent": "7+ years MEL experience (25-30 points)",
            "very_good": "5-6 years MEL experience (20-24 points)",
            "good": "3-4 years MEL experience (15-19 points)", 
            "fair": "1-2 years MEL experience (10-14 points)",
            "poor": "No MEL experience (0-9 points)"
        }
    },
    "technical_skills": {
        "weight": 20,
        "description": "Technical skills in data analysis, software, and tools",
        "scoring_guide": {
            "excellent": "Advanced skills in multiple statistical software, data viz tools (25-30 points)",
            "very_good": "Proficient in statistical software and data analysis (20-24 points)",
            "good": "Basic statistical software knowledge (15-19 points)",
            "fair": "Limited technical skills (10-14 points)", 
            "poor": "No relevant technical skills (0-9 points)"
        }
    },
    "sector_knowledge": {
        "weight": 15,
        "description": "Knowledge of development sector and donor requirements",
        "scoring_guide": {
            "excellent": "Extensive development sector experience with multiple donors (25-30 points)",
            "very_good": "Good development sector knowledge (20-24 points)",
            "good": "Some development sector experience (15-19 points)",
            "fair": "Limited sector knowledge (10-14 points)",
            "poor": "No development sector experience (0-9 points)"
        }
    },
    "communication": {
        "weight": 10,
        "description": "Communication, presentation, and report writing skills",
        "scoring_guide": {
            "excellent": "Exceptional communication skills, published work (25-30 points)",
            "very_good": "Strong communication and presentation skills (20-24 points)",
            "good": "Good communication skills (15-19 points)",
            "fair": "Basic communication skills (10-14 points)",
            "poor": "Poor communication skills (0-9 points)"
        }
    },
    "regional_experience": {
        "weight": 10,
        "description": "Experience in East Africa or similar contexts",
        "scoring_guide": {
            "excellent": "Extensive East Africa experience (25-30 points)",
            "very_good": "Some East Africa experience (20-24 points)",
            "good": "Similar regional experience (15-19 points)",
            "fair": "Limited regional experience (10-14 points)",
            "poor": "No relevant regional experience (0-9 points)"
        }
    }
}

# Keywords for automated detection
EDUCATION_KEYWORDS = [
    "phd", "doctorate", "doctoral", "master", "masters", "msc", "ma", "mba", "bachelor", "degree",
    "development studies", "statistics", "economics", "social sciences", "evaluation", "research",
    "public policy", "international development", "data science", "monitoring and evaluation"
]

EXPERIENCE_KEYWORDS = [
    "mel", "monitoring", "evaluation", "learning", "m&e", "monitoring and evaluation",
    "program evaluation", "impact evaluation", "baseline", "endline", "midterm",
    "data collection", "data analysis", "research", "survey", "assessment",
    "usaid", "world bank", "undp", "unicef", "who", "eu", "dfid", "giz", "donor"
]

TECHNICAL_KEYWORDS = [
    "spss", "stata", "r programming", "python", "sas", "excel", "tableau", "power bi",
    "kobo", "odk", "surveycto", "gis", "arcgis", "qgis", "sql", "database",
    "statistical analysis", "quantitative", "qualitative", "mixed methods",
    "data visualization", "survey design", "sampling"
]

SECTOR_KEYWORDS = [
    "development", "ngo", "international", "humanitarian", "aid", "donor",
    "health", "education", "agriculture", "governance", "gender", "youth",
    "poverty", "sustainability", "capacity building", "community development"
]
