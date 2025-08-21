def get_country_ipv6_adoption_rate(country_code: str, source: str = None):
    '''
    Retrieves the IPv6 adoption rate for a given country, optionally filtered by data source.

    Use this tool when you want to understand the adoption of IPv6 in a specific country,
    or answer questions like:
    - "What is the IPv6 adoption rate in Germany?"
    - "Show me the IPv6 adoption rate from Google for Brazil."
    - "How does Cisco's IPv6 adoption data compare to Akamai's for the Netherlands?"

    Args:
    - `country_code` (str): A string in ISO 3166-1 alpha-2 country code format (e.g., `'NL'`) representing the country to retrieve data for.
    - `source` (str, optional): The data source for IPv6 adoption. Can be one of 'google', 'facebook', 'akamai', 'cisco', 'cloudflare'. If not provided, data from all available sources for the country will be returned.

    Returns:
    A `dict` with the following structure:
    - `status` (str): Indicates the result of the request.
        - `"success"`: Data was successfully retrieved.
        - `"error"`: An issue occurred (e.g., invalid country code, or no data available).
    - `data` (list): Present only if status is `"success"`. A list of entries, each containing:
        - `country_code` (str): The input country code.
        - `date` (str): The date of the adoption rate measurement (e.g., 'YYYY-MM-DD').
        - `percentage` (float): The IPv6 adoption rate as a percentage.
        - `source` (str): The source of the adoption data.
    - `error_message` (str): Present only if status is `"error"`. A human-readable explanation of the failure.

    Example:
    {
        "status": "success",
        "data": [
            {
                "country_code": "NL",
                "date": "2023-01-15",
                "percentage": 50.5,
                "source": "google"
            },
            {
                "country_code": "NL",
                "date": "2023-01-15",
                "percentage": 48.2,
                "source": "akamai"
            },
            {
                "country_code": "NL",
                "date": "2023-02-01",
                "percentage": 51.0,
                "source": "google"
            }
        ]
    }
    '''

    import sqlite3

    DB_PATH = "ripencc_agent/data/insights.db"
    IPV6_ADOPTION_TABLE = "Country_IPv6_Adoption"
    SQL_QUERY = f'''
        SELECT country_code, date, percentage, source
        FROM {IPV6_ADOPTION_TABLE}
        WHERE Country_Code = ?
    '''
    params = [country_code]

    if source:
        SQL_QUERY += " AND source = ?"
        params.append(source)

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(SQL_QUERY, tuple(params))
        rows = cursor.fetchall()

        data = []
        for Country_Code, Date, Percentage, Source in rows:
            data.append({
                "country_code": Country_Code,
                "date": Date,
                "percentage": Percentage,
                "source": Source
            })

        conn.close()

        return {
            "status": "success",
            "data": data
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e)
        }