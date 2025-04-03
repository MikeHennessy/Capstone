import tkinter as tk
import os
from datetime import datetime

def shutdown():
    os.system("sudo shutdown now")  # Emergency shutdown

def reset_panel():
    # Add reset panel functionality here
    pass

# Create the main window
root = tk.Tk()
root.title("Raspberry Pi Touch UI")
root.attributes('-fullscreen', True)  # Fullscreen for touch
root.configure(bg='black')  # Set background to black

# Make elements more touch-friendly
button_pady = 20
button_padx = 40
button_font = ('Arial', 32)
label_font = ('Arial', 28)
small_font = ('Arial', 20)

# Top Frame (Time and Location)
top_frame = tk.Frame(root, bg='black')
top_frame.pack(fill=tk.X, padx=10, pady=10)

# Time on left
time_label = tk.Label(top_frame, text="--:--:--", font=label_font, fg='white', bg='black')
time_label.pack(side=tk.LEFT, padx=20)

# Location in center (latitude and longitude)
location_frame = tk.Frame(top_frame, bg='black')
location_frame.pack(side=tk.LEFT, expand=True)

latitude_label = tk.Label(location_frame, text="Lat: --°", font=small_font, fg='white', bg='black')
latitude_label.pack(pady=5)

longitude_label = tk.Label(location_frame, text="Lon: --°", font=small_font, fg='white', bg='black')
longitude_label.pack(pady=5)

# Middle Frame (Controls and Energy)
middle_frame = tk.Frame(root, bg='black')
middle_frame.pack(expand=True, pady=20)

# Reset panel button (larger for touch)
reset_btn = tk.Button(
    middle_frame,
    text="RESET PANEL TO FLAT",
    font=button_font,
    bg='gray20',
    fg='white',
    command=reset_panel,
    activebackground='gray30',
    activeforeground='white',
    borderwidth=5,
    relief=tk.RAISED,
    padx=button_padx,
    pady=button_pady
)
reset_btn.pack(pady=20)

# Emergency shutdown button (big & red)
shutdown_btn = tk.Button(
    middle_frame,
    text="EMERGENCY SHUT OFF",
    font=button_font,
    bg='red',
    fg='white',
    command=shutdown,
    activebackground='darkred',
    activeforeground='white',
    borderwidth=5,
    relief=tk.RAISED,
    padx=button_padx,
    pady=button_pady
)
shutdown_btn.pack(pady=20)

# Energy generated today
energy_label = tk.Label(
    middle_frame,
    text="Energy Today: 0.0 kWh",
    font=label_font,
    fg='white',
    bg='black'
)
energy_label.pack(pady=20)

# Bottom Frame (Power metrics)
bottom_frame = tk.Frame(root, bg='black')
bottom_frame.pack(fill=tk.X, padx=10, pady=20)

# Make bottom metrics larger for touch
metric_font = ('Arial', 24)

# Power metrics
power_frame = tk.Frame(bottom_frame, bg='black')
power_frame.pack(side=tk.LEFT, expand=True)

power_label = tk.Label(power_frame, text="Power: -- W", font=metric_font, fg='white', bg='black')
power_label.pack(pady=10)

voltage_frame = tk.Frame(bottom_frame, bg='black')
voltage_frame.pack(side=tk.LEFT, expand=True)

voltage_label = tk.Label(voltage_frame, text="Voltage: -- V", font=metric_font, fg='white', bg='black')
voltage_label.pack(pady=10)

current_frame = tk.Frame(bottom_frame, bg='black')
current_frame.pack(side=tk.LEFT, expand=True)

current_label = tk.Label(current_frame, text="Current: -- A", font=metric_font, fg='white', bg='black')
current_label.pack(pady=10)

# Add visual feedback for touch
def on_press(btn):
    btn.config(relief=tk.SUNKEN)

def on_release(btn):
    btn.config(relief=tk.RAISED)
    # Execute command after release (more natural for touch)
    btn.invoke()

# Bind touch feedback to buttons
for btn in [reset_btn, shutdown_btn]:
    btn.bind('<ButtonPress-1>', lambda e, b=btn: on_press(b))
    btn.bind('<ButtonRelease-1>', lambda e, b=btn: on_release(b))

# Update data periodically
def update_data():
    # Update time
    current_time = datetime.now().strftime("%H:%M:%S")
    time_label.config(text=current_time)
    
    # Simulate location data (replace with real GPS data)
    latitude_label.config(text="Lat: 34.05°")
    longitude_label.config(text="Lon: -118.24°")
    
    # Simulate power metrics (replace with real sensor data)
    power_label.config(text="Instantaneous Power: 1250 W")
    voltage_label.config(text="Voltage: 240 V")
    current_label.config(text="Current: 5.2 A")
    energy_label.config(text="Energy Generated Today: 12.5 kWh")
    
    root.after(1000, update_data)  # Update every second

update_data()  # Start updates
root.mainloop()