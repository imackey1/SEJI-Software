from datetime import datetime
from pathlib import Path

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


    if file_size < 1_000_000:
        traits.append("small")

    elif file_size < 100_000_000:
            traits.append("medium")

    else:
         traits.append("large")

    # File types traits
    if file_type == ".exe":
        traits.append("application")

    elif file_type in [".txt", ".docx", ".rtf", ".pdf"]:
        traits.append("document")

    elif file_type in [".jpg", ".jpeg", ".png", ".gif", ".svg", ".psd"]:
        traits.append("image")

    elif file_type in [".mp4", ".mov", ".avi", ".mkv"]:
        traits.append("video")

    elif file_type in [".zip", ".rar", ".7z", ".iso"]:
        traits.append("archive")

    elif file_type in [".py", ".js", ".java", ".cpp", ".bat", ".ps1"]:
        traits.append("script")

    created = get_value("created")
    modified = get_value("modified")

    # Age
    if created:
        if isinstance(created, datetime):
            created_date = created
        else:
            created_date = datetime.strptime(str(created), "%Y-%m-%d")

        age_days = (datetime.now() - created_date).days

        if age_days < 30:
            traits.append("new")
        elif age_days < 365:
            traits.append("fairly_old")
        else:
            traits.append("old")

    # Modification
    if modified:
        if isinstance(modified, datetime):
            modified_date = modified
        else:
            modified_date = datetime.strptime(str(modified), "%Y-%m-%d")

        modified_days = (datetime.now() - modified_date).days

        if modified_days < 30:
            traits.append("recently_modified")
        elif modified_days < 365:
            traits.append("modified_this_year")
        else:
            traits.append("stale")

    return traits

# Test metadata
from types import SimpleNamespace

# Existing NLG dictionary format
test_dict = {
    "name": "Chrome.exe",
    "file_type": ".exe",
    "file_size": 150_000_000,
    "created": "2022-05-10",
    "modified": "2026-09-10"
}

# Shape of the metadata reader's FileRecord
test_record = SimpleNamespace(
    name="Chrome.exe",
    extension=".exe",
    size_bytes=150_000_000,
    is_hidden=False,
    is_system=False,
    word_count=500
)

print("Dictionary traits:", interpret_metadata(test_dict))
print("FileRecord traits:", interpret_metadata(test_record))