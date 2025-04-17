import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header():
    print("""
\033[95m                       

                                        ██╗██████╗ ████████╗██╗     ██╗  ██╗
                                        ██║╚════██╗╚══██╔══╝██║     ██║ ██╔╝
                                        ██║ █████╔╝   ██║   ██║     █████╔╝ 
                                        ██║ ╚═══██╗   ██║   ██║     ██╔═██╗ 
                                        ██║██████╔╝   ██║   ███████╗██║  ██╗
                                        ╚═╝╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝
                                                    
\033[0m
""")
def display_menu(sections):
    for section_name, options in sections.items():
        print(f"\033[1m{section_name}\033[0m")

        sorted_items = sorted(options.items())
        mid_index = (len(sorted_items) + 1) // 2
        left_column = sorted_items[:mid_index]
        right_column = sorted_items[mid_index:]

        # Complète la colonne de droite s'il manque des éléments
        while len(right_column) < len(left_column):
            right_column.append(("", ""))

        for (code1, desc1), (code2, desc2) in zip(left_column, right_column):
            left_text = f"[\033[94m{code1:02d}\033[0m] {desc1}" if code1 != "" else ""
            right_text = f"[\033[94m{code2:02d}\033[0m] {desc2}" if code2 != "" else ""
            print(f"  {left_text:<42}{right_text}")
        print()



def get_user_choice(sections):
    while True:
        choice = input("\033[92m└──>\033[0m Enter your choice: ")
        if choice == "":
            # Entrée sans rien taper = retour au menu
            return None
        elif choice.lower() == 'i':
            print("\n\033[1mExtaz Tools Information:\033[0m")
            print("This is a Python-based interface mimicking the Extaz Tools menu.")
            input("\nPress Enter to return to the menu...")
            return None
        elif choice.lower() == 's':
            print("\n\033[1mExtaz Tools Website:\033[0m")
            input("\nPress Enter to return to the menu...")
            return None
        elif choice.lower() == 'n':
            print("\n\033[1mNext Page:\033[0m")
            print("There are no more pages in this simplified interface.")
            input("\nPress Enter to return to the menu...")
            return None
        elif choice.isdigit():
            choice_int = int(choice)
            for section in sections.values():
                if choice_int in section:
                    return choice_int
            print("\033[91mInvalid choice. Please try again.\033[0m")
        else:
            print("\033[91mInvalid input. Please enter a number or 'i', 's', 'n', or just press Enter.\033[0m")

def execute_choice(choice, sections):
    if choice:
        for section_name, options in sections.items():
            if choice in options:
                print(f"\n\033[1mExecuting: {options[choice]}...\033[0m")
                
                script_name = f"{choice}.py"

                if os.path.exists(script_name):
                    print(f"\033[3mRunning {script_name}...\033[0m\n")
                    os.system(f'python "{script_name}"')
                else:
                    print(f"\033[91mScript {script_name} not found.\033[0m")
                
                input("\nPress Enter to continue...")
                return

def main():
    sections = {
        "Main Menu": {
            1: "Search in the databases",
            2: "Discord Token Spam",
            3: "Discord Webhook Spam",
            4: "IP Lookup",
            5: "IP Lookup Website",
            6: "Phone Number Lookup",
            7: "Phone Number Lookup Account",
        },
    }

    while True:
        clear_screen()
        display_header()
        display_menu(sections)
        choice = get_user_choice(sections)
        if choice is not None:
            execute_choice(choice, sections)

if __name__ == "__main__":
    main()
