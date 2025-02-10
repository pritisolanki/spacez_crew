from crewai.tools import BaseTool
from typing import Type, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from dotenv import load_dotenv
import os
import requests
from openai import OpenAI

load_dotenv()
OpenAI.api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL")
openapibase = os.getenv("OPENAI_API_BASE")

class GPTQuerySchema(BaseModel):
    space_query: str = Field(..., description="Query to be sent to GPT for analysis")
    role: str = Field(..., description="Role of the user")
    model: str = Field(default="gpt-3.5-turbo", description="GPT model to use")
    temperature: float = Field(default=0.7, description="Temperature for response generation")

class GPTTool(BaseTool):
    """Tool to query GPT and get summarized responses"""
    name: str = "QueryGPT"
    description: str = "Query GPT with a specific topic and get a summarized response"
    args_schema: Type[BaseModel] = GPTQuerySchema
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def _create_prompt(self, space_query: str, role: str) -> str:
        """Create a structured prompt for GPT"""
        return f"""
        Please analyze and provide a comprehensive response to the following query:
        {space_query} for {role}
        
        Requirements:
        1. Response should be between 200-250 words
        2. Focus on key points and relevant information
        3. Use clear and concise language
        4. Maintain a professional tone
        """

    def _count_words(self, text: str) -> int:
        """Count words in text"""
        return len(text.split())

    def _run(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the GPT query and return summarized response.

        Parameters:
            space_query (str): Query to analyze
            model (str): GPT model to use
            temperature (float): Temperature for response generation

        Returns:
            Dict[str, Any]: Query results or error message
        """
        try:
            space_query = kwargs.get('space_query')
            role = kwargs.get('role')
            temperature = kwargs.get('temperature', 0.7)

            # Create formatted prompt
            prompt = self._create_prompt(space_query,role)
            
            headers = {
                'Authorization': f'Bearer {OpenAI.api_key}',
                'Content-Type': 'application/json'
            }
            # Make API call
            client = OpenAI(
                base_url=openapibase,
                api_key=OpenAI.api_key,    
            )
            response = client.chat.completions.create(
                model="gpt-4o-mini-2024-07-18",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI space assistant who helps users with their space queries according to {role}.",
                    },
                    {
                        "role": "user",
                        "content": prompt
                    },
                ],
                max_tokens=300
            )
            # Extract response text
            response_text = response.choices[0].message.content.strip()            

            return {
                "status": "success",
                "response": response_text,
                "tokens_used": response.usage.total_tokens,
                "query": space_query
            }

        except OpenAI.OpenAIError as e:
            return {
                "status": "error",
                "message": f"OpenAI API error: {str(e)}",
                "query": space_query
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}",
                "query": space_query
            }

    def _arun(self, space_query: str, model: str = "gpt-4o", temperature: float = 0.7):
        """Async implementation can be added here if needed"""
        raise NotImplementedError("Async version not implemented")