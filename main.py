import tkinter as tk
import constants
import random
from validation import validate_integer, validate_string, validate_float, fields


app = tk.Tk()
app.title("Nostale Upgrade Simulator")


entry_list = []

entry_list = []

for i, field in enumerate(fields):
    label = tk.Label(app, text=field["label"])
    label.grid(row=i, column=0, sticky="w")

    entry = tk.Entry(app)
    entry.grid(row=i, column=1)
    
    entry_list.append(entry)

result_label = tk.Label(app, text="")
result_label.grid(row=len(fields), columnspan=2)

def perform_calculation():
    try:
        values = [entry.get() for entry in entry_list]


        if not all(validate_integer(entry) or validate_float(entry) for entry in entry_list):
            result_label.config(text="Invalid input: Please enter valid numbers")
            return


        numeric_values = [int(value) if validate_integer(entry) else float(value) for value, entry in zip(values, entry_list)]
        
        simCount = 0
        upgr_cost = 0
        while simCount < numeric_values[6]:
            base_upgrLvl = numeric_values[0]
            while base_upgrLvl < numeric_values[1]:
                upgr_cost += constants.wings[base_upgrLvl]*numeric_values[2] + constants.fms[base_upgrLvl]*numeric_values[3] + constants.upitems[base_upgrLvl]*numeric_values[4] + constants.gold[base_upgrLvl]
                random_number = random.randint(0,99)
                #Success with scroll
                if random_number < constants.up_chance[base_upgrLvl] and base_upgrLvl >= 2:
                    base_upgrLvl += 1
                    upgr_cost += numeric_values[5]
                #Fail with scroll -> Return materal cost
                elif random_number > constants.up_chance[base_upgrLvl] and base_upgrLvl >= 2:
                    upgr_cost += numeric_values[5] - constants.upitems[base_upgrLvl]*numeric_values[4]
                #Success without scroll
                elif random_number < constants.up_chance[base_upgrLvl] and base_upgrLvl < 2:
                    base_upgrLvl += 1
                #Fail without scroll -> same cost as success, just dont increase upgrLvl
                
            simCount += 1
        result = upgr_cost/simCount

        result_label.config(text=f"Result: {result:.2f}")

    except ValueError:
        result_label.config(text="Invalid input: Please enter valid numbers")

calculate_button = tk.Button(app, text="Calculate", command=perform_calculation)
calculate_button.grid(row=len(fields) + 1, columnspan=2)

app.mainloop()