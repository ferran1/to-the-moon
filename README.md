# Installation

### Installing the necessary software

Before cloning the respository we need to install some software first.

To run the webapplication it is required to install the latest version of Python:
https://www.python.org/downloads/

It is also required to install Pip (Package manager for Python):
https://pip.pypa.io/en/stable/installation/

To check if Python and Pip have correctly been installed, enter the following commands into your command prompt:

> python -V
> <br />

> pip -V

Additionally install Arduino to run the code for the embedded device:
https://www.arduino.cc/en/software

### Downloading the application to your local machine

On this git projects home page, click on the blue dropdown button with clone on the right side.
After clicking the button, 2 links will appear, HTTP and SSH. Use the HTTP link.

After copying the link, open a terminal of your choice on your local machine (preferably git bash).
In the terminal, navigate to the install location by using the 'cd' command.

If everything was correct the project should be located on your local machine at the current working directory.

### Install the necessary Python dependencies

_Install all Python project dependencies using:_

$ pip install -r requirements.txt

# Run the Flask webapplication

Set the IPV4 adress of your local machine in the **_main.py_** file

> app.run('YOUR IPV4 ADDRESS', port=5000, debug=True, threaded=False)

In the **_Webapplication_** directory, execute the following command to run the webserver:

> python main.py

Then to start the webapplication, go to your browser and enter your IP address with port 5000, for example:

> http://192.168.178.241:5000

# Run the embedded program (Platformio)

Make sure to install the Platformio plugin on VSCode:
https://marketplace.visualstudio.com/items?itemName=platformio.platformio-ide

Platformio docs:
https://docs.platformio.org/en/latest/tutorials/index.html

**_Tothemoon-embedded_** is the project folder you should open in platformio

A schematic of the hardware circuit can be at the following URL:
https://gitlab.fdmci.hva.nl/IoT/2021-2022-sep-jan/individual-project/iot-tombalf/-/blob/main/res/blueprint%20wiring%20diagram%20sketch_bb.png

## Author contact information

ferran.tombal@hva.nl
