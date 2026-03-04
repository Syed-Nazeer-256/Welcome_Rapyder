import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from streamlit_cropper import st_cropper
import requests
import os

# Function to download and cache fonts
@st.cache_data
def download_font(font_url, font_name):
    """Download font from URL and save locally"""
    try:
        response = requests.get(font_url)
        if response.status_code == 200:
            font_path = f"{font_name}.ttf"
            with open(font_path, 'wb') as f:
                f.write(response.content)
            return font_path
    except Exception as e:
        st.warning(f"Could not download {font_name}: {e}")
    return None

# Function to get font with fallback
def get_font(font_size, bold=False):
    """Get font with fallback options"""
    # Try to use local fonts first
    font_attempts = []
    if bold:
        font_attempts = [
            "fonts/Poppins-Bold.ttf", "fonts/DMSans-Bold.ttf", 
            "Poppins-Bold.ttf", "DMSans-Bold.ttf",
            "C:\\Windows\\Fonts\\arialbd.ttf", "C:\\Windows\\Fonts\\segoeuib.ttf"
        ]
    else:
        font_attempts = [
            "fonts/Poppins-Regular.ttf", "fonts/DMSans-Regular.ttf",
            "Poppins-Regular.ttf", "DMSans-Regular.ttf",
            "C:\\Windows\\Fonts\\arial.ttf", "C:\\Windows\\Fonts\\segoeui.ttf"
        ]
    
    # Try specific paths
    for font_path in font_attempts:
        try:
            if os.path.exists(font_path):
                return ImageFont.truetype(font_path, font_size)
        except:
            continue
    
    # Try by name (Pillow can sometimes find them in standard system paths)
    system_fonts = ["arial.ttf", "segoeui.ttf", "calibri.ttf"]
    if bold:
        system_fonts = ["arialbd.ttf", "segoeuib.ttf", "calibrib.ttf"]
        
    for font_name in system_fonts:
        try:
            return ImageFont.truetype(font_name, font_size)
        except:
            continue
            
    # If on Linux/Mac
    unix_fonts = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Helvetica.ttc"
    ]
    for font_path in unix_fonts:
        try:
            return ImageFont.truetype(font_path, font_size)
        except:
            continue
    
    # Final fallback: if default font is used, it will be tiny, so we try one last generic attempt
    try:
        return ImageFont.truetype("arial.ttf", font_size)
    except:
        return ImageFont.load_default()

# Function to create a circular mask
def create_circular_mask(size):
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    return mask

# Function to apply the circular mask to an image
def apply_circular_mask(image, mask):
    output = Image.new("RGBA", image.size, (0, 0, 0, 0))
    output.paste(image, (0, 0), mask)
    return output

