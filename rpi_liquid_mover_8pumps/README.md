# Mixomator9000

## Installation

```
pip3 install adafruit-io
pip3 install firebase-admin

cd /home/paula/automated-liquid-mover/rpi_liquid_mover_8pumps
```

## Config

Adafruit IO config:

```
cp AIOconfig_template.py AIOconfig.py
nano AIOconfig.py
# Add your AIO user and key and save file
```

Firebase config:

```
# Go to your firebase console and generate a service account for your project 
# Docs: https://firebase.google.com/docs/admin/setup#add_firebase_to_your_app
# Download the JSON file and save it in the file `serviceaccount.json` on the server

```

## Running at startup

```
sudo cp drinks.service /etc/system/drinks.service
systemctl enable drinks.service
```

## Running manually

```
python3 drinks_aio.py
```

## Users, working directory and permissions

User (root access):
```
paula
```

Working directory:
```
/home/paula/automated-liquid-mover/rpi_liquid_mover_8pumps
```

Ensure:
```
chmod +x drinks_aio.py
chmod 666 bartender.log
```

## Operating Procedures

## Ordering a drink

### Interfaces

* Web interface (using Firebase)
* App (using Firebase)
* Google Assistant on Google Home
* Amazon Alexa on Echo
* By SSH-ing into the Raspberry Pi

### Logic

* The drink recipes are defined in the `drinks` collection in Firebase
    * It is possible to update the list of known drink recipes through the web app
    * The recipes define how many parts of each liquid is required
* The mapping of which liquids are available at each pump is defined in the `pumps` collection in Firebase
    * The mapping can be updated from the web interface
    * TO-DO: Should this be supported over voice as well?
    * NOTE: The flow does not appear to be different between liquids tested so far, but if there are any major differences (for example: flow of vodka vs tomato juice) then we need to provide a way of defining this flow and using the value in preparing the drinks
* A menu is created based on known recipes and available liquids in Firebase. 
    * The menu defines what drinks can be made and is visible in the web interface. TO-DO: add images for each drink
    * If the ingredients for the drink are not currently available, a drink will not be made, and the user must be informed (TO-DO: how to handle this for voice assistants? create interface for web/app)
    * If all ingredients are available, start making the drink
    * TO-DO: If the requested drink is not on the list (can happen if from voice assistant), then fail gracefully. Option A: Inform user that the drink is not on the menu. Option B: Ask for recipe to see if it can be prepared, and save the recipe to the database of drink recipes (TO-DO: how to implement this conversation)
    * TO-DO: The quantity of the drink overall should be adjustable (defaults to 200 ml) (TO-DO: interfaces must support this option)
    * TO-DO: It should be possible for the user to create their own mix from existing recipe or from scratch, and to save this recipe in the recipe database

## Changing the connection of a pump with a different container

* Put the tube into cleaning container with water (maybe hot water even, or with bleach)
* Put a cup into the machine to collect the water with drink residues from the tube
* Order the `clean` procedure (maybe even several times until the water comes out clean) to clean the tube from the previous drink
* Put the tube into the new drink container 

## Cleaning procedure

* Prepare a cleaning container with water (maybe hot water even, or with bleach)
* Take all tubes out of the containers and put them into the cleaning container
* Put a cup into the machine to collect the water with drink residues from the tubes
* Order the `clean` procedure (maybe even several times until the water comes out clean)
* Take all the tubes out of the cleaning container
* Order the `CLEAN ALL` procedure one more time, in order to move the water through the tubes and fill it with air instead so that we don't end up with storing water in the tubes

## Lifecycle

* TO-DO: If we want to provide the flexibility of the machine being transportable, then we need to define how it will connect to the internet. Example of remembering multiple wifi connections: https://www.thepolyglotdeveloper.com/2016/08/connect-multiple-wireless-networks-raspberry-pi/ 
* TO-DO: Should the machine be able to operate offline, and what are the implications?
