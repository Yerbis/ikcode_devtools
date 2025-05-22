import sys
import time
import textwrap
import ast
import inspect
import subprocess
import tempfile
import os
from ast import Name
from functools import wraps, partial
import json
from datetime import datetime
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton,
                             QLabel, QCheckBox, QRadioButton, QButtonGroup,
                             QLineEdit, QMessageBox, QDialog, 
                             QVBoxLayout, QTextEdit, QTabWidget, QWidget, QListWidget,
                             QListWidgetItem, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy,
                             QFileDialog, QGridLayout, QInputDialog,
                             QScrollArea)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IKcode Devtools GUI -- v1.8.0")
        self.setGeometry(100, 100, 800, 800)
        self.setWindowIcon(QIcon("ikcode.png"))
        self.setStyleSheet("background-color: #1a7689;")

        self.checkbox = QCheckBox("Connect to terminal", self)

        self.blabel = QLabel("   GUI disabled", self)

        self.radio1 = QRadioButton("Record to server log", self)
        self.radio2 = QRadioButton("Do not record to server log", self)

        self.button_group = QButtonGroup(self)

        label = QLabel("IKcode GUI", self)
        label.setFont(QFont("Veranda", 18, QFont.Bold))
        label.setGeometry(0, 0, 500, 100)
        label.setStyleSheet("color: white; background-color: #1a7689; border: 2px solid #ffcc00;")
        label.setAlignment(Qt.AlignCenter)

        self.rlabel = QLabel("Server preferences:", self)
        self.rlabel.setGeometry(10, 500, 500, 100)
        self.rlabel.setStyleSheet("color: white; background-color: #1a7689; font-size:20px; font-family: Veranda;")

        self.tlabel = QLabel("Connect to your \n IKcode account:", self)
        self.tlabel.setGeometry(600, 50, 200, 50)
        self.tlabel.setStyleSheet("color: white; background-color: #1a7689; font-size:16px; font-family: Veranda;")
        self.textbox = QLineEdit(self)
        self.textbox.setGeometry(600, 100, 150, 30)
        self.textbutton = QPushButton("Connect", self)
        self.textbutton.setGeometry(600, 140, 150, 30)

        # Existing CheckInfo button
        self.cbutton = QPushButton("View CheckInfo", self)
        self.cbutton.setStyleSheet("border: 2px solid #ffcc00; background-color: #155e6e; color: white; font-size: 20px; font-family: Veranda;")

        self.initUI()

        pixmap = QPixmap("ikcode.png")
        picture_label = QLabel(self)
        scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        picture_label.setPixmap(scaled_pixmap)
        picture_label.setGeometry(500, 0, 100, 100)
        picture_label.setAlignment(Qt.AlignCenter)

    def initUI(self):
        # Enable GUI / Disable GUI button - keep fixed geometry as is
        self.button = QPushButton("Enable GUI", self)
        self.button.setGeometry(300, 150, 200, 50)
        self.button.setStyleSheet("border: 2px solid #ffcc00; background-color: #155e6e; color: white; font-size: 16px; font-family: Veranda;")
        self.button.clicked.connect(self.on_click)

        self.buttons_container = QWidget(self)
        container_width = 600
        container_height = 110  # Increased height to safely fit buttons + spacing
        container_x = (self.width() - container_width) // 2
        container_y = 370  # Lowered from 330 to 370
        self.buttons_container.setGeometry(container_x, container_y, container_width, container_height)
        self.buttons_container.setStyleSheet("background-color: #135e6c; border-radius: 12px;")

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(16, 12, 16, 12)  # generous padding inside container
        buttons_layout.setSpacing(20)

        # Smaller button style
        button_style = (
            "border: 2px solid #ffcc00;"
            "background-color: #155e6e;"
            "color: white;"
            "font-size: 13px;"  # slightly smaller
            "font-family: Verdana;"
            "padding: 6px 10px;"  # smaller padding
            "border-radius: 7px;"
        )

        def styled_button(text):
            button = QPushButton(text)
            button.setStyleSheet(button_style)
            button.setMinimumHeight(50)  # smaller height
            button.setMinimumWidth(120)
            button.setMaximumWidth(160)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            return button

        self.info_button = styled_button("View\nFile Info")
        self.info_button.clicked.connect(self.view_file_info)

        self.manage_versions_btn = styled_button("Manage\nSaved Versions")
        self.manage_versions_btn.clicked.connect(self.open_version_manager)

        self.cbutton.setText("View\nCheckInfo")
        self.cbutton.setStyleSheet(button_style)
        self.cbutton.setMinimumHeight(50)
        self.cbutton.setMinimumWidth(120)
        self.cbutton.setMaximumWidth(160)
        self.cbutton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        buttons_layout.addWidget(self.info_button)
        buttons_layout.addWidget(self.manage_versions_btn)
        buttons_layout.addWidget(self.cbutton)

        self.buttons_container.setLayout(buttons_layout)

        # Help button
        self.help_button = QPushButton("Help", self)
        self.help_button.setGeometry(690, 740, 100, 50)
        self.help_button.setStyleSheet("border: 2px solid #ffcc00; background-color: #155e6e; color: white; font-size: 20px; font-family: Veranda;")
        self.help_button.clicked.connect(self.help_button_clicked)

        # The rest of your UI setup remains the same...
        self.blabel.setGeometry(300, 210, 200, 50)
        self.blabel.setStyleSheet("background-color: #155e6e; color: white; font-size: 20px; font-family: Veranda;")

        self.checkbox.setStyleSheet("background-color: #155e6e; color: white; font-size: 16px; font-family: Veranda;")
        self.checkbox.setGeometry(300, 270, 200, 50)
        self.checkbox.setChecked(False)
        self.checkbox.stateChanged.connect(self.checkbox_changed)

        self.radio_group = QButtonGroup(self)
        self.radio_group.addButton(self.radio1)
        self.radio_group.addButton(self.radio2)

        self.radio1.setGeometry(10, 610, 200, 50)
        self.radio1.setStyleSheet("background-color: #155e6e; color: white; font-size: 16px; font-family: Veranda;")
        self.radio1.clicked.connect(self.radio1_checked)
        self.radio1.setChecked(True)
        self.log = True

        self.radio2.setGeometry(10, 670, 200, 50)
        self.radio2.setStyleSheet("background-color: #155e6e; color: white; font-size: 16px; font-family: Veranda;")
        self.radio2.clicked.connect(self.radio2_checked)

        self.button_group.addButton(self.radio1)
        self.button_group.addButton(self.radio2)

        self.textbox.setStyleSheet("background-color: #155e6e; color: white; font-size: 16px; font-family: Veranda;")
        self.textbutton.setStyleSheet("border: 2px solid #ffcc00; background-color: #155e6e; color: white; font-size: 20px; font-family: Veranda;")
        self.textbutton.clicked.connect(self.textbutton_clicked)

        self.cbutton.clicked.connect(self.view_check_info)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        container_width = 600
        container_height = 95
        container_x = (self.width() - container_width) // 2
        container_y = 330
        self.buttons_container.setGeometry(container_x, container_y, container_width, container_height)


    def open_version_manager(self):
        # Check if GUI enabled and terminal connected
        gui_enabled = self.button.text() == "Disable GUI"
        terminal_connected = self.checkbox.isChecked()
        if not (gui_enabled and terminal_connected):
            QMessageBox.warning(self, "Error", "GUI must be enabled and terminal connected to manage versions.")
            return
        dlg = VersionManagerDialog(self)
        dlg.exec_()


    def on_click(self):
        self.blabel.setText("   GUI enabled")
        self.button.setText("Disable GUI")
        try:
            self.button.clicked.disconnect()
        except Exception:
            pass
        self.button.clicked.connect(self.off_click)

    def off_click(self):
        self.blabel.setText("   GUI disabled")
        self.button.setText("Enable GUI")
        try:
            self.button.clicked.disconnect()
        except Exception:
            pass
        self.button.clicked.connect(self.on_click)

    def checkbox_changed(self, state):
        if self.log:
            if state == Qt.Checked:
                print("\nTerminal connected")
                if self.button.text() == "Disable GUI" and self.checkbox.isChecked():
                    print("\nGUI successfully connected to terminal")
                    self.blabel.setText("   GUI enabled")
            else:
                print("\nTerminal disconnected")
                if self.button.text() == "Disable GUI" and not self.checkbox.isChecked():
                    print("\nGUI disconnected from terminal")

    def radio1_checked(self):
        self.log = True
        print("\nServer log enabled")

    def radio2_checked(self):
        self.log = False
        print("\nServer log disabled")

    def help_button_clicked(self):
        help_text = """
        <h2>IKcode Devtools GUI Help</h2>

        <p><strong>Welcome to the IKcode Devtools GUI (v1.8.0)!</strong></p>

        <p>This application provides a graphical interface for interacting with IKcode's code analysis and version management tools.</p>

        <h3>Main Features:</h3>
        <ul>
        <li><strong>Enable/Disable GUI:</strong> Click the "Enable GUI" button to activate the interface. When enabled, you can interact with all features.</li>
        <li><strong>Connect to Terminal:</strong> Check the "Connect to terminal" box to allow the GUI to communicate with your terminal session.</li>
        <li><strong>Server Log Preferences:</strong> Use the radio buttons to choose whether actions and info are printed to the server log.</li>
        <li><strong>View File Info:</strong> Click "View File Info" to analyze the current Python file. You'll see stats like function/class counts, comments, blank lines, and a basic lint check.</li>
        <li><strong>View CheckInfo:</strong> Click "View CheckInfo" to analyze decorated functions for variables, imports, loops, and more. (Decorate your functions with <code>@CheckInfo</code> to use this feature.)</li>
        <li><strong>Manage Saved Versions:</strong> Click "Manage Saved Versions" to view, save, backup, and restore versions of your decorated functions.</li>
        <li><strong>Connect to IKcode Account:</strong> Enter your account name and click "Connect" to link the GUI with your IKcode account.</li>
        </ul>

        <h3>How to Use:</h3>
        <ul>
        <li>Start the GUI by running your script or calling <code>runGUI()</code> from your code.</li>
        <li>Enable the GUI and connect to the terminal for full functionality.</li>
        <li>Decorate your functions with <code>@CheckInfo</code> to enable code analysis.</li>
        <li>Use the version manager to save and restore code versions.</li>
        </ul>

        <h3>Example Usage:</h3>
        <pre><code>
        @CheckInfo
        def my_function():
            x = 5
            print(x)
        </code></pre>

        <p>Once saved, you can restore this code later using the <strong>getVersion</strong> button in the GUI.</p>

        <hr>
        <p>For more info, visit: <a href="https://ikgtc.pythonanywhere.com" style="color: blue;">https://ikgtc.pythonanywhere.com</a></p>
        """

        # Scrollable help dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("IKcode Devtools Help")
        dialog.resize(600, 500)

        layout = QVBoxLayout()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        content_widget = QLabel()
        content_widget.setText(help_text)
        content_widget.setWordWrap(True)
        content_widget.setTextFormat(Qt.RichText)  # Enables HTML formatting
        content_widget.setOpenExternalLinks(True)  # So the link is clickable

        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def textbutton_clicked(self):
        text = self.textbox.text()

        if self.log:
            time.sleep(0.3)
            print("\nConnecting to IKcode account...")
            time.sleep(2.7)
            print(f"\nConnected to IKcode account: {text}\n")

    def view_file_info(self):
        # Check if GUI enabled and terminal connected
        gui_enabled = self.button.text() == "Disable GUI"
        terminal_connected = self.checkbox.isChecked()
        if not (gui_enabled and terminal_connected):
            QMessageBox.warning(self, "Error", "GUI must be enabled and terminal connected to view file info.")
            return

        # Get current running file path
        try:
            filename = os.path.abspath(sys.argv[0])
            with open(filename, "r", encoding="utf-8") as f:
                code = f.read()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read file:\n{e}")
            return

        try:
            tree = ast.parse(code)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to parse file:\n{e}")
            return

        all_info = {}

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                analyzer = CodeAnalyzer()
                analyzer.visit(node)
                all_info[node.name] = {
                    "Function Names": analyzer.function_names,
                    "Variable Names": analyzer.variable_names,
                    "Imports": analyzer.imports,
                    "Classes": analyzer.classes,
                    "Loops": analyzer.loops,
                    "Conditionals": analyzer.conditionals,
                    "Comments": analyzer.comments
                }

        # Format info for display
        output = ""
        for func_name, info in all_info.items():
            # Filtering: skip if only function itself in Function Names and no classes/imports/loops/conditionals/comments
            only_self_function = info["Function Names"] == [func_name]
            other_keys_empty = all(not info[key] for key in ["Classes", "Imports", "Loops", "Conditionals", "Comments"])

            if only_self_function and other_keys_empty:
                # Skip printing this function info block
                continue

            output += f"Function: {func_name}\n"
            for key, values in info.items():
                value_str = ", ".join(values) if values else "None"
                output += f"  {key}: {value_str}\n"
            output += "\n"

        # Split code into lines for stats
        lines = code.splitlines()
        code_length = len(lines)

        # Count functions and classes via ast parsing
        try:
            tree = ast.parse(code)
            function_count = sum(isinstance(node, ast.FunctionDef) for node in ast.walk(tree))
            class_count = sum(isinstance(node, ast.ClassDef) for node in ast.walk(tree))
        except Exception:
            function_count = 0
            class_count = 0

        # Count comment lines and blank lines
        comment_lines = sum(1 for line in lines if line.strip().startswith("#"))
        blank_lines = sum(1 for line in lines if not line.strip())

        # Basic lint check: Try compiling
        try:
            compile(code, filename, 'exec')
            lint_errors = "No syntax errors detected."
        except SyntaxError as e:
            lint_errors = f"Syntax Error: {e}"

        # Get date and time
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        info_text = (
            f"Date and time: {now}\n"
            f"File route: {filename}\n"
            f"File name: {os.path.basename(filename)}\n"
            f"Lines of code: {code_length}\n"
            f"Function definitions: {function_count}\n"
            f"Class definitions: {class_count}\n"
            f"Comment lines: {comment_lines}\n"
            f"Blank lines: {blank_lines}\n"
            f"Lint check: {lint_errors}\n"
            "==========================\n"
            
        )

        # Print to terminal if server log enabled
        if self.log:
            print("\n=== File Info ===")
            print(info_text)
            print("=================\n")

        # Show info in message box
        QMessageBox.information(self, "File Info", info_text)

    def view_check_info(self):
    # Check if GUI enabled and terminal connected
        gui_enabled = self.button.text() == "Disable GUI"
        terminal_connected = self.checkbox.isChecked()
        if not (gui_enabled and terminal_connected):
            QMessageBox.warning(self, "Error", "GUI must be enabled and terminal connected to view check info.")
            return

        # Get current running file path
        try:
            filename = os.path.abspath(sys.argv[0])
            with open(filename, "r", encoding="utf-8") as f:
                code = f.read()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read file:\n{e}")
            return

        try:
            tree = ast.parse(code)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to parse file:\n{e}")
            return

        all_info = {}

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                # Look for @CheckInfo decorator
                if not any(isinstance(d, Name) and d.id == "CheckInfo" for d in node.decorator_list):
                    continue  # skip non-decorated functions

                analyzer = CodeAnalyzer()
                analyzer.visit(node)
                all_info[node.name] = {
                    "Function Names": analyzer.function_names,
                    "Variable Names": analyzer.variable_names,
                    "Imports": analyzer.imports,
                    "Classes": analyzer.classes,
                    "Loops": analyzer.loops,
                    "Conditionals": analyzer.conditionals,
                    "Comments": analyzer.comments
                }

        # Format output for CheckInfo only, skipping trivial functions
        output = ""
        for func_name, info in all_info.items():
            only_self_function = info["Function Names"] == [func_name]
            other_keys_empty = all(not info[key] for key in ["Classes", "Imports", "Loops", "Conditionals", "Comments"])

            if only_self_function and other_keys_empty:
                continue

            output += f"Function: {func_name}\n"
            for key, values in info.items():
                value_str = ", ".join(values) if values else "None"
                output += f"  {key}: {value_str}\n"
            output += "\n"

        if not output:
            output = "No detailed CheckInfo data found for any function."

        # Show info in message box (only CheckInfo data)
        QMessageBox.information(self, "CheckInfo", output)




