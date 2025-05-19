from yeelight import Bulb, Flow, transitions
from tkinter import messagebox
import customtkinter as ctk
import IPConfig as IPC


class App(ctk.CTk):
    CONFIG_FILE = "config.json"

        
    def __init__(self):
            super().__init__()
            self.title("Yeelight Bulb Controller")
            self.geometry("800x700")
            self.resizable(False, False)

            self.finder = IPC.IPFinder(ip_range="192.168.1.")
            self.bulb = None
            self.saved_ip = None  ## CHANGED: set manually instead of using load_config

            # Frame for sections
            self.main_frame = ctk.CTkFrame(self)
            self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

            # IP Connecting Section
            self.ip_frame = ctk.CTkFrame(self.main_frame)
            self.ip_frame.pack(pady=10, fill="x")

            self.ip_label = ctk.CTkLabel(self.ip_frame, text="Yeelight IP:")
            self.ip_label.pack(side="left", padx=10, pady=10)
            
            self.ip_entry = ctk.CTkEntry(self.ip_frame, placeholder_text="Enter IP Address")
            self.ip_entry.pack(side="left", padx=10, pady=10, fill="x", expand=True)

            self.check_button = ctk.CTkButton(self.ip_frame, text="Check", command=self.check_bulb)
            self.check_button.pack(side="right", padx=10, pady=10)

            self.auto_button = ctk.CTkButton(self.ip_frame, text="Auto Connect", command=self.auto_connect)  ## ADDED
            self.auto_button.pack(side="right", padx=5, pady=10)  ## ADDED

            # Basic Controls Section
            self.basic_controls_frame = ctk.CTkFrame(self.main_frame)
            self.basic_controls_frame.pack(pady=10, fill="x")

            self.basic_controls_label = ctk.CTkLabel(self.basic_controls_frame, text="Basic Controls")
            self.basic_controls_label.pack(pady=5)

            # First row: Turn On, 50%, Turn Off
            self.controls_frame = ctk.CTkFrame(self.basic_controls_frame)
            self.controls_frame.pack(pady=5, fill="x")

            self.off_button = ctk.CTkButton(self.controls_frame, text="Turn Off", command=self.turn_off, state=ctk.DISABLED)
            self.off_button.pack(side="left", padx=10, pady=5, expand=True, fill="x")
            
            self.brightness_slider = ctk.CTkSlider(self.controls_frame, from_=0, to=100, command=self.set_brightness)
            self.brightness_slider.pack(side="left", padx=10, pady=5, expand=True, fill="x")

            self.on_button = ctk.CTkButton(self.controls_frame, text="Turn On", command=self.turn_on, state=ctk.DISABLED)
            self.on_button.pack(side="left", padx=10, pady=5, expand=True, fill="x")

            # Second row: Modes || these modes are set to me own preferences and can be changed manually
            self.modes_frame = ctk.CTkFrame(self.basic_controls_frame)
            self.modes_frame.pack(pady=5, fill="x")

            self.study_mode_button = ctk.CTkButton(self.modes_frame, text="Study Mode", command=self.set_study_mode)
            self.study_mode_button.pack(side="left", padx=10, pady=5, expand=True, fill="x")

            self.rest_mode_button = ctk.CTkButton(self.modes_frame, text="Rest Mode", command=self.set_rest_mode)
            self.rest_mode_button.pack(side="left", padx=10, pady=5, expand=True, fill="x")

            self.work_mode_button = ctk.CTkButton(self.modes_frame, text="Work Mode", command=self.set_work_mode)
            self.work_mode_button.pack(side="left", padx=10, pady=5, expand=True, fill="x")

            # Third row: Common Colors
            self.colors_frame = ctk.CTkFrame(self.basic_controls_frame)
            self.colors_frame.pack(pady=5, fill="x")

            self.colors = [
                ("White", (255, 255, 255)),
                ("Orange", (255, 165, 0)),
                ("Purple", (100, 20, 128)),
                ("Red", (255, 0, 0)),
                ("Blue", (0, 0, 255)),
                ("Green", (0, 255, 0)),
                ("Cyan", (0, 255, 255)),
                ("Magenta", (255, 0, 255)),
                ("Yellow", (255, 210, 0)),
            ]

            num_colors_per_row = 3
            num_rows = (len(self.colors) + num_colors_per_row - 1) // num_colors_per_row

            for i in range(num_rows):
                row_frame = ctk.CTkFrame(self.colors_frame)
                row_frame.pack(pady=2, fill="x")
                for j in range(num_colors_per_row):
                    index = i * num_colors_per_row + j
                    if index < len(self.colors):
                        color_name, (r, g, b) = self.colors[index]
                        button = ctk.CTkButton(row_frame, text=color_name, command=lambda r=r, g=g, b=b: self.set_color(r, g, b))
                        button.pack(side="left", padx=5, expand=True, fill="x")

            # Custom Color Section
            def validation(new_value):
                return new_value == "" or (new_value.isdigit() and len(new_value) <= 3)

            vcmd = (self.register(validation), "%P")

            self.custom_color_frame = ctk.CTkFrame(self.main_frame)
            self.custom_color_frame.pack(pady=10, fill="x")

            self.custom_color_label = ctk.CTkLabel(self.custom_color_frame, text="Custom Color")
            self.custom_color_label.pack(pady=5)

            self.rgb_label = ctk.CTkLabel(self.custom_color_frame, text="RGB Values (0-255):")
            self.rgb_label.pack(pady=5)

            self.rgb_frame = ctk.CTkFrame(self.custom_color_frame)
            self.rgb_frame.pack(pady=5, fill="x")

            self.r_label = ctk.CTkLabel(self.rgb_frame, text="R:")
            self.r_label.pack(side="left", padx=5)
            self.r_entry = ctk.CTkEntry(self.rgb_frame, width=80, validate="key", validatecommand=vcmd)
            self.r_entry.pack(side="left", padx=5)

            self.g_label = ctk.CTkLabel(self.rgb_frame, text="G:")
            self.g_label.pack(side="left", padx=5)
            self.g_entry = ctk.CTkEntry(self.rgb_frame, width=80, validate="key", validatecommand=vcmd)
            self.g_entry.pack(side="left", padx=5)

            self.b_label = ctk.CTkLabel(self.rgb_frame, text="B:")
            self.b_label.pack(side="left", padx=5)
            self.b_entry = ctk.CTkEntry(self.rgb_frame, width=80, validate="key", validatecommand=vcmd)
            self.b_entry.pack(side="left", padx=5)

            self.apply_color_button = ctk.CTkButton(self.custom_color_frame, text="Apply Color", command=self.apply_custom_color)
            self.apply_color_button.pack(pady=10)

            # Flows Section
            self.flows_frame = ctk.CTkFrame(self.main_frame)
            self.flows_frame.pack(pady=10, fill="x")

            self.flows_label = ctk.CTkLabel(self.flows_frame, text="Light Flows")
            self.flows_label.pack(pady=5)

            self.flow1_button = ctk.CTkButton(self.flows_frame, text="Flow 1: Breathing", command=self.flow1)
            self.flow1_button.pack(side="left", padx=10, pady=5, expand=True, fill="x")

            self.flow2_button = ctk.CTkButton(self.flows_frame, text="Flow 2: Color Cycle", command=self.flow2)
            self.flow2_button.pack(side="left", padx=10, pady=5, expand=True, fill="x")

            self.flow3_button = ctk.CTkButton(self.flows_frame, text="Flow 3: Pulse", command=self.flow3)
            self.flow3_button.pack(side="left", padx=10, pady=5, expand=True, fill="x")


    def check_bulb(self):
            ip = self.ip_entry.get().strip()
            if not ip:
                messagebox.showerror("Error!!", "Please enter an IP address.")
                return
            
            try:
                self.bulb = Bulb(ip)
                self.bulb.get_properties()
                self.on_button.configure(state=ctk.NORMAL)
                self.off_button.configure(state=ctk.NORMAL)
                messagebox.showinfo("Success", "Connected to Yeelight bulb.")
            except Exception as e:
                self.bulb = None
                messagebox.showerror("Error", f"Failed to connect to Yeelight bulb: {str(e)}")

    def auto_connect(self): 
        ip = self.finder.get_bulb_ip()
        if ip:
            self.ip_entry.delete(0, "end")
            self.ip_entry.insert(0, ip)
            messagebox.showinfo("Found Bulb", f"Bulb found at IP: {ip}")
            self.check_bulb()
        else:
            messagebox.showerror("Error", "No bulb found automatically.")

    def turn_on(self):
        if self.bulb:
            try:
                self.bulb.turn_on()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to turn on the bulb: {str(e)}")

    def turn_off(self):
        if self.bulb:
            try:
                self.bulb.turn_off()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to turn off the bulb: {str(e)}")

    def set_brightness(self, value):
        if self.bulb:
            try:
                brightness = int(value)
                self.bulb.set_brightness(brightness)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to set brightness: {str(e)}")

    def set_color(self, r, g, b):
        if self.bulb:
            try:
                self.bulb.set_rgb(r, g, b)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to set color: {str(e)}")

    def apply_custom_color(self):
        if self.bulb:
            try:
                r = int(self.r_entry.get())
                g = int(self.g_entry.get())
                b = int(self.b_entry.get())
                self.bulb.set_rgb(r, g, b)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to apply custom color: {str(e)}")