# --- PREMIUM UI/UX ENHANCEMENTS ---
def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

    /* Global styling */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
        scroll-behavior: smooth;
    }

    .stApp {
        background: linear-gradient(135deg, #fefcf9 0%, #fff5e6 100%) !important;
    }

    /* Keyframes */
    @keyframes slideInRight {
        0% { opacity: 0; transform: translateX(30px); }
        100% { opacity: 1; transform: translateX(0); }
    }

    @keyframes fadeInUp {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }

    @keyframes pulseSoft {
        0% { box-shadow: 0 4px 15px rgba(252, 48, 48, 0.3); }
        50% { box-shadow: 0 4px 25px rgba(252, 48, 48, 0.5); }
        100% { box-shadow: 0 4px 15px rgba(252, 48, 48, 0.3); }
    }

    /* Animation Classes */
    .animate-fade-in-up { animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) both; }
    .animate-slide-in-right { animation: slideInRight 0.8s cubic-bezier(0.16, 1, 0.3, 1) both; }
    .animate-float { animation: float 3s ease-in-out infinite; }
    
    /* Staggered Delays */
    .delay-1 { animation-delay: 0.1s; }
    .delay-2 { animation-delay: 0.2s; }
    .delay-3 { animation-delay: 0.3s; }
    .delay-4 { animation-delay: 0.4s; }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.3) !important;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #4a2c2a !important;
        font-weight: 500;
    }

    /* Input styling */
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.7) !important;
        border: 2px solid rgba(252, 48, 48, 0.1) !important;
        border-radius: 12px !important;
        color: #4a2c2a !important;
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
    }

    .stTextInput input:focus {
        border-color: #fc3030 !important;
        box-shadow: 0 0 15px rgba(252, 48, 48, 0.2) !important;
        transform: scale(1.02);
    }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #fc3030 0%, #ff5e62 100%) !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 0.8rem 3rem !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(252, 48, 48, 0.3) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        animation: pulseSoft 3s infinite;
    }

    .stButton > button:hover {
        transform: translateY(-5px) scale(1.05) !important;
        box-shadow: 0 12px 30px rgba(252, 48, 48, 0.4) !important;
        background: linear-gradient(135deg, #ff5e62 0%, #fc3030 100%) !important;
    }

    /* File Uploader */
    [data-testid="stFileUploader"] {
        background-color: rgba(255, 255, 255, 0.5) !important;
        border: 2px dashed rgba(252, 48, 48, 0.2) !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #fc3030 !important;
        background-color: rgba(255, 255, 255, 0.8) !important;
    }

    /* Titles and Header */
    h1, h2, h3 {
        color: #4a2c2a !important;
        font-weight: 700 !important;
        letter-spacing: -0.03em !important;
    }

    /* Card Preview Animation */
    [data-testid="stImage"] {
        border-radius: 20px !important;
        overflow: hidden !important;
        transition: all 0.5s cubic-bezier(0.165, 0.84, 0.44, 1);
    }
    
    [data-testid="stImage"]:hover {
        transform: scale(1.02) translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.1) !important;
    }

    /* Smooth transition for all elements */
    .element-container {
        transition: all 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit App
st.set_page_config(page_title="Digital Business Card Generator", page_icon="💳", layout="wide")
inject_custom_css()

# Sidebar Logo / Decorative Element
st.sidebar.markdown(f"""
    <div class="animate-float" style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #fc3030; font-family: 'Outfit', sans-serif;">Welcome Creative</h2>
        <div style="height: 4px; width: 60px; background: #fc3030; margin: 0 auto; border-radius: 2px;"></div>
    </div>
""", unsafe_allow_html=True)

# User Inputs with staggered animations
st.sidebar.markdown('<div class="animate-slide-in-right">', unsafe_allow_html=True)
st.sidebar.header("Enter Your Details")
st.sidebar.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="animate-slide-in-right delay-1">', unsafe_allow_html=True)
user_name = st.sidebar.text_input("Your Name", "Swaroop TR")
st.sidebar.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="animate-slide-in-right delay-2">', unsafe_allow_html=True)
job_title = st.sidebar.text_input("Job Title", "Graphic Designer")
st.sidebar.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="animate-slide-in-right delay-3">', unsafe_allow_html=True)
uploaded_image = st.sidebar.file_uploader("Upload Your Photo", type=["png", "jpg", "jpeg"])
st.sidebar.markdown('</div>', unsafe_allow_html=True)

cropped_image = None
if uploaded_image is not None:
    st.sidebar.subheader("Crop Your Photo")
    img = Image.open(uploaded_image)
    cropped_image = st_cropper(img, realtime_update=True, box_color="blue",
                                aspect_ratio=(1,1), return_type="image")

    if cropped_image is not None:
        st.markdown('<div class="animate-fade-in-up">', unsafe_allow_html=True)
        st.subheader("Circular Preview")
        # Process the cropped image to show circular preview
        preview_photo_size = (200, 200) # Smaller size for preview
        preview_user_photo = cropped_image.convert("RGBA").resize(preview_photo_size)
        preview_mask = create_circular_mask(preview_photo_size)
        preview_circular_photo = apply_circular_mask(preview_user_photo, preview_mask)
        st.image(preview_circular_photo, caption="How your photo will look in the circle", use_container_width=False)
        st.info("**Important:** Adjust the cropping box to perfectly fit your face/subject within the square. This square will be precisely fitted into the circular area on the card.")
        st.markdown('</div>', unsafe_allow_html=True)

if st.sidebar.button("Generate Card"):
    if cropped_image is not None:
        # Set the desired output size
        output_size = (2000, 2000)

        # Open the template and resize it
        card = Image.open("wc.png").convert("RGBA")
        card = card.resize(output_size)
        card_width, card_height = card.size

        # Define the outer ring size and position
        outer_ring_size = (825, 825)  # Increased circle size
        ring_thickness = 17  # Ring thickness (not used for drawing, but for context)
        
        # Calculate centered position for the circle
        ring_x = (card_width - outer_ring_size[0]) // 2
        ring_y = (card_height - outer_ring_size[1]) // 2 - 170 # Adjusted downwards by 2 pixels
        
        # Process and add user photo to fill the entire circle area
        user_photo = cropped_image.convert("RGBA")
        photo_size = (823, 823)  # Photo fills the entire circle
        user_photo = user_photo.resize(photo_size)
        mask = create_circular_mask(photo_size)
        circular_photo = apply_circular_mask(user_photo, mask)

        # Position the photo
        photo_x = ring_x
        photo_y = ring_y

        card.paste(circular_photo, (photo_x, photo_y), circular_photo)

        # Add user name with improved font handling and multi-line wrapping
        draw = ImageDraw.Draw(card)
        name_font_size = 90
        name_font = get_font(name_font_size, bold=True)
        
        # Check if we fell back to default tiny font
        test_bbox = draw.textbbox((0, 0), "A", font=name_font)
        line_height = (test_bbox[3] - test_bbox[1]) + 20
        if (test_bbox[3] - test_bbox[1]) < 20: 
             st.warning("Warning: Using system default font. Text might appear very small. Please ensure fonts are available.")

        # Multi-line wrapping logic for Name
        MAX_NAME_WIDTH = 1600
        words = user_name.upper().split()
        name_lines = []
        current_line = []
        
        for word in words:
            test_line = " ".join(current_line + [word])
            line_bbox = draw.textbbox((0, 0), test_line, font=name_font)
            if (line_bbox[2] - line_bbox[0]) <= MAX_NAME_WIDTH:
                current_line.append(word)
            else:
                if current_line:
                    name_lines.append(" ".join(current_line))
                current_line = [word]
        if current_line:
            name_lines.append(" ".join(current_line))

        # Draw name lines
        start_y = 1380
        # If multiple lines, start slightly higher to keep it centered
        if len(name_lines) > 1:
            start_y -= (len(name_lines) - 1) * (line_height // 2)

        last_name_y = start_y
        for i, line in enumerate(name_lines):
            line_bbox = draw.textbbox((0, 0), line, font=name_font)
            line_w = line_bbox[2] - line_bbox[0]
            line_x = (card_width - line_w) // 2
            current_y = start_y + (i * line_height)
            draw.text((line_x, current_y), line, fill="#fc3030", font=name_font, stroke_width=2, stroke_fill="white")
            last_name_y = current_y

        # Add job title with improved font handling
        title_font_size = 55 # Increased slightly
        title_font = get_font(title_font_size, bold=False)
        
        title_text = job_title.upper()
        title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (card_width - title_width) // 2  # Center horizontally
        # Dynamic gap below the last name line
        title_y = last_name_y + line_height + 20 
        draw.text((title_x, title_y), title_text, fill="black", font=title_font)

        # Convert to JPEG
        card = card.convert("RGB")

        # Display the card
        st.image(card, caption="Your Digital Business Card", use_container_width=True)

        # Download button
        buf = BytesIO()
        card.save(buf, format="JPEG")
        byte_im = buf.getvalue()
        
        # Clean file name
        safe_name = "".join([c for c in user_name if c.isalnum() or c in (' ', '_')]).strip().replace(' ', '_')
        if not safe_name: safe_name = "business_card"
        
        st.download_button(
            label="Download Your Professional Card",
            data=byte_im,
            file_name=f"{safe_name}.jpg",
            mime="image/jpeg",
        )
    else:
        st.warning("Please upload and crop your photo to generate the card.")