full_info = {}

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.function_names = []
        self.variable_names = []
        self.imports = []
        self.classes = []
        self.loops = []
        self.conditionals = []
        self.comments = []
        self.visited_main_func = False  # to avoid nested functions

    def visit_FunctionDef(self, node):
        if not self.visited_main_func:
            self.function_names.append(node.name)
            self.visited_main_func = True
            for child in node.body:
                if not isinstance(child, (ast.FunctionDef, ast.ClassDef)):
                    self.visit(child)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.variable_names.append(target.id)
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module = node.module
        for alias in node.names:
            self.imports.append(f"{module}.{alias.name}")
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.classes.append(node.name)
        # Don't descend into class body

    def visit_For(self, node):
        self.loops.append('for')
        self.generic_visit(node)

    def visit_While(self, node):
        self.loops.append('while')
        self.generic_visit(node)

    def visit_If(self, node):
        self.conditionals.append('if')
        self.generic_visit(node)

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            self.comments.append(node.value.value)
        self.generic_visit(node)




class CheckInfo:
    def __init__(self, func):
        self.func = func
        self.full_info = {}
        self._analyze_code()

        # Attach self to the function object for easy access
        setattr(self.func, "_checkinfo_instance", self)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def _analyze_code(self):
        source = inspect.getsource(self.func)
        tree = ast.parse(source)

        analyzer = CodeAnalyzer()

        # The parsed tree contains only one node: the function we decorated
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                analyzer.visit(node)
                break

        self.full_info = {
            "Function Names": analyzer.function_names,
            "Variable Names": analyzer.variable_names,
            "Imports": analyzer.imports,
            "Classes": analyzer.classes,
            "Loops": analyzer.loops,
            "Conditionals": analyzer.conditionals,
            "Comments": analyzer.comments
        }

    def get_info(self):
        return self.full_info


