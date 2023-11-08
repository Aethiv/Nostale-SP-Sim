import tkinter as tk
import traceback

def validate_integer(entry_widget):
    if entry_widget.cget("state") == tk.DISABLED:
        return True
    user_input = entry_widget.get()
    if user_input.isdigit():
        return True
    return False

def validate_string(entry_widget):
    if entry_widget.cget("state") == tk.DISABLED:
        return True
    user_input = entry_widget.get()
    if user_input.isalpha():
        return True
    return False

def validate_float(entry_widget):
    if entry_widget.cget("state") == tk.DISABLED:
        return True
    user_input = entry_widget.get()
    try:
        float(user_input)
        return True
    except ValueError:
        return False
    
fields = [
    {"label": "Current upgrade level:", "validator": validate_integer},
    {"label": "Desired upgrade level:", "validator": validate_integer},
    {"label": "Angel feather cost:", "validator": validate_integer},
    {"label": "FM cost:", "validator": validate_float},
    {"label": "Upgrade item cost:", "validator": validate_integer},
    {"label": "Scroll cost", "validator": validate_float},
    {"label": "Number of simulations:", "validator": validate_integer},
    {"label": "Event %:", "validator": validate_integer},
]