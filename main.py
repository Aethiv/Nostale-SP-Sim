import tkinter as tk
import constants
import random
from validation import validate_integer, validate_string, validate_float, fields
import traceback

def toggle_event():
    if event_checkbox.get():
        entry.config(state=tk.NORMAL)
    else:
        entry.config(state=tk.DISABLED)

app = tk.Tk()
app.title("Nostale Upgrade Simulator")

entry_list = []

for i, field in enumerate(fields):
    label = tk.Label(app, text=field["label"])
    label.grid(row=i, column=0, sticky="w")

    entry = tk.Entry(app)
    entry.grid(row=i, column=1)
    
    if i == 7:
        entry.config(state=tk.DISABLED)
    entry_list.append(entry)
    

event_checkbox = tk.BooleanVar()
checkbox = tk.Checkbutton(app, text="Event",variable=event_checkbox, command=toggle_event)
checkbox.grid(row=len(fields), columnspan=2)

result_label = tk.Label(app, text="")
result_label.grid(row=len(fields)+1, column=0, columnspan=1)

result_label2 = tk.Label(app, text="")
result_label2.grid(row=len(fields)+1, column=1, columnspan=2)

toggle_event()
def perform_calculation():
    try:
        values = [entry.get() for entry in entry_list]

        numeric_values = []
        for value, entry in zip(values, entry_list):
            if entry.cget('state') == tk.DISABLED:
                numeric_values.append(0)
            else:
                if validate_integer(entry):
                    numeric_values.append(int(value))
                elif validate_float(entry):
                    numeric_values.append(float(value))
                else:
                    raise ValueError
                
        simCount = 0
        upgr_cost = 0
        if event_checkbox.get():
            for i in range(len(constants.up_chance)):
                updated_upchance = [x * (1 + numeric_values[7]/100) for x in constants.up_chance]
        else:
            updated_upchance = constants.up_chance
            
        used_items = (0,0,0) #Wings, FMs, Gold    
        while simCount < numeric_values[6]:
            base_upgrLvl = numeric_values[0]
            while base_upgrLvl < numeric_values[1]:
                upgr_cost += constants.wings[base_upgrLvl]*numeric_values[2] + constants.fms[base_upgrLvl]*numeric_values[3] + constants.upitems[base_upgrLvl]*numeric_values[4] + constants.gold[base_upgrLvl]
                random_number = random.randint(0,99)
                #Success with scroll
                if random_number < updated_upchance[base_upgrLvl] and base_upgrLvl >= 2:
                    base_upgrLvl += 1
                    upgr_cost += numeric_values[5]
                #Fail with scroll -> Return materal cost
                elif random_number > updated_upchance[base_upgrLvl] and base_upgrLvl >= 2:
                    upgr_cost += numeric_values[5] - constants.upitems[base_upgrLvl]*numeric_values[4]
                #Success without scroll
                elif random_number < updated_upchance[base_upgrLvl] and base_upgrLvl < 2:
                    base_upgrLvl += 1
                #Fail without scroll -> same cost as success, just dont increase upgrLvl
                used_items = (used_items[0] + constants.wings[base_upgrLvl], used_items[1] + constants.fms[base_upgrLvl],used_items[2] + constants.gold[base_upgrLvl])
            simCount += 1
        result = upgr_cost/simCount
        used_items = (used_items[0]/simCount, used_items[1]/simCount, used_items[2]/simCount)

        result_label.config(text=f"Total cost: {result:.2f}")
        result_label2.config(text=f"Wings: {used_items[0]} FMs: {used_items[1]}" + "\n" + f"Gold: {used_items[2]}")

    except ValueError:
        result_label.config(text="Invalid input: Please enter valid numbers")

calculate_button = tk.Button(app, text="Calculate", command=perform_calculation)
calculate_button.grid(row=len(fields) + 2, columnspan=2)



app.mainloop()