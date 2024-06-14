import os, sys
cwd = os.getcwd()
sys.path.append(os.path.join(cwd))

from Cameras.cameras import get_cameras_data
from Computer_peripherals.computer_peripherals import  get_computer_peripherals_data
from Laptops.laptops import  get_Laptops_data
from Mobiles.Mobiles import get_mobiles_data
from HomeAppliances.HomeAppliances import get_HomeAppliances_data

def getAll():
    get_mobiles_data()
    print("Mobiles Done")
    get_Laptops_data()
    print("Laptops Done")
    get_computer_peripherals_data()
    print("Computer peripherals Done")
    get_HomeAppliances_data()
    print("Home Appliance Done")
    get_cameras_data()
    print("Cameras Done")

getAll()