################################################
#####  Modes  ##################################
################################################

## These modes may be changed as you desire, for me i set them to the values i found are most suitable to me.

    def set_study_mode(self):
        if self.bulb:
            try:
                self.bulb.set_color_temp(3800)
                self.bulb.set_brightness(80)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to set study mode: {str(e)}")

    def set_rest_mode(self):
        if self.bulb:
            try:
                self.bulb.set_color_temp(7000)
                self.bulb.set_brightness(63) 
            except Exception as e:
                messagebox.showerror("Error", f"Failed to set rest mode: {str(e)}")

    def set_work_mode(self):
        if self.bulb:
            try:
                self.bulb.set_color_temp(3500) 
                self.bulb.set_brightness(64)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to set work mode: {str(e)}")


################################################
#####  Flows  ##################################
################################################

## Really unnecessary , just to try flows and flex on your friends.

    def flow1(self):
        if self.bulb:
            try:
                flow = Flow(
                    count=0,
                    action=Flow.actions.recover,
                    transitions=[
                        transitions.RGBTransition(0, 255, 0, duration=2000),  # Green
                        transitions.RGBTransition(0, 0, 0, duration=2000)     # Off
                    ]
                )
                self.bulb.start_flow(flow)
            except Exception as e:
                messagebox.showerror("Error", f"Error in Flow 1: {str(e)}")

    def flow2(self):
        if self.bulb:
            try:
                flow = Flow(
                    count=0,
                    action=Flow.actions.recover,
                    transitions=[
                        transitions.RGBTransition(250, 0, 0, duration=2500),   # Red
                        transitions.RGBTransition(255, 120, 0, duration=2500), # Red-Orange
                        transitions.RGBTransition(250, 200, 52, duration=2500), # Yellow
                        transitions.RGBTransition(50, 240, 50, duration=2500),   # Green
                        transitions.RGBTransition(0, 255, 128, duration=2500), # Green-Cyan
                        transitions.RGBTransition(50, 50, 240, duration=2500),   # Blue
                        transitions.RGBTransition(120, 0, 250, duration=2500), # Purple
                        transitions.RGBTransition(250, 30, 128, duration=2500), # Magenta-Red
                    ]
                )
                self.bulb.start_flow(flow)
            except Exception as e:
                messagebox.showerror("Error", f"Error in Flow 2: {str(e)}")

    def flow3(self):
        if self.bulb:
            try:
                flow = Flow(
                    count=0,
                    action=Flow.actions.recover,
                    transitions=[
                        transitions.RGBTransition(255, 0, 0, duration=1000),  # Red
                        transitions.RGBTransition(0, 255, 0, duration=1000),   # Green
                        transitions.RGBTransition(255, 0, 255, duration=1000),    # Magenta
                        transitions.RGBTransition(0, 0, 255, duration=1000),  # Blue
                        transitions.RGBTransition(255, 255, 0, duration=1000),  # Yellow
                        transitions.RGBTransition(0, 255, 255, duration=1000),   # Cyan

                    ]
                )
                self.bulb.start_flow(flow)
            except Exception as e:
                messagebox.showerror("Error", f"Error in Flow 3: {str(e)}")
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
