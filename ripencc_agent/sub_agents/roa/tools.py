def get_monthly_roa_coverage(country_code: str, ip_family: str, start_date: str, end_date: str) -> dict:
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

    ROA_DB_PATH = "ripencc_agent/data/insights.db"
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