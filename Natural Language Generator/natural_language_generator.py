import random
import dialogue_library as library

#test metadata
metadata = {
    "name": "Chrome.exe",
    "file_type": ".exe",
    "file_size": 150000000
}

def generate_intro(metadata):
    greeting = random.choice(library.GREETINGS)
    insult = random.choice(library.INSULTS)

    return f"{greeting} You {insult}"

#test function
print(generate_intro(metadata))