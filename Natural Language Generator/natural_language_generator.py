import random
import dialogue_library as library
import dialogue_situations as situations
import metadata_interpreter as interpreter

def generate_dialogue(metadata, situation, character_class = None):
    if situation == situations.INTRO:
        return generate_intro(metadata)
    
    elif situation == situations.ATTACK:
        return generate_attack_dialogue(character_class)

    elif situation == situations.DAMAGE:
        return generate_damage_dialogue(character_class)

    elif situation == situations.LOW_HEALTH:
        return generate_low_health_dialogue(character_class)

    elif situation == situations.DODGE:
        return generate_dodge_dialogue(character_class)
    
    elif situation == situations.VICTORY:
        return random.choice(library.VICTORY)

    elif situation == situations.DEFEAT:
        return random.choice(library.DEFEAT)

    else:
        return "Prepare yourself."

def generate_attack_dialogue(character_class = None):
    if character_class in library.CLASS_ATTACKS:
        return random.choice(library.CLASS_ATTACKS[character_class])

    return random.choice(library.ATTACKS)

def generate_damage_dialogue(character_class = None):
    if character_class in library.CLASS_DAMAGE:
        return random.choice(library.CLASS_DAMAGE[character_class])

    return random.choice(library.DAMAGE)

def generate_low_health_dialogue(character_class = None):
    if character_class in library.CLASS_LOW_HEALTH:
        return random.choice(library.CLASS_LOW_HEALTH[character_class])

    return random.choice(library.LOW_HEALTH)

def generate_dodge_dialogue(character_class = None):
    if character_class in library.CLASS_DODGES:
        return random.choice(library.CLASS_DODGES[character_class])

    return random.choice(library.DODGES)

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
if __name__ == "__main__":
    print(generate_intro(metadata))
    print(generate_enemy_dialogue(metadata))
    print()
    
    print(generate_dialogue(metadata, situations.ATTACK))
    print(generate_dialogue(metadata, situations.ATTACK, "Barbarian"))
    print(generate_dialogue(metadata, situations.ATTACK, "Mage"))
    print(generate_dialogue(metadata, situations.ATTACK, "Rogue"))
    print()

    print(generate_dialogue(metadata, situations.DAMAGE))
    print(generate_dialogue(metadata, situations.DAMAGE, "Barbarian"))
    print(generate_dialogue(metadata, situations.DAMAGE, "Mage"))
    print(generate_dialogue(metadata, situations.DAMAGE, "Rogue"))
    print()

    print(generate_dialogue(metadata, situations.LOW_HEALTH))
    print(generate_dialogue(metadata, situations.LOW_HEALTH, "Barbarian"))
    print(generate_dialogue(metadata, situations.LOW_HEALTH, "Mage"))
    print(generate_dialogue(metadata, situations.LOW_HEALTH, "Rogue"))
    print()

    print(generate_dialogue(metadata, situations.DODGE))
    print(generate_dialogue(metadata, situations.DODGE, "Barbarian"))
    print(generate_dialogue(metadata, situations.DODGE, "Mage"))
    print(generate_dialogue(metadata, situations.DODGE, "Rogue"))
    print()

    print(generate_dialogue(metadata, situations.VICTORY))
    print(generate_dialogue(metadata, situations.DEFEAT))
