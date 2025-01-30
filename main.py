import customtkinter as ctk
import os
from platform import system
# Static GUI Variables
PAD_X = 5
PAD_Y = 5
CORNER_RADIUS = 5


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set master frame settings
        ctk.set_appearance_mode("dark")
        self.title("CTK Application")
        self.window_width = 900
        self.window_height = 600
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.x_offset = (self.screen_width-self.window_width) // 2
        self.y_offset = (self.screen_height-self.window_height) // 2
        self.geometry(f"{self.window_width}x{self.window_height}+{self.x_offset}+{self.y_offset}")
        self.minsize(width=700, height=450)

        # Set custom icon for the window based on the OS
        self.set_window_icon_based_on_os()

        # Grid Config
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(2, weight=1)

        # Create Objects
        self.title_frame = TitleFrame(self)
        self.menu_frame = MenuFrame(self)
        self.default_app = DefaultApp(self)
        self.app_1_frame = App1Frame(self)
        self.app_2_frame = App2Frame(self)
        self.app_3_frame = App3Frame(self)
        self.app_4_frame = App3Frame(self)

        # Place Objects
        self.title_frame.grid(row=0, column=0, columnspan=3, pady=(0, PAD_Y*.5), sticky="ew")
        self.menu_frame.grid(row=1, column=0, padx=PAD_X, pady=PAD_Y, sticky="nsew")
        self.default_app.grid(row=1, column=1, columnspan=2, padx=(PAD_X, PAD_X * 1.5), pady=PAD_Y, sticky="nsew")
        self.app_1_frame.grid(row=1, column=1, columnspan=2, padx=(PAD_X, PAD_X*1.5), pady=PAD_Y, sticky="nsew")
        self.app_2_frame.grid(row=1, column=1, columnspan=2, padx=(PAD_X, PAD_X*1.5), pady=PAD_Y, sticky="nsew")
        self.app_3_frame.grid(row=1, column=1, columnspan=2, padx=(PAD_X, PAD_X*1.5), pady=PAD_Y, sticky="nsew")
        self.app_4_frame.grid(row=1, column=1, columnspan=2, padx=(PAD_X, PAD_X*1.5), pady=PAD_Y, sticky="nsew")
        self.default_app.tkraise()

    def set_window_icon_based_on_os(self):
        """Sets the window icon based on the operating system."""
        system_os = system()

        if system_os == "Windows":
            icon_path = ''  # Use .ico for Windows

            # Check if the file exists
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
            else:
                print(f"Error: The icon file {icon_path} does not exist in the directory.")
        else:
            icon_path = ''  # Use .png for Linux

            # Check if the file exists
            if os.path.exists(icon_path):
                pass
                # self.iconphoto(True, icon_path)
            else:
                print(f"Error: The icon file {icon_path} does not exist in the directory.")

    def reload_apps(self):
        # Generate Frames
        self.app_1_frame = App1Frame(self)
        self.app_2_frame = App2Frame(self)
        self.app_3_frame = App3Frame(self)
        self.app_4_frame = App4Frame(self)
        self.default_app = DefaultApp(self)

        # Place Frames
        self.default_app.grid(row=1, column=1, columnspan=2, padx=(PAD_X, PAD_X * 1.5), pady=PAD_Y, sticky="nsew")
        self.app_1_frame.grid(row=1, column=1, columnspan=2, padx=(PAD_X, PAD_X * 1.5), pady=PAD_Y, sticky="nsew")
        self.app_2_frame.grid(row=1, column=1, columnspan=2, padx=(PAD_X, PAD_X * 1.5), pady=PAD_Y, sticky="nsew")
        self.app_3_frame.grid(row=1, column=1, columnspan=2, padx=(PAD_X, PAD_X * 1.5), pady=PAD_Y, sticky="nsew")
        self.app_4_frame.grid(row=1, column=1, columnspan=2, padx=(PAD_X, PAD_X * 1.5), pady=PAD_Y, sticky="nsew")


class TitleFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Grid Config
        self.grid_rowconfigure(0, weight=1)  # Row 0 for the title (no expansion)
        self.grid_columnconfigure(0, weight=1)  # Single column, takes full width

        # Create Objects
        self.title_label = ctk.CTkLabel(self, text="App Title Frame",
                                        font=("Typewriter", 16, "bold"))

        # Place Objects
        self.title_label.grid(row=0, column=0, sticky="ew")

        self.change_title_frame()

    # Custom title_frame text color when appearance_mode is toggled
    def change_title_frame(self):
        """Changes the title label text color based on the appearance mode."""
        if ctk.get_appearance_mode() == "Light":
            self.title_label.configure(text_color="gray35")  # Light mode text color
        else:
            self.title_label.configure(text_color="gray65")  # Dark mode text color


