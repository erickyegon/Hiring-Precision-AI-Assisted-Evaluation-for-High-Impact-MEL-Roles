"""
Living Goods Branding Guide Implementation
Based on Living Goods Branding Guide (August 2022)
"""

import streamlit as st
from typing import Optional

class LivingGoodsBranding:
    """Living Goods brand compliance implementation"""
    
    # Official Living Goods Color Palette (Exact values from branding guide)
    COLORS = {
        # Primary Blue - Main brand color
        "primary_blue": {
            "hex": "#005084",
            "rgb": (0, 80, 132),
            "cmyk": (100, 44, 0, 40),
            "pms": "293"
        },
        
        # Secondary Blue - Supporting color
        "secondary_blue": {
            "hex": "#44ADE2", 
            "rgb": (68, 173, 226),
            "cmyk": (65, 15, 0, 0),
            "pms": "298"
        },
        
        # Accent Orange - Highlight color
        "accent_orange": {
            "hex": "#F47A44",
            "rgb": (244, 122, 68),
            "cmyk": (0, 65, 80, 0),
            "pms": "1585"
        },
        
        # Gray - Neutral color
        "gray": {
            "hex": "#A9BDC9",
            "rgb": (169, 189, 201),
            "cmyk": (14, 0, 0, 25),
            "pms": "5435"
        },
        
        # Additional utility colors
        "white": "#FFFFFF",
        "light_gray": "#F8F9FA",
        "dark_text": "#2E3440",
        "success": "#28A745",
        "warning": "#FFC107",
        "error": "#DC3545"
    }
    
    # Typography specifications
    FONTS = {
        "header": "Franklin Gothic, Arial Black, sans-serif",
        "body": "Century Gothic, Futura, sans-serif",
        "monospace": "Consolas, Monaco, monospace"
    }
    
    @classmethod
    def get_custom_css(cls) -> str:
        """Generate simplified CSS for Living Goods brand compliance"""
        return f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Nunito+Sans:wght@300;400;600;700&display=swap');

        /* Living Goods Brand Colors */
        :root {{
            --lg-primary: #005084;
            --lg-secondary: #44ADE2;
            --lg-accent: #F47A44;
            --lg-gray: #A9BDC9;
        }}

        /* Headers */
        h1, h2, h3 {{
            font-family: 'Oswald', sans-serif !important;
            color: var(--lg-primary) !important;
        }}

        /* Body text */
        .stMarkdown, p, div {{
            font-family: 'Nunito Sans', sans-serif !important;
        }}

        /* Buttons */
        .stButton > button {{
            background-color: var(--lg-primary) !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 600 !important;
        }}

        .stButton > button:hover {{
            background-color: var(--lg-secondary) !important;
        }}

        /* Metrics */
        [data-testid="metric-value"] {{
            color: var(--lg-primary) !important;
            font-family: 'Oswald', sans-serif !important;
        }}

        /* Progress bars */
        .stProgress .st-bo {{
            background-color: var(--lg-primary) !important;
        }}

        /* Sidebar */
        .css-1d391kg {{
            background-color: #F8F9FA !important;
        }}

        /* Hide Streamlit menu */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        </style>
        """
    
    @classmethod
    def apply_branding(cls):
        """Apply Living Goods branding to the Streamlit app"""
        st.markdown(cls.get_custom_css(), unsafe_allow_html=True)
    
    @classmethod
    def create_branded_header(cls, title: str, subtitle: Optional[str] = None):
        """Create a branded header with Living Goods styling"""
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #005084 0%, #44ADE2 100%);
            color: white;
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            text-align: center;
        ">
            <div style="font-size: 2rem; margin-bottom: 1rem;">🏥</div>
            <h1 style="margin: 0; font-family: 'Oswald', sans-serif;">{title}</h1>
            {f'<p style="margin: 0.5rem 0 0 0; font-style: italic;">{subtitle}</p>' if subtitle else ''}
        </div>
        """, unsafe_allow_html=True)

    @classmethod
    def display_logo(cls):
        """Display Living Goods logo placeholder"""
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <div style="font-size: 3rem; color: #005084;">🏥</div>
            <div style="font-family: 'Oswald', sans-serif; color: #005084; font-weight: 700; font-size: 1.5rem;">LIVING GOODS</div>
            <div style="font-family: 'Nunito Sans', sans-serif; color: #A9BDC9; font-size: 0.9rem;">Health for Everyone</div>
        </div>
        """, unsafe_allow_html=True)
    
    @classmethod
    def create_accent_divider(cls):
        """Create a branded divider"""
        st.markdown("""
        <hr style="
            height: 4px;
            background: linear-gradient(90deg, #005084 0%, #F47A44 50%, #44ADE2 100%);
            border: none;
            margin: 2rem 0;
            border-radius: 2px;
        ">
        """, unsafe_allow_html=True)

    @classmethod
    def create_brand_card(cls, content: str):
        """Create a branded card container"""
        st.markdown(f"""
        <div style="
            background-color: white;
            border: 2px solid #005084;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 8px rgba(0, 80, 132, 0.1);
        ">
            {content}
        </div>
        """, unsafe_allow_html=True)
    
    @classmethod
    def get_color(cls, color_name: str) -> str:
        """Get a brand color by name"""
        return cls.COLORS.get(color_name, {}).get('hex', '#000000')
    
    @classmethod
    def create_status_indicator(cls, status: str, message: str):
        """Create a branded status indicator"""
        color_map = {
            'success': '#44ADE2',
            'warning': '#F47A44',
            'error': '#DC3545',
            'info': '#005084'
        }

        color = color_map.get(status, '#A9BDC9')

        st.markdown(f"""
        <div style="
            background-color: {color}15;
            border-left: 4px solid {color};
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        ">
            <strong style="color: {color};">{status.upper()}:</strong> {message}
        </div>
        """, unsafe_allow_html=True)
