import tkinter as tk
import time
import random
from tkdial import Meter
import threading
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from scipy.ndimage.filters import uniform_filter1d
import matplotlib.style as style
import webbrowser # this is for the hyperlink for the documentation button
import sys # this is for the exit button function



#function for the dial
class dial():
    def update():
        while True:
            z = dial.GUI.ParsePacket()
            meter1.set(z)
            print(z)
            time.sleep(time_between_updates) # sleeps that may the dial is smoothed out
    class GUI():
        def ParsePacket():
            n = random.randint(0, 10)
            return n
        
# function is for the graph
def update_plot(frame):
    y = [random.randint(0, 30) for _ in range(101)]
    smoothed_y = uniform_filter1d(y, size=10)
    plot.clear()
    plot.plot(smoothed_y)
    plot.set_ylim(0, 30)
    plot.set_xlim(0, len(smoothed_y))
    plot.set_xlabel('MPH')
    plot.set_ylabel('TIME')

def documentation_link():
    webbrowser.open_new(r"https://github.com/BCsuperhighmileage/Speedometer-MK2")


def exit_function():
    timestamps_file = open("timestamps.csv", "w")
    timestamps_file.truncate() # clears the csv file
    timestamps_file.close()
    sys.exit()

def reset_graph():
    fig.clf() # clears the old graph

    # creates the new graph
    fig = Figure(figsize=(10, 5.1), dpi=100)
    plot = fig.add_subplot(111)
    graph = FigureCanvasTkAgg(fig, master=window)
    graph.draw()
    graph.get_tk_widget().grid(column=1, row=0, columnspan=4, sticky='NESW')

    # Define the animation
    ani = animation.FuncAnimation(fig, update_plot, interval=1000)

    # Set the x-axis and y-axis labels
    plot.set_xlabel('TIME')
    plot.set_ylabel('MPH')

def reset_program():
    reset_graph()
    timestamps_file = open("timestamps.csv", "w")
    timestamps_file.truncate() # clears the csv file
    timestamps_file.close()
    #TODO have this reset the incoming data flow


time_between_updates = 0.1

# setting up the colors of the graph
# view all the colors available for tkinter: http://cs111.wellesley.edu/archive/cs111_fall14/public_html/labs/lab12/tkintercolor.html
MAIN_COLOR = 'white'
SECONDARY_COLOR = 'black'

### START of Setup
window = tk.Tk()

window.geometry("1400x1400")
window.configure(bg=MAIN_COLOR) # default is dark gray

#TODO # What does this do?
window.columnconfigure(1, weight=1, minsize=75)
window.rowconfigure(1, weight=1, minsize=50)


frame = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=1
    )
frame.grid(row=1, column=0, padx=4, pady=4)
### END of Setup



### START of Dial and Label
#TODO
"""
# label for the speedometer
speed_label = tk.Label(window, text ="Speedometer(mph)", bg=MAIN_COLOR, fg=SECONDARY_COLOR)
speed_label.place(x=100, y=400)

# label for the graph
graph_label = tk.Label(window, text ="Change of speed over time(sec)", bg=MAIN_COLOR, fg=SECONDARY_COLOR)
graph_label.place(x=800, y=500)
"""







# Create a frame for the speedometer
speedometer_frame = tk.Frame(master=window)
speedometer_frame.grid(row=0, column=0, padx=40, pady=80, sticky='W')
speedometer_frame.configure(bg=MAIN_COLOR)

# dial
meter1 = Meter(speedometer_frame, start=0, end=160, start_angle=260, end_angle=-340,
               major_divisions=30, minor_divisions=5, fg=MAIN_COLOR, scale_color=SECONDARY_COLOR, needle_color="red",
               text_font="DS-Digital 10", text_color=SECONDARY_COLOR, state="disabled", scroll=False)
meter1.pack(fill='both', expand=True)

# graph

# the figure that will contain the plot for the graph
fig = Figure(figsize=(10, 5.1), dpi=100)
plot = fig.add_subplot(111)

# creating the graph using Tkinter and Matplotlib
graph = FigureCanvasTkAgg(fig, master=window)
graph.draw()
graph.get_tk_widget().grid(column=1, row=0, columnspan=4, sticky='NESW')




# Define the animation
ani = animation.FuncAnimation(fig, update_plot, interval=1000)

# Set the x-axis and y-axis labels
plot.set_xlabel('TIME')
plot.set_ylabel('MPH')

### END of Dial And Graph



# this makes a frame under the other frame
# this makes the 2 frames separated so they do not influence eachother 
# without this the sizing would be off
framer = tk.Frame(window, bg=MAIN_COLOR)
framer.place(relx=0, rely=0.6, relwidth=1, relheight=0.5)


### START of Control Center

# setting up the frame
control_center_frame = ctk.CTkFrame(framer)
control_center_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

# create the main label for the info box
control_center_frame_main_text = ctk.CTkLabel(master=control_center_frame, text="Control Center")
control_center_frame_main_text.grid(row=0, column=0, columnspan=1, padx=10, pady=10)


# buttons for the controls
graph_button_1 = ctk.CTkButton(master=control_center_frame, border_width=2, text="Debug Mode")
graph_button_1.grid(row=1, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

graph_switch_1 = ctk.CTkSwitch(master=control_center_frame, border_width=2, text="Input Fake Data")
graph_switch_1.grid(row=2, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")




# graph control of buttons
graph_button_1 = ctk.CTkButton(master=control_center_frame, border_width=2, text="Reset Graph", command=reset_graph)
graph_button_1.grid(row=0, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

documentation_button = ctk.CTkButton(master=control_center_frame, border_width=2, text="Documentation", command=documentation_link) # TODO link to Github README
documentation_button.grid(row=1, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

# Basic Function Buttons
exit_button = ctk.CTkButton(master=control_center_frame, border_width=2, text="Exit", command=exit_function)
exit_button.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

reset_button = ctk.CTkButton(master=control_center_frame, border_width=2, text="Reset")
reset_button.grid(row=1, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")


# slider 1
graph_settings_slider_label = ctk.CTkLabel(master=control_center_frame, text="Maximum MPH(1-50)")
graph_settings_slider_label.grid(row=4, column=1, columnspan=1, padx=10, pady=10)

graph_settings_slider_1 = ctk.CTkSlider(master=control_center_frame, from_=1, to=50, number_of_steps=49)
graph_settings_slider_1.grid(row=5, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")


# slider 2
graph_settings_slider_label = ctk.CTkLabel(master=control_center_frame, text="Number of Updates per Minute")
graph_settings_slider_label.grid(row=4, column=2, columnspan=1, padx=10, pady=10)

graph_settings_slider_2 = ctk.CTkSlider(master=control_center_frame, from_=0, to=500, number_of_steps=50)
graph_settings_slider_2.grid(row=5, column=2, padx=(20, 10), pady=(10, 10), sticky="ew")

### END of Control Center







### End of Code
threading.Thread(target=dial.update).start() # start this loop with threading
window.mainloop()