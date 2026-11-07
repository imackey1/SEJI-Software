GREETINGS = [
    "Well, well, well...",
    "Oh, look who showed up.",
    "Finally.",
    "Interesting...",
    "Ah, a new challenger.",
    "You again.",
    "Yo.",
    "Oh look."
]

INSULTS = [
    "worthless file",
    "glorified shortcut",
    "walking error",
    "pile of junk",
    "useless executable",
    "pathetic program",
    "waste of space",
    "background app",
    "inferior software",
    "dust collector",
    "have negative aura"
]

ATTACKS = [
    "WALL OF TEXT!",
    "BUFFER OVERLOAD!",
    "FORCE DELETE!",
    "DATA OVERLOAD!",
    "CTRL ALT F4!",
    "RAM RUSH!",
    "FILE CRUSH!",
    "SYSTEM CRASH!",
    "PACKET STRIKE!",
    "CODE BLAST!",
    "MEMORY WIPE!",
    "DISK SLAM!",
    "PROCESS KILL!",
    "STACK OVERFLOW!",
    "FATAL ERROR!"
]

CLASS_ATTACKS = {
    "Barbarian": [
        "FILE SMASH!",
        "DISK CRUSH!",
        "RAW POWER!",
        "HARD DRIVE HAMMER!",
        "DESK SLAM!"
    ],

    "Mage": [
        "CODE CAST!",
        "STACK OVERFLOW!",
        "SCRIPT STORM!",
        "DATA SPELL!",
        "SSD OVERLOAD!",
        "CPU OVERLOAD!"
    ],

    "Rogue": [
        "QUICK ACCESS!",
        "HIDDEN FILE!",
        "SHORTCUT STRIKE!",
        "404 ATTACK!"
    ]
}

DAMAGE = [
    "HEY! WATCH IT!",
    "You actually hit me?!",
    "That all you've got?",
    "System integrity compromised!",
    "That's gonna leave a mark.",
    "I'm still standing!",
    "Ow. Seriously?",
    "ERROR: PAIN DETECTED!"
]

CLASS_DAMAGE = {
    "Barbarian": [
        "THAT'S ALL YOU GOT?!",
        "YOU'LL NEED MORE THAN THAT!",
        "I CAN TAKE IT!",
        "BARELY A SCRATCH!",
        "YOU HIT HARDER THAN I EXPECTED!"
    ],

    "Mage": [
        "MY DEFENSES ARE STILL ONLINE!",
        "SPELL INTERRUPTED!",
        "SYSTEM STABILITY: COMPROMISED!",
        "MY SHIELDS ARE FAILING!",
        "REBOOTING SHIELDS . . .",
        "THAT DISTURBED MY SPELL!"
    ],

    "Rogue": [
        "TOO CLOSE!",
        "YOU ALMOST HAD ME!",
        "NICE TRY!",
        "REGAINING STEALTH . . .",
        "WATCH WHERE YOU'RE AIMING!",
        "YOU GOT LUCKY!"
    ]
}

LOW_HEALTH = [
    "I'm not going down yet!",
    "This system is barely holding together!",
    "I need a backup!",
    "Warning: critical condition!",
    "You won't delete me that easily!",
    "I'm running out of space!",
    "This isn't looking good..."
]

CLASS_LOW_HEALTH = {
    "Barbarian": [
        "I'M NOT DONE YET!",
        "YOU'LL HAVE TO HIT HARDER!",
        "I CAN STILL FIGHT!",
        "THIS IS JUST A SCRATCH!",
        "I CAN TAKE THIS!",
        "I REFUSE TO FALL!"
    ],

    "Mage": [
        "MY MANA IS RUNNING LOW!",
        "SYSTEM CRITICAL!",
        "MY SPELLS ARE FALTERING!",
        "I NEED MORE POWER!",
        "SHIELD FAILURE!",
        "MY DEFENSES ARE COLLAPSING!"
    ],

    "Rogue": [
        "I NEED TO GET OUT OF HERE!",
        "THIS IS GETTING TOO CLOSE!",
        "TIME TO DISAPPEAR!",
        "I'M RUNNING OUT OF OPTIONS!",
        "I CAN'T TAKE ANOTHER HIT!"
    ]
}

