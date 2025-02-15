from typing import Dict
from .search_service import SearchService
from .image_service import ImageService
from .llm_service import VeniceLLM

class DAOAgent:
    """Agent for handling DAO-related queries and generating visualizations"""

    def __init__(self, search_service: SearchService, image_service: ImageService):
        self.search_service = search_service
        self.image_service = image_service
        self.llm = VeniceLLM()
        self.image_style = ""

    async def process_query(self, query: str, style:str) -> Dict:
        """Process user query and return appropriate response"""
        try:
            # 1. Classify the query
            classification = self.llm.classify_query(query)
            
            if not classification["is_dao_query"]:
                return {
                    "success": True,
                    "response": "I can only help with DAO-related questions. Please ask something about DAOs.",
                    "dao_info": None,
                    "image": None
                }

            # 2. Handle DAO-specific queries
            if classification["existing_dao"]:
                # Search for existing DAO
                search_results = self.search_service.search_dao(
                    dao_name=classification["dao_name"],
                    dao_info=classification["dao_info"]
                )
            else:
                # Handle hypothetical/general DAO queries
                response = self.llm.get_general_response(query)
                search_results = {
                    "summary": response,
                    "urls": []
                }

            # 3. Generate visualization for existing DAOs
            if search_results["summary"]:
                # Generate image concept
                image_idea = self.llm.generate_image_idea(
                    dao_name=classification["dao_name"],
                    dao_info=classification["dao_info"],
                    dao_summary=search_results["summary"],
                    style=style
                )

                image_prompt = self.llm.generate_image_prompt(image_idea)
                image = self.image_service.generate_image(image_prompt)

                return {
                    "success": True,
                    "response": search_results["summary"],
                    "dao_info": search_results,
                    "image": image
                }
            else:
                return {
                    "success": True,
                    "response": "Could not find detailed information about this DAO.",
                    "dao_info": None,
                    "image": None
                }

        except Exception as e:
            print(f"Error processing query: {str(e)}")
            return {
                "success": False,
                "error": "Sorry, I encountered an error processing your request. Please try again.",
                "dao_info": None,
                "image": None
            }