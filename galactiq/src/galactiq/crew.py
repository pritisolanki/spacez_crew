from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from galactiq.tools.slack_tool import SlackTool
# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Galactiq():
	"""Galactiq crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def spacez_manger(self) -> Agent:
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
	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def spacez_manager_task(self) -> Task:
		return Task(
			config=self.tasks_config['spacez_manager_task'],
		)

	@task
	def space_mission_agent_task(self) -> Task:
		return Task(
			config=self.tasks_config['space_mission_agent_task'],
		)

	@task
	def satellite_data_agent_task(self) -> Task:
		return Task(
			config=self.tasks_config['satellite_data_agent_task'],
		)
	
	@task
	def celestial_events_agent_task(self) -> Task:
		return Task(
			config=self.tasks_config['celestial_events_agent_task'],
		)
	
	@task
	def research_papers_agent_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_papers_agent_task'],
		)		
	
	@task
	def slack_notification_task(self) -> Task:
		return Task(
			config=self.tasks_config['feedback_agent_task'],
			tools=[SlackTool()]
		)
	
	@crew
	def crew(self) -> Crew:
		"""Creates the Galactiq crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
