from datetime import datetime, date

def interpret_metadata(metadata):
    traits = []

    # Accept dictionary or FileRecord
    def get_value(*keys, default=None):
        for key in keys:
            # Handle dictionaries
            if isinstance(metadata, dict) and key in metadata:
                return metadata[key]

            # Handle objects such as FileRecord
            if hasattr(metadata, key):
                return getattr(metadata, key)

        return default
    # Sizes
    
    file_size = get_value("file_size", "size_bytes", default=0)
    file_type = str(get_value("file_type", "extension", default="")).lower()

    file_name = str(get_value("name", default="") or "").lower()
    word_count = int(get_value("word_count", default=0) or 0)

    # File Sizes
    if file_size < 1_000_000:
        traits.append("small")

    elif file_size < 100_000_000:
            traits.append("medium")

    else:
         traits.append("large")

    # File types traits
    if file_type in {".exe", ".msi", ".app"}:
        traits.append("application")
        traits.append("executable")

    elif file_type in {".txt", ".doc", ".docx", ".rtf", ".pdf", ".md"}:
        traits.append("document")

    elif file_type in {".jpg", ".jpeg", ".png", ".gif", ".svg", ".psd", ".webp"}:
        traits.append("image")

    elif file_type in {".mp4", ".mov", ".avi", ".mkv"}:
        traits.append("video")

    elif file_type in {".zip", ".rar", ".7z", ".iso"}:
        traits.append("archive")

    elif file_type in {".py", ".js", ".java", ".cpp", ".bat", ".ps1", ".sh"}:
        traits.append("script")

    # Text Density
    if word_count >= 1000:
        traits.append("text_heavy")

    # Hidden and system status
    if get_value("is_hidden", default=False):
        traits.append("hidden")

    if get_value("is_system", default=False):
        traits.append("system")

    # Filename-based traits
    if any(word in file_name for word in ("backup", "copy", "old")):
        traits.append("backup")

    if any(word in file_name for word in ("temp", "temporary")):
        traits.append("temporary")

    # Age
    created = get_value("created")
    if created:
        created_date = parse_date(created)
        age_days = (date.today() - created_date).days

        if age_days < 30:
            traits.append("new")
        elif age_days < 365:
            traits.append("fairly_old")
        else:
            traits.append("old")

    # Modification
    modified = get_value("modified")

    if modified:
        modified_date = parse_date(modified)
        modified_days = (date.today() - modified_date).days

        if modified_days < 30:
            traits.append("recently_modified")
        elif modified_days < 365:
            traits.append("modified_this_year")
        else:
            traits.append("stale")

    return traits

def parse_date(value):
    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    return datetime.strptime(str(value)[:10], "%Y-%m-%d").date()
