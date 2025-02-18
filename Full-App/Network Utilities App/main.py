import customtkinter as ctk
import ipaddress
import os
import logging
import netmiko
import pandas as pd
import paramiko
import threading
import time
import queue as q
import socket
from PIL import Image
from platform import system
from tkinter import filedialog, scrolledtext
# Static Variables
PAD_X = 5
PAD_Y = 5
CORNER_RADIUS = 5
ctk.set_appearance_mode("dark")
images = [
            ctk.CTkImage(Image.open('Images/hide.png'), size=(26, 26)),
            ctk.CTkImage(Image.open('Images/show.png'), size=(26, 26))
]
logging.basicConfig(
            filename="Logs/log.log",
            filemode="a",
            format="{asctime} - {levelname} - {message}",
            style="{",
            datefmt="%Y-%m-%d %H:%M"
        )


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set master frame settings
        self.title("Network Apps")
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
        self.app_1_frame = App1Frame(self)
        self.app_2_frame = App2Frame(self)
        self.app_3_frame = App3Frame(self)
        self.app_4_frame = App4Frame(self)
        self.default_app_frame = DefaultAppFrame(self)

        # Place Objects
        self.title_frame.grid(row=0, column=0, columnspan=3, pady=(0, PAD_Y*.5), sticky="ew")
        self.menu_frame.grid(row=1, column=0, padx=PAD_X, pady=PAD_Y, sticky="nsew")
        self.app_1_frame.grid(row=1, column=1, columnspan=2, padx=(PAD_X, PAD_X*1.5), pady=PAD_Y, sticky="nsew")
        self.app_2_frame.grid(row=1, column=1, columnspan=2, padx=(PAD_X, PAD_X*1.5), pady=PAD_Y, sticky="nsew")
        self.app_3_frame.grid(row=1, column=1, columnspan=2, padx=(PAD_X, PAD_X*1.5), pady=PAD_Y, sticky="nsew")
        self.app_4_frame.grid(row=1, column=1, columnspan=2, padx=(PAD_X, PAD_X*1.5), pady=PAD_Y, sticky="nsew")
        self.default_app_frame.grid(row=1, column=1, columnspan=2, padx=(PAD_X, PAD_X*1.5), pady=PAD_Y, sticky="nsew")

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
        self.default_app_frame = DefaultAppFrame(self)

        # Place Frames
        self.default_app_frame.grid(row=1, column=1, columnspan=2, padx=(PAD_X, PAD_X * 1.5), pady=PAD_Y, sticky="nsew")
        self.app_1_frame.grid(row=1, column=1, columnspan=2, padx=(PAD_X, PAD_X * 1.5), pady=PAD_Y, sticky="nsew")
        self.app_2_frame.grid(row=1, column=1, columnspan=2, padx=(PAD_X, PAD_X * 1.5), pady=PAD_Y, sticky="nsew")
        self.app_3_frame.grid(row=1, column=1, columnspan=2, padx=(PAD_X, PAD_X * 1.5), pady=PAD_Y, sticky="nsew")
        self.app_4_frame.grid(row=1, column=1, columnspan=2, padx=(PAD_X, PAD_X * 1.5), pady=PAD_Y, sticky="nsew")

    @staticmethod
    def generate_popup(title, description):
        popup = ctk.CTkToplevel()

        # Force popup to require action
        popup.grab_set()

        # Get screen width and height
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()

        # Get x and y coord for the popup
        x = (screen_width - 400) // 2  # width of popup
        y = (screen_height - 100) // 2  # height of popup

        # Popup UI
        popup.geometry(f'400x100+{x}+{y}')
        popup.title(title)
        popuplabel = ctk.CTkLabel(popup, text=description)
        popuplabel.grid(row=0, column=0, padx=PAD_X, pady=PAD_Y)
        popupbutton = ctk.CTkButton(popup, text="Acknowledge", command=popup.destroy)
        popupbutton.grid(row=2, column=0, padx=PAD_X, pady=PAD_Y)
        popup.columnconfigure(0, weight=1)
        popup.rowconfigure(1, weight=1)


