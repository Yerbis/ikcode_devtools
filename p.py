from ikcode_gtconnect import runGUI


import sys

def show_help():
    print("Showing help info here.")
    
def runGUI():
    print("Arguments:", sys.argv)
    if '--help' in sys.argv or '-h' in sys.argv:
        show_help()
        sys.exit(0)
    
    print("Launching GUI...")
    # GUI launch code here

if __name__ == "__main__":
    runGUI()
