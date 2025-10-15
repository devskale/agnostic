from decimal import Context
from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from agno.os import AgentOS
from agno.db.sqlite import SqliteDb
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from credgoo import get_api_key

agent_storage: str = "./tmp/agents.db"

api_key = get_api_key("tu")

web_agent = Agent(
    name="Web Agent",
    model=OpenAILike(
        id="glm-4.6-355b",
        max_tokens=130000,
        base_url="https://aqueduct.ai.datalab.tuwien.ac.at/v1",
        api_key=api_key,
    ),
    tools=[DuckDuckGoTools()],
    instructions=["Always include sources"],
    # Store the agent sessions in a sqlite database
    db=SqliteDb(db_file=agent_storage),
    # Adds the current date and time to the context
    add_datetime_to_context=True,
    # Adds the history of the conversation to the messages
    add_history_to_context=True,
    # Number of history responses to add to the messages
    num_history_runs=5,
    # Adds markdown formatting to the messages
    markdown=True,
)

finance_agent = Agent(
    name="Finance Agent",
    model=OpenAILike(
        id="qwen-coder-30b",
        max_tokens=16384,
        base_url="https://aqueduct.ai.datalab.tuwien.ac.at/v1",
        api_key=api_key,
    ),
    tools=[YFinanceTools()],
    instructions=["Always use tables to display data"],
    db=SqliteDb(db_file=agent_storage),
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

agent_os = AgentOS(agents=[web_agent, finance_agent])
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve("agno_webfin:app", reload=True)
