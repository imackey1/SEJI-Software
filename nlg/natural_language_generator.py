import random

from . import dialogue_library as library
from . import dialogue_situations as situations
from . import metadata_interpreter as interpreter


def _class_name(character_class):
    # Accept "Mage" or classes_loot_equipment.FighterClass.MAGE - both mean the same thing.
    return getattr(character_class, "value", character_class)


def generate_dialogue(metadata, situation, character_class = None):
    character_class = _class_name(character_class)

    if situation == situations.INTRO:
        return generate_intro(metadata)

    elif situation == situations.ENEMY_INTRO:
        return generate_enemy_dialogue(metadata)
    
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
    character_class = _class_name(character_class)
    if character_class in library.CLASS_ATTACKS:
        return random.choice(library.CLASS_ATTACKS[character_class])

    return random.choice(library.ATTACKS)

def generate_damage_dialogue(character_class = None):
    character_class = _class_name(character_class)
    if character_class in library.CLASS_DAMAGE:
        return random.choice(library.CLASS_DAMAGE[character_class])

    return random.choice(library.DAMAGE)

def generate_low_health_dialogue(character_class = None):
    character_class = _class_name(character_class)
    if character_class in library.CLASS_LOW_HEALTH:
        return random.choice(library.CLASS_LOW_HEALTH[character_class])

    return random.choice(library.LOW_HEALTH)

def generate_dodge_dialogue(character_class = None):
    character_class = _class_name(character_class)
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

    if trait_phrases:
        trait_phrase = random.choice(trait_phrases)
    else:
        trait_phrase = "I'm full of surprises."

    return f"{greeting} {trait_phrase} You're a {insult}"

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
