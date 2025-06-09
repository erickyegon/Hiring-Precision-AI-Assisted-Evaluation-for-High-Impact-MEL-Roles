"""
Professional AI-powered CV Analysis System
Supports Euriai (primary) and Groq (fallback) providers
"""

import os
import json
import logging
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
import asyncio
from utils.euri_client import EuriClient
from groq import Groq
from config.job_description import (
    MEL_MANAGER_JOB_DESCRIPTION, 
    SCORING_CRITERIA
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CVAnalysisResult:
    """Data class for CV analysis results"""
    filename: str
    overall_score: float
    category_scores: Dict[str, float]
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
    key_qualifications: Dict[str, str]
    experience_summary: str
    education_summary: str
    technical_skills: List[str]
    fit_assessment: str
    ranking_tier: str
    ai_provider: str

class ProfessionalCVAnalyzer:
    """Professional CV analyzer with dual AI provider support"""
    
    def __init__(self, euriai_api_key: str = "", groq_api_key: str = ""):
        self.euriai_api_key = euriai_api_key
        self.groq_api_key = groq_api_key
        
        # Initialize AI clients
        self.euriai_client = None
        self.groq_client = None
        
        # Initialize Euriai (primary provider)
        if euriai_api_key:
            try:
                self.euriai_client = EuriClient(euriai_api_key)
                logger.info("✅ Euriai client initialized (Primary Provider)")
            except Exception as e:
                logger.warning(f"Failed to initialize Euriai: {str(e)}")
        
        # Initialize Groq (fallback provider)
        if groq_api_key:
            try:
                self.groq_client = Groq(api_key=groq_api_key)
                logger.info("✅ Groq client initialized (Fallback Provider)")
            except Exception as e:
                logger.warning(f"Failed to initialize Groq: {str(e)}")
        
        # Validate at least one provider is available
        if not self.euriai_client and not self.groq_client:
            raise ValueError("❌ No AI providers available. Please provide valid API keys.")
    
    def count_tokens(self, text: str) -> int:
        """Estimate token count for text"""
        return int(len(text.split()) * 1.33)
    
    def _extract_json_from_response(self, text: str) -> str:
        """Extract JSON from AI response"""
        text = text.strip()
        start_idx = text.find('{')
        if start_idx == -1:
            return text
        
        brace_count = 0
        end_idx = start_idx
        
        for i, char in enumerate(text[start_idx:], start_idx):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_idx = i
                    break
        
        return text[start_idx:end_idx + 1] if brace_count == 0 else text
    
    def create_analysis_prompt(self, cv_text: str) -> str:
        """Create comprehensive analysis prompt"""
        return f"""
You are an expert HR consultant specializing in Monitoring, Evaluation, and Learning (MEL) positions. 
Analyze the following CV against the MEL Manager job requirements and provide a comprehensive evaluation.

JOB DESCRIPTION:
{MEL_MANAGER_JOB_DESCRIPTION}

SCORING CRITERIA:
{json.dumps(SCORING_CRITERIA, indent=2)}

CV TO ANALYZE:
{cv_text}

Provide a detailed analysis in the following JSON format:

{{
    "overall_score": <float between 0-100>,
    "category_scores": {{
        "education": <float between 0-30>,
        "experience": <float between 0-30>, 
        "technical_skills": <float between 0-30>,
        "sector_knowledge": <float between 0-30>,
        "communication": <float between 0-30>,
        "regional_experience": <float between 0-30>
    }},
    "strengths": [<list of key strengths>],
    "weaknesses": [<list of areas for improvement>],
    "recommendations": [<list of specific recommendations>],
    "key_qualifications": {{
        "highest_education": "<description>",
        "years_of_experience": "<number>",
        "mel_experience": "<description>",
        "technical_expertise": "<description>",
        "sector_focus": "<description>"
    }},
    "experience_summary": "<2-3 sentence summary>",
    "education_summary": "<1-2 sentence summary>",
    "technical_skills": [<list of technical skills>],
    "fit_assessment": "<overall assessment>",
    "ranking_tier": "<Excellent/Very Good/Good/Fair/Poor>"
}}

IMPORTANT: Respond with ONLY the JSON object, no other text.
"""
    
    async def analyze_with_euriai(self, cv_text: str, filename: str) -> Optional[CVAnalysisResult]:
        """Analyze CV using Euriai API"""
        if not self.euriai_client:
            return None
        
        try:
            prompt = self.create_analysis_prompt(cv_text)
            
            if self.count_tokens(prompt) > 7000:
                logger.warning(f"Prompt too long for {filename}, truncating")
                cv_text = cv_text[:3000] + "...[truncated]"
                prompt = self.create_analysis_prompt(cv_text)
            
            messages = [
                {"role": "system", "content": "You are an expert HR consultant. Respond with ONLY valid JSON."},
                {"role": "user", "content": prompt}
            ]
            
            content = self.euriai_client.chat_completion(
                messages=messages,
                temperature=0.1,
                max_tokens=2000
            )
            
            content = self._extract_json_from_response(content.strip())
            
            try:
                result_data = json.loads(content)
                return self._create_analysis_result(filename, result_data, "Euriai")
            except json.JSONDecodeError as e:
                logger.error(f"Euriai JSON error for {filename}: {str(e)}")
                return None
                
        except Exception as e:
            logger.error(f"Euriai analysis error for {filename}: {str(e)}")
            return None
    
    async def analyze_with_groq(self, cv_text: str, filename: str) -> Optional[CVAnalysisResult]:
        """Analyze CV using Groq API"""
        if not self.groq_client:
            return None
        
        try:
            prompt = self.create_analysis_prompt(cv_text)
            
            if self.count_tokens(prompt) > 7000:
                cv_text = cv_text[:3000] + "...[truncated]"
                prompt = self.create_analysis_prompt(cv_text)
            
            response = self.groq_client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": "You are an expert HR consultant. Respond with ONLY valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content.strip()
            content = self._extract_json_from_response(content)
            
            try:
                result_data = json.loads(content)
                return self._create_analysis_result(filename, result_data, "Groq")
            except json.JSONDecodeError as e:
                logger.error(f"Groq JSON error for {filename}: {str(e)}")
                return None
                
        except Exception as e:
            logger.error(f"Groq analysis error for {filename}: {str(e)}")
            return None
    
    def _create_analysis_result(self, filename: str, data: Dict, provider: str) -> CVAnalysisResult:
        """Create analysis result with provider tracking"""
        category_scores = data.get("category_scores", {})
        
        overall_score = data.get("overall_score", 0.0)
        if overall_score == 0.0 and category_scores:
            overall_score = self.calculate_weighted_score(category_scores)
        
        ranking_tier = data.get("ranking_tier", "Fair")
        if not ranking_tier:
            if overall_score >= 90:
                ranking_tier = "Excellent"
            elif overall_score >= 80:
                ranking_tier = "Very Good"
            elif overall_score >= 70:
                ranking_tier = "Good"
            elif overall_score >= 60:
                ranking_tier = "Fair"
            else:
                ranking_tier = "Poor"
        
        return CVAnalysisResult(
            filename=filename,
            overall_score=overall_score,
            category_scores=category_scores,
            strengths=data.get("strengths", ["Analysis completed"]),
            weaknesses=data.get("weaknesses", ["Requires further review"]),
            recommendations=data.get("recommendations", ["Consider for evaluation"]),
            key_qualifications=data.get("key_qualifications", {"status": "Analyzed"}),
            experience_summary=data.get("experience_summary", "Experience extracted"),
            education_summary=data.get("education_summary", "Education extracted"),
            technical_skills=data.get("technical_skills", ["Skills identified"]),
            fit_assessment=data.get("fit_assessment", "Assessment completed"),
            ranking_tier=ranking_tier,
            ai_provider=provider
        )
    
    async def analyze_cv(self, cv_text: str, filename: str) -> Optional[CVAnalysisResult]:
        """Analyze CV using best available provider"""
        logger.info(f"Analyzing CV: {filename}")
        
        # Try Euriai first (primary provider)
        if self.euriai_client:
            result = await self.analyze_with_euriai(cv_text, filename)
            if result:
                logger.info(f"✅ {filename} analyzed with Euriai - Score: {result.overall_score:.1f}")
                return result
            else:
                logger.warning(f"⚠️ Euriai failed for {filename}, trying Groq")
        
        # Fallback to Groq
        if self.groq_client:
            result = await self.analyze_with_groq(cv_text, filename)
            if result:
                logger.info(f"✅ {filename} analyzed with Groq - Score: {result.overall_score:.1f}")
                return result
            else:
                logger.error(f"❌ Groq also failed for {filename}")
        
        logger.error(f"❌ All providers failed for {filename}")
        return None
    
    async def analyze_batch(self, cv_data: List[Dict], max_concurrent: int = 1) -> List[CVAnalysisResult]:
        """Analyze batch of CVs with rate limiting"""
        all_results = []
        total = len(cv_data)
        
        logger.info(f"Starting professional CV analysis of {total} CVs")
        
        for i, cv_item in enumerate(cv_data, 1):
            if cv_item.get("error") or not cv_item.get("text"):
                logger.warning(f"Skipping {cv_item['filename']} due to processing error")
                continue
            
            result = await self.analyze_cv(cv_item["text"], cv_item["filename"])
            
            if result:
                all_results.append(result)
            
            # Progress logging
            if i % 10 == 0:
                success_rate = len(all_results) / i * 100
                logger.info(f"📊 Progress: {i}/{total} processed, {len(all_results)} successful ({success_rate:.1f}%)")
            
            # Rate limiting
            if i < total:
                await asyncio.sleep(2)
        
        logger.info(f"🎉 Analysis complete: {len(all_results)}/{total} CVs analyzed")
        return all_results
    
    def calculate_weighted_score(self, category_scores: Dict[str, float]) -> float:
        """Calculate weighted overall score"""
        total_score = 0.0
        total_weight = 0.0
        
        for category, score in category_scores.items():
            if category in SCORING_CRITERIA:
                weight = SCORING_CRITERIA[category]["weight"]
                total_score += (score * weight / 30)
                total_weight += weight
        
        return (total_score / total_weight * 100) if total_weight > 0 else 0.0
