def is_valid_format(file, valid_formats):
    """Check if the file format is valid."""
    return any(file.name.endswith(fmt) for fmt in valid_formats)
