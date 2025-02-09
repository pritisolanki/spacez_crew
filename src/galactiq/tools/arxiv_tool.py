from crewai.tools import BaseTool
from typing import Type, Dict, Any, List
from pydantic import BaseModel, Field, ConfigDict
import requests
import xml.etree.ElementTree as ET

class ArxivSearchSchema(BaseModel):
    query: str = Field(..., description="Search query for arXiv papers")
    max_results: int = Field(default=3, description="Maximum number of results to return")
    start: int = Field(default=0, description="Starting index for results")

class ArxivTool(BaseTool):
    """Tool to search academic papers on arXiv"""
    name: str = "SearchArxiv"
    description: str = "Search for academic papers on arXiv using a search query."
    args_schema: Type[BaseModel] = ArxivSearchSchema
    model_config = ConfigDict(arbitrary_types_allowed=True)
    base_url: str = "http://export.arxiv.org/api/query"

    def _parse_entry(self, entry) -> Dict:
        """Parse a single entry from arXiv XML response."""
        authors = [author.find('{http://www.w3.org/2005/Atom}name').text 
                  for author in entry.findall('{http://www.w3.org/2005/Atom}author')]
        
        categories = [cat.get('term') for cat in entry.findall('{http://www.w3.org/2005/Atom}category')]
        
        return {
            'id': entry.find('{http://www.w3.org/2005/Atom}id').text,
            'title': entry.find('{http://www.w3.org/2005/Atom}title').text.strip(),
            'summary': entry.find('{http://www.w3.org/2005/Atom}summary').text.strip(),
            'authors': authors,
            'published': entry.find('{http://www.w3.org/2005/Atom}published').text,
            'updated': entry.find('{http://www.w3.org/2005/Atom}updated').text,
            'categories': categories,
            'pdf_link': next(
                link.get('href') for link in entry.findall('{http://www.w3.org/2005/Atom}link')
                if link.get('title') == 'pdf'
            ),
        }

    def _run(self, query: str, max_results: int = 3, start: int = 0) -> Dict[str, Any]:
        """
        Execute the arXiv search.

        Parameters:
            query (str): Search query
            max_results (int): Maximum number of results to return
            start (int): Starting index for results

        Returns:
            Dict[str, Any]: Search results or error message
        """
        try:
            params = {
                'search_query': f'all:{query}',
                'start': start,
                'max_results': max_results
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            # Parse XML response
            root = ET.fromstring(response.content)

            # Check total results using opensearch namespace
            total_results = int(root.find('{http://a9.com/-/spec/opensearch/1.1/}totalResults').text)
            if total_results == 0:
                return {
                    "status": "noresults",
                    "results": [],
                    "total_results": 0,
                    "message": f"No results found for query: {query}"
                }
            # Extract entries
            entries = root.findall('{http://www.w3.org/2005/Atom}entry')
            
            # Parse results
            results = [self._parse_entry(entry) for entry in entries]
            
            return {
                "status": "success",
                "results": results,
                "total_results": len(results)
            }
            
        except requests.RequestException as e:
            return {
                "status": "error",
                "message": f"Error fetching arXiv data: {str(e)}"
            }
        except ET.ParseError as e:
            return {
                "status": "error",
                "message": f"Error parsing arXiv response: {str(e)}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}"
            }