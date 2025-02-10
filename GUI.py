import tkinter as tk
from tkinter import ttk, messagebox, Text, Entry, Button, Frame
from simulation import simulate, chart
from models import solution
from contextlib import contextmanager
import sys
import io

@contextmanager
def capture_output() -> io.StringIO:
    """Context manager to capture stdout output."""
    new_out = io.StringIO()
    old_out = sys.stdout
    sys.stdout = new_out
    try:
        yield sys.stdout
    finally:
        sys.stdout = old_out

def display_output(output: str) -> None:
    """Displays simulation outputs in the GUI."""
    text_output.configure(state="normal")
    text_output.insert(tk.END, output)
    text_output.insert(tk.END, "\n"+100*"="+"\n")
    text_output.configure(state="disabled")

def run_solution() -> None:
    """Runs the queuing solution and displays the output in the GUI."""
    try:
        # Retrieve inputs
        arrival_rate = float(entry_arrival_rate.get())
        service_rate = float(entry_service_rate.get())
        num_servers = int(entry_num_servers.get())
        capacity = entry_capacity.get()
        
        if capacity.strip():
            capacity = int(capacity)
        else:
            capacity = float('inf')

        # Capture the solution output
        with capture_output() as output:
            solution(arrival_rate, service_rate, num_servers, capacity)
        
        # Display the captured output
        display_output(output.getvalue())
    except Exception as e:
        messagebox.showerror("Error", f"{str(e)}")

def run_simulation() -> None:
    """Runs the queuing simulation and displays the output in the GUI."""
    try:
        # Retrieve inputs
        arrival_rate = float(entry_arrival_rate.get())
        service_rate = float(entry_service_rate.get())
        num_customers= int(entry_num_customers.get())

        # Capture the simulation output
        with capture_output() as output:
            simulate(arrival_rate, service_rate,num_customers)

        # Display the captured output
        display_output(output.getvalue())
            
            
            
        chart()
            
        
    except Exception as e:
        messagebox.showerror("Error", f"{str(e)}")

# Create the main window
root = tk.Tk()
root.title("Queueing System Simulator")
root.geometry("1200x800")  # Initial size

# Configure row and column weights to allow resizing
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=2)  # Input frame with proportion
root.rowconfigure(1, weight=0)  # Buttons frame (fixed)
root.rowconfigure(2, weight=2)  # Output frame with more proportion

# Input frame (Top)
frame_inputs = Frame(root, padx=5, pady=5)
frame_inputs.grid(row=0, column=0, sticky="nsew")
frame_inputs.columnconfigure(1, weight=1)  # Allow input fields to stretch

# Add input fields and labels to input_frame
label_num_servers = ttk.Label(frame_inputs, text="Number of Servers (c):")
label_num_servers.grid(row=2, column=0, sticky="w", padx=5, pady=2)
entry_num_servers = Entry(frame_inputs)
entry_num_servers.grid(row=2, column=1, sticky="ew", padx=5, pady=2)

label_service_rate = ttk.Label(frame_inputs, text="Service Rate (μ):")
label_service_rate.grid(row=1, column=0, sticky="w", padx=5, pady=2)
entry_service_rate = Entry(frame_inputs)
entry_service_rate.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

label_num_customers = ttk.Label(frame_inputs, text="Number of Customers:")
label_num_customers.grid(row=4, column=0, sticky="w", padx=5, pady=2)
entry_num_customers = Entry(frame_inputs)
entry_num_customers.grid(row=4, column=1, sticky="ew", padx=5, pady=2)

label_arrival_rate = ttk.Label(frame_inputs, text="Arrival Rate (λ):")
label_arrival_rate.grid(row=0, column=0, sticky="w", padx=5, pady=2)
entry_arrival_rate = Entry(frame_inputs)
entry_arrival_rate.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

label_capacity = ttk.Label(frame_inputs, text="System capacity (k) (leave empty for infinity): ")
label_capacity.grid(row=3, column=0, padx=5, pady=5, sticky="w")
entry_capacity = ttk.Entry(frame_inputs)
entry_capacity.grid(row=3, column=1,sticky="ew", padx=5, pady=5)

# Buttons frame (Middle)
buttons_frame = Frame(root, padx=5, pady=5)
buttons_frame.grid(row=1, column=0, sticky="nsew")

# Configure button frame layout
buttons_frame.columnconfigure(0, weight=1)

# Add buttons to buttons_frame
btn_run_solution = Button(buttons_frame, text="Run Solution", command=run_solution)
btn_run_solution.grid(row=0, column=0, sticky="ew", pady=2)

btn_run_simulation = Button(buttons_frame, text="Run Simulation", command=run_simulation)
btn_run_simulation.grid(row=1, column=0, sticky="ew", pady=2)

# Output frame (Bottom)
text_output = Text(root, wrap="word")
text_output.grid(row=2, column=0, sticky="nsew")

# Start the Tkinter event loop
root.mainloop()