DODGES = [
    "MISSED!",
    "TOO SLOW!",
    "NOT TODAY!",
    "NICE TRY!",
    "DODGED!",
    "ACCESS DENIED!",
    "404: HIT NOT FOUND!"
]

CLASS_DODGES = {
    "Barbarian": [
        "MISSED ME!",
        "TOO SLOW!",
        "COME CLOSER!",
        "YOU CALL THAT AN ATTACK?!",
        "TRY HITTING HARDER!"
    ],

    "Mage": [
        "SPELL DODGED!",
        "YOUR ATTACK HAS BEEN NULLIFIED!",
        "ACCESS DENIED!",
        "SHIELDS ACTIVE",
        "MAGICALLY AVOIDED!"
    ],

    "Rogue": [
        "TOO SLOW!",
        "NICE TRY!",
        "NOT TODAY!",
        "CAN'T CATCH ME!",
        "YOU CAN'T HIT WHAT YOU CAN'T CATCH!",
        "MISSED!"
    ]
}

VICTORY = [
    "K.O.!",
    "SYSTEM VICTORY!",
    "FILE DELETED!",
    "THAT'S A WRAP!",
    "YOU'VE BEEN DELETED!",
    "CRITICAL HIT!",
    "SUCCESSFUL TERMINATION!"
]

DEFEAT = [
    "SYSTEM FAILURE...",
    "FILE CORRUPTED...",
    "CONNECTION LOST...",
    "PROCESS TERMINATED.",
    "GAME OVER.",
    "REBOOTING . . .",
    "ERROR 404: FILE NOT FOUND."
]

TRAIT_PHRASES = {
    "small": [
        "Don't underestimate my size.",
        "I'm smaller than you expected.",
        "Size isn't everything."
    ],

    "medium": [
        "I'm right in the middle.",
        "I'm no small file.",
        "I'm not exactly lightweight."
    ],

    "large": [
        "I've got more data than I know what to do with.",
        "There's a reason they gave me all this space.",
        "You don't get this big by accident."
    ],

    "old": [
        "I've been here longer than you.",
        "I've seen things you wouldn't understand.",
        "Experience beats youth."
    ],

    "fairly_old": [
        "I've been around for a while.",
        "I've got some history.",
        "I'm not exactly new here."
    ],

    "new": [
        "I just got here.",
        "Fresh out of the file system.",
        "I'm new around here."
    ],

    "recently_modified": [
        "I was just updated.",
        "Freshly modified.",
        "I just got an upgrade."
    ],

    "modified_this_year": [
        "I've seen some changes recently.",
        "I've been updated this year.",
        "I'm still being worked on."
    ],

    "stale": [
        "Nobody has touched me in ages.",
        "I've been sitting here for a long time.",
        "I'm overdue for an update."
    ],

    "application": [
        "I'm a program built to get things done.",
        "I know my way around this system.",
        "I was made to run."
    ],

    "document": [
        "I've got plenty to say.",
        "Better read carefully.",
        "I've got this written down."
    ],

    "image": [
        "Picture this.",
        "You should have seen this coming.",
        "Say cheese."
    ],

    "video": [
        "This is going to be entertaining.",
        "Get ready for the playback.",
        "Let's make this worth watching."
    ],

    "archive": [
        "I've got plenty packed away.",
        "Everything I need is compressed.",
        "Good luck unpacking this."
    ],

    "script": [
        "I've got a few commands for you.",
        "Let's execute this.",
        "I've already planned my next move."
    ],

    
    "text_heavy": [
        "I've got more words than you have patience.",
        "Read carefully. There's a lot to unpack.",
        "I could write a whole book about this fight."
    ],

    "hidden": [
        "You weren't supposed to find me.",
        "I'm much harder to track than I look.",
        "Some things are better left hidden."
    ],

    "system": [
        "I operate at the core of this machine.",
        "System authority recognized.",
        "You don't have permission to challenge me."
    ],

    "executable": [
        "Double-click and watch what happens.",
        "I was built to run the show.",
        "Ready to launch."
    ],

    "backup": [
        "You thought I was gone? I've got a backup.",
        "Never underestimate a saved copy.",
        "I keep a spare version of myself."
    ],

    "temporary": [
        "I won't be here for long.",
        "Enjoy this while it lasts.",
        "Temporary file, permanent problem."
    ]

}

