import flet as ft
import multiprocessing


config = {
    "monitor_resolution": {
        "top": 0,
        "left": 0,
        "width": 1920,
        "height": 1080,
        "mon": 0,
    },
    "shutdown_pc": False,
    "fishing_screen": {"x1": 666, "x2": 1248, "y1": 316, "y2": 419},
    "fishing_filter": {"hsv_min": [0, 33, 135], "hsv_max": [90, 255, 255]},
}


class Settings:
    def __init__(self):
        for name, value in config.items():
            setattr(self, name, value)


def main(page: ft.Page):
    page.title = "TLFishing"
    # page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    screen_text = ft.Text("Разрешение экрана", size=20)
    screen_width_textfield = ft.TextField(
        label="Ширина", expand=True, value=str(settings.monitor_resolution["width"])
    )
    screen_height_textfield = ft.TextField(
        label="Высота", expand=True, value=str(settings.monitor_resolution["height"])
    )
    screen_number = ft.TextField(
        label="Номер", expand=True, value=str(settings.monitor_resolution["mon"])
    )
    screen_textgield_row = ft.Row(
        controls=[screen_width_textfield, screen_height_textfield, screen_number]
    )

    screen_column = ft.Column(
        controls=[screen_text, screen_textgield_row],
    )
    screen_box = ft.Container(
        content=screen_column,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.INDIGO_500,
        margin=10,
        padding=10,
        border_radius=10,
    )

    page.add(screen_box)


settings = Settings()
ft.app(main)
