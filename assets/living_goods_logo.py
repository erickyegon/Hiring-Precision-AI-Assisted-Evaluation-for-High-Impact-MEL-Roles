"""
Living Goods Logo Implementation
SVG logo placeholder compliant with branding guidelines
"""

def get_living_goods_logo_svg(color="primary", size="medium"):
    """
    Generate Living Goods logo SVG
    
    Args:
        color: "primary" (#005084), "white", or "secondary" (#44ADE2)
        size: "small", "medium", "large"
    """
    
    # Color mapping
    colors = {
        "primary": "#005084",
        "white": "#FFFFFF", 
        "secondary": "#44ADE2"
    }
    
    # Size mapping
    sizes = {
        "small": {"width": 120, "height": 40},
        "medium": {"width": 180, "height": 60},
        "large": {"width": 240, "height": 80}
    }
    
    logo_color = colors.get(color, colors["primary"])
    dimensions = sizes.get(size, sizes["medium"])
    
    # Professional logo placeholder (replace with actual Living Goods logo)
    svg_logo = f"""
    <svg width="{dimensions['width']}" height="{dimensions['height']}" viewBox="0 0 240 80" xmlns="http://www.w3.org/2000/svg">
        <!-- Background circle -->
        <circle cx="40" cy="40" r="35" fill="{logo_color}" opacity="0.1"/>
        
        <!-- Main logo symbol -->
        <g transform="translate(10, 15)">
            <!-- Heart symbol representing "Living" -->
            <path d="M30 20 C30 15, 25 10, 20 10 C15 10, 10 15, 10 20 C10 30, 20 40, 30 50 C40 40, 50 30, 50 20 C50 15, 45 10, 40 10 C35 10, 30 15, 30 20 Z" 
                  fill="{logo_color}" opacity="0.8"/>
            
            <!-- Plus symbol representing "Goods/Health" -->
            <rect x="25" y="15" width="10" height="30" fill="{logo_color}"/>
            <rect x="15" y="25" width="30" height="10" fill="{logo_color}"/>
        </g>
        
        <!-- Company name -->
        <text x="80" y="30" font-family="Oswald, Franklin Gothic, Arial Black, sans-serif" 
              font-size="18" font-weight="700" fill="{logo_color}">LIVING</text>
        <text x="80" y="50" font-family="Oswald, Franklin Gothic, Arial Black, sans-serif" 
              font-size="18" font-weight="700" fill="{logo_color}">GOODS</text>
        
        <!-- Tagline -->
        <text x="80" y="65" font-family="Nunito Sans, Century Gothic, sans-serif" 
              font-size="10" fill="{logo_color}" opacity="0.7">Health for Everyone</text>
    </svg>
    """
    
    return svg_logo

def get_logo_with_breathing_room(color="primary", size="medium", background_color="#FFFFFF"):
    """
    Get logo with proper breathing room as per branding guidelines
    """
    logo_svg = get_living_goods_logo_svg(color, size)
    
    # Add breathing room container
    return f"""
    <div style="
        background-color: {background_color};
        padding: 2rem;
        border-radius: 8px;
        display: inline-block;
        margin: 1rem 0;
    ">
        {logo_svg}
    </div>
    """
