"""
Report generation utilities for CV analysis results
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from typing import List, Dict
import json
from datetime import datetime
from utils.ai_analyzer_clean import CVAnalysisResult

class ReportGenerator:
    """Generate comprehensive reports from CV analysis results"""
    
    def __init__(self):
        self.tier_colors = {
            "Excellent": "#2E8B57",
            "Very Good": "#32CD32", 
            "Good": "#FFD700",
            "Fair": "#FF8C00",
            "Poor": "#DC143C"
        }
    
    def create_summary_dataframe(self, results: List[CVAnalysisResult]) -> pd.DataFrame:
        """Create summary DataFrame from analysis results"""
        data = []
        for result in results:
            # Clean and format the data to avoid Arrow serialization issues
            years_exp = result.key_qualifications.get("years_of_experience", "")
            if isinstance(years_exp, (int, float)):
                years_exp = str(years_exp)
            elif not isinstance(years_exp, str):
                years_exp = str(years_exp) if years_exp is not None else ""

            row = {
                "Rank": 0,  # Will be set after sorting
                "Filename": str(result.filename),
                "Overall Score": float(result.overall_score),
                "Ranking Tier": str(result.ranking_tier),
                "Education Score": float(result.category_scores.get("education", 0)),
                "Experience Score": float(result.category_scores.get("experience", 0)),
                "Technical Skills Score": float(result.category_scores.get("technical_skills", 0)),
                "Sector Knowledge Score": float(result.category_scores.get("sector_knowledge", 0)),
                "Communication Score": float(result.category_scores.get("communication", 0)),
                "Regional Experience Score": float(result.category_scores.get("regional_experience", 0)),
                "Highest Education": str(result.key_qualifications.get("highest_education", "")),
                "Years of Experience": years_exp,
                "MEL Experience": str(result.key_qualifications.get("mel_experience", "")),
                "Technical Expertise": str(result.key_qualifications.get("technical_expertise", "")),
                "Sector Focus": str(result.key_qualifications.get("sector_focus", "")),
                "Experience Summary": str(result.experience_summary),
                "Education Summary": str(result.education_summary),
                "Technical Skills": ", ".join([str(skill) for skill in result.technical_skills]),
                "Key Strengths": " | ".join([str(s) for s in result.strengths[:3]]),  # Top 3 strengths
                "Key Weaknesses": " | ".join([str(w) for w in result.weaknesses[:3]]),  # Top 3 weaknesses
                "Recommendations": " | ".join([str(r) for r in result.recommendations[:2]]),  # Top 2 recommendations
                "Fit Assessment": str(result.fit_assessment)
            }
            data.append(row)

        df = pd.DataFrame(data)
        df = df.sort_values("Overall Score", ascending=False).reset_index(drop=True)
        df["Rank"] = range(1, len(df) + 1)  # Add ranking from 1 to N

        # Reorder columns to put Rank first
        cols = ["Rank"] + [col for col in df.columns if col != "Rank"]
        df = df[cols]

        return df
    
    def create_score_distribution_chart(self, results: List[CVAnalysisResult]) -> go.Figure:
        """Create score distribution histogram"""
        scores = [result.overall_score for result in results]
        
        fig = px.histogram(
            x=scores,
            nbins=20,
            title="Overall Score Distribution",
            labels={"x": "Overall Score", "y": "Number of Candidates"},
            color_discrete_sequence=["#1f77b4"]
        )
        
        fig.add_vline(x=sum(scores)/len(scores), line_dash="dash", 
                     annotation_text=f"Average: {sum(scores)/len(scores):.1f}")
        
        fig.update_layout(
            xaxis_title="Overall Score",
            yaxis_title="Number of Candidates",
            showlegend=False
        )
        
        return fig
    
    def create_tier_distribution_chart(self, results: List[CVAnalysisResult]) -> go.Figure:
        """Create ranking tier distribution pie chart"""
        tier_counts = {}
        for result in results:
            tier = result.ranking_tier
            tier_counts[tier] = tier_counts.get(tier, 0) + 1
        
        fig = px.pie(
            values=list(tier_counts.values()),
            names=list(tier_counts.keys()),
            title="Candidate Distribution by Ranking Tier",
            color=list(tier_counts.keys()),
            color_discrete_map=self.tier_colors
        )
        
        return fig
    
    def create_category_scores_chart(self, results: List[CVAnalysisResult], top_n: int = 20) -> go.Figure:
        """Create category scores comparison for top candidates"""
        # Sort by overall score and take top N
        sorted_results = sorted(results, key=lambda x: x.overall_score, reverse=True)[:top_n]
        
        categories = ["education", "experience", "technical_skills", 
                     "sector_knowledge", "communication", "regional_experience"]
        
        fig = go.Figure()
        
        for i, result in enumerate(sorted_results):
            scores = [result.category_scores.get(cat, 0) for cat in categories]
            fig.add_trace(go.Scatterpolar(
                r=scores,
                theta=categories,
                fill='toself',
                name=result.filename[:20] + "..." if len(result.filename) > 20 else result.filename,
                opacity=0.7
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 30]
                )),
            showlegend=True,
            title=f"Category Scores Comparison - Top {top_n} Candidates"
        )
        
        return fig
    
    def create_top_candidates_table(self, results: List[CVAnalysisResult], top_n: int = 10) -> pd.DataFrame:
        """Create table of top candidates with key information"""
        sorted_results = sorted(results, key=lambda x: x.overall_score, reverse=True)[:top_n]
        
        data = []
        for i, result in enumerate(sorted_results, 1):
            row = {
                "Rank": i,
                "Candidate": result.filename,
                "Overall Score": f"{result.overall_score:.1f}",
                "Tier": result.ranking_tier,
                "Education": result.key_qualifications.get("highest_education", "")[:50] + "...",
                "Experience": result.key_qualifications.get("years_of_experience", ""),
                "MEL Experience": result.key_qualifications.get("mel_experience", "")[:50] + "...",
                "Key Strengths": " | ".join(result.strengths[:2])  # Top 2 strengths
            }
            data.append(row)
        
        return pd.DataFrame(data)
    
    def generate_detailed_report(self, result: CVAnalysisResult) -> Dict:
        """Generate detailed report for a single candidate"""
        report = {
            "candidate_info": {
                "filename": result.filename,
                "overall_score": result.overall_score,
                "ranking_tier": result.ranking_tier,
                "fit_assessment": result.fit_assessment
            },
            "scores": {
                "overall": result.overall_score,
                "categories": result.category_scores
            },
            "qualifications": result.key_qualifications,
            "summaries": {
                "experience": result.experience_summary,
                "education": result.education_summary
            },
            "technical_skills": result.technical_skills,
            "assessment": {
                "strengths": result.strengths,
                "weaknesses": result.weaknesses,
                "recommendations": result.recommendations
            }
        }
        return report
    
    def export_to_excel(self, results: List[CVAnalysisResult], filename: str = None) -> str:
        """Export analysis results to Excel file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cv_analysis_results_{timestamp}.xlsx"
        
        # Create summary DataFrame
        df_summary = self.create_summary_dataframe(results)
        
        # Create detailed results
        detailed_data = []
        for result in results:
            detailed_data.append(self.generate_detailed_report(result))
        
        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            # Summary sheet
            df_summary.to_excel(writer, sheet_name='Summary', index=True)
            
            # Top candidates sheet
            top_candidates = self.create_top_candidates_table(results, 20)
            top_candidates.to_excel(writer, sheet_name='Top_Candidates', index=False)
            
            # Statistics sheet
            stats_data = self.calculate_statistics(results)
            pd.DataFrame([stats_data]).to_excel(writer, sheet_name='Statistics', index=False)
            
            # Individual detailed reports (top 50)
            sorted_results = sorted(results, key=lambda x: x.overall_score, reverse=True)[:50]
            for i, result in enumerate(sorted_results):
                sheet_name = f"Candidate_{i+1}"[:31]  # Excel sheet name limit
                detailed_df = self.create_detailed_candidate_df(result)
                detailed_df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        return filename
    
    def create_detailed_candidate_df(self, result: CVAnalysisResult) -> pd.DataFrame:
        """Create detailed DataFrame for a single candidate"""
        data = [
            ["Filename", result.filename],
            ["Overall Score", f"{result.overall_score:.1f}"],
            ["Ranking Tier", result.ranking_tier],
            ["", ""],
            ["CATEGORY SCORES", ""],
            ["Education", f"{result.category_scores.get('education', 0):.1f}"],
            ["Experience", f"{result.category_scores.get('experience', 0):.1f}"],
            ["Technical Skills", f"{result.category_scores.get('technical_skills', 0):.1f}"],
            ["Sector Knowledge", f"{result.category_scores.get('sector_knowledge', 0):.1f}"],
            ["Communication", f"{result.category_scores.get('communication', 0):.1f}"],
            ["Regional Experience", f"{result.category_scores.get('regional_experience', 0):.1f}"],
            ["", ""],
            ["KEY QUALIFICATIONS", ""],
            ["Highest Education", result.key_qualifications.get("highest_education", "")],
            ["Years of Experience", result.key_qualifications.get("years_of_experience", "")],
            ["MEL Experience", result.key_qualifications.get("mel_experience", "")],
            ["Technical Expertise", result.key_qualifications.get("technical_expertise", "")],
            ["Sector Focus", result.key_qualifications.get("sector_focus", "")],
            ["", ""],
            ["SUMMARIES", ""],
            ["Experience Summary", result.experience_summary],
            ["Education Summary", result.education_summary],
            ["", ""],
            ["TECHNICAL SKILLS", ""],
        ]
        
        # Add technical skills
        for skill in result.technical_skills:
            data.append(["", skill])
        
        data.extend([
            ["", ""],
            ["STRENGTHS", ""],
        ])
        
        # Add strengths
        for strength in result.strengths:
            data.append(["", strength])
        
        data.extend([
            ["", ""],
            ["WEAKNESSES", ""],
        ])
        
        # Add weaknesses
        for weakness in result.weaknesses:
            data.append(["", weakness])
        
        data.extend([
            ["", ""],
            ["RECOMMENDATIONS", ""],
        ])
        
        # Add recommendations
        for rec in result.recommendations:
            data.append(["", rec])
        
        data.extend([
            ["", ""],
            ["FIT ASSESSMENT", ""],
            ["", result.fit_assessment]
        ])
        
        return pd.DataFrame(data, columns=["Field", "Value"])
    
    def calculate_statistics(self, results: List[CVAnalysisResult]) -> Dict:
        """Calculate summary statistics"""
        scores = [result.overall_score for result in results]
        
        tier_counts = {}
        for result in results:
            tier = result.ranking_tier
            tier_counts[tier] = tier_counts.get(tier, 0) + 1
        
        stats = {
            "total_candidates": len(results),
            "average_score": sum(scores) / len(scores) if scores else 0,
            "median_score": sorted(scores)[len(scores)//2] if scores else 0,
            "max_score": max(scores) if scores else 0,
            "min_score": min(scores) if scores else 0,
            "excellent_tier": tier_counts.get("Excellent", 0),
            "very_good_tier": tier_counts.get("Very Good", 0),
            "good_tier": tier_counts.get("Good", 0),
            "fair_tier": tier_counts.get("Fair", 0),
            "poor_tier": tier_counts.get("Poor", 0),
            "top_10_percent_threshold": sorted(scores, reverse=True)[len(scores)//10] if len(scores) >= 10 else max(scores) if scores else 0,
            "top_25_percent_threshold": sorted(scores, reverse=True)[len(scores)//4] if len(scores) >= 4 else max(scores) if scores else 0
        }
        
        return stats
