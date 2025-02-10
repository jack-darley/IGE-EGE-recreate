from psychopy import monitors
import math
import tkinter as tk
import csv

class MonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x300")
        self.root.title("Monitor Selector")

        # Load options from CSV
        self.monitor_data = self.load_monitor_options("monitor_db.csv")
        self.options = list(self.monitor_data.keys())  # Monitor names

        # Dropdown Menu
        self.dropdown_var = tk.StringVar()
        if self.options:  # Set default only if options exist
            self.dropdown_var.set(self.options[0])

        self.dropdown = tk.OptionMenu(root, self.dropdown_var, *self.options)
        self.dropdown.config(width=15)
        self.dropdown.pack(pady=5)

        # Select Button
        self.select_button = tk.Button(root, text="Select Monitor",
                                        command=self.print_selection)
        self.select_button.pack()

        # Variable to store selected monitor data
        self.selected_specs = None

        # Quit button to close UI after selection
        self.quit_button = tk.Button(root, text="Confirm & Close", command=self.quit_app)
        self.quit_button.pack()

        
    def load_monitor_options(self, filename):
        """Load monitor options from a CSV file."""
        monitor_data = {}
        try:
            with open(filename, "r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    name = row[0]
                    monitor_data[name] = {
                        "width": int(row[1]),
                        "height": int(row[2]),
                        "size": float(row[3]),
                    }
        except FileNotFoundError:
            options = ["No monitors found"]
        return monitor_data
    
    def print_selection(self):
        selection = self.dropdown_var.get()
        specs = self.monitor_data.get(selection, {})

        # Extract values
        width = specs["width"]
        height = specs["height"]
        size = specs["size"]

        self.selected_specs = {
            "monitor_name": selection,
            "width": width,
            "height": height,
            "size": size
        }

    def quit_app(self):
        """Closes the Tkinter app."""
        self.root.quit()
        self.root.destroy()

    def get_selected_monitor(self):
        """Runs the Tkinter app and waits for selection."""
        self.root.mainloop()  # Start Tkinter loop
        return self.selected_specs  # Return selected monitor details

