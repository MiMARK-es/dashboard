import os
import pandas as pd
import shutil
from datetime import datetime
from utils.config import UPLOAD_FOLDER

def handle_upload(file, area, expected_file):
    """Save uploaded files and create a backup if needed."""
    area_path = os.path.join(UPLOAD_FOLDER, area)
    os.makedirs(area_path, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Determine the correct extension based on the uploaded file type
    if file.name.endswith('.csv'):
        extension = 'csv'
    elif file.name.endswith('.xlsx'):
        extension = 'xlsx'
    else:
        raise ValueError("Unsupported file format")

    # Save the file with the expected name and correct extension
    filepath = os.path.join(area_path, f"{expected_file}.{extension}")

    # Create backup if file already exists
    if os.path.exists(filepath):
        backup_folder = os.path.join("/tmp/backups", area)
        os.makedirs(backup_folder, exist_ok=True)
        backup_path = os.path.join(backup_folder, f"{expected_file}_{timestamp}.{extension}")
        shutil.move(filepath, backup_path)
        print(f"Moved existing file to backup: {backup_path}")

    # Save new file
    with open(filepath, "wb") as f:
        f.write(file.getbuffer())
    print(f"Saved new file as: {filepath}")

def get_last_upload_info(area, expected_filename):
    """Return the last upload info for a specific expected file in an area."""
    area_path = os.path.join(UPLOAD_FOLDER, area)
    if not os.path.exists(area_path):
        return None

    # Filter files in the area folder that match the expected filename
    files = [(file, os.path.getmtime(os.path.join(area_path, file))) 
             for file in os.listdir(area_path) if expected_filename in file]

    if not files:
        return None

    # Find the latest file based on the modification time
    latest_file = max(files, key=lambda x: x[1])
    timestamp = datetime.fromtimestamp(latest_file[1]).strftime("%Y-%m-%d %H:%M:%S")
    return {"filename": latest_file[0], "timestamp": timestamp}

import pandas as pd

def validate_file_format(file, expected_filename, area, areas_config):
    """Validate the structure of the uploaded file based on its name and the area."""
    # Get the expected columns for the file
    if area not in areas_config or expected_filename not in areas_config[area]:
        return False  # No validation rules defined for this file
    
    expected_columns = areas_config[area][expected_filename]

    try:
        # Check if the file is CSV or Excel and load it accordingly
        if file.name.endswith('.csv'):
            # Attempt to read with common delimiters: ',' and ';'
            try:
                df = pd.read_csv(file)  # Default is ','
            except pd.errors.ParserError:
                try:
                    df = pd.read_csv(file, delimiter=';')  # Try with ';' as delimiter
                except pd.errors.ParserError as e:
                    print(f"ParserError reading CSV file with both ',' and ';' delimiters: {e}")
                    return False  # Unable to parse with either delimiter
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
        else:
            return False  # Unsupported format

        # Validate columns
        if all(column in df.columns for column in expected_columns):
            return True
        else:
            return False
    except Exception as e:
        print(f"Error reading file: {e}")
        return False

