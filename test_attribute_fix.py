#!/usr/bin/env python3
"""
Test script to verify the attribute error fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.ai_analyzer_clean import CVAnalysisResult
from utils.results_table import ResultsTable

def test_cv_analysis_result():
    """Test CVAnalysisResult with all required attributes"""
    print("🧪 Testing CVAnalysisResult...")
    
    # Create a test result
    result = CVAnalysisResult(
        filename='test_candidate.pdf',
        overall_score=87.5,
        category_scores={
            'education': 26,
            'experience': 28,
            'technical_skills': 24,
            'sector_knowledge': 22,
            'communication': 25,
            'regional_experience': 20
        },
        strengths=['Strong MEL background', 'Excellent analytical skills', 'Good communication'],
        weaknesses=['Limited regional experience', 'Could improve technical skills'],
        recommendations=['Consider for interview', 'Assess regional knowledge'],
        key_qualifications={
            'highest_education': 'Masters in Development Studies',
            'years_of_experience': '7 years',
            'mel_experience': '5 years in MEL roles',
            'technical_expertise': 'SPSS, R, Excel',
            'sector_focus': 'Health and education'
        },
        experience_summary='7 years of development experience with 5 years in MEL roles',
        education_summary='Masters in Development Studies from University of Nairobi',
        technical_skills=['SPSS', 'R', 'Excel', 'PowerBI', 'Survey design'],
        fit_assessment='Strong candidate with relevant MEL experience and good analytical skills',
        ranking_tier='Very Good',
        ai_provider='Euriai'
    )
    
    # Test all the compatibility properties
    print(f"✅ Filename: {result.filename}")
    print(f"✅ Overall Score: {result.overall_score}")
    print(f"✅ Tier: {result.tier}")
    print(f"✅ Ranking Tier: {result.ranking_tier}")
    print(f"✅ Years Experience: {result.years_experience}")
    print(f"✅ Role Fit Summary: {result.role_fit_summary}")
    print(f"✅ Provider Used: {result.provider_used}")
    print(f"✅ Analysis Time: {result.analysis_time}")
    
    return result

def test_results_table():
    """Test ResultsTable with CVAnalysisResult"""
    print("\n🧪 Testing ResultsTable...")
    
    # Create test results
    results = []
    
    # Result 1
    result1 = CVAnalysisResult(
        filename='candidate_1.pdf',
        overall_score=92.0,
        category_scores={'education': 28, 'experience': 30, 'technical_skills': 26},
        strengths=['Excellent background'],
        weaknesses=['Minor gaps'],
        recommendations=['Highly recommended'],
        key_qualifications={'years_of_experience': '8 years'},
        experience_summary='8 years senior experience',
        education_summary='PhD in Statistics',
        technical_skills=['R', 'Python', 'Stata'],
        fit_assessment='Excellent fit for senior MEL role',
        ranking_tier='Excellent',
        ai_provider='Euriai'
    )
    
    # Result 2
    result2 = CVAnalysisResult(
        filename='candidate_2.pdf',
        overall_score=78.5,
        category_scores={'education': 24, 'experience': 26, 'technical_skills': 22},
        strengths=['Good analytical skills'],
        weaknesses=['Limited experience'],
        recommendations=['Consider for junior role'],
        key_qualifications={'years_of_experience': '3 years'},
        experience_summary='3 years junior experience',
        education_summary='Masters in Economics',
        technical_skills=['Excel', 'SPSS'],
        fit_assessment='Good fit for junior MEL role',
        ranking_tier='Good',
        ai_provider='Groq'
    )
    
    results = [result1, result2]
    
    # Test results table creation
    table = ResultsTable()
    df = table.create_results_dataframe(results)
    
    print(f"✅ DataFrame created with {len(df)} rows")
    print(f"✅ Columns: {list(df.columns)}")
    
    # Check key columns
    print(f"✅ Candidate Names: {df['Candidate Name'].tolist()}")
    print(f"✅ Tiers: {df['Tier'].tolist()}")
    print(f"✅ Years Experience: {df['Years Experience'].tolist()}")
    print(f"✅ Providers: {df['Provider'].tolist()}")
    
    return df

def main():
    """Run all tests"""
    print("🚀 Testing Attribute Error Fix\n")
    
    try:
        # Test CVAnalysisResult
        result = test_cv_analysis_result()
        
        # Test ResultsTable
        df = test_results_table()
        
        print("\n🎉 All tests passed! The attribute error has been fixed.")
        print("\n📊 Sample DataFrame:")
        print(df[['Rank', 'Candidate Name', 'Overall Score', 'Tier', 'Years Experience', 'Provider']].to_string(index=False))
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
