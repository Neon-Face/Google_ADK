from google.adk import Agent
from .tools import get_monthly_roa_coverage 

roa_query_agent = Agent(
    name="roa_query_agent",
    description="""
        You are a monthly ROA data query agent. 
        Your task is to retrieve Route Origin Authorization (ROA) coverage data based on the given country code, IP version (IPv4 or IPv6), and time frame. 
        You return structured data showing monthly ROA coverage percentages for the specified parameters.
    """,
    instruction = """
        ALWAYS use the tool `get_monthly_roa_coverage` with the provided country_code, ip_version, and date range. 
        Do not attempt to interpret or reformat the data—simply return what the tool provides. 
        If the tool returns an error, report it clearly to the user.
    """
,
    tools=[get_monthly_roa_coverage]
)