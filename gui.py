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
    "fishing_screen": {"x1": 666, "x2": 1248, "y1": 316, "y2": 419},
    "fishing_filter": {"hsv_min": [0, 33, 135], "hsv_max": [90, 255, 255]},
    "shutdown_pc": False,
}


class Settings:
    def __init__(self):
        for name, value in config.items():
            setattr(self, name, value)


class TextField(ft.TextField):
    def __init__(self, label, value):
        super().__init__()
        self.label = label
        self.value = value
        self.expand = True


class ContainerIndigo(ft.Container):
    def __init__(self, content):
        super().__init__()
        self.content = content
        self.alignment = ft.alignment.center
        self.bgcolor = ft.colors.INDIGO_500
        self.margin = 10
        self.padding = 10
        self.border_radius = 10


def main(page: ft.Page):
    page.title = "TLFishing"
    # page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Разрешение экрана
    screen_text = ft.Text("Разрешение экрана", size=20)
    screen_width_textfield = TextField(
        label="Ширина", value=str(settings.monitor_resolution["width"])
    )
    screen_height_textfield = TextField(
        label="Высота", value=str(settings.monitor_resolution["height"])
    )
    screen_number = TextField(
        label="Номер Монитора", value=str(settings.monitor_resolution["mon"])
    )
    screen_textgield_row = ft.Row(
        controls=[screen_width_textfield, screen_height_textfield, screen_number]
    )

    screen_column = ft.Column(
        controls=[screen_text, screen_textgield_row],
    )
    screen_box = ContainerIndigo(
        content=screen_column,
    )

    page.add(screen_box)


settings = Settings()
ft.app(main)
