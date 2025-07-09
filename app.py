import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from streamlit_cropper import st_cropper

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

# Streamlit App
st.set_page_config(page_title="Digital Business Card Generator", page_icon="💳")

st.title("Digital Business Card Generator")
st.write("Create your own professional digital business card with ease.")

# User Inputs
st.sidebar.header("Enter Your Details")
user_name = st.sidebar.text_input("Your Name", "VAIBHAV SATISH KUMAR ARORA")
job_title = st.sidebar.text_input("Job Title", "SR. ACCOUNT DIRECTOR - ENTERPRISE")
uploaded_image = st.sidebar.file_uploader("Upload Your Photo", type=["png", "jpg", "jpeg"])

cropped_image = None
if uploaded_image is not None:
    st.sidebar.subheader("Crop Your Photo")
    img = Image.open(uploaded_image)

    col1, col2 = st.columns(2) # Create two columns

    with col1:
        cropped_image = st_cropper(img, realtime_update=True, box_color="blue",
                                    aspect_ratio=(1,1), return_type="image")

    with col2:
        if cropped_image is not None:
            st.subheader("Circular Preview")
            # Process the cropped image to show circular preview
            preview_photo_size = (200, 200) # Smaller size for preview
            preview_user_photo = cropped_image.convert("RGBA").resize(preview_photo_size)
            preview_mask = create_circular_mask(preview_photo_size)
            preview_circular_photo = apply_circular_mask(preview_user_photo, preview_mask)
            st.image(preview_circular_photo, caption="How your photo will look in the circle", use_column_width=False)
            st.info("**Important:** Adjust the cropping box to perfectly fit your face/subject within the square. This square will be precisely fitted into the circular area on the card.")

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

        # Add user name
        draw = ImageDraw.Draw(card)
        try:
            name_font_size = 80 # Scaled font size
            name_font = ImageFont.truetype("fonts/Poppins-Bold.ttf", name_font_size)
        except IOError:
            st.warning("Arial Bold font not found. Using default font.")
            name_font = ImageFont.load_default()
        name_text = user_name.upper()
        name_bbox = draw.textbbox((0, 0), name_text, font=name_font)
        name_width = name_bbox[2] - name_bbox[0]
        name_x = (card_width - name_width) // 2  # Center horizontally
        name_y = 1400 # Scaled position (adjusted)
        draw.text((name_x, name_y), name_text, fill="#fc3030", font=name_font)

        # Add job title
        try:
            title_font_size = 50 # Scaled font size
            title_font = ImageFont.truetype("fonts/Poppins-Regular.ttf", title_font_size)
        except IOError:
            st.warning("Arial font not found. Using default font.")
            title_font = ImageFont.load_default()
        title_text = job_title.upper()
        title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (card_width - title_width) // 2  # Center horizontally
        title_y = 1500 # Scaled position (adjusted)
        draw.text((title_x, title_y), title_text, fill="black", font=title_font)

        # Convert to JPEG
        card = card.convert("RGB")

        # Display the card
        st.image(card, caption="Your Digital Business Card", use_column_width=True)

        # Download button
        buf = BytesIO()
        card.save(buf, format="JPEG")
        byte_im = buf.getvalue()
        st.download_button(
            label="Download Business Card",
            data=byte_im,
            file_name="business_card.jpg",
            mime="image/jpeg",
        )
    else:
        st.warning("Please upload and crop your photo to generate the card.")
