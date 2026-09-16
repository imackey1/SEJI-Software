from datetime import datetime

def interpret_metadata(metadata):
    traits = []

    # Sizes
    file_size = metadata["file_size"]

    if file_size < 1_000_000:
        traits.append("small")

    elif file_size < 100_000_000:
            traits.append("medium")

    else:
         traits.append("large")

    # File types
    file_type = metadata["file_type"].lower()
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

    # Age
    # Placeholder 
    if "created" in metadata:
        created_date = datetime.strptime(metadata["created"], "%Y-%m-%d")
        current_date = datetime.now()

        age_days = (current_date - created_date).days

        if age_days < 30:
            traits.append("new")
        elif age_days < 365:
            traits.append("fairly_old")
        else:
            traits.append("old")

    # Modification
    if "modified" in metadata:
        modified_date = datetime.strptime(metadata["modified"], "%Y-%m-%d")
        current_date = datetime.now()

        modified_days = (current_date - modified_date).days

        if modified_days < 30:
            traits.append("recently_modified")
        elif modified_days < 365:
            traits.append("modified_this_year")
        else:
            traits.append("stale")

    return traits

# Test metadata
metadata = {
    "name": "Chrome.exe",
    "file_type": ".exe",
    "file_size": 150000000,
    "created": "2022-05-10",
    "modified": "2026-09-10"
}

traits = interpret_metadata(metadata)

print("Traits:", traits)