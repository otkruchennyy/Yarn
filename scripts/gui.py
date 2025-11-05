import customtkinter as ctk
import settingsLogic as sl
import json

CONFIG_DIR = "config"
config_file = "../config/config.json"

# Базовые цвета
BG_DARK = '#111111'      # Основной фон
BG_CARD = '#121212'      # Карточки, панели

# Акцентные (тускло-синие)
ACCENT_PRIMARY = "#202020"   # Основной акцент
ACCENT_SECONDARY = "#252525" # Второстепенный
ACCENT_LIGHT = "#7a7a7a"     # Светлый акцент

# Текст
TEXT_MAIN = '#e0e0e0'    # Основной текст
TEXT_MUTED = '#a0a0a0'   # Второстепенный текст

selected_color = ACCENT_PRIMARY

refresh_rate = 2000
font_family = "Arial"  # Unbounded
font_size = 12
font_style = (font_family, font_size)


class basicTextAnalyzer:
    def __init__(self):
        self.config_data = {}
        self.after_id = None
        self.load_config()
        
        if self.config_data.get("termsAccepted"):
            self.create_main_app()
        else:
            self.show_terms_dialog()

    def load_config(self):
        try:
            with open("../config/config.json", "r", encoding="utf-8") as f:
                self.config_data = json.load(f)
        except FileNotFoundError:
            self.config_data = {"termsAccepted": False}

    def show_terms_dialog(self): # Окно с соглашением
        self.terms_win = ctk.CTk()
        self.terms_win.title("Соглашение")
        self.terms_win.geometry("400x200")
        self.terms_win.iconbitmap("../assets/ico/basicTextAnalyser-256.ico")
        label = ctk.CTkLabel(self.terms_win, text="Примите условия использования(Пока нет)")
        label.pack(pady=20)
        
        accept_btn = ctk.CTkButton(
            self.terms_win, 
            text="Принять", 
            command=self.on_terms_accepted
        )
        accept_btn.pack(pady=10)
        
        self.terms_win.mainloop()
    
    def on_terms_accepted(self): # Обработчик принятия условий
        self.config_data["termsAccepted"] = True
        self.save_config()
        self.terms_win.quit()
        self.terms_win.destroy()
        self.create_main_app()
    
    def create_main_app(self): # Создание основного приложения
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.app = ctk.CTk()
        self.app.geometry("400x300")
        self.app.title("basicTextAnalyzer")
        self.app.iconbitmap("../assets/ico/basicTextAnalyser-256.ico")
        self.app.protocol("WM_DELETE_WINDOW", self.on_close)
        self._create_widgets()
        self.app.mainloop()

    def on_close(self): # Обработчик закрытия окна
        if self.after_id:
            self.app.after_cancel(self.after_id)
        self.app.quit()
        self.app.destroy()
    
    def save_config(self):
        with open("../config/config.json", "w", encoding="utf-8") as f:
            json.dump(self.config_data, f, indent=2, ensure_ascii=False)

    def darken_color(self, hex_color, factor=0.8):
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, int(c * factor)) for c in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"

    def update_padding(self):
        if not self.app.winfo_exists():
            return
        
        try:
            width = self.userInput_container.winfo_width()
            self.user_input.configure(padx=int(width * 0.05))
            
            if self.app.winfo_exists():
                self.after_id = self.app.after(refresh_rate, self.update_padding)
        except Exception:
            pass


    
    def paintSettings(self, key):
        result = sl.set_active_button(key)
        print(f"Button {key} pressed, result: {result}")

        if result == "a":
            self.app_settings.place(relx=1, rely=1, anchor="e", x=-60, y=-160)
            self.app_settings.lift()
        elif result == "b":
            self.app_settings.place(relx=1, rely=1, anchor="e", x=-60, y=-160)
            self.app_settings.lift()
        elif result == "c":
            self.app_settings.place(relx=1, rely=1, anchor="e", x=-60, y=-160)
            self.app_settings.lift()
        elif result == "d":
            self.app_settings.place(relx=1, rely=1, anchor="e", x=-60, y=-160)
            self.app_settings.lift()
        elif result == "e":
            self.app_settings.place(relx=1, rely=1, anchor="e", x=-60, y=-160)
            self.app_settings.lift()
        elif result == "f":
            self.app_settings.place(relx=1, rely=1, anchor="e", x=-60, y=-160)
            self.app_settings.lift()
        elif result == "s":
            self.app_settings.place(relx=1, rely=1, anchor="e", x=-60, y=-160)
            self.app_settings.lift()
        else:
            self.app_settings.place_forget()

    def _create_widgets(self):
        main = ctk.CTkFrame(self.app, fg_color=BG_DARK)
        main.pack(fill="both", expand=True)

        # плавающее меню
        self.app_settings = ctk.CTkFrame(
            main,
            fg_color=ACCENT_PRIMARY,
            width=500,
            height=300,
            border_width=1,
            border_color=ACCENT_SECONDARY
        )

        aside = ctk.CTkFrame(main, width=100, fg_color=ACCENT_SECONDARY)
        aside.pack(side="left", fill="y")

# --------------------------------------------------------------------------------------------------------

        # центральная панель
        self.userInput_container = ctk.CTkFrame(main, fg_color="transparent")
        self.userInput_container.pack(side="left", fill="both", expand=True)

        self.user_input = ctk.CTkTextbox(
            self.userInput_container, 
            fg_color="transparent", 
            font=font_style
        )
        self.user_input.pack(
            side="left",
            fill="both",
            expand=True,
            pady=5
        )
        
        self.update_padding()

