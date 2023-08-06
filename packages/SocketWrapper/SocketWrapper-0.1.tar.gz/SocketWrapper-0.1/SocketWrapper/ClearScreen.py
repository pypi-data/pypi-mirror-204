from os import system, name

'''
Checks what OS the user is on, and runs the appropriate command to clear the terminal
'''
def clear():
    if name == 'nt':
        _ = system('cls')
    else: # For mac and linux(here, os.name is 'posix')
        _ = system('clear')