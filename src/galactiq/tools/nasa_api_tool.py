from crewai.tools import BaseTool
from typing import Type, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
import requests
from datetime import datetime

class NASASearchSchema(BaseModel):
    """Input schema for NASA API Tool."""
    endpoint: str = Field(
        ..., 
        description="NASA API endpoint to query (apod, neo, earth, epic)",
        pattern="^(apod|neo|earth|epic)$"
    )
    date: str = Field(
        default=None,
        description="Date for the query in YYYY-MM-DD format (optional)",
        pattern="^\d{4}-\d{2}-\d{2}$"
    )
    count: int = Field(
        default=1,
        description="Number of results to return (for APOD endpoint)",
        ge=1,
        le=100
    )

class NASATool(BaseTool):
    """Tool to interact with NASA's public APIs"""
    name: str = "NASA_API_Tool"
    description: str = """
    Access NASA's public APIs to fetch space-related data. Available endpoints:
    - apod: Astronomy Picture of the Day
    - neo: Near Earth Object data
    - earth: Earth imagery
    - epic: Earth Polychromatic Imaging Camera
    """
    args_schema: Type[BaseModel] = NASASearchSchema
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    # Replace with your NASA API key or use DEMO_KEY for testing
    api_key: str = os.getenv("NASA_API_KEY")
    base_urls: Dict[str, str] = {
        "apod": "https://api.nasa.gov/planetary/apod",
        "neo": "https://api.nasa.gov/neo/rest/v1/feed",
        "earth": "https://api.nasa.gov/planetary/earth/assets",
        "epic": "https://api.nasa.gov/EPIC/api/natural/date"
    }

    def _format_apod_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format APOD API response"""
        if isinstance(data, list):
            return {
                "status": "success",
                "count": len(data),
                "results": [{
                    "date": item.get("date"),
                    "title": item.get("title"),
                    "explanation": item.get("explanation"),
                    "url": item.get("url"),
                    "media_type": item.get("media_type")
                } for item in data]
            }
        return {
            "status": "success",
            "count": 1,
            "results": [{
                "date": data.get("date"),
                "title": data.get("title"),
                "explanation": data.get("explanation"),
                "url": data.get("url"),
                "media_type": data.get("media_type")
            }]
        }

    def _format_neo_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format NEO API response"""
        neo_data = []
        for date, asteroids in data["near_earth_objects"].items():
            for asteroid in asteroids:
                neo_data.append({
                    "id": asteroid["id"],
                    "name": asteroid["name"],
                    "date": date,
                    "diameter_min": asteroid["estimated_diameter"]["kilometers"]["estimated_diameter_min"],
                    "diameter_max": asteroid["estimated_diameter"]["kilometers"]["estimated_diameter_max"],
                    "is_hazardous": asteroid["is_potentially_hazardous_asteroid"],
                    "close_approach_date": asteroid["close_approach_data"][0]["close_approach_date"],
                    "miss_distance_km": float(asteroid["close_approach_data"][0]["miss_distance"]["kilometers"])
                })
        return {
            "status": "success",
            "count": len(neo_data),
            "results": neo_data
        }

    def _run(self, endpoint: str, date: str = None, count: int = 1) -> Dict[str, Any]:
        """
        Execute the NASA API query.

        Parameters:
            endpoint (str): NASA API endpoint to query
            date (str): Date for the query in YYYY-MM-DD format
            count (int): Number of results to return (for APOD endpoint)

        Returns:
            Dict[str, Any]: API response or error message
        """
        try:
            url = self.base_urls.get(endpoint)
            if not url:
                return {
                    "status": "error",
                    "message": f"Invalid endpoint: {endpoint}"
                }

            params = {"api_key": self.api_key}
            
            if date:
                if endpoint == "apod":
                    params["date"] = date
                elif endpoint == "neo":
                    params.update({
                        "start_date": date,
                        "end_date": date
                    })
                elif endpoint in ["earth", "epic"]:
                    params["date"] = date

            if endpoint == "apod" and count > 1:
                params["count"] = count
                
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if endpoint == "apod":
                return self._format_apod_response(data)
            elif endpoint == "neo":
                return self._format_neo_response(data)
            
            # For other endpoints, return formatted raw data
            return {
                "status": "success",
                "data": data
            }

        except requests.RequestException as e:
            return {
                "status": "error",
                "message": f"Error fetching NASA data: {str(e)}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}"
            }