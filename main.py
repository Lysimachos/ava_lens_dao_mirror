import streamlit as st
import asyncio
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
        /* Clean layout */
        .block-container {
            padding: 2rem;
            max-width: 1800px;
        }
        
        /* Hide default elements */
        #MainMenu, footer, header {
            visibility: hidden;
        }
        
        /* Simple button styling */
        .stButton button {
            width: 100%;
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
            st.image('app/ava_lens.jpg')
        except Exception as e:
            st.error(f"Failed to load avatar: {str(e)}")
            
    with header_right:
        st.header("Ava Lens")
        st.subheader("Your Creative Guide to the DAO Universe")

    # Add spacing
    st.write("")

    # Initialize services
    search_service = SearchService()
    image_service = ImageService()
    agent = DAOAgent(search_service, image_service)

    # Main input area
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
        generate_button = st.button("✨ Generate", use_container_width=True)

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
                            st.write(response["dao_info"]["summary"])
                            
                            if response["dao_info"].get("urls"):
                                st.markdown("### 🔗 Relevant Links")
                                for url in response["dao_info"]["urls"]:
                                    st.markdown(f"- [{url}]({url})")
                        
                        with image_col:
                            if response.get("image"):
                                st.image(response["image"])
                                st.markdown("### 🎨 Image Prompt")
                                st.write(response.get("image_prompt"))
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