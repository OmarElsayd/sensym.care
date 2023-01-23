# This file will install the required packages to create the development environment needed for the software
import sys
import subprocess

def install_package():
    sysInfo = str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2])
    if sysInfo != "3.10.5":
        print("Python 3.10 is required to run this software")
        print("Please install Python 3.10 and run this script again")
        sys.exit(1)

    if str(sys.platform).lower() == "linux":
        try:
            print("Your system is running Linux")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("All packages installed successfully")
        except:
            print("Error! Couldn't install the required packages")
            print("Please install pip manually using the following command:")
            print("py get-pip.py on Windows\npython3 get-pip.py on Linux and Mac")
    elif str(sys.platform).lower() == "darwin":
        try:
            print("Your system is running Mac")
            subprocess.check_call([sys.executable,"-m" "brew", "install", "-r", "requirements.txt"])
            print("All packages installed successfully")
        except:
            print("Error! Couldn't install the required packages")
            print("Please install pip manually using the following command:")
            print("py get-pip.py on Windows\npython3 get-pip.py on Linux and Mac")
            print("If you are using a Mac, please install the following packages manually using brew:")
            print("pyaudio, matplotlib, numpy, wave, speech_recognition, pydub")

    elif str(sys.platform).lower() == "win32":
        try:
            print("Your system is running Windows")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("All packages installed successfully")
        except:
            print("Error! Couldn't install the required packages")
            print("Please install pip manually using the following command:")
            print("py get-pip.py on Windows\npython3 get-pip.py on Linux and Mac")



if __name__ == "__main__":
    install_package()