def Help(topic=None):
    general_help = """
Welcome to IKcode GTconnect!

This package includes:
  • CheckInfo — a Python decorator to analyze function internals.
  • runGUI — launch a GUI terminal connector to interact with the tool visually.
  • Help — view usage documentation.
  • setVersion — manage and set package versions.

How to import:

    from ikcode_gtconnect import CheckInfo, runGUI, Help, setVersion

How to use CheckInfo:

    @CheckInfo
    def my_function():
        pass

    info = my_function._checkinfo_instance.get_info()
    print(info)

To run the GUI:

    runGUI()

To set or update the package version:

    setVersion("1.7.1")

For more specific help:

    Help(CheckInfo)      # Help on CheckInfo
    Help(runGUI)         # Help on the GUI
    Help("gui")          # Help on the GUI
    Help(setVersion)     # Help on setVersion
"""

    gui_help = """
IKcode GUI Terminal Connector - GUI Help

To use the GUI:

1. Import and run:
       from ikcode_gtconnect import runGUI
       runGUI()

2. Enable GUI:
       Click "Enable GUI" to activate.

3. Connect to terminal:
       Check the "Connect to terminal" checkbox (after enabling GUI).

4. Server logging:
       Use radio buttons to toggle logging.

5. CheckInfo button:
       Click 'View CheckInfo' to display analysis (must decorate a function first).
"""

    checkinfo_help = """
CheckInfo - Decorator Help

Purpose:
    Analyze a function’s code to extract info on variables, loops, imports, etc.

Usage:
    from ikcode_gtconnect import CheckInfo

    @CheckInfo
    def my_func():
        x = 5
        for i in range(x):
            print(i)

    info = my_func._checkinfo_instance.get_info()
    print(info)

Methods:
    get_info() — returns a dictionary of code analysis

Note:
    CheckInfo only works on user-defined functions.
"""

    setversion_help = """
getVersion - File management Help

Purpose:
    Save files with versioning and manage saved versions, and restoring ability.

Usage:
    from ikcode_devtools import getVersion

    @getVersion
    def example_function():
        x = 5
        for i in range(x):
            print(i)
    
        What this does is it will take the code of the function that is decorated with setVersion
        and save it to a file with the version number in the filename.
        You can access and manage these saved versions through the GUI by clicking the "Manage Saved Versions" button.
        This will open a dialog where you can view, save, and restore different versions of the function.

Notes:
    - This helps to ensure consistent behavior by locking to a known version.
    - Version strings should follow semantic versioning: "major.minor.patch".
    - Calling setVersion updates internal version tracking, useful before running other methods.
"""

    # Dispatcher logic
    if topic is None:
        print(general_help)
    elif isinstance(topic, str) and topic.lower() == "gui":
        print(gui_help)
    elif topic.__name__ == "runGUI":
        print(gui_help)
    elif topic.__name__ == "CheckInfo":
        print(checkinfo_help)
    elif topic.__name__ == "getVersion":
        print(setversion_help)
    else:
        print("Unrecognized help topic. Try Help(), Help(CheckInfo), Help(runGUI), or Help(setVersion).")

