import streamlit as st
from app.services.image_service import ImageService, VeniceAiModelStyles
from PIL import Image

def setup_page_config():
    st.set_page_config(
        page_title="AvaLens AI",
        page_icon="🎨",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

def apply_custom_css():
    st.markdown("""
        <style>
        /* Main container */
        .main {
            padding: 2rem;
        }
        
        /* Header styling */
        .header-container {
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 2rem;
        }
        
        .avatar-image {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            object-fit: cover;
        }
        
        /* Input fields */
        .stTextInput input, .stTextArea textarea {
            border-radius: 10px;
            border: 2px solid #f0f2f6;
            padding: 10px;
        }
        
        /* Button styling */
        .stButton button {
            background-color: #FF4B4B;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            border: none;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            background-color: #FF6B6B;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        /* Select box styling */
        .stSelectbox {
            border-radius: 10px;
        }
        
        /* Remove default Streamlit padding */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }
        
        /* Generated image container */
        .generated-image {
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    setup_page_config()
    apply_custom_css()

    # Load and display avatar with title
    avatar = Image.open('app/ava_lens.jpg')
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(
            f"""
            <div class="header-container">
                <img src="data:image/png;base64,{Image.open('app/ava_lens.jpg').tobytes()}" class="avatar-image">
                <h1>AvaLens AI Image Generator</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Main content area
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        prompt = st.text_area(
            "What would you like me to create?",
            placeholder="Describe your imagination...",
            height=100,
            key="prompt"
        )

    with right_col:
        style_options = sorted([style.value for style in VeniceAiModelStyles])
        selected_style = st.selectbox(
            "Art Style",
            options=style_options,
            index=style_options.index("3D Model")
        )

    # Center the generate button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        generate_button = st.button("✨ Generate", use_container_width=True)

    if generate_button:
        if not prompt:
            st.warning("Please enter a prompt first!")
            return
            
        with st.spinner("🎨 Creating your masterpiece..."):
            image_service = ImageService()
            image = image_service.generate_image(prompt, selected_style)
            
            if image:
                # Center and display the generated image
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image(image, use_column_width=True, clamp=True, output_format="PNG")
            else:
                st.error("Failed to generate image. Please try again.")

if __name__ == "__main__":
    main() 