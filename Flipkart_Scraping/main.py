import os
import sys

cwd = os.getcwd()
sys.path.append(os.path.join(cwd))

from Cameras.cameras import scrap_cameras_data
from Computer_peripherals.computer_peripherals import scrap_computer_peripherals_data
from Laptops.laptops import scrap_Laptops_data
from Mobiles.Mobiles import scrap_mobiles_data
from HomeAppliances.HomeAppliances import scrap_HomeAppliances_data

def scrap_all_data():

    try:
        scrap_mobiles_data()
        print("Mobile data scraped successfully.")

        scrap_Laptops_data()
        print("Laptop data scraped successfully.")

        scrap_computer_peripherals_data()
        print("Computer peripherals data scraped successfully.")

        scrap_HomeAppliances_data()
        print("Home appliances data scraped successfully.")

        scrap_cameras_data()
        print("Camera data scraped successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    scrap_all_data()
