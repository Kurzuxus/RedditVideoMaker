import flet as ft
from src.scraper import DataScraper
from src.video_editor import VideoEditor

class RedditVideoMakerApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.configure_page()
        self.steps = [
            ft.Text("⏳ Scraping Reddit...", size=18),
            ft.Text("⏳ Generating Images & Audio...", size=18),
            ft.Text("⏳ Editing Video...", size=18),
            ]
        
        self.build_ui()

    # -----------------------
    # Page Configuration
    # -----------------------

    def update_step(self, index: int, done: bool) -> None:
        icon = "✅" if done else "⏳"

        titles = [
            "Scraping Reddit...",
            "Generating Images & Audio...",
            "Editing Video..."
        ]

        self.steps[index].value = f"{icon} {titles[index]}"

        self.page.update()


    def configure_page(self) -> None:
        self.page.fonts = {
            "Pixel": r"fonts/Tiny5-Regular.ttf"
        }

        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # -----------------------
    # Event Handlers
    # -----------------------

    def start_process(self) -> None:

        scraper = DataScraper()

        try:
            scraper.run()

            self.update_step(0, True)

        finally:
            self.update_step(1, True)
            scraper.close()

        editor = VideoEditor()

        editor.run()

        self.update_step(2, True)
        
    def clear_files(self) -> None:
        print("Clear Files")

    # -----------------------
    # UI Builders
    # -----------------------

    def create_logo(self) -> ft.Image:
        return ft.Image(
            src="site_logo.png",
            width=100,
            height=100,
        )

    def create_title(self) -> ft.Text:
        return ft.Text(
            value="Reddit Video Maker",
            color="white",
            size=40,
            font_family="Pixel",
        )

    def create_start_button(self) -> ft.Container:
        return ft.Container(
            bgcolor="orange",
            width=150,
            height=45,
            border_radius=15,
            alignment=ft.alignment.Alignment.CENTER,
            on_click=lambda e :self.page.run_thread(self.start_process),
            border=ft.Border(
                right=ft.BorderSide(6, "white"),
                bottom=ft.BorderSide(4, "white"),
                top=ft.BorderSide(1.5, "white"),
                left=ft.BorderSide(1.5, "white"),
            ),
            content=ft.Text(
                "Start",
                size=26,
                color="white",
                font_family="Pixel",
            ),
        )

    def create_clear_button(self) -> ft.Container:
        return ft.Container(
            bgcolor="blue",
            width=100,
            height=45,
            border_radius=15,
            alignment=ft.alignment.Alignment.CENTER,
            on_click=self.clear_files,
            border=ft.Border(
                right=ft.BorderSide(6, "white"),
                bottom=ft.BorderSide(4, "white"),
                top=ft.BorderSide(1.5, "white"),
                left=ft.BorderSide(1.5, "white"),
            ),
            content=ft.Text(
                "Clear",
                size=26,
                color="white",
                font_family="Pixel",
            ),
        )

    def create_footer(self) -> ft.Container:
        return ft.Container(
            content=ft.Text(
                "© 2026 Informatica • Reddit Video Maker",
                size=14,
                color=ft.Colors.GREY_500,
                italic=True,
            ),
            alignment=ft.alignment.Alignment.CENTER,
            margin=ft.margin.Margin.only(top=30, bottom=10),
        )

    # -----------------------
    # Build Layout
    # -----------------------

    def build_ui(self) -> None:

        progress_panel = ft.Column(
            controls=self.steps,
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )

        header = ft.Column(
            controls=[
                self.create_logo(),
                self.create_title(),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        )

        buttons = ft.Row(
            controls=[
                self.create_clear_button(),
                self.create_start_button(),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        footer = ft.Column(
            controls=[self.create_footer()],
            alignment=ft.MainAxisAlignment.END,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )

        self.page.add(
            header,
            buttons,
            progress_panel,
            footer
        )


# -----------------------
# App Entry Point
# -----------------------

def main(page: ft.Page):
    RedditVideoMakerApp(page)


ft.run(main, assets_dir="assets1")