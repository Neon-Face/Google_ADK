import sqlite3
from typing import Optional

def get_country_ipv6_adoption_rate(country_code: str, source: Optional[str] = None, specific_date: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
    '''
    Retrieves the IPv6 adoption rate for a given country, optionally filtered by data source and date.

    Use this tool when you want to understand the adoption of IPv6 in a specific country,
    or answer questions like:
    - "What is the IPv6 adoption rate in Germany?"
    - "Show me the IPv6 adoption rate from Google for Brazil on 2023-03-15."
    - "How does Cisco's IPv6 adoption data compare to Akamai's for the Netherlands between 2022 and 2024?"
    - "What's the latest IPv6 adoption rate for Japan?"

    Args:
    - `country_code` (str): A string in ISO 3166-1 alpha-2 country code format (e.g., `'NL'`) representing the country to retrieve data for.
    - `source` (str, optional): The data source for IPv6 adoption. Can be one of 'google', 'facebook', 'akamai', 'cisco', 'cloudflare'. If not provided, data from all available sources for the country will be returned.
    - `specific_date` (str, optional): A specific date in 'YYYY-MM-DD' format to retrieve the adoption rate for. If provided, `start_date` and `end_date` will be ignored.
    - `start_date` (str, optional): The start date of a range in 'YYYY-MM-DD' format. Used for fetching data over a period.
    - `end_date` (str, optional): The end date of a range in 'YYYY-MM-DD' format. Used for fetching data over a period.

    Returns:
    A `dict` with the following structure:
    - `status` (str): Indicates the result of the request.
        - `"success"`: Data was successfully retrieved.
        - `"error"`: An issue occurred (e.g., invalid country code, or no data available).
    - `data` (list): Present only if status is `"success"`. A list of entries.
        - If `specific_date`, `start_date`, and `end_date` are all `None`, it returns the latest available entry for each unique source for the given country.
        - Otherwise, it returns entries matching the specified date or date range.
        Each entry contains:
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
            }
        ]
    }
    '''

    DB_PATH = "ripencc_agent/data/insights.db"
    IPV6_ADOPTION_TABLE = "Country_IPv6_Adoption"

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        data = []
        SQL_QUERY = ""
        params = []

        if specific_date:
            SQL_QUERY = f'''
                SELECT cc, date, percentage, source
                FROM {IPV6_ADOPTION_TABLE}
                WHERE cc = ? AND date = ?
            '''
            params = [country_code, specific_date]
            if source:
                SQL_QUERY += " AND source = ?"
                params.append(source)
            cursor.execute(SQL_QUERY, tuple(params))
            rows = cursor.fetchall()
        elif start_date or end_date:
            SQL_QUERY = f'''
                SELECT cc, date, percentage, source
                FROM {IPV6_ADOPTION_TABLE}
                WHERE cc = ?
            '''
            params = [country_code]
            if source:
                SQL_QUERY += " AND source = ?"
                params.append(source)
            if start_date:
                SQL_QUERY += " AND date >= ?"
                params.append(start_date)
            if end_date:
                SQL_QUERY += " AND date <= ?"
                params.append(end_date)
            cursor.execute(SQL_QUERY, tuple(params))
            rows = cursor.fetchall()
        else: # Default: get latest for each source
            # Subquery to find the maximum date for each source for the given country
            subquery_conditions = "WHERE cc = ?"
            subquery_params = [country_code]
            if source:
                subquery_conditions += " AND source = ?"
                subquery_params.append(source)

            SQL_QUERY = f'''
                SELECT T1.cc, T1.date, T1.percentage, T1.source
                FROM {IPV6_ADOPTION_TABLE} T1
                INNER JOIN (
                    SELECT source, MAX(date) AS MaxDate
                    FROM {IPV6_ADOPTION_TABLE}
                    {subquery_conditions}
                    GROUP BY source
                ) T2 ON T1.source = T2.source AND T1.date = T2.MaxDate
                WHERE T1.cc = ?
            '''
            # The outer query's WHERE clause may also need to filter by source if provided
            outer_where_params = [country_code]
            if source:
                SQL_QUERY += " AND T1.source = ?"
                outer_where_params.append(source)

            # Combine subquery parameters and outer query parameters for the final execution
            full_params = subquery_params + outer_where_params
            cursor.execute(SQL_QUERY, tuple(full_params))
            rows = cursor.fetchall()

        for cc_val, date_val, percentage_val, source_val in rows:
            data.append({
                "country_code": cc_val,
                "date": date_val,
                "percentage": percentage_val,
                "source": source_val
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