import os
import re
import pandas as pd
from datetime import datetime
from urllib.parse import urlparse, parse_qs


def contains_day_or_month(text):
    """
    Check if the given text contains a day of the week or a month.

    Args:
        text (str): The input text to check.

    Returns:
        tuple: A tuple containing a boolean indicating whether a match was found,
        and the matched text (day or month) if found.
    """

    # Regular expressions for days of the week and months
    days_of_week = r"\b(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b"
    months = r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b"
    pattern = f"({days_of_week}|{months})"

    match = re.search(pattern, text, re.IGNORECASE)

    if not match:
        return False, None

    matched_text = match.group(0)
    if re.match(days_of_week, matched_text, re.IGNORECASE):
        return True, matched_text


def extract_year_from_url(url: str) -> str:
    """
    Extract the year from the URL.

    Args:
        url (str): The URL to extract the year from.

    Returns:
        str: The extracted year in yyyy format.
    """
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    range_param = query_params.get("range", [])[0]
    if range_param:
        try:
            # Extract year from the range parameter
            start_date_str = range_param.split("-")[0]
            date_obj = datetime.strptime(start_date_str, "%b%d.%Y")
            return date_obj.strftime("%Y")
        except ValueError:
            print(f"Error extracting year from URL: {url}")
            return "1900"  # Default year if extraction fails
    return "1900"  # Default year if range parameter is missing


def reformat_scraped_data(data: list, filename: str, url: str) -> pd.DataFrame:
    """
    Reformat scraped data and save it as a DataFrame and a CSV file.

    Args:
        data (list): The scraped data as a list of lists.
        filename (str): Filename for the output CSV file.
        url (str): The URL used to extract the year for date formatting.

    Returns:
        pd.DataFrame: The reformatted data as a DataFrame.
    """
    current_date = ""
    current_time = ""
    structured_rows = []

    # Extract the year from the URL
    year = extract_year_from_url(url)

    for row in data:
        if len(row) == 1 or len(row) == 5:
            match, day = contains_day_or_month(row[0])
            if match:
                current_date = row[0].replace(day, "").replace("\n", "").strip()
                # Convert date to yyyy.mm.dd format
                try:
                    date_obj = datetime.strptime(f"{current_date} {year}", "%b %d %Y")
                    current_date = date_obj.strftime("%Y.%m.%d")
                except ValueError:
                    print(f"Date formatting error: {current_date}")
                    current_date = ""
        if len(row) == 4:
            current_time = row[0]

        if len(row) == 5:
            current_time = row[1]

        if len(row) > 1:
            event = row[-1]
            impact = row[-2]
            currency = row[-3]
            structured_rows.append(
                [current_date, current_time, currency, impact, event]
            )

    df = pd.DataFrame(
        structured_rows, columns=["date", "time", "currency", "impact", "event"]
    )
    os.makedirs("news", exist_ok=True)
    df.to_csv(f"news/{filename}.csv", index=False)

    return df
