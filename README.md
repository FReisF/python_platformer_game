# Python-Platformer

* This game is developed in pygame. All assets comes from the original python-platformer game.
* Phase 1 and 2 are based on the original and are self contained scripts. All classes and functions are contained in the scripts.
* Phase 3 script is modular. All classes and functions are set on "classes" folder and the phase 3 gathers all configuration for the phase 3 of the game (positions of the objects, enemies, traps etc) from the file ".classes/p3_variables.py" so to modify the phase 3 it is necessary to modify p3_variables only.
* Phase 4 script is pretty much the same is Phase 3. The Difference in Phase 4 is that the positions were all suggested using Google Gemini Pro 1.5. The configuration of the objects is slightly odd but still look like a platformer game. All scripts were uploaded to the prompt and the following prompt text was used:

  Those files belong to a game being developed in python with the pygame library. The "phase_3.py" has a code for starting the game. All the objects in this archive are built based on the configuration of "p3_variables.py". Could you build a "phase_4.py" and a "p4_variables.py" with a new game phase based on the scripts I have. 


*Feel free to create new phases based on the modular examples in Phase 3 and Phase 4. I am aware that the definitions of positions are not so clear (Gen AI understand it well enough seems so)