VERSIONS_FILE = "versions.json"

def load_versions():
    if os.path.exists(VERSIONS_FILE):
        with open(VERSIONS_FILE, 'r') as f:
            return json.load(f)
    else:
        return {"ready_to_save": {}, "saved_codes": {}, "backup_codes": {}}

def save_versions(data):
    with open(VERSIONS_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def getVersion(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    # Extract source code and add/update ready_to_save
    source = inspect.getsource(func)
    versions = load_versions()
    versions["ready_to_save"][func.__name__] = source
    save_versions(versions)
    return wrapper

class VersionManagerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Saved Versions")
        self.resize(600, 400)

        self.versions = load_versions()

        self.tabs = QTabWidget(self)

        # Tabs
        self.ready_to_save_tab = QWidget()
        self.saved_codes_tab = QWidget()
        self.backup_codes_tab = QWidget()

        self.tabs.addTab(self.ready_to_save_tab, "Codes Ready to Save")
        self.tabs.addTab(self.saved_codes_tab, "Saved Codes")
        self.tabs.addTab(self.backup_codes_tab, "Backup Codes")

        # Layouts for each tab
        self.ready_layout = QVBoxLayout()
        self.saved_layout = QVBoxLayout()
        self.backup_layout = QVBoxLayout()

        self.ready_list = QListWidget()
        self.saved_list = QListWidget()
        self.backup_list = QListWidget()

        self.ready_layout.addWidget(self.ready_list)
        self.saved_layout.addWidget(self.saved_list)
        self.backup_layout.addWidget(self.backup_list)

        self.ready_to_save_tab.setLayout(self.ready_layout)
        self.saved_codes_tab.setLayout(self.saved_layout)
        self.backup_codes_tab.setLayout(self.backup_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

        # Populate lists
        self.populate_ready_to_save()
        self.populate_saved_codes()
        self.populate_backup_codes()

        

    def populate_ready_to_save(self):
        self.ready_list.clear()
        for func_name in self.versions.get("ready_to_save", {}):
            widget = QWidget()
            layout = QHBoxLayout()
            layout.setContentsMargins(5, 5, 5, 5)

            label = QLabel(func_name)
            save_btn = QPushButton("Save")
            delete_btn = QPushButton("Delete")

            save_btn.clicked.connect(lambda _, fn=func_name: self.save_code(fn))
            delete_btn.clicked.connect(lambda _, fn=func_name: self.confirm_delete(fn, "ready"))

            layout.addWidget(label)
            layout.addStretch()
            layout.addWidget(save_btn)
            layout.addWidget(delete_btn)

            widget.setLayout(layout)
            item = QListWidgetItem()
            item.setSizeHint(widget.sizeHint())
            self.ready_list.addItem(item)
            self.ready_list.setItemWidget(item, widget)

    def populate_saved_codes(self):
        self.saved_list.clear()
        for func_name, versions in self.versions.get("saved_codes", {}).items():
            for ver in versions:
                version_id = ver.get("version_id", "v?")

                widget = QWidget()
                layout = QHBoxLayout()
                layout.setContentsMargins(5, 5, 5, 5)

                label = QLabel(f"{func_name} - {version_id}")
                backup_btn = QPushButton("Add to Backup")
                delete_btn = QPushButton("Delete")

                backup_btn.clicked.connect(lambda _, fn=func_name, v=ver: self.add_to_backup(fn, v))
                delete_btn.clicked.connect(lambda _, fn=func_name, vid=version_id: self.confirm_delete(fn, "saved", vid))

                layout.addWidget(label)
                layout.addStretch()
                layout.addWidget(backup_btn)
                layout.addWidget(delete_btn)

                widget.setLayout(layout)
                item = QListWidgetItem()
                item.setSizeHint(widget.sizeHint())
                self.saved_list.addItem(item)
                self.saved_list.setItemWidget(item, widget)

    def populate_backup_codes(self):
        self.backup_list.clear()
        for func_name, versions in self.versions.get("backup_codes", {}).items():
            for ver in versions:
                version_id = ver.get("version_id", "v?")

                item_widget = QWidget()
                layout = QHBoxLayout()
                layout.setContentsMargins(5, 2, 5, 2)
                layout.setSpacing(10)

                label = QLabel(f"{func_name} - {version_id}")
                restore_btn = QPushButton("Restore")
                delete_btn = QPushButton("Delete")

                restore_btn.clicked.connect(partial(self.restore_code, func_name, ver))
                delete_btn.clicked.connect(lambda _, fn=func_name, vid=version_id: self.confirm_delete(fn, "backup", vid))

                layout.addWidget(label)
                layout.addStretch()
                layout.addWidget(restore_btn)
                layout.addWidget(delete_btn)

                item_widget.setLayout(layout)
                item = QListWidgetItem()
                item.setSizeHint(item_widget.sizeHint())
                self.backup_list.addItem(item)
                self.backup_list.setItemWidget(item, item_widget)


    def save_code(self, func_name):
        code = self.versions["ready_to_save"].pop(func_name, None)
        if code is None:
            QMessageBox.warning(self, "Warning", "Code not found!")
            return

        version_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        saved_versions = self.versions["saved_codes"].setdefault(func_name, [])
        saved_versions.append({"version_id": version_id, "code": code})

        save_versions(self.versions)
        self.populate_ready_to_save()
        self.populate_saved_codes()

    def add_to_backup(self, func_name, version):
        backups = self.versions["backup_codes"].setdefault(func_name, [])
        backups.append(version)

        # Optionally remove from saved_codes or keep it
        saved_list = self.versions["saved_codes"].get(func_name, [])
        if version in saved_list:
            saved_list.remove(version)

        save_versions(self.versions)
        self.populate_saved_codes()
        self.populate_backup_codes()



    def restore_code(self, func_name, version):
        # Prompt user for file path or empty for default
        text, ok = QInputDialog.getText(
            self, 
            "Restore Code", 
            "Enter full file path to save the restored code,\n"
            "or leave empty to save in the current directory:"
        )
        if not ok:
            return  # User cancelled

        # Determine save path
        if text.strip():
            filename = text.strip()
        else:
            # Save to user's current working directory
            safe_version_id = version['version_id'].replace(':', '-').replace(' ', '_')
            filename = f"{func_name}_{safe_version_id}.py"
            current_dir = os.getcwd()  # Use working directory instead of __file__
            filename = os.path.join(current_dir, filename)

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(version['code'])
            QMessageBox.information(self, "Success", f"Code restored to:\n{filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to restore code:\n{e}")


    def delete_version(self, func_name, version_id=None, category=None):
        if category not in ["ready_to_save", "saved_codes", "backup_codes"]:
            QMessageBox.warning(self, "Delete Failed", "Invalid category for deletion.")
            return

        if not os.path.exists(VERSIONS_FILE):
            QMessageBox.warning(self, "Delete Failed", "No versions file found.")
            return

        try:
            with open(VERSIONS_FILE, "r", encoding="utf-8") as f:
                versions = json.load(f)

            if category == "ready_to_save":
                if func_name in versions["ready_to_save"]:
                    del versions["ready_to_save"][func_name]
            else:
                entries = versions[category].get(func_name, [])
                filtered = [v for v in entries if v.get("version_id") != version_id]
                if filtered:
                    versions[category][func_name] = filtered
                else:
                    del versions[category][func_name]

            with open(VERSIONS_FILE, "w", encoding="utf-8") as f:
                json.dump(versions, f, indent=4)

            # Update memory and UI
            self.versions = load_versions()
            self.populate_ready_to_save()
            self.populate_saved_codes()
            self.populate_backup_codes()

            QMessageBox.information(self, "Deleted", f"Version deleted from {category}.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Deletion failed:\n{e}")

    def confirm_delete(self, func_name, category, version_id=None):
    # Create a friendly message
        if category == "ready":
            msg = f"Are you sure you want to delete '{func_name}' from Ready to Save?"
        elif category == "saved":
            msg = f"Are you sure you want to delete version '{version_id}' of '{func_name}' from Saved Codes?"
        elif category == "backup":
            msg = f"Are you sure you want to delete backup version '{version_id}' of '{func_name}'?"
        else:
            return

        reply = QMessageBox.question(self, "Delete Confirmation", msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        # Perform deletion
        if category == "ready":
            self.versions.get("ready_to_save", {}).pop(func_name, None)
        elif category == "saved":
            versions = self.versions.get("saved_codes", {}).get(func_name, [])
            self.versions["saved_codes"][func_name] = [v for v in versions if v.get("version_id") != version_id]
            if not self.versions["saved_codes"][func_name]:
                self.versions["saved_codes"].pop(func_name, None)
        elif category == "backup":
            backups = self.versions.get("backup_codes", {}).get(func_name, [])
            self.versions["backup_codes"][func_name] = [b for b in backups if b.get("version_id") != version_id]
            if not self.versions["backup_codes"][func_name]:
                self.versions["backup_codes"].pop(func_name, None)

        save_versions(self.versions)
        self.populate_ready_to_save()
        self.populate_saved_codes()
        self.populate_backup_codes()




def runGUI():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    print("\n\nIKcode GUI terminal connector\n")
    print("Server log:\n")
    runGUI()
