import tkinter as tk
from tkinter import ttk
import simulation
from parameters import genes, interactions, promoter_rates

def run_gui():
    # Set up the main app window
    root = tk.Tk()
    root.title("Gene Expression Simulator")

    # Sync the text entry when the slider is moved
    def update_entry_when_slider_moves(var, entry_field):
        def callback(*_):
            # Only update the entry if it's not currently being edited
            if entry_field.focus_get() != entry_field:
                entry_field.delete(0, tk.END)
                entry_field.insert(0, f"{var.get():.2f}")
        return callback

    # Sync the slider when text entry is changed
    def update_slider_on_entry_change(var, entry_field):
        def callback():
            val = float(entry_field.get())
            var.set(val)
  
        return callback

    row_idx = 0

    # How much influence proteins have on mRNA expression
    ttk.Label(root, text="Interaction Weights").grid(row=row_idx, columnspan=3)
    row_idx += 1

    for pair in interactions:
        src, tgt = pair
        label_text = f"{src} -> {tgt}"
        ttk.Label(root, text=label_text).grid(row=row_idx, column=0)

        weight_var = tk.DoubleVar()
        simulation.interaction_weights[(src, tgt)] = weight_var

        # Slider from -1 to 1 for interaction strength
        weight_slider = ttk.Scale(root, from_=-1, to=1, orient="horizontal", length=200, variable=weight_var)
        weight_slider.grid(row=row_idx, column=1)

        # Entry box for manual value input
        weight_entry = ttk.Entry(root, width=6)
        weight_entry.grid(row=row_idx, column=2)
        weight_entry.insert(0, "0.0")  # Default value

        weight_var.trace_add("write", update_entry_when_slider_moves(weight_var, weight_entry))
        weight_entry.bind("<Return>", update_slider_on_entry_change(weight_var, weight_entry))

        row_idx += 1

    ttk.Label(root, text="Promoter Transition Rates").grid(row=row_idx, columnspan=3, pady=(10, 0))
    row_idx += 1

    for gene_name in genes:
        # Initisalise transition dictionary
        simulation.promoter_transition[gene_name] = {}

    
        transition_parameters = [
            ("OFF -> INITIATED", "off_to_initiated" ),
            ("INITIATED -> ON", "initiated_to_on"),
            ("INITIATED -> OFF", "initiated_to_off"),
            ("ON -> OFF", "on_to_off"),
        ]

        # Creating sliders for transition probability
        for label, key in transition_parameters:
            
            ttk.Label(root, text=f"{gene_name} {key}").grid(row=row_idx, column=0)

            initial_val = promoter_rates[gene_name][key]
            promoter_var = tk.DoubleVar(value=initial_val)
            simulation.promoter_transition[gene_name][key] = promoter_var

            promoter_slider = ttk.Scale(root, from_=0.0, to=1.0, orient="horizontal", length=200, 
                                        variable=simulation.promoter_transition[gene_name][key])
            
            promoter_slider.grid(row=row_idx, column=1)
            promoter_entry = ttk.Entry(root, width=6)
            promoter_entry.grid(row=row_idx, column=2)
            promoter_entry.insert(0, f"{initial_val:.2f}")

            promoter_var.trace_add("write", update_entry_when_slider_moves(promoter_var, promoter_entry))
            promoter_entry.bind("<Return>", update_slider_on_entry_change(promoter_var, promoter_entry))

            row_idx += 1

    # Run simulation button (hooks into simulation module)
    ttk.Button(root, text="Run Simulation", command=simulation.simulation).grid(row=row_idx, columnspan=3, pady=10)

    # Fire up the GUI loop
    root.mainloop()
