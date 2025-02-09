from crewai.tools import BaseTool
from typing import Type, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
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
        1. Response should be between 350-400 words
        2. Focus on key points and relevant information
        3. Use clear and concise language
        4. Maintain a professional tone
        5. Include relevant examples where appropriate
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
            gpt_model = kwargs.get('model', model)

            # Create formatted prompt
            prompt = self._create_prompt(space_query,role)
            
            # Make API call
            client = openai.OpenAI(
                api_key=openai.api_key,
                base_url=openapibase
            )
            # Make API call
            response = openai.ChatCompletion.create(
                model=model,
                openapibase=openapibase,
                messages=[
                    {"role": "system", "content": "You are a knowledgeable space research assistant providing detailed analysis and summaries."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=600  # Approximately 450 words
            )

            # Extract response text
            response_text = response.choices[0].message.content.strip()
            word_count = self._count_words(response_text)

            return {
                "status": "success",
                "response": response_text,
                "word_count": word_count,
                "model_used": model,
                "tokens_used": response.usage.total_tokens,
                "query": space_query
            }

        except openai.error.OpenAIError as e:
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