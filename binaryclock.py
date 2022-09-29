"""This namespace handles logic for displaying and switching inner logic of a binaryclock"""
#Handle imports
from symbol import arglist
from sense_hat import SenseHat
import time, datetime, signal, sys

#Define constant variables
hour_color = (0, 255, 0)
minute_color = (0, 0, 255)
second_color = (255, 0, 0)
pm_color = (192, 16, 128)
off = (0, 0, 0)

#Setup objects
hat = SenseHat()
hat.clear()
mode = 0 #0 = 12h, 1 = 24h
direction = 0 #1 = vertical, 0 = horizontal
endbool = False
#Define helping functions
def signal_term_handler(signal, frame):
    """This method is used for eventhandling signal sigint and sigterm interrupts.
    Displays a message on the sensehat and then proceeds to exit current process"""
    hat.show_message('Programmet slutter')
    sys.exit(0)

def pushed_up(event):
    """This method influences the global variable mode which determines in which format the
    binary clock is displayed"""
    global mode
    if(event.action == "released"):
        hat.clear()
        mode = 0

def pushed_down(event):
    """This method influences the global variable mode which determines in which format the
    binary clock is displayed"""
    global mode
    if(event.action == "released"):
        hat.clear()
        mode = 1

def pushed_left(event):
    """This method influences the global variable direction which determines in which direction the
    binary clock is displayed"""
    global direction
    if(event.action == "released"):
        hat.clear()
        direction = 0

def pushed_right(event):
    """This method influences the global variable direction which determines in which direction the
    binary clock is displayed"""
    global direction
    if(event.action == "released"):
        hat.clear()
        direction = 1

def pushed_middle(event):
    """This method influences the global variable endbool which determines if the program should end"""
    global endbool
    if(event.action == "released"):
        endbool = True

def display_binary(value, row, color):
    """This method takes a integer value, integer row 
    and a triple then it proceeds to display it on the sensehat.
    
    note: This method is influenced by a global variable
    named direction which influences the displayed direction and the amount of columns."""
    
    if(direction == 0):
        binary_str = '{0:8b}'.format(value)
        for x in range(0, 8):
            if binary_str[x] == '1':
                print(x)
                hat.set_pixel(x, row, color)
            else:
                hat.set_pixel(x, row, off)
    else:
        if len(str(value))==1:
            value="0"+str(value)
        arr = [int(a) for a in str(value)]
        
        print(arr)
        binary_str = '{0:4b}'.format(arr[1])
        for x in range(0, 4):
            if binary_str[x] == '1':
                hat.set_pixel(row+1, x, color)
            else:
                hat.set_pixel(row+1, x, off)
        binary_str = '{0:4b}'.format(arr[0])
        for x in range(0, 4):
            if binary_str[x] == '1':
                hat.set_pixel(row, x, color)
            else:
                hat.set_pixel(row, x, off)

def main():
    """Main function that takes args and changes variables then begins the program"""
    hat.show_message('Programmet starter')
    while True:
        if(endbool):
            hat.show_message('Programmet slutter')
            sys.exit(0)
        t = datetime.datetime.now()
        if(mode == 0):
            v = t.strftime("%I:%M:%S:%P")
            t = datetime.datetime.strptime(t.strftime("%I:%M:%S"),"%H:%M:%S")
            ispm=v.split(':')[3]=="pm"
            if ispm:
                 hat.set_pixel(0, 0, pm_color)
            else:
                hat.set_pixel(0, 0, off)
            hat.set_pixel(7, 7, pm_color)
        else:
            hat.set_pixel(7, 7, off)
        display_binary(t.hour, 2, hour_color)
        display_binary(t.minute, 4, minute_color)
        display_binary(t.second, 6, second_color)
        time.sleep(1)
        #End program

#Setup events
signal.signal(signal.SIGTERM, signal_term_handler)
signal.signal(signal.SIGINT, signal_term_handler)
hat.stick.direction_down = pushed_down
hat.stick.direction_up = pushed_up
hat.stick.direction_left = pushed_left
hat.stick.direction_right = pushed_right
hat.stick.direction_middle = pushed_middle

#Begin program
if __name__ == "__main__":
    argsL = sys.argv[1::]
    for arg in argsL:
        vari,valu = arg.split("=")
        if vari == 'direction':
            direction = int(valu)
        elif vari == 'mode':
            mode=int(valu)
    main()





