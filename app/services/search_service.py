from tavily import Client
from app.config import TAVILY_API_KEY


class SearchService:
    """Service for searching DAO information using Tavily"""
    
    def __init__(self):
        self.client = Client(api_key=TAVILY_API_KEY)

    def search_dao(self, dao_name: str, dao_info:str) -> dict:
        """Search for comprehensive DAO information"""

        try:
            query = (
                f"{dao_name} decentralized autonomous organization DAO"
            )
            if dao_info:
                query += f" {dao_info}"

            results = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=2
            )
            
            return {
                "summary": results.get('answer', 'No information found'),
                "urls": [r.get('url') for r in results.get('results', [])][:2]
            }
        except Exception as e:
            print(f"Search error: {str(e)}")
            return {
                "summary": "Unable to fetch DAO information at this time.",
                "urls": []
            } 