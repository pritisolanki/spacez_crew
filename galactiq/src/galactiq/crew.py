from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from galactiq.tools.slack_tool import SlackTool
from galactiq.tools.arxiv_tool import ArxivTool
from galactiq.tools.gpt_tool import GPTTool
import json

@CrewBase
class Galactiq():
	"""Galactiq crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def spacez_manager(self) -> Agent:
		return Agent(
			config=self.agents_config['spacez_manager'],
			verbose=True
		)

	@agent
	def spacez_mission_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['spacez_mission_agent'],
			verbose=True
		)

	@agent
	def spacez_satellite_data_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['spacez_satellite_data_agent'],
			verbose=True
		)

	@agent
	def spacez_celestial_events_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['spacez_celestial_events_agent'],
			verbose=True
		)

	@agent
	def spacez_research_papers_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['spacez_research_papers_agent'],
			verbose=True
		)

	@agent
	def feedback_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['feedback_agent'],
			verbose=True
		)

	@task
	def spacez_manager_task(self) -> Task:
		return Task(
			config=self.tasks_config['spacez_manager_task'],
			output_file="resource_response.json",
			completion_handler=self.process_query_response # Calls internal method
		)

	@task
	def space_mission_agent_task(self) -> Task:
		return Task(
			config=self.tasks_config['space_mission_agent_task'],
			tools=[GPTTool()]
		)

	@task
	def satellite_data_agent_task(self) -> Task:
		return Task(
			config=self.tasks_config['satellite_data_agent_task'],
			tools=[GPTTool()]
		)

	@task
	def celestial_events_agent_task(self) -> Task:
		return Task(
			config=self.tasks_config['celestial_events_agent_task'],
			tools=[GPTTool()]
		)

	@task
	def research_papers_agent_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_papers_agent_task'],
			output_file="resource_response.txt",
			tools=[ArxivTool()]
		)

	@task
	def slack_notification_task(self) -> Task:
		return Task(
			config=self.tasks_config['slack_notification_task'],
			tools=[SlackTool()]
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Galactiq crew"""
		return Crew(
			agents=[self.spacez_mission_agent(),
            self.spacez_satellite_data_agent(),
            self.spacez_celestial_events_agent(),
            self.spacez_research_papers_agent(),
            self.feedback_agent()],  # Automatically created by the @agent decorator
			tasks=self.tasks,  # Automatically created by the @task decorator
			process=Process.hierarchical,
			manager_agent=self.spacez_manager(),
			verbose=True,
		)

	def classify_query(self, space_query):
		"""Classifies query and returns the correct agent name"""
		
		space_query_lower = space_query.lower()

		if "space mission" in space_query_lower:
			return "spacez_mission_agent"
		elif "satellite" in space_query_lower or "orbit" in space_query_lower:
			return "spacez_satellite_data_agent"
		elif "celestial" in space_query_lower or "event" in space_query_lower or "eclipse" in space_query_lower:
			return "spacez_celestial_events_agent"
		elif "research paper" in space_query_lower or "study" in space_query_lower:
			return "spacez_research_papers_agent"
		else:
			return None  # If no valid category is found

	def process_query_response(self, response):
		print('-----------------------------------------------')
		print('in process queyr')
		"""Formats the response into JSON before returning."""
		
		space_query = self.tasks_config['spacez_manager_task'].get("space_query", "")
		agent_name = self.classify_query(space_query)
		print('-----------------------------------------------')
		print(f"Agent name: {agent_name}")
		if not agent_name:  # No agent found
			research_response = "We apologize, but we have no information at this moment. Your query has been forwarded to the backend team for further research."
			json_output = {
				"query": space_query,
				"response": research_response,
				"status": "not_found"
			}
		else:
			assigned_task = getattr(self, f"{agent_name}_task")()  # Get the correct task dynamically
			agent_response = assigned_task.run()  # Run the task to get the agent's response

			if agent_response and agent_response.strip():
				research_response = agent_response if agent_response else "No valid response received."
				json_output = {
					"query": space_query,
					"response": research_response,
					"status": "success"
				}
		print('-----------------------------------------------')
		print(agent_response)
		print('-----------------------------------------------')
		self.tasks_config['spacez_manager_task']['research_response'] = research_response  
		# Save JSON output
		with open("resource_response.json", "w") as json_file:
			json.dump(json_output, json_file, indent=4)

		return json.dumps(json_output, indent=4)
