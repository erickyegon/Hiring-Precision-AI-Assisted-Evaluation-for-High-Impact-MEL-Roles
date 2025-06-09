"""
Results table component for CV analysis with filtering and export capabilities
"""

import pandas as pd
import streamlit as st
from typing import List, Dict, Any
from datetime import datetime
import io

class ResultsTable:
    """Professional results table with filtering and export capabilities"""
    
    def __init__(self):
        self.df = None
    
    def create_results_dataframe(self, results: List[Any]) -> pd.DataFrame:
        """Create a comprehensive results DataFrame"""
        data = []
        
        for i, result in enumerate(results, 1):
            # Handle both FlexibleAnalysisResult and CVAnalysisResult
            if hasattr(result, 'category_scores'):
                category_scores = result.category_scores
            else:
                category_scores = getattr(result, 'scores', {})
            
            row = {
                'Rank': i,
                'Candidate Name': self._extract_candidate_name(result.filename),
                'Overall Score': f"{result.overall_score:.1f}%",
                'Tier': result.tier,
                'Education': category_scores.get('education', 0),
                'Experience': category_scores.get('experience', 0),
                'Technical': category_scores.get('technical_skills', category_scores.get('technical', 0)),
                'Sector Knowledge': category_scores.get('domain_knowledge', category_scores.get('sector_knowledge', 0)),
                'Communication': category_scores.get('communication', 0),
                'Regional Exp': category_scores.get('leadership', category_scores.get('regional_experience', 0)),
                'Years Experience': getattr(result, 'years_experience', 0),
                'Role Fit Summary': getattr(result, 'role_fit_summary', 'Not available'),
                'Filename': result.filename,
                'Provider': getattr(result, 'provider_used', 'Unknown'),
                'Analysis Time': f"{getattr(result, 'analysis_time', 0):.2f}s"
            }
            data.append(row)
        
        self.df = pd.DataFrame(data)
        return self.df
    
    def _extract_candidate_name(self, filename: str) -> str:
        """Extract candidate name from filename"""
        # Remove file extension
        name = filename.rsplit('.', 1)[0]
        
        # Remove timestamp patterns (e.g., "- 2025-04-16 12-39-31")
        import re
        name = re.sub(r'\s*-\s*\d{4}-\d{2}-\d{2}\s+\d{2}-\d{2}-\d{2}', '', name)
        
        # Clean up common patterns
        name = name.replace('_', ' ').replace('-', ' ')
        
        # Capitalize properly
        name = ' '.join(word.capitalize() for word in name.split())
        
        return name
    
    def display_filterable_table(self, df: pd.DataFrame):
        """Display an interactive filterable table"""
        st.subheader("📊 Candidate Analysis Results")
        
        # Filtering controls
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            min_score = st.slider(
                "Minimum Overall Score (%)",
                min_value=0,
                max_value=100,
                value=0,
                step=5,
                help="Filter candidates by minimum overall score"
            )
        
        with col2:
            tier_filter = st.multiselect(
                "Filter by Tier",
                options=df['Tier'].unique(),
                default=df['Tier'].unique(),
                help="Select tiers to display"
            )
        
        with col3:
            min_experience = st.slider(
                "Minimum Years Experience",
                min_value=0,
                max_value=int(df['Years Experience'].max()) if len(df) > 0 else 20,
                value=0,
                help="Filter by minimum years of experience"
            )
        
        with col4:
            search_name = st.text_input(
                "Search Candidate Name",
                placeholder="Enter name to search...",
                help="Search for specific candidates"
            )
        
        # Apply filters
        filtered_df = self._apply_filters(df, min_score, tier_filter, min_experience, search_name)
        
        # Display summary statistics
        self._display_summary_stats(filtered_df)
        
        # Display the filtered table
        if len(filtered_df) > 0:
            # Format the display table
            display_df = self._format_display_table(filtered_df)
            
            st.dataframe(
                display_df,
                use_container_width=True,
                height=400,
                column_config={
                    "Rank": st.column_config.NumberColumn("Rank", width="small"),
                    "Overall Score": st.column_config.TextColumn("Overall Score", width="small"),
                    "Tier": st.column_config.TextColumn("Tier", width="medium"),
                    "Role Fit Summary": st.column_config.TextColumn("Role Fit Summary", width="large")
                }
            )
            
            # Export options
            self._display_export_options(filtered_df)
            
        else:
            st.warning("No candidates match the current filters.")
    
    def _apply_filters(self, df: pd.DataFrame, min_score: int, tier_filter: List[str], 
                      min_experience: int, search_name: str) -> pd.DataFrame:
        """Apply all filters to the DataFrame"""
        filtered_df = df.copy()
        
        # Score filter
        filtered_df['Score_Numeric'] = filtered_df['Overall Score'].str.rstrip('%').astype(float)
        filtered_df = filtered_df[filtered_df['Score_Numeric'] >= min_score]
        
        # Tier filter
        if tier_filter:
            filtered_df = filtered_df[filtered_df['Tier'].isin(tier_filter)]
        
        # Experience filter
        filtered_df = filtered_df[filtered_df['Years Experience'] >= min_experience]
        
        # Name search filter
        if search_name:
            filtered_df = filtered_df[
                filtered_df['Candidate Name'].str.contains(search_name, case=False, na=False)
            ]
        
        # Re-rank after filtering
        filtered_df = filtered_df.sort_values('Score_Numeric', ascending=False).reset_index(drop=True)
        filtered_df['Rank'] = range(1, len(filtered_df) + 1)
        
        # Remove temporary column
        filtered_df = filtered_df.drop('Score_Numeric', axis=1)
        
        return filtered_df
    
    def _display_summary_stats(self, df: pd.DataFrame):
        """Display summary statistics for filtered results"""
        if len(df) == 0:
            return
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Candidates", len(df))
        
        with col2:
            avg_score = df['Overall Score'].str.rstrip('%').astype(float).mean()
            st.metric("Average Score", f"{avg_score:.1f}%")
        
        with col3:
            excellent_count = len(df[df['Tier'] == 'Excellent'])
            st.metric("Excellent Tier", excellent_count)
        
        with col4:
            avg_experience = df['Years Experience'].mean()
            st.metric("Avg Experience", f"{avg_experience:.1f} years")
        
        with col5:
            top_score = df['Overall Score'].str.rstrip('%').astype(float).max()
            st.metric("Top Score", f"{top_score:.1f}%")
    
    def _format_display_table(self, df: pd.DataFrame) -> pd.DataFrame:
        """Format the table for better display"""
        display_df = df.copy()
        
        # Select and reorder columns for display
        display_columns = [
            'Rank', 'Candidate Name', 'Overall Score', 'Tier',
            'Education', 'Experience', 'Technical', 'Sector Knowledge',
            'Communication', 'Regional Exp', 'Years Experience', 'Role Fit Summary'
        ]
        
        display_df = display_df[display_columns]
        
        return display_df
    
    def _display_export_options(self, df: pd.DataFrame):
        """Display export options for the filtered results"""
        st.subheader("📥 Export Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Excel export
            excel_buffer = self._create_excel_export(df)
            st.download_button(
                label="📊 Download as Excel",
                data=excel_buffer,
                file_name=f"cv_analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Download filtered results as Excel file"
            )
        
        with col2:
            # CSV export
            csv_buffer = self._create_csv_export(df)
            st.download_button(
                label="📄 Download as CSV",
                data=csv_buffer,
                file_name=f"cv_analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                help="Download filtered results as CSV file"
            )
        
        with col3:
            # Summary report
            if st.button("📋 Generate Summary Report", help="Generate a detailed summary report"):
                self._display_summary_report(df)
    
    def _create_excel_export(self, df: pd.DataFrame) -> bytes:
        """Create Excel export with multiple sheets"""
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Main results sheet
            df.to_excel(writer, sheet_name='Results', index=False)
            
            # Summary statistics sheet
            summary_data = {
                'Metric': ['Total Candidates', 'Average Score', 'Excellent Tier', 'Very Good Tier', 'Good Tier'],
                'Value': [
                    len(df),
                    f"{df['Overall Score'].str.rstrip('%').astype(float).mean():.1f}%",
                    len(df[df['Tier'] == 'Excellent']),
                    len(df[df['Tier'] == 'Very Good']),
                    len(df[df['Tier'] == 'Good'])
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        return output.getvalue()
    
    def _create_csv_export(self, df: pd.DataFrame) -> str:
        """Create CSV export"""
        return df.to_csv(index=False)
    
    def _display_summary_report(self, df: pd.DataFrame):
        """Display a comprehensive summary report"""
        st.subheader("📋 Summary Report")
        
        if len(df) == 0:
            st.warning("No data to summarize.")
            return
        
        # Overall statistics
        st.write("**Overall Statistics:**")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"- Total Candidates Analyzed: {len(df)}")
            st.write(f"- Average Overall Score: {df['Overall Score'].str.rstrip('%').astype(float).mean():.1f}%")
            st.write(f"- Average Years Experience: {df['Years Experience'].mean():.1f} years")
        
        with col2:
            tier_counts = df['Tier'].value_counts()
            st.write("**Tier Distribution:**")
            for tier, count in tier_counts.items():
                percentage = (count / len(df)) * 100
                st.write(f"- {tier}: {count} ({percentage:.1f}%)")
        
        # Top performers
        st.write("**Top 5 Performers:**")
        top_5 = df.head(5)[['Rank', 'Candidate Name', 'Overall Score', 'Tier']]
        st.dataframe(top_5, use_container_width=True)
        
        # Category analysis
        st.write("**Average Category Scores:**")
        categories = ['Education', 'Experience', 'Technical', 'Sector Knowledge', 'Communication', 'Regional Exp']
        category_avgs = {cat: df[cat].mean() for cat in categories}
        
        category_df = pd.DataFrame(list(category_avgs.items()), columns=['Category', 'Average Score'])
        category_df = category_df.sort_values('Average Score', ascending=False)
        st.dataframe(category_df, use_container_width=True)
