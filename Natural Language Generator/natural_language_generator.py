import random
import dialogue_library as library
import metadata_interpreter as interpreter

def generate_intro(metadata):
    traits = interpreter.interpret_metadata(metadata)

    greeting = random.choice(library.GREETINGS)
    insult = random.choice(library.INSULTS)

    trait_phrase = ""

    for trait in traits:
        if trait in library.TRAIT_PHRASES:
            trait_phrase = random.choice(library.TRAIT_PHRASES[trait])
            break

    return f"{greeting} {trait_phrase} You {insult}"


#test metadata
metadata = {
    "name": "Chrome.exe",
    "file_type": ".exe",
    "file_size": 150000000,
    "created": "2022-05-10",
    "modified": "2026-09-10"
}

#test function
print(generate_intro(metadata))