import json
import requests
from app.config import VENICE_API_KEY

class VeniceLLM:
    """Venice AI service for LLM interactions"""
    
    def __init__(self):
        self.api_url = "https://api.venice.ai/api/v1/chat/completions"
        self.model = "dolphin-2.9.2-qwen2-72b"
        self.headers = {
            "Authorization": f"Bearer {VENICE_API_KEY}",
            "Content-Type": "application/json"
        }

    def _call_api(self, prompt: str) -> str:
        """Make API call to Venice"""
        try:
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}]
            }
            response = requests.post(self.api_url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Venice API call failed: {str(e)}")
            raise

    def classify_query(self, query: str) -> dict:
        """Classify the query and extract relevant information"""
        prompt = f"""Analyze this query about DAOs (Decentralized Autonomous Organizations).
        Query: {query}
        
        Return JSON with these fields:
        - dao_name: Name of specific DAO (null if none)
        - dao_info: Keywords about what the DAO does/focuses on (null if none)
        - is_dao_query: True if about DAOs
        - existing_dao: True if about a known DAO, false if hypothetical/general
        
        Examples:
        "Tell me about MakerDAO" -> {{"dao_name": "MakerDAO", "dao_info": "null", "is_dao_query": true, "existing_dao": true}}
        "What is a DAO?" -> {{"dao_name": null, "dao_info": "what is a DAO", "is_dao_query": true, "existing_dao": false}}
        "Create a DAO for gaming" -> {{"dao_name": null, "dao_info": "Create a dao for gaming community", "is_dao_query": true, "existing_dao": false}}
        "How is the weather?" -> {{"dao_name": null, "dao_info": null, "is_dao_query": false, "existing_dao": false}}"""
        
        try:
            response = self._call_api(prompt)
            return json.loads(response)
        except:
            return {"dao_name": None, "dao_info": None, "is_dao_query": False, "existing_dao": False}

    def generate_image_idea(self, dao_name: str, dao_info: str, dao_summary: str, style: str = "modern") -> str:
        """Generate creative image idea for DAO visualization"""
        context = "\n".join(filter(None, [
            f"DAO Name: {dao_name}" if dao_name else None,
            f"Focus: {dao_info}" if dao_info else None,
            f"Summary: {dao_summary}" if dao_summary else None
        ]))
        
        prompt = f"""Create a {style} visual concept for this DAO:
        {context}

        Create a unique, abstract design that:
        1. Represents the DAO's core purpose visually
        2. Includes blockchain/crypto elements (nodes, connections, tokens)
        3. Shows decentralization and community
        4. Maintains professional and clean aesthetic
        
        Return only the visual concept, no explanations."""
        
        return self._call_api(prompt)

    def generate_image_prompt(self, image_idea: str) -> str:
        """Convert concept into optimized image generation prompt"""
        prompt = f"""Enhance this image concept for AI generation:
        {image_idea}

        Create a detailed prompt that:
        1. Uses (()) for important elements, () for secondary details
        2. Includes specific style and composition details
        3. Adds technical aspects: 4K, detailed, professional
        4. Maintains crypto/blockchain aesthetic

        Example structure:
        ((main subject)), (supporting elements), style details, technical specs, composition

        Return only the enhanced prompt."""
        
        return self._call_api(prompt)

    def get_general_response(self, query: str) -> str:
        """Provide informative response about DAOs"""
        prompt = f"""Answer this DAO-related question clearly and concisely:
        {query}

        Guidelines:
        1. Use simple language
        2. Include real examples
        3. Focus on practical understanding
        4. Keep it under 150 words
        
        Return only the answer."""
        
        return self._call_api(prompt)