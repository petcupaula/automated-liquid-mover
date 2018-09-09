#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import json
import logging

# Assuming for now that the flow rate is the same for all pumps and liquids
FLOW_RATE = 60.0/100.0

# Number of seconds dedicated to cleaning each pump
CLEAN_TIME = 20

# Logging
LOG_LEVEL = logging.INFO
LOG_FILE = "bartender.log"
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"

class Bartender(): 

    drinks = {}
    pumps = {}
    menu = {}
    
    #################################
    #  SETUP
    #################################

    # Create a menu of available drinks
    def createMenu(self, drinks, availIngredients):
        for drink in drinks.keys():
            # Build the recipe from the pins corresponding to the ingredient and the ml to use
            recipe = {}
            for ing in drinks[drink]['ingredients'].keys():
                if ing in availIngredients:
                    pin = availIngredients[ing]
                    ml = drinks[drink]['ingredients'][ing]
                    recipe[pin] = ml
                else:
                    break
            # Ensure that all ingredients are available, and only then put the drink with its recipe on the menu
            if len(recipe) == len(drinks[drink]['ingredients']):
                self.menu[drink] = {'ingredients': drinks[drink]['ingredients'], 'recipe': recipe}
        # Save menu to JSON file
        with open('data/menu.json', 'w') as outfile:
            json.dump(self.menu, outfile, indent = 4)

    def setup(self):
        GPIO.setmode(GPIO.BCM)

        logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)

        # Load pump configuration from file
        self.pumps = json.load(open('data/pumps.json'))

        # Loop through pins and set mode and state to 'low'
        for pump in self.pumps.keys():
            print("Configuring pin", str(self.pumps[pump]["pin"]))
            GPIO.setup(self.pumps[pump]["pin"], GPIO.OUT, initial=GPIO.HIGH)
        
        # Make a dict of available ingredients and the corresponding pin
        ingredients = {}
        for p in self.pumps.values():
            if p['value']: 
                ingredients[p['value']] = p['pin']

        # Load drinks
        self.drinks = json.load(open('data/drinks.json'))

        # Create a menu
        self.createMenu(self.drinks, ingredients)


    #################################
    #  DRINK MIXING
    #################################

    def pour(self, pin, pourTime):
        GPIO.output(pin, GPIO.LOW)
        time.sleep(pourTime)
        GPIO.output(pin, GPIO.HIGH) 

    def makeDrink(self, drink):
        # Ensure drink is on the menu
        if drink not in self.menu:
            if drink in self.drinks:
                print("Cannot prepare drink. Not on the menu today.")
                logging.info("Cannot prepare drink. Not on the menu today. Drink: "+drink)
            else:
                print("Cannot prepare drink. Don't know the recipe.")
                logging.info("Cannot prepare drink. Don't know the recipe. Drink: "+drink)
            return
        # Prepare drink
        recipe = self.menu[drink]['recipe']
        print("Preparing your drink")
        logging.info("Drink preparation started: "+drink)
        for step in recipe.keys():
            pin = step
            ml = recipe[step]
            pourTime = ml * FLOW_RATE
            print("Pouring for", pourTime)
            self.pour(pin, pourTime)
        print("Finished preparing drink. Enjoy!")
        logging.info("Drink preparation finished")
        return


    def clean(self):
        print("Starting to clean pumps one by one")
        logging.info("Cleaning started")
        for pump in self.pumps.keys():
            print("Cleaning", pump)
            self.pour(self.pumps[pump]["pin"], CLEAN_TIME)
        logging.info("Cleaning finished")


    def __init__(self):
        self.setup()

#bartender = Bartender()
#bartender.makeDrink('Fruit Mix')
#bartender.clean()