ENEMY_PHRASES = {
    "small": [
        "Don't underestimate me.",
        "Small doesn't mean harmless.",
        "You won't have an easy time with me."
    ],

    "medium": [
        "Let's see what you've got.",
        "You picked the wrong fight.",
        "I'm ready for you."
    ],

    "large": [
        "You really think you can take me?",
        "You're standing against something much bigger than you.",
        "You should have stayed away."
    ],

    "new": [
        "Let's see what I'm capable of.",
        "I'm new, but I'm ready.",
        "Everyone has a first fight."
    ],

    "fairly_old": [
        "I've been around for a while.",
        "I've survived this long for a reason.",
        "I've seen plenty of files like you."
    ],

    "old": [
        "I've been here longer than you.",
        "I've survived longer than most.",
        "Experience is on my side."
    ],

    "recently_modified": [
        "I'm freshly updated.",
        "I've just been changed.",
        "You caught me at my strongest."
    ],

    "modified_this_year": [
        "I've had some changes recently.",
        "I'm not the same file I used to be.",
        "I've been improved."
    ],

    "stale": [
        "I've been waiting here for a long time.",
        "Nobody has touched me in ages.",
        "Finally, something interesting."
    ],

    "application": [
        "I'm ready to execute.",
        "I'm built to run.",
        "System process initiated."
    ],

    "document": [
        "I've got plenty to say.",
        "You'll be reading about this later.",
        "Consider this another chapter."
    ],

    "image": [
        "Remember this picture.",
        "You won't forget what you see.",
        "Say cheese."
    ],

    "video": [
        "This should be worth watching.",
        "Let's make this entertaining.",
        "Roll the tape."
    ],

    "archive": [
        "I've got plenty packed away.",
        "Everything I need is stored inside.",
        "Good luck getting through me."
    ],

    "script": [
        "Executing.",
        "I've already planned my next move.",
        "You just triggered the wrong script."
    ],

    
    "text_heavy": [
        "Prepare yourself for a wall of text.",
        "I've got a thousand things to say.",
        "You'll never get through all my data."
    ],

    "hidden": [
        "You'll never see me coming.",
        "You should not have found this file.",
        "Try fighting something you can't track."
    ],

    "system": [
        "Critical system process engaged.",
        "You are challenging system authority.",
        "Access denied. Prepare for termination."
    ],

    "executable": [
        "Execution begins now.",
        "Ready to launch an attack.",
        "Initiating combat sequence."
    ],

    "backup": [
        "I always have another copy.",
        "You can't erase every version of me.",
        "I was prepared for this."
    ],

    "temporary": [
        "Let's make this short.",
        "I'm temporary, but you're still in danger.",
        "My time is limited. Yours is too."
    ]

}

ENEMY_ENDINGS = [
    "You're finished.",
    "Prepare yourself.",
    "This is your last mistake.",
    "You won't get away.",
    "Let's end this.",
    "Your luck ends here.",
    "You should have stayed away.",
    "Nowhere to run.",
    "Get ready.",
    "This won't end well for you."
]

# Metadata-based combat dialogue
# Used when no class-specific metadata line is available.

