#!/usr/bin/env python3
"""
Script to scrape population tables from Azerbaijan President's website
and save each table as a separate CSV file.
"""

import requests
from bs4 import BeautifulSoup
import csv
import os
from typing import List, Tuple


def fetch_page(url: str) -> str:
    """Fetch the HTML content from the given URL."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def extract_tables(html_content: str) -> List[Tuple[BeautifulSoup, int]]:
    """Extract all tables from the HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table')
    return [(table, idx) for idx, table in enumerate(tables, 1)]


def table_to_csv(table: BeautifulSoup, filename: str) -> None:
    """Convert an HTML table to CSV and save it."""
    rows = []

    # Extract all rows from the table
    for row in table.find_all('tr'):
        cells = []
        # Get both th and td cells
        for cell in row.find_all(['th', 'td']):
            # Get text and clean it
            text = cell.get_text(strip=True)
            # Handle colspan and rowspan if needed
            colspan = int(cell.get('colspan', 1))
            cells.extend([text] * colspan)

        if cells:  # Only add non-empty rows
            rows.append(cells)

    # Ensure all rows have the same number of columns
    if rows:
        max_cols = max(len(row) for row in rows)
        for row in rows:
            while len(row) < max_cols:
                row.append('')

    # Write to CSV
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"Saved {filename} ({len(rows)} rows, {max_cols if rows else 0} columns)")


def get_table_name(table: BeautifulSoup, index: int) -> str:
    """Try to determine a meaningful name for the table."""
    # Look for caption
    caption = table.find('caption')
    if caption:
        return caption.get_text(strip=True)

    # Look for a heading before the table
    prev_elem = table.find_previous(['h1', 'h2', 'h3', 'h4', 'h5'])
    if prev_elem:
        text = prev_elem.get_text(strip=True)
        if text and len(text) < 100:  # Reasonable length for a heading
            return text

    return f"table_{index}"


def sanitize_filename(name: str) -> str:
    """Sanitize the table name to be a valid filename."""
    # Remove or replace invalid filename characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')

    # Limit length
    if len(name) > 100:
        name = name[:100]

    # Replace spaces with underscores
    name = name.replace(' ', '_')

    return name


def main():
    """Main function to scrape tables and save as CSV files."""
    url = "https://president.az/az/pages/view/azerbaijan/population"

    print(f"Fetching page: {url}")
    html_content = fetch_page(url)

    print("Extracting tables...")
    tables = extract_tables(html_content)

    if not tables:
        print("No tables found on the page!")
        return

    print(f"Found {len(tables)} table(s)")

    # Create output directory if it doesn't exist
    output_dir = "population_tables"
    os.makedirs(output_dir, exist_ok=True)

    # Process each table
    for table, index in tables:
        table_name = get_table_name(table, index)
        safe_name = sanitize_filename(table_name)
        # Always include index to ensure unique filenames
        filename = os.path.join(output_dir, f"table_{index}_{safe_name}.csv")

        print(f"\nProcessing Table {index}: {table_name}")
        table_to_csv(table, filename)

    print(f"\nAll tables saved to '{output_dir}/' directory")


if __name__ == "__main__":
    main()
