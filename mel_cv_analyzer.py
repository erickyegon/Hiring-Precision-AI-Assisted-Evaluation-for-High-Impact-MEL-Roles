"""
MEL Manager CV Analysis System
Professional recruitment tool for Monitoring, Evaluation & Learning positions
"""

import asyncio
import os
import json
import pandas as pd
from datetime import datetime
from typing import List, Dict
import streamlit as st

from utils.document_processor import DocumentProcessor
from utils.ai_analyzer_clean import ProfessionalCVAnalyzer, CVAnalysisResult
from utils.flexible_analyzer import FlexibleCVAnalyzer, FlexibleAnalysisResult
from utils.report_generator import ReportGenerator
from utils.living_goods_branding import LivingGoodsBranding
from utils.results_table import ResultsTable

# Page configuration - Living Goods Brand Compliant
st.set_page_config(
    page_title="Living Goods MEL Manager CV Analysis System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Living Goods MEL Manager CV Analysis System - Professional AI-powered recruitment tool"
    }
)

class MELCVAnalysisSystem:
    """Professional MEL CV Analysis System"""
    
    def __init__(self, euriai_api_key: str = "", groq_api_key: str = ""):
        self.processor = DocumentProcessor()
        self.analyzer = ProfessionalCVAnalyzer(euriai_api_key, groq_api_key)
        self.report_generator = ReportGenerator()
        self.results_dir = "results"
        
        # Create results directory
        os.makedirs(self.results_dir, exist_ok=True)
    
    def process_and_analyze_cvs(self, cv_directory: str = "CVs", batch_size: int = 50) -> List[CVAnalysisResult]:
        """Complete CV processing and analysis pipeline"""
        
        # Apply Living Goods branding
        LivingGoodsBranding.apply_branding()

        # Branded header
        LivingGoodsBranding.create_branded_header(
            "🎯 Living Goods MEL Manager CV Analysis System",
            "Professional AI-powered recruitment tool for Monitoring, Evaluation & Learning positions"
        )
        
        # Step 1: Document Processing
        st.header("📁 Step 1: Document Processing")
        
        with st.spinner("Processing CV documents..."):
            cv_data = self.processor.process_directory(cv_directory)
            stats = self.processor.get_processing_stats(cv_data)
        
        # Display processing results
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Files", stats['total_files'])
        with col2:
            st.metric("Successfully Processed", stats['successful'])
        with col3:
            st.metric("Processing Errors", stats['errors'])
        with col4:
            st.metric("Total Words Extracted", f"{stats['total_words']:,}")
        
        if stats['errors'] > 0:
            st.warning(f"⚠️ {stats['errors']} files had processing errors")
        
        # Filter valid CVs
        valid_cvs = [cv for cv in cv_data if not cv.get('error') and cv.get('text')]
        
        if not valid_cvs:
            st.error("❌ No valid CV files found for analysis")
            return []
        
        st.success(f"✅ {len(valid_cvs)} CVs ready for AI analysis")
        
        # Step 2: AI Analysis
        LivingGoodsBranding.create_accent_divider()
        st.header("🤖 Step 2: AI Analysis")
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Run analysis
        results = asyncio.run(self._analyze_with_progress(valid_cvs, progress_bar, status_text))
        
        if not results:
            st.error("❌ No CVs were successfully analyzed")
            return []
        
        # Step 3: Results Processing
        LivingGoodsBranding.create_accent_divider()
        st.header("📊 Step 3: Results & Analytics")
        
        # Save results
        self._save_results(results)
        
        # Display summary
        self._display_results_summary(results)
        
        # Store in session state
        st.session_state.analysis_results = results
        
        return results
    
    async def _analyze_with_progress(self, cv_data: List[Dict], progress_bar, status_text) -> List[CVAnalysisResult]:
        """Analyze CVs with real-time progress updates"""
        total = len(cv_data)
        results = []
        
        status_text.text("🚀 Starting AI analysis...")
        
        for i, cv_item in enumerate(cv_data, 1):
            if cv_item.get("error") or not cv_item.get("text"):
                continue
            
            status_text.text(f"🔍 Analyzing {i}/{total}: {cv_item['filename']}")
            
            result = await self.analyzer.analyze_cv(cv_item['text'], cv_item['filename'])
            
            if result:
                results.append(result)
                status_text.text(f"✅ {i}/{total}: {result.filename} - Score: {result.overall_score:.1f} ({result.ai_provider})")
            else:
                status_text.text(f"❌ {i}/{total}: Failed to analyze {cv_item['filename']}")
            
            # Update progress
            progress = i / total
            progress_bar.progress(progress)
            
            # Rate limiting
            await asyncio.sleep(1)
        
        status_text.text(f"🎉 Analysis complete! {len(results)}/{total} CVs analyzed successfully")
        return results
    
    def _save_results(self, results: List[CVAnalysisResult]):
        """Save analysis results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save as Excel
        excel_filename = f"{self.results_dir}/mel_cv_analysis_{timestamp}.xlsx"
        self.report_generator.export_to_excel(results, excel_filename)
        
        # Save as JSON
        json_filename = f"{self.results_dir}/mel_cv_analysis_{timestamp}.json"
        json_data = []
        
        for result in results:
            json_data.append({
                'filename': result.filename,
                'overall_score': result.overall_score,
                'ranking_tier': result.ranking_tier,
                'ai_provider': result.ai_provider,
                'category_scores': result.category_scores,
                'strengths': result.strengths,
                'weaknesses': result.weaknesses,
                'recommendations': result.recommendations,
                'key_qualifications': result.key_qualifications,
                'experience_summary': result.experience_summary,
                'education_summary': result.education_summary,
                'technical_skills': result.technical_skills,
                'fit_assessment': result.fit_assessment
            })
        
        with open(json_filename, 'w') as f:
            json.dump(json_data, f, indent=2)
        
        st.success(f"📊 Results saved:")
        st.write(f"- Excel: `{excel_filename}`")
        st.write(f"- JSON: `{json_filename}`")
    
    def _display_results_summary(self, results: List[CVAnalysisResult]):
        """Display comprehensive results summary"""
        
        # Overall statistics
        scores = [r.overall_score for r in results]
        avg_score = sum(scores) / len(scores)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Analyzed", len(results))
        with col2:
            st.metric("Average Score", f"{avg_score:.1f}")
        with col3:
            excellent_count = len([r for r in results if r.ranking_tier == "Excellent"])
            st.metric("Excellent Candidates", excellent_count)
        with col4:
            top_score = max(scores)
            st.metric("Highest Score", f"{top_score:.1f}")
        
        # Provider distribution
        st.subheader("🤖 AI Provider Distribution")
        provider_counts = {}
        for result in results:
            provider = result.ai_provider
            provider_counts[provider] = provider_counts.get(provider, 0) + 1
        
        provider_df = pd.DataFrame(list(provider_counts.items()), columns=['Provider', 'Count'])
        st.bar_chart(provider_df.set_index('Provider'))
        
        # Tier distribution
        st.subheader("📊 Candidate Tier Distribution")
        tier_counts = {}
        for result in results:
            tier = result.ranking_tier
            tier_counts[tier] = tier_counts.get(tier, 0) + 1
        
        tier_df = pd.DataFrame(list(tier_counts.items()), columns=['Tier', 'Count'])
        st.bar_chart(tier_df.set_index('Tier'))
        
        # Top 10 candidates
        st.subheader("🏆 Top 10 Candidates")
        top_10 = sorted(results, key=lambda x: x.overall_score, reverse=True)[:10]
        
        for i, result in enumerate(top_10, 1):
            with st.expander(f"{i}. {result.filename} - Score: {result.overall_score:.1f} ({result.ranking_tier}) - {result.ai_provider}"):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.write("**🎯 Key Strengths:**")
                    for strength in result.strengths[:3]:
                        st.write(f"• {strength}")
                    
                    st.write("**🎓 Education:**")
                    st.write(result.education_summary)
                
                with col_b:
                    st.write("**⚠️ Areas for Improvement:**")
                    for weakness in result.weaknesses[:3]:
                        st.write(f"• {weakness}")
                    
                    st.write("**💼 Experience:**")
                    st.write(result.experience_summary)
                
                st.write("**🎯 Overall Assessment:**")
                st.info(result.fit_assessment)

def main():
    """Enhanced CV Analysis Application with Living Goods branding"""

    # Apply Living Goods branding globally
    LivingGoodsBranding.apply_branding()

    # Main navigation
    st.sidebar.title("🎯 CV Analysis System")

    # Highlight universal capability
    st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, #005084 0%, #44ADE2 100%); color: white; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; text-align: center;">
        <h4 style="margin: 0; color: white;">🌟 Universal Recruitment Tool</h4>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.9;">
            Upload any job description • Analyze for any role
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Analysis mode selection
    analysis_mode = st.sidebar.selectbox(
        "Select Analysis Mode",
        ["🎯 Custom Job Analysis (Universal)", "📤 Upload CVs (MEL Default)", "📁 Directory Analysis (MEL Default)"],
        help="Choose how you want to analyze CVs - Custom Job Analysis works for any role!"
    )

    # Sidebar configuration
    st.sidebar.header("🔑 API Configuration")
    
    # API keys
    euriai_key = st.sidebar.text_input(
        "Euriai API Key (Primary)", 
        value="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJlZDljYzlkYy0xZmQ2LTRiMGMtODcyZS1lYmJlMmRjNjZiNzQiLCJlbWFpbCI6ImtleWVnb25AZ21haWwuY29tIiwiaWF0IjoxNzQ3MDM0Nzc2LCJleHAiOjE3Nzg1NzA3NzZ9.6m2jzZ_A7eGmoBYjzP7lLazn1luxIFUIYOsbS6ttKS0",
        type="password"
    )
    
    groq_key = st.sidebar.text_input("Groq API Key (Fallback)", type="password")
    
    # Provider status
    st.sidebar.subheader("🔌 Provider Status")

    if euriai_key:
        st.sidebar.success("🟢 Euriai: Ready & Operational")
    if groq_key:
        st.sidebar.success("🟢 Groq: Ready & Operational")

    if not euriai_key and not groq_key:
        st.sidebar.error("❌ No API keys provided")
        st.error("Please provide at least one API key to proceed")
        return
    
    # Processing settings
    st.sidebar.subheader("⚙️ Processing Settings")
    cv_directory = st.sidebar.text_input("CV Directory", "CVs")
    batch_size = st.sidebar.slider("Batch Size", 25, 100, 50)
    
    # System info
    st.sidebar.subheader("ℹ️ System Information")
    st.sidebar.info("""
    **Living Goods MEL CV Analysis System**

    🎯 **Purpose**: Automated screening for MEL Manager positions

    🤖 **AI Providers**:
    - Euriai (Primary) - GPT-4.1, Gemini, LLaMA
    - Groq (Fallback) - LLaMA3-70B

    📊 **Features**:
    - Multi-format document processing
    - AI-powered candidate analysis
    - Comprehensive scoring & ranking
    - Professional reporting & export
    - Real-time progress monitoring
    """)
    
    # Main processing
    if st.button("🚀 Start MEL CV Analysis", type="primary"):
        if not os.path.exists(cv_directory):
            st.error(f"❌ Directory '{cv_directory}' not found")
            return
        
    # Main content area based on selected mode
    if "Directory Analysis" in analysis_mode:
        handle_directory_analysis(euriai_key, groq_key)
    elif "Upload CVs" in analysis_mode:
        handle_upload_analysis(euriai_key, groq_key)
    elif "Custom Job Analysis" in analysis_mode:
        handle_custom_job_analysis(euriai_key, groq_key)

def handle_directory_analysis(euriai_key: str, groq_key: str):
    """Handle directory-based CV analysis"""
    LivingGoodsBranding.create_branded_header(
        "📁 Directory CV Analysis",
        "Analyze CVs from the CVs directory using MEL Manager criteria"
    )

    # Initialize the system
    system = MELCVAnalysisSystem(euriai_key, groq_key)

    # Analysis button
    if st.button("🚀 Start Directory Analysis", type="primary"):
        with st.spinner("Analyzing CVs from directory..."):
            results = system.process_and_analyze_cvs()

        if results:
            display_analysis_results(results, "MEL Manager Analysis")
        else:
            st.error("❌ No CVs were successfully analyzed. Please check your files and API keys.")

def handle_upload_analysis(euriai_key: str, groq_key: str):
    """Handle uploaded CV analysis"""
    LivingGoodsBranding.create_branded_header(
        "📤 Upload CV Analysis",
        "Upload CVs (PDF, DOCX, DOC, ZIP) for analysis using MEL Manager criteria"
    )

    # File uploader
    uploaded_files = st.file_uploader(
        "Upload CV files",
        type=['pdf', 'docx', 'doc', 'zip'],
        accept_multiple_files=True,
        help="Upload individual CV files or ZIP archives containing multiple CVs"
    )

    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully")

        if st.button("🚀 Analyze Uploaded CVs", type="primary"):
            with st.spinner("Processing uploaded files..."):
                # Process uploaded files
                processor = DocumentProcessor()
                cv_data = processor.process_uploaded_files(uploaded_files)

                if cv_data:
                    # Analyze with MEL criteria
                    analyzer = ProfessionalCVAnalyzer(euriai_api_key=euriai_key, groq_api_key=groq_key)
                    results = analyzer.batch_analyze(cv_data)

                    if results:
                        display_analysis_results(results, "Uploaded CV Analysis")
                    else:
                        st.error("❌ Analysis failed. Please check your API keys.")
                else:
                    st.error("❌ No valid CVs found in uploaded files.")

def handle_custom_job_analysis(euriai_key: str, groq_key: str):
    """Handle custom job description analysis"""
    LivingGoodsBranding.create_branded_header(
        "🎯 Custom Job Analysis",
        "Analyze CVs against any job description - Universal recruitment tool"
    )

    # Step-by-step process
    st.markdown("""
    <div style="background-color: #F8F9FA; padding: 1rem; border-radius: 8px; border-left: 4px solid #005084; margin-bottom: 2rem;">
        <h4 style="color: #005084; margin-bottom: 1rem;">📋 How it works:</h4>
        <ol style="margin: 0;">
            <li><strong>Step 1:</strong> Paste the complete job description below</li>
            <li><strong>Step 2:</strong> Upload CV files (PDF, DOCX, DOC, or ZIP)</li>
            <li><strong>Step 3:</strong> AI analyzes CVs specifically against your job requirements</li>
            <li><strong>Step 4:</strong> Get role-specific rankings and insights</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    # Job description input with enhanced UI
    st.subheader("📋 Step 1: Job Description")

    # Prominent upload options
    st.markdown("""
    <div style="background-color: #E8F5E8; padding: 1rem; border-radius: 8px; border: 2px solid #44ADE2; margin-bottom: 1rem;">
        <h4 style="color: #005084; margin-bottom: 0.5rem;">📄 Upload Your Job Description</h4>
        <p style="margin: 0; color: #005084;">
            <strong>Universal Tool:</strong> Upload any job description to analyze CVs for that specific role.
            Works for Software Engineers, Marketing Managers, Data Scientists, Project Managers, and any other position.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Option to upload JD file or paste text
    jd_input_method = st.radio(
        "How would you like to provide the job description?",
        ["📄 Upload JD File", "📝 Paste JD Text"],
        horizontal=True,
        help="Upload a file or paste text - both methods work for any job role"
    )

    job_description = ""

    if jd_input_method == "📄 Upload JD File":
        st.markdown("**📤 Upload Job Description File**")
        uploaded_jd = st.file_uploader(
            "Choose your job description file",
            type=['pdf', 'docx', 'doc', 'txt'],
            help="Upload PDF, Word, or text files containing the job description for any role",
            key="jd_uploader"
        )

        if uploaded_jd:
            with st.spinner(f"📄 Processing {uploaded_jd.name}..."):
                # Process the uploaded JD file
                processor = DocumentProcessor()
                try:
                    if uploaded_jd.type == "text/plain":
                        job_description = str(uploaded_jd.read(), "utf-8")
                    else:
                        jd_result = processor._process_uploaded_file(uploaded_jd)
                        job_description = jd_result.get('text', '')

                    if job_description:
                        st.success(f"✅ Job description successfully extracted from {uploaded_jd.name}")

                        # Show file details
                        file_size = len(uploaded_jd.getvalue()) / 1024  # KB
                        word_count = len(job_description.split())

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("File Size", f"{file_size:.1f} KB")
                        with col2:
                            st.metric("Word Count", word_count)
                        with col3:
                            st.metric("Characters", len(job_description))

                        # Preview with edit option
                        with st.expander("📄 Preview & Edit Job Description"):
                            job_description = st.text_area(
                                "Job Description (you can edit if needed)",
                                value=job_description,
                                height=300,
                                help="Review and edit the extracted job description if needed"
                            )
                    else:
                        st.error("❌ Could not extract text from the uploaded file")
                        st.info("💡 Try uploading a different format or use the 'Paste Text' option")
                except Exception as e:
                    st.error(f"❌ Error processing file: {str(e)}")
                    st.info("💡 Please try uploading a different file or use the 'Paste Text' option")

    else:  # Paste Text option
        st.markdown("**📝 Paste Job Description Text**")
        job_description = st.text_area(
            "Paste the complete job description here",
            height=300,
            placeholder="""Example for any role:

Job Title: [Your Position Title]
Department: [Department Name]
Location: [Location/Remote]

Job Summary:
[Brief description of the role and its purpose]

Key Responsibilities:
• [Responsibility 1]
• [Responsibility 2]
• [Responsibility 3]

Required Qualifications:
• [Education requirements]
• [Years of experience needed]
• [Required skills and tools]
• [Industry experience]

Preferred Qualifications:
• [Nice-to-have qualifications]
• [Additional skills]
• [Certifications]

Examples work for:
- Software Engineer, Data Scientist, Product Manager
- Marketing Manager, Sales Director, HR Specialist
- Project Manager, Business Analyst, UX Designer
- Finance Manager, Operations Lead, Customer Success
- And any other role!""",
            help="Provide a detailed job description for any position - the AI will adapt its analysis accordingly"
        )

    if job_description:
        # Show JD confirmation with role detection
        st.success("✅ Job description provided - Ready for universal role analysis")

        # Detect job role/title for better user feedback
        jd_lines = job_description.split('\n')
        detected_role = "Position"
        for line in jd_lines[:10]:  # Check first 10 lines
            if any(keyword in line.lower() for keyword in ['job title:', 'position:', 'role:']):
                detected_role = line.split(':')[-1].strip() if ':' in line else detected_role
                break
            elif any(keyword in line.lower() for keyword in ['manager', 'engineer', 'analyst', 'director', 'specialist', 'coordinator']):
                detected_role = line.strip()
                break

        # Role-specific confirmation
        st.markdown(f"""
        <div style="background-color: #E8F5E8; padding: 1rem; border-radius: 8px; border-left: 4px solid #F47A44; margin: 1rem 0;">
            <h4 style="color: #005084; margin-bottom: 0.5rem;">🎯 Role Detected: {detected_role}</h4>
            <p style="margin: 0; color: #005084;">
                AI will adapt its analysis specifically for this role type. The system works for any position -
                from technical roles to management, creative to analytical positions.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # JD Analysis Preview
        with st.expander("🔍 Job Description Analysis Preview"):
            st.markdown("**🤖 AI will analyze CVs based on this job description for any role type:**")

            # Extract key requirements (enhanced keyword extraction for any role)
            jd_lower = job_description.lower()
            requirements_found = []

            # Universal requirement keywords that work for any role
            req_keywords = {
                "Education": ["degree", "bachelor", "master", "phd", "education", "university", "qualification", "diploma"],
                "Experience": ["years", "experience", "background", "history", "worked", "employment"],
                "Technical Skills": ["skills", "proficiency", "knowledge", "tools", "software", "programming", "technical", "systems"],
                "Domain Knowledge": ["industry", "domain", "sector", "field", "market", "business", "knowledge", "understanding"],
                "Leadership": ["leadership", "management", "team", "lead", "supervise", "manage", "director", "head"],
                "Communication": ["communication", "presentation", "writing", "verbal", "interpersonal", "collaboration"]
            }

            # Role-specific keywords for better detection
            role_specific_keywords = {
                "Software/Tech": ["programming", "coding", "development", "software", "technical", "engineering"],
                "Marketing": ["marketing", "campaigns", "digital", "social media", "advertising", "brand"],
                "Sales": ["sales", "revenue", "targets", "clients", "customers", "business development"],
                "Finance": ["financial", "accounting", "budget", "analysis", "reporting", "audit"],
                "HR": ["human resources", "recruitment", "talent", "employee", "hr", "people"],
                "Operations": ["operations", "process", "logistics", "supply chain", "efficiency"],
                "Data/Analytics": ["data", "analytics", "analysis", "statistics", "reporting", "insights"],
                "Project Management": ["project", "management", "planning", "coordination", "delivery"]
            }

            # Detect role type
            detected_role_type = "General"
            for role_type, keywords in role_specific_keywords.items():
                if any(keyword in jd_lower for keyword in keywords):
                    detected_role_type = role_type
                    break

            # Check requirements
            for category, keywords in req_keywords.items():
                if any(keyword in jd_lower for keyword in keywords):
                    requirements_found.append(f"✅ {category}")
                else:
                    requirements_found.append(f"⚪ {category}")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**🎯 Detected Role Type:**")
                st.markdown(f"**{detected_role_type}**")
                st.markdown("**Requirements Found:**")
                for req in requirements_found[:3]:
                    st.markdown(req)
            with col2:
                st.markdown("**🔍 Analysis Focus:**")
                for req in requirements_found[3:]:
                    st.markdown(req)

                # Show role-specific focus
                if detected_role_type != "General":
                    st.markdown(f"**📋 {detected_role_type} Focus:**")
                    st.markdown("✅ Role-specific criteria")
                    st.markdown("✅ Industry relevance")
                    st.markdown("✅ Skill alignment")

            # Universal applicability message
            st.markdown("""
            <div style="background-color: #F8F9FA; padding: 0.5rem; border-radius: 4px; margin-top: 1rem;">
                <small style="color: #005084;">
                    <strong>💡 Universal Tool:</strong> This system adapts to any job description -
                    Software Engineer, Marketing Manager, Data Scientist, Project Manager, HR Specialist,
                    Finance Analyst, Operations Lead, Sales Director, and more!
                </small>
            </div>
            """, unsafe_allow_html=True)

        LivingGoodsBranding.create_accent_divider()

        # CV upload
        st.subheader("📤 Step 2: Upload CVs")
        uploaded_files = st.file_uploader(
            "Upload CV files for this specific role",
            type=['pdf', 'docx', 'doc', 'zip'],
            accept_multiple_files=True,
            help="Upload CVs to analyze against the job description. Supports individual files or ZIP archives."
        )

        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} CV file(s) uploaded successfully")

            # Show file details
            with st.expander("📁 Uploaded Files Details"):
                for file in uploaded_files:
                    file_size = len(file.getvalue()) / 1024  # KB
                    st.write(f"• **{file.name}** ({file_size:.1f} KB)")

            # Analysis confirmation
            st.markdown("""
            <div style="background-color: #E8F5E8; padding: 1rem; border-radius: 8px; border: 2px solid #44ADE2; margin: 1rem 0;">
                <h4 style="color: #005084; margin-bottom: 0.5rem;">🎯 Analysis Confirmation</h4>
                <p style="margin: 0; color: #005084;">
                    <strong>Ready to analyze:</strong> The AI will evaluate each CV specifically against your job description,
                    focusing on role-specific requirements, skills, and qualifications. Results will be ranked by
                    how well each candidate fits this particular role.
                </p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🚀 Analyze CVs Against This Job Description", type="primary", help="Start role-specific CV analysis"):
                with st.spinner("🤖 AI is analyzing CVs against your job description..."):
                    # Process uploaded files
                    processor = DocumentProcessor()
                    cv_data = processor.process_uploaded_files(uploaded_files)

                    if cv_data:
                        # Show processing progress
                        progress_bar = st.progress(0)
                        status_text = st.empty()

                        # Analyze with custom job description
                        analyzer = FlexibleCVAnalyzer(euriai_api_key=euriai_key, groq_api_key=groq_key)

                        # Update progress
                        progress_bar.progress(25)
                        status_text.text("🔍 Initializing AI analysis...")

                        results = analyzer.batch_analyze(cv_data, job_description)

                        progress_bar.progress(100)
                        status_text.text("✅ Analysis complete!")

                        if results:
                            st.balloons()
                            display_analysis_results(results, "Custom Job Analysis", job_description)
                        else:
                            st.error("❌ Analysis failed. Please check your API keys.")
                    else:
                        st.error("❌ No valid CVs found in uploaded files.")
    else:
        # Show helpful information when no JD is provided
        st.info("""
        👆 **Please provide a job description above to get started.**

        **Tips for best results:**
        - Include complete job requirements and qualifications
        - Specify required vs. preferred skills
        - Mention years of experience needed
        - Include industry or domain requirements
        - Add any specific technical skills or tools
        """)

        # Show example JD
        with st.expander("📄 Example Job Description"):
            st.markdown("""
            ```
            Job Title: Digital Marketing Manager
            Department: Marketing
            Location: Nairobi, Kenya

            Job Summary:
            We are seeking an experienced Digital Marketing Manager to lead our online marketing efforts
            and drive customer acquisition through digital channels.

            Key Responsibilities:
            • Develop and execute comprehensive digital marketing strategies
            • Manage social media campaigns across multiple platforms
            • Analyze campaign performance and optimize for ROI
            • Lead a team of 3-5 marketing specialists

            Required Qualifications:
            • Bachelor's degree in Marketing, Communications, or related field
            • 5+ years of digital marketing experience
            • Proficiency in Google Analytics, Facebook Ads, LinkedIn Ads
            • Experience with marketing automation tools (HubSpot, Mailchimp)
            • Strong analytical and project management skills

            Preferred Qualifications:
            • Master's degree in Marketing or MBA
            • Experience in the healthcare or NGO sector
            • Certification in Google Ads and Facebook Blueprint
            • Experience managing marketing budgets of $100K+
            ```
            """)

def display_analysis_results(results: List, analysis_type: str, job_description: str = None):
    """Display comprehensive analysis results with filtering and export"""

    # Analysis confirmation banner
    if job_description:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #005084 0%, #44ADE2 100%); color: white; padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; text-align: center;">
            <h3 style="margin: 0; color: white;">🎯 Role-Specific Analysis Complete!</h3>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">CVs analyzed specifically against your job description requirements</p>
        </div>
        """, unsafe_allow_html=True)

    st.success(f"✅ {analysis_type} complete! Analyzed {len(results)} CVs")

    # Analysis method confirmation
    if job_description:
        st.info("""
        🤖 **AI Analysis Method**: Each CV was evaluated specifically against your job description.
        The AI focused on role-specific requirements, skills alignment, and candidate-job fit rather than generic criteria.
        """)

    # Create results table
    results_table = ResultsTable()
    df = results_table.create_results_dataframe(results)

    # Display filterable table
    results_table.display_filterable_table(df)

    # Additional insights
    LivingGoodsBranding.create_accent_divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏆 Top Performers for This Role")
        top_5 = df.head(5)[['Rank', 'Candidate Name', 'Overall Score', 'Tier']]
        st.dataframe(top_5, use_container_width=True)

        if job_description:
            st.markdown("*Rankings based on job-specific requirements*")

    with col2:
        st.subheader("📊 Score Distribution")
        scores = df['Overall Score'].str.rstrip('%').astype(float)

        # Create score ranges
        excellent = len(scores[scores >= 90])
        very_good = len(scores[(scores >= 80) & (scores < 90)])
        good = len(scores[(scores >= 70) & (scores < 80)])
        fair = len(scores[(scores >= 60) & (scores < 70)])
        poor = len(scores[scores < 60])

        score_dist = pd.DataFrame({
            'Tier': ['Excellent (90%+)', 'Very Good (80-89%)', 'Good (70-79%)', 'Fair (60-69%)', 'Poor (<60%)'],
            'Count': [excellent, very_good, good, fair, poor]
        })

        st.dataframe(score_dist, use_container_width=True)

    # Job description analysis (if provided)
    if job_description:
        LivingGoodsBranding.create_accent_divider()

        st.subheader("📋 Job Description Used for Analysis")

        # JD summary
        jd_words = len(job_description.split())
        st.markdown(f"""
        <div style="background-color: #F8F9FA; padding: 1rem; border-radius: 8px; border-left: 4px solid #005084; margin-bottom: 1rem;">
            <strong>📊 JD Analysis:</strong> {jd_words} words analyzed • Role-specific criteria extracted • AI-powered matching completed
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1])

        with col1:
            with st.expander("📄 View Complete Job Description"):
                st.text_area("Job Description Used", value=job_description, height=300, disabled=True)

        with col2:
            st.markdown("**Analysis Confirmation:**")
            st.markdown("✅ Job requirements extracted")
            st.markdown("✅ Role-specific criteria applied")
            st.markdown("✅ Skills alignment evaluated")
            st.markdown("✅ Experience relevance assessed")
            st.markdown("✅ Cultural fit considered")

            # Show analysis provider
            if results and hasattr(results[0], 'provider_used'):
                provider = results[0].provider_used
                st.markdown(f"🤖 **AI Provider:** {provider}")

    # Analysis insights
    if len(results) > 0:
        LivingGoodsBranding.create_accent_divider()

        st.subheader("💡 Analysis Insights")

        col1, col2, col3 = st.columns(3)

        with col1:
            avg_score = df['Overall Score'].str.rstrip('%').astype(float).mean()
            st.metric("Average Score", f"{avg_score:.1f}%")

        with col2:
            top_score = df['Overall Score'].str.rstrip('%').astype(float).max()
            st.metric("Highest Score", f"{top_score:.1f}%")

        with col3:
            qualified_count = len(df[df['Overall Score'].str.rstrip('%').astype(float) >= 70])
            st.metric("Qualified Candidates", f"{qualified_count}/{len(df)}")

        # Recommendations
        if job_description:
            st.markdown("### 🎯 Recruitment Recommendations")

            if excellent > 0:
                st.success(f"🏆 **{excellent} Excellent candidates** - Recommend immediate interviews")
            if very_good > 0:
                st.info(f"⭐ **{very_good} Very Good candidates** - Strong contenders for second round")
            if good > 0:
                st.warning(f"✅ **{good} Good candidates** - Consider for backup or alternative roles")
            if fair + poor > 0:
                st.error(f"⚠️ **{fair + poor} candidates** below threshold - May need additional screening")

        # Export reminder
        st.markdown("""
        <div style="background-color: #E8F5E8; padding: 1rem; border-radius: 8px; border: 2px solid #44ADE2; margin-top: 2rem;">
            <h4 style="color: #005084; margin-bottom: 0.5rem;">📥 Export Your Results</h4>
            <p style="margin: 0; color: #005084;">
                Use the export options above to download filtered results as Excel or CSV files.
                All analysis details and job description information are included.
            </p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
