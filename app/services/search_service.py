from tavily import TavilyClient
from app.config import TAVILY_API_KEY
import streamlit as st


class SearchService:
    """Service for searching DAO information using Tavily"""
    
    def __init__(self):
        st.write(TAVILY_API_KEY)
        self.client = TavilyClient(api_key=TAVILY_API_KEY)

    def search_dao(self, dao_name: str, dao_info:str) -> dict:
        """Search for comprehensive DAO information"""

        try:
            query = (
                f"{dao_name}"
            )
            if dao_info:
                query += f" {dao_info}"

            results = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=2
            )
            answers = [result_dict.get("content") for result_dict in results.get("results")]
            answer = answers[0] if len(answers)>0 else ""
            answer = answer + " " + answers[1] if len(answers)>1 else answer
            return {
                "summary": answer,
                "urls": [r.get('url') for r in results.get('results', [])][:2]
            }
        except Exception as e:
            print(f"Search error: {str(e)}")
            return {
                "summary": "Unable to fetch DAO information at this time.",
                "urls": []
            } 
