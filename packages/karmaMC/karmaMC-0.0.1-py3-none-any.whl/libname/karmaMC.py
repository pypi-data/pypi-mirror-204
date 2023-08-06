import time
import pyautogui as pt
import keyboard
from colorama import Fore

def fail_safe():
    fs = True

    while fs == True:
        if keyboard.is_pressed(["shift", "+"]):
             print(f"{Fore.RED}failsafe_activated")
             fs = False
             (exit)

def disconnect ():
    pt.hotkey('esc')
    pt.click(960, 650)

def drag_click(x,y,var):
    pt.moveTo(x,y)
    pt.click(button=var)
    time.sleep(0.5)

def tab():
    if(pt.pixel(955,600)==(255,255,255)): #connection_error
        print(f"{Fore.LIGHTYELLOW_EX}connection_error")
        connection_error()

    elif(pt.pixel(944,102)==(255,255,255)): #server_list
        print(f"{Fore.CYAN}server_list")
        join_server()
        
    elif(pt.pixel(1685,385)==(85,255,255)): #minehut
        print(f"{Fore.LIGHTCYAN_EX}minehut")
        start_server()
    
    else:
        print(f"{Fore.LIGHTGREEN_EX}in_server/undefined") #in_server/undefined
    
    
def join_server():
      drag_click(575,400,"left")
      time.sleep(8)
      tab()

def connection_error():
    drag_click(955,600,"left")
    tab()

def start_server():
    pt.hotkey("1")
    pt.rightClick()
    drag_click(850,550,"left")
    drag_click(850,270,"left")

def func_list():
    print(f"{Fore.LIGHTMAGENTA_EX}failsafe(shift, +)")
    print(f"{Fore.LIGHTCYAN_EX}disconnect()")
    print(f"{Fore.LIGHTMAGENTA_EX}drag_click(x,y,variation)")
    print(f"{Fore.LIGHTCYAN_EX}tab()")
    print(f"{Fore.LIGHTMAGENTA_EX}join_server()")
    print(f"{Fore.LIGHTCYAN_EX}connection_error()")
    print(f"{Fore.LIGHTMAGENTA_EX}start_server()")
    print(f"{Fore.WHITE}")