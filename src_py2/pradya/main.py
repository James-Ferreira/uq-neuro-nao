import code
import scripts
from src_py2.robot.nao_robot import NAORobot


# 1. SETUP
robot = NAORobot("clas")
robot.mm.sit()


while True:
    try:
        reload(scripts)
        
        BLOCK_MAP = {
            name: func for name, func in scripts.__dict__.items()
            if callable(func) and not name.startswith("__")
        }
    except Exception as e:
        print("\n!!! ERROR IN scripts.py: " + str(e))
        raw_input("Fix and press Enter to retry...")
        continue

    print("\n" + "="*30)
    print("Available scripts: " + ", ".join(sorted(BLOCK_MAP.keys())))
    print("Type a script name to run it.")
    print("Type 'test' for interactive mode.")
    print("="*30)
    
    choice = raw_input("Action > ").strip()

    if choice.lower() == 'test':
        print("\n--- INTERACTIVE MODE (Ctrl-D to return) ---")
        code.interact(banner="", local=locals()) 
        print("--- BACK TO MENU ---")

    elif choice in BLOCK_MAP:
        try:
            BLOCK_MAP[choice](robot)
        except Exception as e:
            print("Execution Error: " + str(e))
    
    elif choice == "":
        continue
    
    else:
        print("Invalid choice. (For Live Mode, type 'test')")