# CCHCS Title Frame
class TitleFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Grid Config
        self.grid_rowconfigure(0, weight=1)  # Row 0 for the title (no expansion)
        self.grid_columnconfigure(0, weight=1)  # Single column, takes full width

        # Create Objects
        self.title_label = ctk.CTkLabel(self, text="NETWORK SERVICES",
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
    apps = ["Credential Test", "Command Runner", "CIDR Calculator", "Packet Capture"]

    def __init__(self, master: 'MainApp'):  # Specify the type of master as MainApp
        super().__init__(master)
        self.master = master

        self.switch_var = ctk.StringVar(value="Dark Mode")

        # Grid Config
        self.configure(corner_radius=CORNER_RADIUS)
        self.rowconfigure(9, weight=1)

        # Create buttons for MenuFrame
        self.app_1 = ctk.CTkButton(self, text=self.apps[0], command=lambda: self.handle_app(1))
        self.app_2 = ctk.CTkButton(self, text=self.apps[1], command=lambda: self.handle_app(2))
        self.app_3 = ctk.CTkButton(self, text=self.apps[2], command=lambda: self.handle_app(3))
        self.app_4 = ctk.CTkButton(self, text=self.apps[3], command=lambda: self.handle_app(4))
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
            self.master.default_app_frame,
            self.master.app_1_frame,
            self.master.app_2_frame,
            self.master.app_3_frame,
            self.master.app_4_frame
        ]

        app_names = [
            "Default App",
            "Credential Tester",
            "Command Runner",
            "CIDR Calculator",
            "Packet Capture"
        ]

        if 0 <= app_index <= len(frame_mapping):
            frame_mapping[app_index].tkraise()

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
class DefaultAppFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Frame Configuration/Variables
        self.configure(corner_radius=CORNER_RADIUS)

        # Grid Config
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Create Objects
        self.default_label = ctk.CTkLabel(self, text="Waiting for app selection...")
        self.revision_number = ctk.CTkLabel(self, text="Version 1.1", font=("Arial", 10, "italic"))

        # Place Objects
        self.default_label.grid(row=0, column=0, padx=PAD_X, pady=PAD_Y, sticky="nsew")
        self.revision_number.grid(row=2, column=0, columnspan=3)


