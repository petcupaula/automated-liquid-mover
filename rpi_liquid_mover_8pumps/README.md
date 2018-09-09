# Operating Procedures

## Ordering a drink

### Interfaces

* Google Assistant on Google Home
* Amazon Alexa on Echo
* Web interface?
* App?
* By connecting directly to the Raspberry Pi

### Logic

* The drink recipes are defined in `drinks.json`
    * It should be possible to easily update the list of known drink recipes (TO-DO: to be updated by who and what is the process of updating? what means to easily update? github pull request? edit in an interface? on the fly provide receipt? where should the file be stored)
    * The recipes should define how many parts of each liquid is required
* The mapping of which liquids are available at each pump is defined in `pumps.json`
    * The mapping should be easy to update from an interface (TO-DO: do we support this over voice as well, or through a web interface/app only?)
    * The flow does not appear to be different between liquids tested so fat, but if there are any major differences (for example: flow of vodka vs tomato juice) then we need to provide a way of defining this flow and using the value in preparing the drinks
* A menu is created (`menu.json`) based on known recipes and available liquids. The menu defines what drinks can be made.
    * This menu should be displayed in an interface (TO-DO: if web interface/app, add images for each drink)
    * If the ingredients for the drink are not currently available, a drink will not be made, and the user must be informed (TO-DO: how to handle this for voice assistants? create interface for web/app)
    * If all ingredients are available, start making the drink
    * If the requested drink is not on the list (can happen if from voice assistant), then fail gracefully. Option A: Inform user that the drink is not on the menu. Option B: Ask for recipe to see if it can be prepared, and save the recipe to the database of drink recipes (TO-DO: how to implement this conversation, and if database needs to be updated, then it means the Rpi should also have write access to the recipes file)
    * The quantity of the drink overall should be adjustable (defaults to 200 ml) (TO-DO: interfaces must support this option)
    * It should be possible for the user to create their own mix from existing recipe or from scratch, and to save this recipe in the recipe database

## Changing the connection of a pump with a different container

* Put the tube into cleaning container with water (maybe hot water even, or with bleach)
* Put a cup into the machine to collect the water with drink residues from the tube
* Run the `CLEAN [PUMP#]` procedure (maybe even several times until the water comes out clean) to clean the tube from the previous drink
* Put the tube into the new drink container 
* Run the `PREPARE [PUMP#]` procedure (maybe even several times until the liquid is visible throughout the length of the tube) to move the liquid from the new container through the tube, and push out any air, so it is ready for the next drink

## Cleaning procedure

* Prepare a cleaning container with water (maybe hot water even, or with bleach?)
* Take all tubes out of the containers and put them into the cleaning container
* Put a cup into the machine to collect the water with drink residues from the tubes
* Run the `CLEAN ALL` procedure (maybe even several times until the water comes out clean)
* Take all the tubes out of the cleaning container
* Run the `CLEAN ALL` procedure one more time, in order to move the water through the tubes and fill it with air instead so that we don't end up with storing water in the tubes

## Connectivity

* TO-DO: If we want to provide the flexibility of the machine being transportable, then we need to define how it will connect to the internet. Example of remembering multiple wifi connections: https://www.thepolyglotdeveloper.com/2016/08/connect-multiple-wireless-networks-raspberry-pi/ 
* TO-DO: Should the machine be able to operate offline, and what are the implications?