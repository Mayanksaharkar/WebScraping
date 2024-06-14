import os
import sys

cwd = os.getcwd()
sys.path.append(os.path.join(cwd))

from Cameras.cameras import scrap_cameras
from Computer_peripherals.computer_peripherals import scrap_computer_peripherals
from Laptops.laptops import scrap_Laptops
from Mobiles.Mobiles import scrap_mobiles
from HomeAppliances.HomeAppliances import scrap_HomeAppliances


def scrap_all_data():
    try:
        # scrap_mobiles()
        # print("Mobile data scraped successfully.")
        #
        # scrap_Laptops()
        # print("Laptop data scraped successfully.")
        #
        # scrap_computer_peripherals()
        # print("Computer peripherals data scraped successfully.")

        scrap_HomeAppliances()
        print("Home appliances data scraped successfully.")

        scrap_cameras()
        print("Camera data scraped successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    scrap_all_data()