class App1Frame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # App Configuration/Variables
        self.default_button_color = ['#3a7ebf', '#1f538d']
        self.validated = False
        self.validate_button_color = "orange"
        self.validate_text_color = "black"
        self.current_image = 0
        self.results = []
        self.file_path = ""
        self.start_time = 0.0
        self.queue = q.Queue()

        # Grid Config
        self.rowconfigure(15, weight=1)
        self.columnconfigure(1, weight=1)

        # Create Objects
        self.close_button = ctk.CTkButton(self, text="X", fg_color="red4", hover_color="firebrick3", width=10,
                                          height=10, command=self.master.reload_apps)
        self.label = ctk.CTkLabel(self, text="SSH Credential Check", font=("Roboto", 20))
        self.select_file = ctk.CTkButton(self, text="Import CSV", command=self.import_csv, width=50)
        self.program_description = ctk.CTkLabel(self,
                                                text="CSV must contain a column named 'device_name' and 'ip_address'")
        self.tacacs_user = ctk.CTkEntry(self, placeholder_text="TACACS Username", width=175)
        self.tacacs_pwd = ctk.CTkEntry(self, placeholder_text="TACACS Password", width=175, show="*")
        self.dnac_ro_pwd = ctk.CTkEntry(self, placeholder_text="DNAC Password", width=175, show="*")
        self.local_pwd = ctk.CTkEntry(self, placeholder_text="Local Device Password", width=175,
                                      show="*", )
        self.image_button = ctk.CTkButton(self, text="", image=images[self.current_image], compound="left",
                                          fg_color="transparent", width=26, command=self.toggle_hide)
        self.submit_button = ctk.CTkButton(self, text="Check Fields", command=self.validate)
        self.progress_bar = ctk.CTkProgressBar(self)

        # Place Objects
        self.close_button.grid(row=0, column=1, padx=PAD_X, pady=PAD_Y, sticky="e")
        self.label.grid(row=2, column=1, padx=PAD_X, pady=PAD_Y)
        self.select_file.grid(row=3, column=1, padx=PAD_X, pady=PAD_Y)
        self.program_description.grid(row=4, column=1, padx=PAD_X, pady=PAD_Y)
        self.tacacs_user.grid(row=5, column=1, padx=PAD_X, pady=PAD_Y)
        self.tacacs_pwd.grid(row=6, column=1, padx=PAD_X, pady=PAD_Y)
        self.dnac_ro_pwd.grid(row=7, column=1, padx=PAD_X, pady=PAD_Y)
        self.local_pwd.grid(row=8, column=1, padx=PAD_X, pady=PAD_Y)
        self.image_button.grid(row=9, column=1, padx=PAD_X, pady=PAD_Y)
        self.submit_button.grid(row=10, column=1, padx=PAD_X, pady=PAD_Y)

    def import_csv(self):
        # Open file dialog to select file
        self.file_path = filedialog.askopenfilename()

        if self.file_path:
            # Check if the file extension is .csv
            if not self.file_path.lower().endswith('.csv'):
                self.program_description.configure(text="Please select a CSV file.",
                                                   text_color="firebrick1")
                self.master.generate_popup("Error", "The selected file is not a CSV file.")
                return  # Exit the function if the file is not a CSV

            # If the file is CSV, proceed with further validation
            accepted_columns = ["Device_Name", "IP_Address"]
            try:
                # Read the CSV into a DataFrame
                df = pd.read_csv(self.file_path)

                # Validate the columns in the CSV
                for col in df.columns:
                    if col not in accepted_columns:
                        self.program_description.configure(text=f"'Device_Name' or 'IP_Address' column not found.",
                                                           text_color="firebrick1")
                        self.master.generate_popup("Error", "CSV column names are incorrect.")
                        self.validated = False
                        return  # Exit the function if columns are not correct
                # If the columns are correct
                self.program_description.configure(text="Import successful!", text_color="green")
                self.validated = True

            except Exception as e:
                # Handle errors that might occur during CSV reading (e.g., file format issues)
                self.program_description.configure(text=f"Error reading the file: {str(e)}",
                                                   text_color="firebrick1")
                self.master.generate_popup("Error", f"Error: {str(e)}")

    def toggle_hide(self):
        if self.current_image == 0:
            self.current_image = 1
            self.image_button.configure(image=images[1])
            self.tacacs_pwd.configure(show="")
            self.dnac_ro_pwd.configure(show="")
            self.local_pwd.configure(show="")
        else:
            self.current_image = 0
            self.image_button.configure(image=images[0])
            self.tacacs_pwd.configure(show="*")
            self.dnac_ro_pwd.configure(show="*")
            self.local_pwd.configure(show="*")

    def check_fields(self):
        if not self.tacacs_user.get():
            self.tacacs_user.configure(border_color="red")
        else:
            self.tacacs_user.configure(border_color="green")
        if not self.tacacs_pwd.get():
            self.tacacs_pwd.configure(border_color="red")
        else:
            self.tacacs_pwd.configure(border_color="green")
        if not self.dnac_ro_pwd.get():
            self.dnac_ro_pwd.configure(border_color="red")
        else:
            self.dnac_ro_pwd.configure(border_color="green")
        if not self.local_pwd.get():
            self.local_pwd.configure(border_color="red")
        else:
            self.local_pwd.configure(border_color="green")

    def validate(self):
        self.check_fields()
        if (self.tacacs_user.get() and self.tacacs_pwd.get() and self.dnac_ro_pwd.get() and self.local_pwd.get()
                and self.validated):
            self.submit_button.configure(text="Execute", command=self.execute, fg_color="green", hover_color="green")
            self.check_fields()
        else:
            self.submit_button.configure(text="Validate", fg_color=self.validate_button_color,
                                         text_color=self.validate_text_color)
            self.master.generate_popup("Validation Failed", "Fields are missing information or the CSV file is bad.")

    def execute(self):
        threading.Thread(target=self.execute_task).start()

    def execute_task(self):
        start_time = time.time()
        logging.warning(f'------------------------------ Start runtime Log ------------------------------')
        print(self.tacacs_user.get())
        print(self.tacacs_pwd.get())
        time.sleep(1)
        print(self.dnac_ro_pwd.get())
        print(self.local_pwd.get())
        self.load_devices_data()
        self.assign_workers(8)
        self.master.generate_popup("Success", f"Runtime: {round((time.time() - start_time), 2)} seconds.")
        self.master.reload_apps()

    def execute_progress(self):
        start_qsize = self.queue.qsize()
        self.progress_bar.grid(row=14, column=1)
        self.update()
        while not self.queue.empty():
            progress = start_qsize - self.queue.qsize()
            self.master.after(0, self.update_progress_bar, progress)

    def update_progress_bar(self, progress):
        self.progress_bar.set(progress)
        self.progress_bar.update()

    def load_devices_data(self):
        df = pd.read_csv(self.file_path)
        df.columns = [c.replace(' ', '_') for c in df.columns]
        data_dict = df.to_dict(orient='records')
        for device in data_dict:
            self.queue.put(device)

    def worker(self):
        while True:
            try:
                host = self.queue.get(timeout=1)  # Add timeout to avoid indefinite blocking
                self.connect(host)
                self.queue.task_done()  # Mark task done
            except q.Empty:
                break

    def assign_workers(self, threads):
        threads_list = []
        thread_event = threading.Event()  # Event to signal completion of workers

        def worker_thread():
            self.worker()
            thread_event.set()  # Signal that worker is done

        for t in range(threads):
            thread = threading.Thread(target=worker_thread)
            threads_list.append(thread)
            thread.start()

        for thread in threads_list:
            thread.join()  # Wait for all threads to complete
            thread_event.clear()  # Reset the event

    # SSH Function
    def connect(self, host):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        device_dict = {
            "Device_Name": host["Device_Name"],
            "IP_Address": host["IP_Address"],
            "Status": ""
        }
        try:
            print(f'Attempting SSH to {host["IP_Address"]} using TACACS.')
            logging.warning(f'Attempting SSH to {host["IP_Address"]} using TACACS.')
            ssh.connect(hostname=host["IP_Address"], username=self.tacacs_user.get(), password=self.tacacs_pwd.get(),
                        timeout=3)
            device_dict["Status"] = "Success"
            print(f'TACACS Authentication to {host["IP_Address"]} was successful.')
            logging.warning(f'TACACS Authentication to {host["IP_Address"]} was successful.')
        except paramiko.ssh_exception.NoValidConnectionsError:
            device_dict["Status"] = "Connection Failure"
            print(f'Connection to {host["IP_Address"]} was unsuccessful.')
            logging.critical(f'Connection to {host["IP_Address"]} was unsuccessful.')
        except (paramiko.SSHException, paramiko.AuthenticationException, paramiko.BadAuthenticationType):
            try:
                print(f'User TACACS Failed. Attempting SSH to {host["IP_Address"]} using RO TACACS.')
                logging.critical(f'User TACACS Failed. Attempting SSH to {host["IP_Address"]} using RO TACACS.')
                ssh.connect(hostname=host["IP_Address"], username="dnac", password=self.dnac_ro_pwd.get(),
                            timeout=3)
                device_dict["Status"] = "DNAC authentication Success"
                logging.warning(f'DNAC authentication to {host["IP_Address"]} was successful.')
            except (paramiko.SSHException, paramiko.AuthenticationException, paramiko.BadAuthenticationType):
                try:
                    print(f'User and RO TACACS Failed. Attempting SSH to {host["IP_Address"]} using Local.')
                    logging.critical(f'User and RO TACACS Failed. Attempting SSH to {host["IP_Address"]} using Local.')
                    ssh.connect(hostname=host["IP_Address"], username="cchcs", password=self.local_pwd.get(), timeout=3)
                    print(f'Local authentication to {host["IP_Address"]} was successful.')
                    logging.warning(f'Local authentication to {host["IP_Address"]} was successful.')
                    device_dict["Status"] = "Local authentication Successful"
                except (paramiko.SSHException, paramiko.AuthenticationException, paramiko.BadAuthenticationType):
                    print(f'Local Authentication to {host["IP_Address"]} was unsuccessful.')
                    logging.critical(f'Local Authentication to {host["IP_Address"]} was unsuccessful.')
                    device_dict["Status"] = "TACACS/Local authentication Failure"
        except socket.timeout:
            device_dict["Status"] = "Connection Timeout"
            print(f'Connection to {host["IP_Address"]} timed out.')
            logging.critical(f'Connection to {host["IP_Address"]} timed out.')
        self.results.append(device_dict)
        ssh.close()


