# blum-crypto-bot-and-test-game
Contains a remake of the Blum crypto game in pygames and a couple of different bots that take different approaches to play the game, this ranges from the use of computer vision and image recognition models, to simple pixel camparison algoeithms.
The files are jumbled, but the game file is test.py, as for the rest, i wish you goodluck in finding the bot capabilities.
Any and all changes or suggestions are welcome.
[Bomb Avoidance Game 15_06_2024 00_18_04](https://github.com/VenoeAI/blum-crypto-bot-and-test-game/assets/117848928/77e52e7e-575d-4b01-908e-8e78a86170f3)

# NOTE
You will need a very good pc to be able to use any of the bots without lag, timeout have been added on the bots to avoid cases of the bot running forever when the windows key 'Q' does not succcesfully quit the program. 

# INFO
* get_screen_region.py; some of the bots would ask you to provide an area of the screen that they can act on. this program helps for you to easily click and drag the portion of the screen you want to capture and get the data that you can then use.
* test.py; this is the actual game file, created with pygames. adjust speed in the code if you want to increase game speed. can be used to test the tracking capabilities of the AI model.
* best.pt; this is the computer vision AI model file, it is a YOLOv8 model, you are welcome to continue training the model as I built it to only detect the bombs. Why this was done was to make the mouse perform random clicks while avoiding the bomb. This makes sure that the mouse makes random clicks which would make it undetectable, clicks the Blums while avoiding the bombs.
