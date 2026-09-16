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
         traits.append("has_creation_date")

    # Modification
    if "modified" in metadata:
         traits.append("has_modified_date")

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