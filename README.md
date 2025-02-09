# Galactiq Crew

Welcome to the Galactiq Crew project, powered by [crewAI](https://crewai.com). GalacticIQ - Unlocking the Universe, One Question at a Time. Presented by Team SpaceZ, is an AI-powered space education platform for researchers, educators, and students. It provides information on space data based on the persona.

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` from AI/ML, `SLACK_BOT_TOKEN` and `MODEL` into the `.env` file**

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

## Tools and Technologies
- **OpenAI API**: The OpenAI API is used to generate responses to user queries.GPT-4o model.
- **Slack API**: The Slack API is used to send and receive messages from the Slack workspace.
- **Arxiv API**: The Arxiv API is used to fetch research papers and articles.
- **Nasa API**: The NASA API is used to fetch space data .
- **CrewAI**: CrewAI is a Python library that simplifies the development of AI-powered chatbots and virtual assistants.
- **Python**: The project is built using Python, a high-level, general-purpose programming language.
- **Next.js**: The frontend is built using Next.JS, a React framework for building server-rendered applications.
- **Vercel**: The frontend is hosted on Vercel, a cloud platform for static sites and serverless functions.
- **GCP**: The CrewAI project is deployed on Google Cloud Platform

## Team Social

- [Priti Solanki LinkedIn](https://www.linkedin.com/in/pritisolanki/)
- [Vishal Kumar LinkedIn](https://www.linkedin.com/in/vishalx360/)
- [Shamas Liaqat LinkedIn](https://www.linkedin.com/in/shamasliaqat/)

## Support

For support, questions, or feedback regarding the Galactiq Crew or crewAI.
- Reach out to us through our [GitHub repository](https://github.com/pritisolanki/spacez_crew)
- Email us at [Support](mailto:pritisolanki@purplespot.ink)


Unlocking the Universe, One Question at a Time. 🚀