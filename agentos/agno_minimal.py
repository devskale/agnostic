from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from credgoo import get_api_key

api_key = get_api_key("tu")


assistant = Agent(
    name="Assistant",
    model=OpenAIChat(
        id="qwen-coder-30b",
        base_url="https://aqueduct.ai.datalab.tuwien.ac.at/v1",
        api_key=api_key,
    ),
    instructions=["You are a helpful AI assistant."],
    markdown=True,
)

agent_os = AgentOS(
    id="glmos",
    description="glm agentos",
    agents=[assistant],
)

app = agent_os.get_app()

if __name__ == "__main__":
    # Default port is 7777; change with port=...
    agent_os.serve(app="agno_minimal:app", reload=True)
