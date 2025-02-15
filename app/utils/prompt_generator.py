class PromptGenerator:
    @staticmethod
    def generate_dao_prompt(dao_name: str, dao_summary: str) -> str:
        """
        Generate a prompt for image generation
        """
        return f"""Create a modern, minimalist logo for {dao_name} DAO. 
        The design should reflect its purpose: {dao_summary[:100]}. 
        Style: Clean, professional, with subtle blockchain elements.
        Color scheme: Blue and purple gradient.""" 