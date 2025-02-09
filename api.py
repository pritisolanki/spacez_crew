from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from galactiq.crew import Galactiq

app = FastAPI(
    title="Galactiq API", description="API for running Galactiq crew operations"
)

# Add CORS middleware to allow requests from localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CrewInput(BaseModel):
    space_query: str
    role: str = "educator"
    category: str = "space mission"
    topic: str = "Space"
    research_response: str = "response will be return in this variable"


@app.post("/run-crew")
async def run_crew(input_data: CrewInput):
    try:
        # Prepare inputs dictionary
        inputs = input_data.dict()
        inputs["current_year"] = str(datetime.now().year)

        # Run the crew
        result = Galactiq().crew().kickoff(inputs=inputs)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
