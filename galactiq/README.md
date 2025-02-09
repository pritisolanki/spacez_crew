# Galactiq Crew

Welcome to the Galactiq Crew project, powered by [crewAI](https://crewai.com). GalacticIQ - Unlocking the Universe, One Question at a Time. Presented by Team SpaceZ, is an AI-powered space education platform for researchers, educators, and students. It provides information on space data based on the persona.

## Frontend
Frontend is built using Next.JS and hosted on Vercel. You can find the frontend code [GalactiqIQ Frontend](https://github.com/kumarvishalben/galact-iq)

## Demo
Checkout the demo > [GalactiqIQ](https://galact-iq.vishalx360.dev/)

## Understanding Your Crew
The galactIQ Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

Therer are six agents in the galactIQ Crew:
- **spacez_manager**: Receives query and assigns the tasks to appropriate agents. Return response to customer and for unresolved queries send it to the backend team.
- **spacez_mission_agent**: Provide information about space missions and their payloads
- **spacez_satellite_data_agent**: Provide information about satellite data
- **spacez_celestial_events_agent**: Provide information about celestial events
- **spacez_research_papers_agent**: Provide information about research papers
- **feedback_agent**: Collect feedback and push the feedback to the slack channel

Unlocking the Universe, One Question at a Time. 🚀