class App2Frame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # App Configuration/Variables
        self.device_dict = {
            "Site1": ["10.1.100.11", "10.1.200.11"],
            "Site2": ["10.2.100.11", "10.2.200.11"],
            "Site3": ["10.3.100.11", "10.3.200.11"],
            "Site4": ["10.4.100.11", "10.4.200.11"]
        }
        self.ssh_client = None
        self.default_button_fg_color = ('#3B8ED0', '#1F6AA5')
        self.default_button_hover_color = ('#36719F', '#144870')
        self.default_button_text_color = ('#DCE4EE', '#DCE4EE')
        self.connection_thread = None

        # Grid Config
        self.rowconfigure([14], weight=1)
        self.columnconfigure([0, 10], weight=1)

        # Create Objects
        self.close_button = ctk.CTkButton(self, text="X", fg_color="red4", hover_color="firebrick3", width=10,
                                          height=10, command=self.master.reload_apps)
        self.description = ctk.CTkLabel(self,
                                        text="Select a Site & Device - OR - enter a specific IP;\n "
                                             "specific IP takes priority.\n"
                                             "(NOTE: Output is non-interactive)")
        self.credential_label = ctk.CTkLabel(self, text="Credentials")
        self.username = ctk.CTkEntry(self, placeholder_text="Username")
        self.password = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.site_selection = ctk.CTkOptionMenu(self,
                                                values=["None", "Site1", "Site2", "Site3", "Site4"])
        self.device_selection = ctk.CTkOptionMenu(self, values=["None", "Core", "WLC"])
        self.ip_address = ctk.CTkEntry(self, placeholder_text="Switch IP")
        self.connect_button = ctk.CTkButton(self, text="Connect", command=self.ssh_connection)
        self.command_1 = ctk.CTkButton(self, text="Get Info",
                                       command=lambda: self.cli_command("sh version"))
        self.command_2 = ctk.CTkButton(self, text="Sister-Site",
                                       command=lambda: self.cli_command("sh int desc | i ASE|ister|Dark"))
        self.command_3 = ctk.CTkButton(self, text="CDP Neighbors",
                                       command=lambda: self.cli_command("sh cdp nei | s rt0|core|enssw"))
        self.command_4 = ctk.CTkButton(self, text="Tunnels")
        self.command_5 = ctk.CTkButton(self, text="Show Counters", command=lambda: self.cli_command(
            "show int counter | exclude Gi1/1/[1-4]|Gi2/1/[1-4]|Gi3/1/[1-4]|Gi4/1/[1-4]"))
        self.command_6 = ctk.CTkButton(self, text="Clear Counters", fg_color="gold2", hover_color="gold3",
                                       text_color="black",
                                       command=lambda: self.cli_command([["clear counters", r"confirm"], ["\n", ""]],
                                                                        True))
        self.output_text = scrolledtext.ScrolledText(self, background="gray", width=100, height=14, font="Arial 12",
                                                     cursor="", wrap=ctk.WORD, state=ctk.DISABLED)

        # Place Objects
        self.close_button.grid(row=0, column=11, padx=PAD_X, pady=PAD_Y, sticky="e")
        self.description.grid(row=1, column=1, columnspan=3, padx=PAD_X, pady=PAD_Y)
        self.credential_label.grid(row=2, column=1, columnspan=3)
        self.username.grid(row=3, column=1, columnspan=3, padx=PAD_X*2, pady=PAD_Y)
        self.password.grid(row=4, column=1, columnspan=3, padx=PAD_X*2, pady=PAD_Y)
        self.site_selection.grid(row=5, column=1, padx=PAD_X, pady=PAD_Y)
        self.device_selection.grid(row=5, column=2, padx=PAD_X, pady=PAD_Y)
        self.ip_address.grid(row=5, column=3, padx=PAD_X, pady=PAD_Y)
        self.connect_button.grid(row=12, column=1, columnspan=3, padx=PAD_X, pady=PAD_Y)
        self.command_1.grid(row=15, column=1, padx=PAD_X, pady=PAD_Y)
        self.command_2.grid(row=15, column=2, padx=PAD_X, pady=PAD_Y)
        self.command_3.grid(row=15, column=3, padx=PAD_X, pady=PAD_Y)
        self.command_4.grid(row=16, column=1, padx=PAD_X, pady=PAD_Y)
        self.command_5.grid(row=16, column=2, padx=PAD_X, pady=PAD_Y)
        self.command_6.grid(row=16, column=3, padx=PAD_X, pady=PAD_Y)
        self.output_text.grid(row=14, column=0, columnspan=12, pady=(PAD_Y, PAD_Y*2), sticky="ew")

    def cli_command(self, command, confirm=False):
        def execute_command():
            if hasattr(self, "ssh_client") and self.ssh_client.is_alive():
                try:
                    if confirm:
                        print("Confirmed")
                        self.ssh_client.send_multiline(command)
                        output = f"\n!!!!! Counters cleared !!!!!"
                    else:
                        output = self.ssh_client.send_command(command, use_textfsm=True)
                        print(output)

                    if len(output) == 0:
                        self.add_output(f"\n!!!!! No information returned !!!!!")
                    elif isinstance(output, list):
                        for k, v in output[0].items():
                            converted_text = f"\n{k.title()}: {v}"
                            self.add_output(converted_text)
                    else:
                        self.add_output(f"\n{output}")
                except Exception as e:
                    self.add_output(f"\n!!!!! Error sending command: {e} !!!!!")
            else:
                self.add_output("\n!!!!! SSH connection is not active. Unable to send the command. !!!!!")

        command_thread = threading.Thread(target=execute_command)
        command_thread.start()

    def add_output(self, text, color="black"):
        # Temporarily enable the ScrolledText widget to insert text
        self.output_text.config(state=ctk.NORMAL)  # Set state to NORMAL allowing text insertion

        # Create a tag with the desired color
        tag_name = f"{color}_tag"  # Generate a unique tag name for each color
        self.output_text.tag_configure(tag_name, foreground=color)

        # Insert text at the end and apply the tag
        self.output_text.insert(ctk.END, text, tag_name)  # Apply color to inserted text
        self.output_text.see(ctk.END)

        # Disable the widget again after inserting
        self.output_text.config(state=ctk.DISABLED)  # Disable the widget again after inserting

    def ssh_connection(self):
        def validate_ip(_):
            try:
                ipaddress.ip_address(_)
                return True
            except ValueError:
                return False

        def establishing_connect_button():
            self.connect_button.configure(
                text="Establishing...",
                text_color="black",
                fg_color="gold2",
                hover_color="gold3",
                command=connect_or_disconnect,
            )

        def disconnect_connect_button():
            self.connect_button.configure(
                text="Disconnect",
                fg_color="firebrick3",
                hover_color="firebrick4",
                command=connect_or_disconnect,
            )

        def reset_connect_button():
            self.connect_button.configure(
                text="Connect",
                text_color=self.default_button_text_color,
                fg_color=self.default_button_fg_color,
                hover_color=self.default_button_hover_color,
                command=connect_or_disconnect,
            )

        def connect_or_disconnect():
            if self.connect_button.cget("text") == "Connect":
                # Connect logic
                def connect():
                    try:
                        switch = {
                            "device_type": "cisco_ios",
                            "ip": ip,
                            "username": user,
                            "password": pwd,
                            "secret": pwd,
                        }

                        if validate_ip(ip) and user and pwd:
                            try:
                                self.add_output(f"\nAttempting to connect to {ip}...")
                                establishing_connect_button()
                                self.ssh_client = netmiko.ConnectHandler(**switch)
                                disconnect_connect_button()
                                self.add_output(f"\nConnected to {ip} successfully!")
                            except paramiko.SSHException as ssh_e:
                                self.add_output(str(ssh_e))
                                reset_connect_button()
                        else:
                            self.add_output(
                                "\nPlease verify that credentials are entered and the IP or selection is correct."
                            )
                    except ValueError as ve:
                        self.add_output(f"\nError: {ve}")
                        reset_connect_button()
                    except Exception as rand_e:
                        self.add_output(f"\nUnexpected error: {rand_e}")
                        reset_connect_button()

                self.connection_thread = threading.Thread(target=connect)
                self.connection_thread.start()
            else:
                # Disconnect logic
                if hasattr(self, "ssh_client"):
                    try:
                        self.ssh_client.disconnect()
                        self.add_output("\n" + "*" * 45 + "\nDisconnected successfully.\n" + "*" * 45)
                    except Exception as e:
                        self.add_output(f"\n!!!!! Error during disconnect: {e} !!!!!")

                else:
                    print(f"Connection alive = {self.ssh_client.is_alive()}")
                reset_connect_button()
        user = self.username.get().strip()
        pwd = self.password.get().strip()
        ip = self.get_ip()
        self.add_output(f"\n" + "*" * 45)
        connect_or_disconnect()

    def get_ip(self):
        ip = self.ip_address.get().strip()
        site = self.site_selection.get().strip()
        device_type = self.device_selection.get().strip()
        if ip:
            return ip
        elif site != "None" and device_type != "None":
            if device_type == "Core":
                return self.device_dict[site][0]
            elif device_type == "WLC":
                return self.device_dict[site][1]
            else:
                return "None selected"


