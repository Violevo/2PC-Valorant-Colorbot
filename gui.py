import os
import queue
import json
from threading import Thread
from tkinter import PhotoImage

try:
    import keyboard
except ImportError:
    os.system("pip install keyboard")
    import keyboard
try:
    import customtkinter
except ImportError:
    os.system("pip install customtkinter")
    import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue", "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()  

        # Load config
        with open('config.json', 'r') as file:
            config = json.load(file)

        # Update variables from config
        self.aim_key = config['TOGGLE_KEY']
        self.trigger_key = config['TRIGGER_KEY']
        self.trigger_delay = config['TRIGGER_DELAY']
        self.fov = config['FOV']
        self.accuracy = config['ACCURACY']
        self.shared_color = config['ENEMY_COLOR']
        self.resolution = config['RESOLUTION']

        self.formatted_resolution = 'x'.join(map(str, self.resolution))

        # Initialise variables
        self.key_queue = queue.Queue()
        self.current_key_target = None 

        # Configure window
        self.resizable(False, False)
        self.title("github.com/Violevo")
        self.iconbitmap("icon.ico")
        self.geometry("750x220")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame, 
            text="Coloraim v1.0.0", 
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Sidebar buttons to change pages
        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame, 
            text="Aimbot", 
            command=self.aimbot_button
        )
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = customtkinter.CTkButton(
            self.sidebar_frame, 
            text="Triggerbot", 
            command=self.trigger_button
        )
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_3 = customtkinter.CTkButton(
            self.sidebar_frame, 
            text="Misc", 
            command=self.misc_button
        )
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        # Main Content Frame (container for pages)
        self.content_frame = customtkinter.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, rowspan=6, sticky="nsew")

        # Create pages for each sidebar button
        self.aimbot_frame = customtkinter.CTkFrame(self.content_frame)
        self.triggerbot_frame = customtkinter.CTkFrame(self.content_frame)
        self.misc_frame = customtkinter.CTkFrame(self.content_frame)

        for frame in (self.aimbot_frame, self.triggerbot_frame, self.misc_frame):
            frame.grid(row=0, column=0, sticky="nsew")

        # ---------------------------
        # Aimbot Page (default)
        # ---------------------------
        self.switch_aim = customtkinter.CTkSwitch(
            master=self.aimbot_frame, 
            text="Enabled", 
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.switch_aim.grid(row=0, column=0, padx=20, pady=20)

        self.button_aim_key = customtkinter.CTkButton(
            master=self.aimbot_frame, 
            hover_color="grey", 
            fg_color="#343638", 
            border_color="#565B5E", 
            text="Key: " + self.aim_key, 
            command=lambda: self.change_key_text("aim"), 
            font=customtkinter.CTkFont(size=20)
        )
        self.button_aim_key.grid(row=0, column=1, padx=10, pady=20)

        self.combobox_aim_color = customtkinter.CTkComboBox(
            master=self.aimbot_frame, 
            fg_color="#343638", 
            border_color="#565B5E", 
            values=["Purple", "Red", "Yellow"], 
            command=self.color_change_callback,  # Updated callback for shared color
            font=customtkinter.CTkFont(size=20)
        )
        self.combobox_aim_color.grid(row=0, column=2, padx=10, pady=20)
        self.combobox_aim_color.set(self.shared_color)

        self.label_aim_FOV = customtkinter.CTkLabel(
            master=self.aimbot_frame, 
            text="FOV", 
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.label_aim_FOV.grid(row=1, column=0, padx=10, pady=20)

        self.slider_aim_FOV = customtkinter.CTkSlider(
            master=self.aimbot_frame, 
            command=self.FOV_slider_callback, 
            from_=0, to=360
        )
        self.slider_aim_FOV.grid(row=1, column=1, padx=0, pady=20)
        self.slider_aim_FOV.set(self.fov)

        self.label_aim_FOV_value = customtkinter.CTkLabel(
            master=self.aimbot_frame, 
            width=80, height=20, 
            font=customtkinter.CTkFont(size=20, weight="bold"),
            text=str(self.fov)
        )
        self.label_aim_FOV_value.grid(row=1, column=2, padx=0, pady=20)

        self.label_aim_precision = customtkinter.CTkLabel(
            master=self.aimbot_frame, 
            text="Accuracy", 
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.label_aim_precision.grid(row=2, column=0, padx=10, pady=20)

        self.slider_aim_precision = customtkinter.CTkSlider(
            master=self.aimbot_frame, 
            command=self.precision_slider_callback, 
            from_=0, to=100
        )
        self.slider_aim_precision.grid(row=2, column=1, padx=0, pady=20)
        self.slider_aim_precision.set(self.accuracy)

        self.label_aim_precision_value = customtkinter.CTkLabel(
            master=self.aimbot_frame, 
            width=80, height=20, 
            font=customtkinter.CTkFont(size=20, weight="bold"), 
            text=str(self.accuracy)
        )
        self.label_aim_precision_value.grid(row=2, column=2, padx=0, pady=20)

        # ---------------------------
        # Triggerbot Page
        # ---------------------------
        self.switch_trigger = customtkinter.CTkSwitch(
            master=self.triggerbot_frame, 
            text="Enabled", 
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.switch_trigger.grid(row=0, column=0, padx=20, pady=20)

        self.button_trigger_key = customtkinter.CTkButton(
            master=self.triggerbot_frame, 
            hover_color="grey", 
            fg_color="#343638", 
            border_color="#565B5E", 
            text="Key: " + self.trigger_key, 
            command=lambda: self.change_key_text("trigger"), 
            font=customtkinter.CTkFont(size=20)
        )
        self.button_trigger_key.grid(row=0, column=1, padx=10, pady=20)

        self.combobox_trigger_color = customtkinter.CTkComboBox(
            master=self.triggerbot_frame, 
            fg_color="#343638", 
            border_color="#565B5E", 
            values=["Purple", "Red", "Yellow"], 
            command=self.color_change_callback,  # Updated callback for shared color
            font=customtkinter.CTkFont(size=20)
        )
        self.combobox_trigger_color.grid(row=0, column=2, padx=10, pady=20)
        self.combobox_trigger_color.set(self.shared_color)

        self.label_trigger_delay = customtkinter.CTkLabel(
            master=self.triggerbot_frame, 
            text="Delay (ms)", 
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.label_trigger_delay.grid(row=1, column=0, padx=10, pady=20)

        self.slider_trigger_delay = customtkinter.CTkSlider(
            master=self.triggerbot_frame, 
            command=self.delay_slider_callback, 
            from_=25, to=500
        )
        self.slider_trigger_delay.grid(row=1, column=1, padx=0, pady=20)
        self.slider_trigger_delay.set(self.trigger_delay)

        self.label_trigger_delay_value = customtkinter.CTkLabel(
            master=self.triggerbot_frame, 
            width=80, height=20, 
            font=customtkinter.CTkFont(size=20, weight="bold"),
            text=str(self.trigger_delay)
        )
        self.label_trigger_delay_value.grid(row=1, column=2, padx=0, pady=20)

        # ---------------------------
        # Misc Page
        # ---------------------------

        self.label_resolution_input = customtkinter.CTkLabel(
            master=self.misc_frame, 
            text="Resolution: ", 
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.label_resolution_input.grid(row=0, column=0, padx=20, pady=20)

        self.resolution_input = customtkinter.CTkEntry(
            master=self.misc_frame, 
            fg_color="#343638", 
            border_color="#565B5E", 
            font=customtkinter.CTkFont(size=20),  # Font size of the input text
        )
        self.resolution_input.grid(row=0, column=1, padx=10, pady=20)
        self.resolution_input.insert(0,self.formatted_resolution)

        self.label_config_load = customtkinter.CTkLabel(
            master=self.misc_frame, 
            text="Load Config:", 
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.label_config_load.grid(row=1, column=0, padx=20, pady=20)

        self.button_config_load = customtkinter.CTkButton(
            master=self.misc_frame, 
            hover_color="grey", 
            fg_color="#343638", 
            border_color="#565B5E", 
            text="Load", 
            command = self.load_config, 
            font=customtkinter.CTkFont(size=20)
        )
        self.button_config_load.grid(row=1, column=1, padx=10, pady=20)

        self.label_config_save = customtkinter.CTkLabel(
            master=self.misc_frame, 
            text="Save Config:", 
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.label_config_save.grid(row=2, column=0, padx=20, pady=20)

        self.button_config_save = customtkinter.CTkButton(
            master=self.misc_frame, 
            hover_color="grey", 
            fg_color="#343638", 
            border_color="#565B5E", 
            text="Save", 
            command = self.save_config, 
            font=customtkinter.CTkFont(size=20)
        )
        self.button_config_save.grid(row=2, column=1, padx=10, pady=20)

        # Set the default page to Aimbot
        self.show_frame(self.aimbot_frame)

    def show_frame(self, frame):
        """Raise the given frame to the top of the content area."""
        frame.tkraise()

    def aimbot_button(self):
        self.show_frame(self.aimbot_frame)

    def trigger_button(self):
        self.show_frame(self.triggerbot_frame)

    def misc_button(self):
        self.show_frame(self.misc_frame)

    def on_key_event(self, key_event):
        key_name = key_event.name  # Get the pressed key's name
        self.key_queue.put(key_name)
        # Update the correct key button based on the current target.
        if self.current_key_target == "aim":
            self.aim_key = f"Key: {key_name}"
            self.button_aim_key.configure(text=self.aim_key)
        elif self.current_key_target == "trigger":
            self.trigger_key = f"Key: {key_name}"
            self.button_trigger_key.configure(text=self.trigger_key)
        # Reset the target after updating
        self.current_key_target = None

    def key_listener_thread(self):
        keyboard.on_press(self.on_key_event)
        keyboard.wait()

    def change_key_text(self, key_target):
        # Set which key button is to be updated and start the listener thread.
        self.current_key_target = key_target
        listener_thread = Thread(target=self.key_listener_thread, daemon=True)
        listener_thread.start()

    def color_change_callback(self, new_color):
        """This callback updates both color comboboxes to use the same shared color."""
        self.shared_color = new_color
        self.combobox_aim_color.set(new_color)
        self.combobox_trigger_color.set(new_color)
        self.shared_color = new_color

    def FOV_slider_callback(self, value):
        self.slider_aim_FOV.set(value)
        self.label_aim_FOV_value.configure(text=int(value))
        self.fov = value

    def delay_slider_callback(self, value):
        self.slider_trigger_delay.set(value)
        self.label_trigger_delay_value.configure(text=int(value))
        self.trigger_delay = value

    def precision_slider_callback(self, value):
        self.slider_aim_precision.set(value)
        self.label_aim_precision_value.configure(text=int(value))
        self.accuracy = value

    def load_config(self):
        with open('config.json', 'r') as file:
            config = json.load(file)
        
        self.aim_key = config['TOGGLE_KEY']
        self.trigger_key = config['TRIGGER_KEY']
        self.trigger_delay = config['TRIGGER_DELAY']
        self.fov = config['FOV']
        self.accuracy = config['ACCURACY']
        self.shared_color = config['ENEMY_COLOR']

        print("config loaded")

    def save_config(self):

        resolution = (self.resolution_input.get()).split('x')

        config = {
                    "TOGGLE_KEY": self.aim_key.removeprefix("Key: "),
                    "TRIGGER_KEY": self.trigger_key.removeprefix("Key: "),
                    "TRIGGER_DELAY": round(self.trigger_delay),
                    "FOV": round(self.fov),
                    "ACCURACY": round(self.accuracy),
                    "RESOLUTION": resolution,
                    "ENEMY_COLOR": self.shared_color
                }

        with open("config.json", "w") as file:
            json.dump(config, file, indent=4)

        print("saved config")


if __name__ == "__main__":
    app = App()
    app.mainloop()
