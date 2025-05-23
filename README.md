


IKcode Dvtools is used to connect your Python terminal to IKcode’s database, allowing file exchange and much more.
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

    pip install ikcode-devtools

Keep it Updated

The package may update frequently. To ensure full functionality, run this command daily or before each use:

    pip install --upgrade ikcode-devtools

2. Use and Import the Package
Run GUI Directly from Terminal

Run this command in your terminal to open the GUI directly:

    ikcode-devtools

Import in Python (Recommended)

Open your Python file and import the package:

    import ikcode_devtools # Make sure to use an underscore(_)

Or import specific methods:

    from ikcode_devtools import runGUI, CheckInfo

Available Methods (as of v1.8)

    runGUI()
    CheckInfo (decorator)
    Help()
    getVersion

3. How to Use the Methods
runGUI()

To launch the GUI interface, import and call this function:

    from ikcode_devtools import runGUI
    runGUI()

CheckInfo()

This is a decorator that checks detailed info about any Python function it decorates.

Usage:

    from ikcode_devtools import CheckInfo
    
    @CheckInfo
    def my_function():
        # your code here

Place @CheckInfo immediately above the function you want to analyze.

Help()

This is a function that lets you get help directly in the terminal when you run it

Usage:

    from ikcode_devtools import Help
    print(Help()) # Print general help
    print(Help(runGUI)) # Print help on runGUI()
    print(Help(CheckInfo)) # Print help on CheckInfo
    print(Help(gui) # Print help on the GUI
    print(Help(getVersion) # Print help on getVersion
    print(Help(getInspect) # Print help on getInspect

How to Use getVersion to Restore Saved Code

The getVersion function allows you to restore a previous version of your code that was saved using saveVersion. This is perfect for rolling back to earlier states if something breaks or if you want to review older code.
Restoring a Version

To restore a version:

    Click the “Get Version” or “Load Version” button in your application.
    A list of saved versions will appear, often labeled by date/time or version name.
    Select the version you want to restore.
    The current code will be replaced with the contents of the selected version.

Important: Restoring a version will overwrite your current code. Make sure to save the current state with saveVersion before restoring another version.
When to Use getVersion

    After testing changes that didn't work as expected.
    To compare current code with a previous version.
    When you've accidentally removed important logic and need to recover it.

Pro Tip: Use saveVersion frequently, and getVersion becomes your time machine for development!
4. Help Manual & Features


Function Inspection with @getInspect

The @getInspect decorator analyzes your Python functions to provide detailed insights about their execution, structure, and complexity.
Importing

    from ikcode_devtools import getInspect
  

Usage

Decorate any function you want to inspect with @getInspect. For example:

    @getInspect
    def my_function(x):
        total = 0
        for i in range(x):
            total += i
        return total
    my_function() # Will only work if the function is called
  

Important:

You must call the decorated function at least once for inspection data to be generated and stored. The inspection runs when the function executes.

    result = my_function(10)
  

Viewing Inspection Results

Inspection results are stored in the global dictionary inspection_results keyed by function name. You can directly view it in your python file:

    from ikcode_devtools import inspection_results
    
    print(inspection_results.get("my_function"))
  

OR, In the GUI, clicking the "Run Inspection" button will display a summary of all inspected functions and their analysis data.

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

 GUI.
    Remember to enable and connect the GUI before using @CheckInfo for full functionality.