TRAIT_COMBAT_DIALOGUE = {
    "attack": {
        "large": [
            "ALL THAT DATA, ALL THAT DAMAGE!",
            "OVERWHELMING FILE SIZE!",
        ],
        "script": [
            "EXECUTING ATTACK SEQUENCE!",
            "RUNNING DAMAGE COMMAND!",
        ],
        "executable": [
            "LAUNCHING ATTACK!",
            "EXECUTION IN PROGRESS!",
        ],
        "hidden": [
            "SURPRISE ATTACK!",
            "YOU NEVER SAW THAT COMING!",
        ],
        "backup": [
            "I'VE GOT ANOTHER COPY OF THIS ATTACK!",
            "BACKUP POWER ACTIVATED!",
        ],
    },

    "damage": {
        "large": [
            "THAT BARELY MADE A DENT IN MY DATA!",
            "YOU'LL NEED MORE THAN THAT TO WIPE ME!",
        ],
        "script": [
            "ERROR! THAT WASN'T IN MY SCRIPT!",
            "INTERRUPTED, BUT STILL RUNNING!",
        ],
        "executable": [
            "MY PROCESS IS STILL RUNNING!",
            "EXECUTION NOT TERMINATED!",
        ],
        "hidden": [
            "YOU FOUND ME, BUT YOU HAVEN'T BEATEN ME!",
            "I'M STILL HIDING IN THE SYSTEM!",
        ],
        "backup": [
            "I STILL HAVE A BACKUP!",
            "YOU HAVEN'T DELETED THE ORIGINAL!",
        ],
    },

    "low_health": {
        "large": [
            "MY DATA IS RUNNING OUT!",
            "I'M LOSING TOO MUCH STORAGE!",
        ],
        "script": [
            "CRITICAL ERROR! SCRIPT FAILURE IMMINENT!",
            "MY COMMANDS ARE STARTING TO FAIL!",
        ],
        "executable": [
            "EXECUTION FAILURE IMMINENT!",
            "PROCESS STATUS: CRITICAL!",
        ],
        "hidden": [
            "I NEED TO DISAPPEAR BEFORE I'M DELETED!",
            "MY HIDING PLACE ISN'T SAFE ANYMORE!",
        ],
        "backup": [
            "I NEED TO RESTORE FROM BACKUP!",
            "THIS COPY IS ALMOST GONE!",
        ],
    },

    "dodge": {
        "large": [
            "TOO MUCH DATA FOR YOU TO HIT!",
            "YOU CAN'T HANDLE ALL THIS!",
        ],
        "script": [
            "COMMAND AVOIDED!",
            "YOUR ATTACK WAS NOT EXECUTED!",
        ],
        "executable": [
            "PROCESS MOVED OUT OF RANGE!",
            "EXECUTION DODGED!",
        ],
        "hidden": [
            "YOU CAN'T HIT WHAT YOU CAN'T FIND!",
            "VANISHED FROM YOUR SEARCH!",
        ],
        "backup": [
            "WRONG COPY!",
            "YOU HIT MY BACKUP LOCATION!",
        ],
    },
}


# Special dialogue when both the character class and metadata trait match.
# These lines take priority over the general trait dialogue above.

CLASS_TRAIT_COMBAT_DIALOGUE = {
    "Barbarian": {
        "attack": {
            "large": [
                "BIG FILE! BIGGER IMPACT!",
                "RAW DATA SMASH!",
            ],
            "backup": [
                "I'LL SMASH YOU WITH EVERY COPY!",
            ],
        },
        "damage": {
            "large": [
                "YOU CALL THAT DAMAGE?! I'M MASSIVE!",
            ],
        },
        "low_health": {
            "large": [
                "I'M STILL THE BIGGEST FILE HERE!",
            ],
        },
        "dodge": {
            "large": [
                "TOO BIG TO MISS? TOO BAD!",
            ],
        },
    },

    "Mage": {
        "attack": {
            "script": [
                "SCRIPT STORM!",
                "STACK OVERFLOW BLAST!",
            ],
            "executable": [
                "EXECUTE: DESTRUCTION!",
            ],
        },
        "damage": {
            "script": [
                "MY CODE IS STILL INTACT!",
            ],
        },
        "low_health": {
            "script": [
                "SYSTEM WARNING! MANA DEPLETED!",
            ],
        },
        "dodge": {
            "script": [
                "YOUR ATTACK FAILED TO COMPILE!",
            ],
        },
    },

    "Rogue": {
        "attack": {
            "hidden": [
                "SILENT FILE STRIKE!",
                "HIDDEN ACCESS ATTACK!",
            ],
            "backup": [
                "YOU'RE FIGHTING THE WRONG COPY!",
            ],
        },
        "damage": {
            "hidden": [
                "YOU'LL NEVER CATCH MY REAL LOCATION!",
            ],
        },
        "low_health": {
            "hidden": [
                "TIME TO DISAPPEAR INTO THE FILE SYSTEM!",
            ],
        },
        "dodge": {
            "hidden": [
                "YOU CAN'T HIT A HIDDEN FILE!",
            ],
        },
    },
}