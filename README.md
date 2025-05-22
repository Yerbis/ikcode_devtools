
IKcode GUI terminal connector



IKcode GTC is used to connect your Python terminal to IKcode’s database, allowing file exchange and much more.
1. Install and Setup IKcode GTC

⚠️ It is recommended to create a virtual environment before installing packages.
Using VSCode

Follow these steps to create a virtual environment:

    Press Ctrl + Shift + P to open the command palette.
    Type and select Python: Select Interpreter.
    Click + Create new environment.
    Choose .venv folder and select the ‘Global’ path (it should say “Global” next to it).

Using Terminal (any OS)

Open your terminal (BASH, PowerShell, Command Prompt) and run:

python -m venv .venv

Then activate the environment:

    Windows: .venv\Scripts\activate
    macOS/Linux: source .venv/bin/activate

Now your virtual environment is ready!
Install the Package

Open the terminal in your project folder (Ctrl + Shift + ` in VSCode) and run:

pip install ikcode_gtconnect

Keep it Updated

The package may update frequently. To ensure full functionality, run this command daily or before each use:

pip install --upgrade ikcode_gtconnect

2. Use and Import the Package
Run GUI Directly from Terminal

Run this command in your terminal to open the GUI directly:

ikcode-gtconnect

Import in Python (Recommended)

Open your Python file and import the package:

import ikcode_gtconnect

Or import specific methods:

from ikcode_gtconnect import runGUI, CheckInfo

Available Methods (as of v1.7.1)

    runGUI()
    CheckInfo (decorator)

3. How to Use the Methods
runGUI()

To launch the GUI interface, import and call this function:

from ikcode_gtconnect import runGUI
runGUI()

CheckInfo()

This is a decorator that checks detailed info about any Python function it decorates.

Usage:

from ikcode_gtconnect import CheckInfo

@CheckInfo
def my_function():
    # your code here

Place @CheckInfo immediately above the function you want to analyze.
4. Help Manual & Features

Welcome to the IKcode GUI Terminal Connector! This tool lets you connect your GUI to a terminal session, manage server logging preferences, and analyze Python functions with CheckInfo.
Enabling the GUI

    Click the Enable GUI button to activate the GUI.
    When enabled, the label below the button changes to GUI enabled, and the button text switches to Disable GUI.
    Click again to disable the GUI.

Connecting to the Terminal

    Check the Connect to terminal checkbox to link the GUI to the terminal session.
    You must enable the GUI first before connecting.
    The label will confirm when connected.

Server Logging Preferences

    Select whether to record interactions to the server log.
    Options via radio buttons:
        Record to server log — enables logging (default).
        Do not record to server log — disables logging.

Connecting to Your IKcode Account

    Enter your IKcode account name or ID in the Connect to your IKcode account textbox.
    Click the Connect button to simulate connection.
    Connection progress messages will display in the terminal output.

CheckInfo Feature

    @CheckInfo analyzes a function's code, gathering details such as variable names, imports, classes, loops, and more.
    Access the info via function._checkinfo_instance.get_info() or the View CheckInfo button in the GUI.
    Remember to enable and connect the GUI before using @CheckInfo for full functionality.