# Base Frame for all app buttons
class MenuFrame(ctk.CTkFrame):

    def __init__(self, master: 'MainApp'):  # Specify the type of master as MainApp
        super().__init__(master)
        self.master = master

        self.apps = ["App 1", "App 2", "App 3", "App 4"]
        self.switch_var = ctk.StringVar(value="Dark Mode")

        # Grid Config
        self.configure(corner_radius=CORNER_RADIUS)
        self.rowconfigure(9, weight=1)

        # Create buttons for MenuFrame
        self.app_1 = ctk.CTkButton(self, text=self.apps[0], command=lambda: self.handle_app(0))
        self.app_2 = ctk.CTkButton(self, text=self.apps[1], command=lambda: self.handle_app(1))
        self.app_3 = ctk.CTkButton(self, text=self.apps[2], command=lambda: self.handle_app(2))
        self.app_4 = ctk.CTkButton(self, text=self.apps[3], command=lambda: self.handle_app(3))
        self.ui_switch = ctk.CTkSwitch(self, text="Dark Mode", variable=self.switch_var, onvalue="Dark Mode",
                                       offvalue="Light Mode", command=self.theme_switcher)

        # Place buttons
        self.app_1.grid(row=1, column=0, padx=PAD_X, pady=(20, 10), sticky="ew")
        self.app_2.grid(row=2, column=0, padx=PAD_X, pady=10, sticky="ew")
        self.app_3.grid(row=3, column=0, padx=PAD_X, pady=10, sticky="ew")
        self.app_4.grid(row=4, column=0, padx=PAD_X, pady=10, sticky="ew")
        self.ui_switch.grid(row=10, column=0, padx=PAD_X, pady=PAD_Y)

    # Handle button click for each app
    def handle_app(self, app_index):
        frame_mapping = [
            self.master.app_1_frame,
            self.master.app_2_frame,
            self.master.app_3_frame,
            self.master.app_4_frame
        ]

        if 0 <= app_index < len(frame_mapping):
            frame_mapping[app_index].tkraise()
            print(f"{self.apps[app_index]} selected")

    def theme_switcher(self):
        """ Switch appearance mode and update switch text """
        # Switch the appearance mode
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
            self.ui_switch.configure(text="Light Mode")  # Update text to "Light Mode"
        else:
            ctk.set_appearance_mode("Dark")
            self.ui_switch.configure(text="Dark Mode")  # Update text to "Dark Mode"

        # After switching appearance mode, update the title frame's text color.
        self.master.title_frame.change_title_frame()


# Waiting for app selection frame
class DefaultApp(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Frame Configuration/Variables
        self.configure(corner_radius=CORNER_RADIUS)

        # Grid Config
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Create Objects
        self.default_label = ctk.CTkLabel(self, text="Waiting for app selection...")

        # Place Objects
        self.default_label.grid(row=0, column=0, padx=PAD_X, pady=PAD_Y, sticky="nsew")


class App1Frame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # App Configuration/Variables

        # Grid Config
        self.rowconfigure(3, weight=1)
        self.columnconfigure([0, 10], weight=1)

        # Create Objects
        self.close_button = ctk.CTkButton(self, text="Close", width=30, command=self.master.reload_apps)
        self.placeholder = ctk.CTkLabel(self, text="Additional App Here")

        # Place Objects
        self.close_button.grid(row=0, column=11, padx=PAD_X, pady=PAD_Y, sticky="e")
        self.placeholder.grid(row=3, column=1, padx=PAD_X, pady=PAD_Y)


class App2Frame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # App Configuration/Variables

        # Grid Config
        self.rowconfigure(3, weight=1)
        self.columnconfigure([0, 10], weight=1)

        # Create Objects
        self.close_button = ctk.CTkButton(self, text="Close", width=30, command=self.master.reload_apps)
        self.placeholder = ctk.CTkLabel(self, text="Additional App Here")

        # Place Objects
        self.close_button.grid(row=0, column=11, padx=PAD_X, pady=PAD_Y, sticky="e")
        self.placeholder.grid(row=3, column=1, padx=PAD_X, pady=PAD_Y)


class App3Frame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # App Configuration/Variables

        # Grid Config
        self.rowconfigure(3, weight=1)
        self.columnconfigure([0, 10], weight=1)

        # Create Objects
        self.close_button = ctk.CTkButton(self, text="Close", width=30, command=self.master.reload_apps)
        self.placeholder = ctk.CTkLabel(self, text="Additional App Here")

        # Place Objects
        self.close_button.grid(row=0, column=11, padx=PAD_X, pady=PAD_Y, sticky="e")
        self.placeholder.grid(row=3, column=1, padx=PAD_X, pady=PAD_Y)


class App4Frame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # App Configuration/Variables

        # Grid Config
        self.rowconfigure(3, weight=1)
        self.columnconfigure([0, 10], weight=1)

        # Create Objects
        self.close_button = ctk.CTkButton(self, text="Close", width=30, command=self.master.reload_apps)
        self.placeholder = ctk.CTkLabel(self, text="Additional App Here")

        # Place Objects
        self.close_button.grid(row=0, column=11, padx=PAD_X, pady=PAD_Y, sticky="e")
        self.placeholder.grid(row=3, column=1, padx=PAD_X, pady=PAD_Y)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
