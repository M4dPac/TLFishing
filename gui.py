import customtkinter
import multiprocessing


config = {
    "monitor_resolution": {
        "top": 0,
        "left": 0,
        "width": 1920,
        "height": 1080,
        "mon": 2,
    },
    "shutdown_pc": False,
    "fishing_screen": {"x1": 666, "x2": 1248, "y1": 316, "y2": 419},
    "fishing_filter": {"hsv_min": [0, 33, 135], "hsv_max": [90, 255, 255]},
}


class Settings:
    def __init__(self):
        for name, value in config.items():
            setattr(self, name, value)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("TLFshing Setup")
        self.geometry("1100x580")
        # self.resizable(False, False)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.screen_setting_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.screen_setting_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        self.screen_title = customtkinter.CTkLabel(
            self.screen_setting_frame, text="Screen", fg_color="transparent"
        )
        self.screen_title.grid(row=0, column=0, padx=20, pady=20)
        self.entry = customtkinter.CTkEntry(
            self.screen_setting_frame, placeholder_text="Width"
        )
        self.entry.grid(row=1, column=1, padx=20, pady=20)

        self.entry1 = customtkinter.CTkEntry(
            self.screen_setting_frame, placeholder_text="Height"
        )
        self.entry1.grid(row=1, column=2, padx=20, pady=20)
        self.checkbox_1 = customtkinter.CTkCheckBox(self, text="checkbox_1")

        self.checkbox_1.grid(row=1, column=0, padx=20, pady=20)

        self.button_start = customtkinter.CTkButton(
            self, text="start", command=lambda: print("Start fishing")
        )
        self.button_end = customtkinter.CTkButton(
            self, text="exit", command=lambda: exit()
        )

        self.button_start.grid(row=2, column=0, padx=20, pady=20)
        self.button_end.grid(row=2, column=1, padx=20, pady=20)


app = App()
app.mainloop()