class App3Frame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # App Configuration/Variables

        # Grid Config
        self.rowconfigure([5, 17], weight=1)
        self.columnconfigure([0, 10], weight=1)

        # Create Objects
        self.close_button = ctk.CTkButton(self, text="X", fg_color="red4", hover_color="firebrick3", width=10,
                                          height=10, command=self.master.reload_apps)
        self.app_title = ctk.CTkLabel(self, text="CIDR Calculator", font=("Courier", 20, "bold"))
        self.addressentry = ctk.CTkEntry(self, placeholder_text="10.0.0.0/8")
        self.calculate = ctk.CTkButton(self, text="Calculate", width=30, command=self.calculate_subnet)
        self.net_label = ctk.CTkLabel(self, text="Network Address",
                                      font=("Arial", 15, "bold"), text_color="#3B8ED0")
        self.net_address = ctk.CTkLabel(self, text="")
        self.mask_label = ctk.CTkLabel(self, text="Subnet Mask",
                                       font=("Arial", 15, "bold"), text_color="#3B8ED0")
        self.net_mask = ctk.CTkLabel(self, text="")
        self.broadcast_label = ctk.CTkLabel(self, text="Broadcast Address",
                                            font=("Arial", 15, "bold"), text_color="#3B8ED0")
        self.net_bcast = ctk.CTkLabel(self, text="")
        self.hosts_label = ctk.CTkLabel(self, text="Host Count",
                                        font=("Arial", 15, "bold"), text_color="#3B8ED0")
        self.net_hosts = ctk.CTkLabel(self, text="")
        self.range_label = ctk.CTkLabel(self, text="Usable Range",
                                        font=("Arial", 15, "bold"), text_color="#3B8ED0")
        self.net_range = ctk.CTkLabel(self, text="")

        # Place Objects
        self.close_button.grid(row=0, column=11, padx=PAD_X, pady=PAD_Y, sticky="e")
        self.app_title.grid(row=1, column=1, columnspan=5, padx=PAD_X, pady=PAD_Y)
        self.addressentry.grid(row=2, column=3, padx=PAD_X, pady=PAD_Y)
        self.calculate.grid(row=3, column=3, padx=PAD_X, pady=PAD_Y)
        self.net_label.grid(row=7, column=3, sticky="s")
        self.net_address.grid(row=8, column=3, pady=(0, 5))
        self.mask_label.grid(row=9, column=3)
        self.net_mask.grid(row=10, column=3, pady=(0, 5))
        self.broadcast_label.grid(row=11, column=3)
        self.net_bcast.grid(row=12, column=3, pady=(0, 5))
        self.hosts_label.grid(row=13, column=3)
        self.net_hosts.grid(row=14, column=3, pady=(0, 5))
        self.range_label.grid(row=15, column=3)
        self.net_range.grid(row=16, column=3, pady=(0, 5))
        self.k = ctk.CTk

    def calculate_subnet(self):
        ip_text = self.addressentry.get()
        try:
            ip = ipaddress.ip_network(self.addressentry.get(), strict=False)
            try:
                self.net_address.configure(text=ip.network_address)
                self.net_mask.configure(text=ip.netmask)
                self.net_bcast.configure(text=ip.broadcast_address)
                self.net_hosts.configure(text=ip.num_addresses - 2)
                self.net_range.configure(text=f"{ip[1]} - {ip[-2]}")
            except IndexError as e:
                self.net_address.configure(text="")
                self.net_mask.configure(text="")
                self.net_bcast.configure(text="")
                self.net_hosts.configure(text="")
                self.net_range.configure(text="")
                self.master.generate_popup("Raise Exception", "Invalid IP address or CIDR notation")
            except ValueError as e:
                self.net_address.configure(text="")
                self.net_mask.configure(text="")
                self.net_bcast.configure(text="")
                self.net_hosts.configure(text="")
                self.net_range.configure(text="")
                self.master.generate_popup("Raise Exception", "Invalid IP address or CIDR notation")
        except ValueError as e:
            self.net_address.configure(text="")
            self.net_mask.configure(text="")
            self.net_bcast.configure(text="")
            self.net_hosts.configure(text="")
            self.net_range.configure(text="")
            self.master.generate_popup("Raise Exception", "Invalid IP address or CIDR notation")
        except IndexError as e:
            self.net_address.configure(text="")
            self.net_mask.configure(text="")
            self.net_bcast.configure(text="")
            self.net_hosts.configure(text="")
            self.net_range.configure(text="")
            self.master.generate_popup("Raise Exception", "Invalid IP address or CIDR notation")

    # def is_valid_ip(self, ip):
    #     try:
    #         ipaddress.ip_address(ip)
    #         return True
    #     except ValueError:
    #         return False
    #
    # def is_subnet(self, ip):
    #     try:
    #         ipaddress.ip_network(ip)
    #         return True
    #     except ValueError:
    #         return False


class App4Frame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # App Configuration/Variables

        # Grid Config
        self.rowconfigure(3, weight=1)
        self.columnconfigure([0, 10], weight=1)

        # Create Objects
        self.close_button = ctk.CTkButton(self, text="X", fg_color="red4", hover_color="firebrick3", width=10,
                                          height=10, command=self.master.reload_apps)
        self.placeholder = ctk.CTkLabel(self, text="Coming Soon...")

        # Place Objects
        self.close_button.grid(row=0, column=11, padx=PAD_X, pady=PAD_Y, sticky="e")
        self.placeholder.grid(row=3, column=1, padx=PAD_X, pady=PAD_Y)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
