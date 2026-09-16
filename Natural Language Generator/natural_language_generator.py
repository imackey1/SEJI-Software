import random
import dialogue_library as library
import metadata_interpreter as interpreter

def generate_intro(metadata):
    traits = interpreter.interpret_metadata(metadata)

    greeting = random.choice(library.GREETINGS)
    insult = random.choice(library.INSULTS)

    trait_phrases = []

    for trait in traits:
        if trait in library.TRAIT_PHRASES:
            trait_phrases.append(
                random.choice(library.TRAIT_PHRASES[trait])
            )

    trait_phrase = random.choice(trait_phrases)
        
    return f"{greeting} {trait_phrase} You {insult}"

def generate_enemy_dialogue(metadata):
    traits = interpreter.interpret_metadata(metadata)

    dialogue_options = []

    for trait in traits:
        if trait in library.ENEMY_PHRASES:
            dialogue_options.extend(library.ENEMY_PHRASES[trait])

    if dialogue_options:
        phrase = random.choice(dialogue_options)
    else:
        phrase = "Prepare yourself."

    ending = random.choice(library.ENEMY_ENDINGS)

    return f"{phrase} {ending}" 

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
print(generate_enemy_dialogue(metadata))