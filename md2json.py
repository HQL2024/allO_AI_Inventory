import os
import pandas as pd
from io import StringIO


def clean_markdown_table(markdown_str):
    # Remove separator lines (lines containing at least three '-' characters)
    lines = markdown_str.split('\n')
    cleaned_lines = [line for line in lines if
                     not all(char == '-' or char == ' ' for char in line.replace('|', '').strip())]
    return '\n'.join(cleaned_lines)


def markdown_table_to_json(markdown_str, file_name, folder_path):
    # Clean up separator lines
    cleaned_markdown = clean_markdown_table(markdown_str)

    # Use pandas to read the Markdown table, and force all columns to be read as strings to prevent automatic conversion
    df = pd.read_csv(StringIO(cleaned_markdown), sep='|', skipinitialspace=True, dtype=str)

    # Remove unnecessary columns (such as index and empty columns)
    df = df.drop(df.columns[[0, -1]], axis=1)

    # Convert the DataFrame to JSON, ensuring ASCII encoding is avoided
    json_data = df.to_json(orient='records', force_ascii=False, indent=4)

    # Create the folder (if it doesn't exist)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Build the full file path
    file_path = os.path.join(folder_path, f'{file_name}.json')

    # Save the JSON data to a file using UTF-8 encoding
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(json_data)

    return json_data
