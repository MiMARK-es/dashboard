import os
from datetime import datetime
import shutil

def handle_upload(file, area, upload_folder):
    """Save uploaded files and create a backup if needed."""
    area_path = os.path.join(upload_folder, area)
    os.makedirs(area_path, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filepath = os.path.join(area_path, file.name)

    # Create backup if file already exists
    if os.path.exists(filepath):
        backup_folder = f"/var/data/backups/{area}"
        os.makedirs(backup_folder, exist_ok=True)
        backup_path = os.path.join(backup_folder, f"{file.name}_{timestamp}")
        shutil.move(filepath, backup_path)

    # Save new file
    with open(filepath, "wb") as f:
        f.write(file.getbuffer())

def get_last_upload_info(area, upload_folder):
    """Return the last upload info for an area."""
    area_path = os.path.join(upload_folder, area)
    if not os.path.exists(area_path):
        return None

    files = [(file, os.path.getmtime(os.path.join(area_path, file))) for file in os.listdir(area_path)]
    if not files:
        return None

    latest_file = max(files, key=lambda x: x[1])
    timestamp = datetime.fromtimestamp(latest_file[1]).strftime("%Y-%m-%d %H:%M:%S")
    return {"filename": latest_file[0], "timestamp": timestamp}

def is_valid_format(file, valid_formats):
    """Check if the file format is valid."""
    return any(file.name.endswith(fmt) for fmt in valid_formats)
