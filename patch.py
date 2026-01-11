"""
Class to validate and update current patch information
"""

import requests
import os
from PIL import Image
from urllib.request import urlopen

class Patch_Data:
    def __init__(self):

        """Initialise recent patch data
        Gets the current patch and list of champions
        Download any necessary icons
        """
        self.LOG_PREFIX = "Patch:"
        
        current_patch = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]
        self.CURRENT_PATCH = current_patch
        
        champion_data = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{current_patch}/data/en_US/champion.json").json()
        champions = {champion for champion in champion_data["data"].keys()}
        self.CHAMPIONS = champions
        
        self.validate_icons()
        
    
    def download_icon(self, champion: str):
        """Downloads and saves champion icon"""
        
        image_url = f"http://ddragon.leagueoflegends.com/cdn/{self.CURRENT_PATCH}/img/champion/{champion}.png"
        image = Image.open(urlopen(image_url))
        image.save(f"./icons/{champion}.png")
    
    
    def validate_icons(self):
        """Check currently downloaded icons with list of champions"""
        
        current_icons = set(os.listdir("icons"))
        # append .png
        current_icons = {icon[:-4] for icon in current_icons}
        difference = self.CHAMPIONS - current_icons
        print(f"{self.LOG_PREFIX} Found {len(difference)} missing champion icons")
        
        if not difference:
            print(f"{self.LOG_PREFIX} Icons up to date")
        else:
            print(f"{self.LOG_PREFIX} Downloading icons...")
            counter = 1
            for champion in difference:
                print(f"Icon Download: {champion} ({counter}/{len(difference)} {round(counter*100/len(difference),2)}%)")
                self.download_icon(champion)
                counter += 1
            print(f"\n{self.LOG_PREFIX} Downloading Complete")