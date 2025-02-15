import streamlit as st
import asyncio
from PIL import Image
from app.services.search_service import SearchService
from app.services.image_service import ImageService, VeniceAiModelStyles
from app.services.agent_service import DAOAgent

def setup_page():
    st.set_page_config(
        page_title="Ava Lens | AI-Powered DAO Explorer",
        page_icon="🎨",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

def apply_custom_css():
    st.markdown("""
        <style>
        /* Global styles */
        * {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
        }
        
        /* Main container */
        .main {
            padding: 3rem;
            background-color: #FFFFFF;
        }
        
        /* Title styles - significantly larger */
        .stMarkdown h1, .stHeader h1 {
            color: #1E1E1E !important;
            font-size: 4.5rem !important;  /* Much larger title */
            font-weight: 800 !important;
            margin-bottom: 1rem !important;
            letter-spacing: -4px !important;
            line-height: 1.1 !important;
        }
        
        /* Description text - significantly larger */
        .stMarkdown p:first-of-type {
            color: #4A4A4A !important;
            font-size: 2.5rem !important;  /* Much larger description */
            font-weight: 400 !important;
            margin-bottom: 2.5rem !important;
            letter-spacing: -1px !important;
            line-height: 1.2 !important;
        }

        /* Section headers */
        h2 {
            color: #1E1E1E;
            font-size: 2.4rem !important;
            font-weight: 600 !important;
            margin: 2rem 0 !important;
        }
        
        /* Regular text */
        p, div {
            font-size: 1.4rem !important;
            line-height: 1.6 !important;
            color: #2C2C2C;
        }
        
        /* Clean up header area */
        .block-container {
            padding: 4rem 5rem;
            max-width: 1800px;
            margin: 0 auto;
        }
        
        /* Remove default Streamlit elements */
        #MainMenu, footer, header {
            visibility: hidden;
        }
        
        /* Streamlit elements styling */
        .stTextArea textarea {
            font-size: 1.4rem !important;
            padding: 1.5rem !important;
            border: 2px solid #E0E0E0;
            border-radius: 15px;
            background-color: #FFF;
        }
        
        .stSelectbox > div > div {
            font-size: 1.3rem !important;
        }
        
        .stButton button {
            font-size: 1.4rem !important;
            padding: 1.2rem 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

async def process_query(agent: DAOAgent, query: str, style:str="abstract"):
    return await agent.process_query(query=query, style=style)

available_styles = [style.value for style in VeniceAiModelStyles]

def main():
    setup_page()
    apply_custom_css()

    # Header with avatar
    st.write("")
    header_left, header_right = st.columns([1, 3])
    
    with header_left:
        try:
            st.image('app/ava_lens.jpg', width=240)
        except Exception as e:
            st.error(f"Failed to load avatar: {str(e)}")
            
    with header_right:
        st.markdown('<p>Ava Lens</p>', unsafe_allow_html=True)
        st.markdown('<p>Your Creative Guide to the DAO Universe</p>', unsafe_allow_html=True)

    # Initialize services
    search_service = SearchService()
    image_service = ImageService()
    agent = DAOAgent(search_service, image_service)

    # Main input area
    st.write("")
    
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        query = st.text_area(
            "",
            placeholder="✨ Ask about a DAO or explore the world of decentralized organizations...",
            height=120
        )

    with right_col:
        st.write("")
        style_options = sorted([style.value for style in VeniceAiModelStyles])
        selected_style = st.selectbox(
            "🎨 Art Style",
            options=style_options,
            index=style_options.index("3D Model")
        )

    # Generate button
    st.write("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_button = st.button("✨ Generate Magic", use_container_width=True)

    if generate_button:
        if not query:
            st.warning("🤔 Please enter a query first!")
            return
            
        with st.spinner("🎨 Creating your unique DAO visualization..."):
            try:
                response = asyncio.run(process_query(agent, query, selected_style))
                
                if response["success"]:
                    if response.get("dao_info"):
                        st.write("")
                        info_col, image_col = st.columns([3, 2])
                        
                        with info_col:
                            st.markdown("## 📚 DAO Information")
                            st.write(response["dao_info"]["summary"])
                            
                            if response["dao_info"].get("urls"):
                                st.markdown("## 🔗 Relevant Links")
                                for url in response["dao_info"]["urls"]:
                                    st.markdown(f"- [{url}]({url})")
                        
                        with image_col:
                            if response.get("image"):
                                st.markdown("## 🎨 Visualization")
                                st.image(response["image"], use_column_width=True)
                            else:
                                st.error("🎨 Failed to generate image.")
                    else:
                        st.write(response["response"])
                else:
                    st.error(f"❌ Error: {response['error']}")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 