# --------------------------------------------------------------------------------------------------------

        # left-aside color
        aside_color_container = ctk.CTkFrame(
            aside, 
            fg_color=ACCENT_PRIMARY, 
            width=100, 
            height=120
        )
        aside_color_container.pack(side="bottom")

        colorPicker = ctk.CTkButton(
            aside_color_container,
            text="",
            width=80,
            height=60,
            fg_color=ACCENT_PRIMARY,
            hover_color=self.darken_color(selected_color, 0.8),
            border_width=2,
            border_color=ACCENT_SECONDARY
        )
        colorPicker.pack(side="left")

        open_colorPicker = ctk.CTkButton(
            aside_color_container,
            text=">>",
            width=20,
            height=60,
            fg_color=ACCENT_PRIMARY,
            hover_color=self.darken_color(selected_color, 0.8),
            border_width=1,
            border_color=ACCENT_SECONDARY
        )
        open_colorPicker.pack()

# --------------------------------------------------------------------------------------------------------

        # left-aside style
        aside_style_container = ctk.CTkFrame(
            aside, 
            fg_color=ACCENT_PRIMARY, 
            width=100, 
            height=120
        )
        aside_style_container.pack(side="bottom")

        stylePicker = ctk.CTkButton(
            aside_style_container,
            text="",
            width=80,
            height=60,
            fg_color=ACCENT_PRIMARY,
            hover_color=self.darken_color(selected_color, 0.8),
            border_width=2,
            border_color=ACCENT_SECONDARY
        )
        stylePicker.pack(side="left")

        open_stylePicker = ctk.CTkButton(
            aside_style_container,
            text=">>",
            width=20,
            height=60,
            fg_color=ACCENT_PRIMARY,
            hover_color=self.darken_color(selected_color, 0.8),
            border_width=1,
            border_color=ACCENT_SECONDARY
        )
        open_stylePicker.pack()

# --------------------------------------------------------------------------------------------------------

        # left-aside panel
        left_aside_container = ctk.CTkFrame(
            aside,
            fg_color=ACCENT_PRIMARY,
            width=100,
            border_width=1,
            border_color=ACCENT_SECONDARY
        )
        left_aside_container.pack(side="left", fill="y")

# --------------------------------------------------------------------------------------------------------

        # Right-aside panel
        control_panel = ctk.CTkFrame(
            main, 
            width=50,
            fg_color=ACCENT_PRIMARY,
            border_width=1,
            border_color=ACCENT_SECONDARY
        )
        control_panel.pack(side="right", fill="y")

        btn1 = ctk.CTkButton(
            control_panel,
            text="A",
            width=40,
            height=30,
            fg_color=ACCENT_PRIMARY,
            border_width=1,
            border_color=ACCENT_SECONDARY,
            hover_color=ACCENT_SECONDARY,
            command=lambda: self.paintSettings("a")
        )
        btn1.pack(side="top", padx=5, pady=1)

        btn2 = ctk.CTkButton(
            control_panel,
            text="B",
            width=40,
            height=30,
            fg_color=ACCENT_PRIMARY,
            border_width=1,
            border_color=ACCENT_SECONDARY,
            hover_color=ACCENT_SECONDARY,
            command=lambda: self.paintSettings("b")
        )
        btn2.pack(side="top", padx=5, pady=1)

        btn3 = ctk.CTkButton(
            control_panel,
            text="C",
            width=40,
            height=30,
            fg_color=ACCENT_PRIMARY,
            border_width=1,
            border_color=ACCENT_SECONDARY,
            hover_color=ACCENT_SECONDARY,
            command=lambda: self.paintSettings("c")
        )
        btn3.pack(side="top", padx=5, pady=1)
        
        btn4 = ctk.CTkButton(
            control_panel,
            text="D",
            width=40,
            height=30,
            fg_color=ACCENT_PRIMARY,
            border_width=1,
            border_color=ACCENT_SECONDARY,
            hover_color=ACCENT_SECONDARY,
            command=lambda: self.paintSettings("d")
        )
        btn4.pack(side="top", padx=5, pady=1)

        btn5 = ctk.CTkButton(
            control_panel,
            text="E",
            width=40,
            height=30,
            fg_color=ACCENT_PRIMARY,
            border_width=1,
            border_color=ACCENT_SECONDARY,
            hover_color=ACCENT_SECONDARY,
            command=lambda: self.paintSettings("e")
        )
        btn5.pack(side="top", padx=5, pady=1)

        btn6 = ctk.CTkButton(
            control_panel,
            text="F",
            width=40,
            height=30,
            fg_color=ACCENT_PRIMARY,
            border_width=1,
            border_color=ACCENT_SECONDARY,
            hover_color=ACCENT_SECONDARY,
            command=lambda: self.paintSettings("f")
        )
        btn6.pack(side="top", padx=5, pady=1)

        preferences = ctk.CTkButton(
            control_panel,
            text="☰",
            width=40,
            height=30,
            fg_color=ACCENT_PRIMARY,
            border_width=1,
            border_color=ACCENT_SECONDARY,
            hover_color=ACCENT_SECONDARY,
            command=lambda: self.paintSettings("s")
        )
        preferences.pack(side="bottom", padx=5, pady=1)

# --------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    app = basicTextAnalyzer()