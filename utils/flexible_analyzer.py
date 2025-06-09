"""
Flexible CV Analyzer that works with custom job descriptions
"""

import json
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from utils.euri_client import EuriClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class FlexibleAnalysisResult:
    """Results from flexible CV analysis"""
    filename: str
    overall_score: float
    tier: str
    category_scores: Dict[str, float]
    strengths: List[str]
    weaknesses: List[str]
    years_experience: int
    role_fit_summary: str
    provider_used: str
    analysis_time: float

class FlexibleCVAnalyzer:
    """Flexible CV analyzer that adapts to any job description"""
    
    def __init__(self, euriai_api_key: str = None, groq_api_key: str = None):
        """Initialize the flexible analyzer"""
        self.euriai_client = None
        self.groq_client = None
        
        # Initialize Euriai client (primary)
        if euriai_api_key:
            try:
                self.euriai_client = EuriClient(euriai_api_key)
                if self.euriai_client.test_connection():
                    logger.info("✅ Euriai client initialized (Primary Provider)")
                else:
                    logger.warning("⚠️ Euriai connection test failed")
                    self.euriai_client = None
            except Exception as e:
                logger.error(f"❌ Failed to initialize Euriai client: {str(e)}")
                self.euriai_client = None
        
        # Initialize Groq client (fallback)
        if groq_api_key:
            try:
                import groq
                self.groq_client = groq.Groq(api_key=groq_api_key)
                logger.info("✅ Groq client initialized (Fallback Provider)")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Groq client: {str(e)}")
                self.groq_client = None
    
    def analyze_cv_with_jd(self, cv_text: str, job_description: str, filename: str) -> FlexibleAnalysisResult:
        """Analyze CV against a custom job description"""
        import time
        start_time = time.time()
        
        # Extract evaluation criteria from job description
        criteria = self._extract_criteria_from_jd(job_description)
        
        # Create analysis prompt
        prompt = self._create_flexible_analysis_prompt(cv_text, job_description, criteria)
        
        # Try Euriai first, then Groq
        analysis_result = None
        provider_used = "None"
        
        if self.euriai_client:
            try:
                response = self.euriai_client.chat_completion(
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1,
                    max_tokens=2000
                )
                analysis_result = self._parse_analysis_response(response)
                provider_used = "Euriai"
                logger.info(f"✅ {filename} analyzed with Euriai")
            except Exception as e:
                logger.warning(f"⚠️ Euriai analysis failed for {filename}: {str(e)}")
        
        if not analysis_result and self.groq_client:
            try:
                response = self.groq_client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1,
                    max_tokens=2000
                )
                analysis_result = self._parse_analysis_response(response.choices[0].message.content)
                provider_used = "Groq"
                logger.info(f"✅ {filename} analyzed with Groq")
            except Exception as e:
                logger.error(f"❌ Groq analysis failed for {filename}: {str(e)}")
        
        if not analysis_result:
            # Fallback result
            analysis_result = self._create_fallback_result()
            provider_used = "Fallback"
        
        analysis_time = time.time() - start_time
        
        return FlexibleAnalysisResult(
            filename=filename,
            overall_score=analysis_result.get('overall_score', 0),
            tier=analysis_result.get('tier', 'Unknown'),
            category_scores=analysis_result.get('category_scores', {}),
            strengths=analysis_result.get('strengths', []),
            weaknesses=analysis_result.get('weaknesses', []),
            years_experience=analysis_result.get('years_experience', 0),
            role_fit_summary=analysis_result.get('role_fit_summary', 'Analysis unavailable'),
            provider_used=provider_used,
            analysis_time=analysis_time
        )
    
    def _extract_criteria_from_jd(self, job_description: str) -> Dict[str, str]:
        """Extract key evaluation criteria from job description"""
        # Default criteria that work for most roles
        default_criteria = {
            "education": "Educational qualifications and certifications",
            "experience": "Relevant work experience and achievements",
            "technical_skills": "Technical skills and tools proficiency",
            "domain_knowledge": "Industry/domain specific knowledge",
            "communication": "Communication and interpersonal skills",
            "leadership": "Leadership and management experience"
        }
        
        # TODO: In future, use AI to extract specific criteria from JD
        # For now, return default criteria
        return default_criteria
    
    def _create_flexible_analysis_prompt(self, cv_text: str, job_description: str, criteria: Dict[str, str]) -> str:
        """Create analysis prompt based on job description and criteria"""
        
        criteria_text = "\n".join([f"- {key.title()}: {desc}" for key, desc in criteria.items()])
        
        prompt = f"""
You are an expert HR analyst. Analyze the following CV against the provided job description and evaluate the candidate across the specified criteria.

JOB DESCRIPTION:
{job_description}

EVALUATION CRITERIA:
{criteria_text}

CV TO ANALYZE:
{cv_text}

Please provide a comprehensive analysis in the following JSON format:

{{
    "overall_score": <score from 0-100>,
    "tier": "<Excellent (90-100) | Very Good (80-89) | Good (70-79) | Fair (60-69) | Poor (<60)>",
    "category_scores": {{
        "education": <score from 0-30>,
        "experience": <score from 0-30>,
        "technical_skills": <score from 0-30>,
        "domain_knowledge": <score from 0-30>,
        "communication": <score from 0-30>,
        "leadership": <score from 0-30>
    }},
    "strengths": [
        "<strength 1>",
        "<strength 2>",
        "<strength 3>"
    ],
    "weaknesses": [
        "<weakness 1>",
        "<weakness 2>"
    ],
    "years_experience": <total years of relevant experience>,
    "role_fit_summary": "<2-3 sentence summary of how well the candidate fits this specific role>"
}}

Focus on:
1. How well the candidate's background matches the job requirements
2. Relevant experience in the specific domain/industry
3. Technical skills alignment with job needs
4. Leadership and communication abilities
5. Educational background relevance
6. Overall potential for success in this role

Provide specific, actionable insights based on the job description provided.
"""
        return prompt
    
    def _parse_analysis_response(self, response: str) -> Dict:
        """Parse the AI analysis response"""
        try:
            # Extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response[start_idx:end_idx]
                result = json.loads(json_str)
                
                # Validate and clean the result
                return self._validate_analysis_result(result)
            else:
                logger.error("No valid JSON found in response")
                return self._create_fallback_result()
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            return self._create_fallback_result()
        except Exception as e:
            logger.error(f"Error parsing analysis response: {str(e)}")
            return self._create_fallback_result()
    
    def _validate_analysis_result(self, result: Dict) -> Dict:
        """Validate and clean analysis result"""
        # Ensure all required fields exist with defaults
        validated = {
            'overall_score': max(0, min(100, result.get('overall_score', 0))),
            'tier': result.get('tier', 'Unknown'),
            'category_scores': result.get('category_scores', {}),
            'strengths': result.get('strengths', [])[:5],  # Limit to 5
            'weaknesses': result.get('weaknesses', [])[:3],  # Limit to 3
            'years_experience': max(0, result.get('years_experience', 0)),
            'role_fit_summary': result.get('role_fit_summary', 'Analysis completed')
        }
        
        # Ensure category scores are valid
        for category in validated['category_scores']:
            validated['category_scores'][category] = max(0, min(30, validated['category_scores'][category]))
        
        return validated
    
    def _create_fallback_result(self) -> Dict:
        """Create fallback result when analysis fails"""
        return {
            'overall_score': 0,
            'tier': 'Analysis Failed',
            'category_scores': {
                'education': 0,
                'experience': 0,
                'technical_skills': 0,
                'domain_knowledge': 0,
                'communication': 0,
                'leadership': 0
            },
            'strengths': ['Analysis could not be completed'],
            'weaknesses': ['Unable to evaluate'],
            'years_experience': 0,
            'role_fit_summary': 'Analysis failed due to technical issues'
        }
    
    def batch_analyze(self, cv_data: List[Dict], job_description: str) -> List[FlexibleAnalysisResult]:
        """Analyze multiple CVs against a job description"""
        results = []
        
        logger.info(f"Starting flexible analysis of {len(cv_data)} CVs")
        
        for i, cv in enumerate(cv_data, 1):
            if cv.get('error'):
                # Skip CVs with processing errors
                logger.warning(f"Skipping {cv['filename']} due to processing error")
                continue
            
            logger.info(f"Analyzing CV {i}/{len(cv_data)}: {cv['filename']}")
            
            result = self.analyze_cv_with_jd(
                cv_text=cv['text'],
                job_description=job_description,
                filename=cv['filename']
            )
            
            results.append(result)
        
        logger.info(f"🎉 Flexible analysis complete: {len(results)} CVs analyzed")
        return results
