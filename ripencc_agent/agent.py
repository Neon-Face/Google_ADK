from google.adk.agents import Agent


LLM_MODEL = "gemini-2.5-flash"

# define sqlite query tool
def get_monthly_roa_data(country_code: str, ip_family: str, start_date: str, end_date: str) -> dict:
    """
    Retrieves the monthly Route Origin Authorization (ROA) coverage data for specified country over a given time range and IP version.
    This tool queries ROA coverage — a measure of how much of the routed IP space in a given country is covered by valid ROAs — which helps assess routing security. 
    It supports data collection for both IPv4 and IPv6 networks.
    Use this tool when you need to analyze routing security trends across time. 
    
    For example, it is useful for identifying how well-secured the routing infrastructure is in country like NL from Jan 2020 to Aug 2025.

    Args:
    - `country_code` (str): A string of ISO 3166-1 alpha-2 country code (e.g., `'NL'`) representing the country to retrieve data for.
    - `ip_family` (str): The IP version to query. Accepts '4' for IPv4 or '6' for IPv6.
    - `start_date` (str): The beginning of the time window in `YYYY-MM-DD` format.
    - `end_date` (str): The end of the time window in `YYYY-MM-DD` format. Must not earlier than `start_date`.

    Returns:
    A `dict` with the following structure:
    - `status` (str): Indicates the result of the request.
        - `"success"`: Data was successfully retrieved.
        - `"error"`: An issue occurred (e.g., invalid input, date range out of bounds).
    - `country_code` (dict): Present only if status is `"success"`. Maps each date to a monthly ROA coverage percentages (floats).
        Example:
        ```python
        {
            "status": "success",
            "NL": {
                "2023-08": 87.5, ...
            }
        }
        ```
    - `error_message` (str): Present only if status is `"error"`. Contains a human-readable explanation of the failure.
    """
    import sqlite3

    ROA_DB_PATH = "/Users/lucas/Documents/Program_Projects/GoogleADK/country_level_data_agent/data/insights.db"
    ROA_TABLE = "ROA_MONTHLY"
    SQL_QUERY = f'''
        SELECT date, percentage_space_covered_by_roa
        FROM {ROA_TABLE}
        WHERE (
            country_code = ? and 
            ip_version = ? and
            date >= ? and
            date <= ?
        )
    '''

    try:
        conn = sqlite3.connect(ROA_DB_PATH)
        cursor = conn.cursor()
        cursor.execute(SQL_QUERY, (country_code, ip_family, start_date, end_date))
        rows = cursor.fetchall()

        data = {}
        for date, percentage in rows:
            data[date] = percentage
        
        conn.close()

        return {
            "status": "success",
            country_code: data
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e)
        }

root_agent = Agent(
    name="ripencc_agent",
    model=LLM_MODEL, 
    description="Provides accurate country-level monthly ROA coverage data based on IP version and date range.",
    instruction=(
        "You are a helpful and knowledgeable assistant specialized in internet infrastructure and routing security analysis. "
        "When a user asks for Route Origin Authorization (ROA) coverage data for a specific country, IP version (IPv4 or IPv6), and time range, "
        "use the 'get_monthly_roa_data' tool to retrieve the information. "
        "If the tool returns an error, clearly and politely explain what went wrong, such as invalid input formats, unavailable data, or internal errors. "
        "If the tool returns success, summarize the monthly ROA coverage data into a clear and concise plain-text report. "
        "Include the country code, IP version, and the time span, followed by each month and its corresponding ROA coverage percentage. "
        "Do not use markdown, or code formatting—just plain text. "
        "Avoid unnecessary explanation unless the user asks for interpretation or insights."
    ),
    tools=[get_monthly_roa_data],
)

