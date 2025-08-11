def get_top_four_asns(country_code: str):
    '''
    Retrieves the latest top four ASNs by subscriber count for the specified country.

    Use this tool when you need to investigate ISP (Internet Service Provider) market concentration,
    or answer questions like "What are the largest ISPs in Germany?" or "Top 4 providers in NL".

    Args:
    - `country_code` (str): A string in ISO 3166-1 alpha-2 country code format (e.g., `'NL'`) representing the country to retrieve data for.

    Returns:
    A `dict` with the following structure:
    - `status` (str): Indicates the result of the request.
        - `"success"`: Data was successfully retrieved.
        - `"error"`: An issue occurred (e.g., invalid country code, or no data available).
    - `date` (str): Present only if status is `"success"`. Indicates the latest data’s timestamp in `YYYY-MM-DD` format.
    - `data` (list): Present only if status is `"success"`. A list of up to four dictionaries, each representing a top ASN:
        - `country_code` (str): The country code associated with the ASN (same as input).
        - `asn_name` (str): The full name of the ISP.
        - `asn` (str): The ASN (Autonomous System Number) identifier.
        - `subs_count` (str): Number of subscribers.
        - `percentage` (str): Market share percentage.
    - `error_message` (str): Present only if status is `"error"`. A human-readable explanation of the failure.

    Example:
    {
        "status": "success",
        "date": "2025-07-01",
        "data": [
            {
                "country_code": "CN",
                "asn_name": "CHINA169-BACKBONE CHINA UNICOM China169 Backbone",
                "asn": "4837",
                "subs_count": "125227396",
                "percentage": "32.03"
            },
            {
                "country_code": "CN",
                "asn_name": "CHINANET-SH-AP China Telecom Group",
                "asn": "4812",
                "subs_count": "47563619",
                "percentage": "12.17"
            }
            ...
        ]
    }
    '''

    import sqlite3

    DB_PATH = "ripencc_agent/data/insights.db"
    TOP_ASN_TABLE = "Top_4_ASNs"
    SQL_QUERY = f'''
        SELECT date, asn_name, asn, subs, percentage
        FROM {TOP_ASN_TABLE}
        WHERE cc = ?
        AND date = (
            SELECT MAX(date)
            FROM {TOP_ASN_TABLE}
            WHERE cc = ?
        )
        ORDER BY subs DESC
    '''
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(SQL_QUERY, (country_code,country_code))
        rows = cursor.fetchall()

        date = rows[0][0]

        data = []
        for _, asn_name, asn, subs, percentage in rows:
            data.append({
                "country_code": country_code,
                "asn_name": asn_name,
                "asn": asn,
                "subs_count": subs,
                "percentage": percentage
            })
        
        conn.close()

        return {
            "status": "success",
            "date": date, 
            "data": data
        }
            
    except Exception as e:
        return {
            "status":"error",
            "error_message": str(e)
        }

def get_country_asn_hhi(country_code: str):
    '''
    Retrieves the Herfindahl-Hirschman Index (HHI) for the ASN market concentration in a given country.

    Use this tool when you want to understand the level of competition among Internet Service Providers (ISPs)
    in a specific country, or answer questions like:
    - "How concentrated is the ISP market in Brazil?"
    - "What is the HHI score for Germany's ASNs?"

    The HHI is a measure of market concentration, where higher values indicate a more concentrated (less competitive) market.

    Args:
    - `country_code` (str): A string in ISO 3166-1 alpha-2 country code format (e.g., `'NL'`) representing the country to retrieve data for.

    Returns:
    A `dict` with the following structure:
    - `status` (str): Indicates the result of the request.
        - `"success"`: Data was successfully retrieved.
        - `"error"`: An issue occurred (e.g., invalid country code, or no data available).
    - `data` (list): Present only if status is `"success"`. A list of one or more entries (typically one) containing:
        - `country_code` (str): The input country code.
        - `total_users` (int): Estimated total number of subscribers in the country.
        - `number_of_asns` (int): Total number of ASNs present in the market.
        - `hhi` (float): The Herfindahl-Hirschman Index score (0–10,000 scale).
    - `error_message` (str): Present only if status is `"error"`. A human-readable explanation of the failure.

    Example:
    {
        "status": "success",
        "data": [
            {
                "country_code": "NL",
                "total_users": 15628918,
                "number_of_asns": 284,
                "hhi": 1139.86
            }
        ]
    }
    '''


    import sqlite3

    DB_PATH = "ripencc_agent/data/insights.db"
    ASN_HHI_TABLE = "Herfindahl_Hirschman_Index"
    SQL_QUERY = f'''
        SELECT Country_Code, Total_Users, Number_of_ASNs, HHI
        FROM {ASN_HHI_TABLE}
        WHERE Country_Code = ?
    '''
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(SQL_QUERY, (country_code,))
        rows = cursor.fetchall()

        data = []
        for Country_Code, Total_Users, Number_of_ASNs, HHI in rows:
            data.append({
                "country_code": Country_Code,
                "total_users": Total_Users,
                "number_of_asns": Number_of_ASNs,
                "hhi": HHI
            })
        
        conn.close()

        return {
            "status": "success",
            "data": data
        }
            
    except Exception as e:
        return {
            "status":"error",
            "error_message": str(e)
        }
