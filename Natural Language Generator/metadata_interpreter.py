


def interpret_metadata(metadata):
    traits = []

    if metadata["file_size"] > 100_000_000:
        traits.append("large")

    if metadata["file_type"] == ".exe":
        traits.append("application")

    return traits