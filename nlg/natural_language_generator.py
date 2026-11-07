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
        return _generate_combat_dialogue(
            metadata, situations.ATTACK, character_class
        )

    elif situation == situations.DAMAGE:
        return _generate_combat_dialogue(
            metadata, situations.DAMAGE, character_class
        )

    elif situation == situations.LOW_HEALTH:
        return _generate_combat_dialogue(
            metadata, situations.LOW_HEALTH, character_class
        )

    elif situation == situations.DODGE:
        return _generate_combat_dialogue(
            metadata, situations.DODGE, character_class
        )
    
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

def _generate_combat_dialogue(metadata, situation, character_class=None):
    character_class = _class_name(character_class)
    traits = interpreter.interpret_metadata(metadata)

    # First priority: class + metadata trait combination.
    class_dialogue = library.CLASS_TRAIT_COMBAT_DIALOGUE.get(
        character_class, {}
    ).get(situation, {})

    for trait in traits:
        if trait in class_dialogue:
            return random.choice(class_dialogue[trait])

    # Second priority: metadata trait dialogue.
    trait_dialogue = library.TRAIT_COMBAT_DIALOGUE.get(situation, {})

    for trait in traits:
        if trait in trait_dialogue:
            return random.choice(trait_dialogue[trait])

    # Third priority: existing class-specific dialogue.
    class_dialogue_fallbacks = {
        situations.ATTACK: library.CLASS_ATTACKS,
        situations.DAMAGE: library.CLASS_DAMAGE,
        situations.LOW_HEALTH: library.CLASS_LOW_HEALTH,
        situations.DODGE: library.CLASS_DODGES,
    }

    generic_fallbacks = {
        situations.ATTACK: library.ATTACKS,
        situations.DAMAGE: library.DAMAGE,
        situations.LOW_HEALTH: library.LOW_HEALTH,
        situations.DODGE: library.DODGES,
    }

    class_lines = class_dialogue_fallbacks[situation]

    if character_class in class_lines:
        return random.choice(class_lines[character_class])

    # Final priority: existing generic dialogue.
    return random.choice(generic_fallbacks[situation])