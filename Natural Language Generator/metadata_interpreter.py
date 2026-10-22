from datetime import datetime, date

# Accept metadata from dictionary or object
def get_value(metadata, *keys, default=None):
    for key in keys:
        if isinstance(metadata, dict):
            if key in metadata:
                return metadata[key]
        elif hasattr(metadata, key):
            return getattr(metadata, key)

    return default

# Convert a value to an integer without crashing
def safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError, OverflowError):
        return default

#Parse common date formats; return None if invalid
def parse_date(value):
    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    if not isinstance(value, str) or not value.strip():
        return None

    try:
        return date.fromisoformat(value.strip()[:10])
    except ValueError:
        return None

# Convert metadata to dialogue traits
def interpret_metadata(metadata):
    traits = []

    if metadata is None:
        return traits
    
    # Sizes
    file_size = safe_int(get_value(metadata, "file_size", "size_bytes", default=0))

    file_type = str(get_value(metadata, "file_type", "extension", default="") or "").lower().strip()
    if file_type and not file_type.startswith("."):
        file_type = "." + file_type

    file_name = str(get_value(metadata, "name", default="") or "").lower()

    word_count = safe_int(get_value(metadata, "word_count", default=0))

    # File Sizes
    if file_size < 1_000_000:
        traits.append("small")

    elif file_size < 100_000_000:
        traits.append("medium")

    else:
        traits.append("large")

    # File types traits
    if file_type in {".exe", ".msi", ".app"}:
        traits.extend(["application", "executable"])

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
    if get_value(metadata, "is_hidden", default=False):
        traits.append("hidden")

    if get_value(metadata, "is_system", default=False):
        traits.append("system")

    # Filename clues
    name_parts = file_name.replace("\\", "/").split("/")
    name = name_parts[-1]
    name_without_extension = name.rsplit(".", 1)[0]

    words = set(
        name_without_extension
        .replace("-", "_")
        .replace(" ", "_")
        .split("_")
    )

    # Filename-based traits
    if words.intersection({"backup", "copy", "old", "bak"}):
        traits.append("backup")

    if words.intersection({"temp", "temporary", "tmp"}):
        traits.append("temporary")

    # Creation date
    created = parse_date(get_value(metadata, "created"))

    if created:
        age_days = (date.today() - created).days

        if 0 <= age_days < 30:
            traits.append("new")

        elif 30 <= age_days < 365:
            traits.append("fairly_old")

        elif age_days >= 365:
            traits.append("old")

    # Modification date
    modified = parse_date(get_value(metadata, "modified"))

    if modified:
        modified_days = (date.today() - modified).days

        if 0 <= modified_days < 30:
            traits.append("recently_modified")

        elif 30 <= modified_days < 365:
            traits.append("modified_this_year")

        elif modified_days >= 365:
            traits.append("stale")

    return traits
