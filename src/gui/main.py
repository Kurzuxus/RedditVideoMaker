from typing import Any
from json import dump,load

import flet as ft
import flet_video as ftv
from src.scraper import DataScraper
from src.video_editor import VideoEditor
from src.config import OUTPUT_PATH,USER_SETTINGS_PATH,load_user_settings


class RedditVideoMakerApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.configure_page()

        self.build_ui()

    def update_step(self, index: int, done: bool) -> None:
        icon = "✅" if done else "⏳"
        color= "white" if done else ft.Colors.GREY_500

        titles = [
            "Scraping Reddit...",
            "Generating Images & Audio...",
            "Editing Video..."
        ]

        self.steps[index].value = f"{icon} {titles[index]}"
        self.steps[index].color=color

        self.steps[index].update()

    def configure_page(self) -> None:
        self.page.fonts = {
            "Pixel": r"fonts/Tiny5-Regular.ttf"
        }

        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.title='RVM'


    def on_scraper_update(self, message: str) -> None:

        if message == "Scraping Reddit...":
            self.update_step(0, True)
        elif message =="Generating Images & Audio...":
            self.update_step(1, True)
        elif message =="Editing Video...":
            self.update_step(2, True)

        self.page.update()

    def start_process(self) -> None:

        scraper = DataScraper(callback=self.on_scraper_update)

        try:
            scraper.run()

        finally:
            scraper.close()

        editor = VideoEditor(callback=self.on_scraper_update)

        editor.run()

        self.create_video_box()
        
    def clear_files(self) -> None:
        self.page.controls.clear()
        self.page.update()

        self.build_ui()
        self.page.update()
       
    def create_settings_bu(self) -> ft.Container:
        return ft.Container(
            bgcolor="#181a1f",
            border_radius=8,
            padding=ft.Padding.all(3),
            border=ft.Border(
                right=ft.BorderSide(4, "#cfd0d1"),
                bottom=ft.BorderSide(3, "#cfd0d1"),
                top=ft.BorderSide(1.5, "#cfd0d1"),
                left=ft.BorderSide(1.5, "#cfd0d1"),
            ),
            content=ft.Image(
                src='settings_gear.png',
                width=30,
                height=30
            ),
            on_click=lambda e: self.page.show_dialog(AppDialog())
        )

    def create_logo(self) -> ft.Image:
        return ft.Image(
            src="app_logo.png",
            width=150,
            height=150,
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

    def create_process_steps(self)-> list[ft.Text]:
        self.steps = [
            ft.Text("⏳ Scraping Reddit...", size=18,font_family='Pixel',color=ft.Colors.GREY_600),
            ft.Text("⏳ Generating Images & Audio...", size=18,font_family='Pixel',color=ft.Colors.GREY_600),
            ft.Text("⏳ Editing Video...", size=18,font_family='Pixel',color=ft.Colors.GREY_600),
            ]
        
        return self.steps
    
    def create_footer(self) -> ft.Container:
        return ft.Container(
            content=ft.Text(
                "© 2026 Informatica • Reddit Video Maker",
                size=16,
                color=ft.Colors.GREY_500,
                italic=True,
                font_family='Pixel'
            ),
            alignment=ft.alignment.Alignment.CENTER,
            margin=ft.margin.Margin.only(top=30, bottom=10),
        )

    def create_video_box(self) -> None:
        video_box=ftv.Video(
            playlist=[ftv.VideoMedia(resource=str(OUTPUT_PATH))],
            width=500,
            height=600,
        )

        self.video_column.width=500
        self.video_column.height=600
        self.page.scroll=ft.ScrollMode.ALWAYS

        self.video_column.controls.append(video_box)

        self.page.update()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

    def build_ui(self) -> None:

        progress_panel = ft.Column(
            controls=self.create_process_steps(), # type: ignore
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )

        header = ft.Column(
            controls=[
                ft.Row(controls=[self.create_logo(),self.create_settings_bu()],
                    alignment=ft.MainAxisAlignment.CENTER),
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

        self.video_column=ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
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
            self.video_column,
            footer
        )

class AppDialog(ft.AlertDialog):
    def __init__(self,**kwds: Any) -> None:
        super().__init__(**kwds)

        settings=load_user_settings()

        self.SUBREDDIT = settings["subreddit"]
        self.NUMBER_OF_COMMENTS = settings["number_of_comments"]
        self.MAX_COMMENT_CHAR = settings["max_comment_char"]
        self.BACKGROUND_VIDEO=settings['background_video']

        self.Images=["Minecraft","GTA","Subway"]
        self.SELECTED_VIDEO=self.BACKGROUND_VIDEO

        self.content=self.content_construction()
        self.bgcolor='#17191E'
        self.scrollable=True

        self.actions=self.create_action_buttons() # type: ignore



    def bg_video_change(self,e:ft.ControlEvent):
        reponsive= self.content.content.controls[-1].content.controls[2].controls
        for i in reponsive:
            card_data :str = i.controls[0].data
            if e.control.data == card_data:
                e.control.border=ft.Border.all(width=2,color='#F5980A')
                self.SELECTED_VIDEO :str = card_data
                continue
            i.controls[0].border= ft.Border.all(width=2,color='#595957')


    def increment_values(self, e:ft.ControlEvent):
        if abs(e.data) == 1:
            current_value=int(self.comments_field.value)
            if e.data >0:
                new_value=current_value + 1
            else:
                new_value=current_value - 1
            self.comments_field.value=str(new_value)
            self.comments_field.update()
        else:
            current_value=int(self.length_field.value)
            if e.data >0:
                new_value=current_value + 1
            else:
                new_value=current_value - 1
            self.length_field.value=str(new_value)
            self.length_field.update()            

    def create_heading(self):
        return ft.Row(
            controls=[
                ft.Image(
                    src='settings_gear.png',
                    width=30,
                    height=30
                ),
                ft.Text(
                    value='Settings',
                    font_family='Pixel',
                    size=24,
                    weight='bold' # pyright: ignore[reportArgumentType]
                )
            ] # pyright: ignore[reportArgumentType]
        )

    def create_subreddit_settings(self):

        self.subreddit_field = ft.TextField(
            bgcolor='#191c20',
            value=self.SUBREDDIT,
            border_color='#595957',
            border_radius=12,
            cursor_color='#F5980A',
            text_style=ft.TextStyle(
                font_family='Pixel'
            ),
            text_size=18,
            helper='Example: AskReddit',
            helper_style=ft.TextStyle(
                font_family='Pixel',
                color='#78787a',
                size=16
            )
        )

        return ft.Container(
            padding=ft.Padding.only(top=10),
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(
                                icon=ft.Icons.CIRCLE_ROUNDED,
                                color="#F5980A",
                                size=10
                            ),
                            ft.Text(
                                value="Subreddit",
                                font_family="Pixel",
                                size=22,
                            )
                        ]
                    ),

                    ft.Text(
                        value='Choose the subreddit to get posts from.',
                        font_family='Pixel',
                        color="#78787a",
                        size=16
                    ),

                    self.subreddit_field
                ]
            )
        )

    def create_comments_settings(self):

        self.comments_field = ft.TextField(
            bgcolor='#191c20',
            value=str(self.NUMBER_OF_COMMENTS),
            border_color='#27282a',
            cursor_color='#F5980A',
            border_radius=0,
            height=45,
            width=120,
            text_align=ft.TextAlign.CENTER,
            text_style=ft.TextStyle(
                font_family='Pixel'
            ),
            text_size=18
        )

        return ft.Container(
            padding=ft.Padding.only(top=10),
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(
                                icon=ft.Icons.CIRCLE_ROUNDED,
                                color="#F5980A",
                                size=10
                            ),
                            ft.Text(
                                value="Number of Comments",
                                font_family="Pixel",
                                size=22,
                            )
                        ]
                    ),

                    ft.Text(
                        value='Set how many comments to include in a video.',
                        font_family='Pixel',
                        color="#78787a",
                        size=16
                    ),

                    ft.Row(
                        spacing=0,
                        controls=[
                            ft.Container(
                                border=ft.Border.all(
                                    color='#595957',
                                    width=2
                                ),
                                bgcolor='#191c20',
                                border_radius=8,
                                width=45,
                                height=45,
                                data=-1,
                                on_click=lambda e: self.increment_values(e=e.control),
                                content=ft.Icon(
                                    icon=ft.Icons.REMOVE_ROUNDED
                                )
                            ),

                            self.comments_field,

                            ft.Container(
                                border=ft.Border.all(
                                    color='#595957',
                                    width=2
                                ),
                                bgcolor='#191c20',
                                border_radius=8,
                                width=45,
                                height=45,
                                data=1,
                                on_click=lambda e: self.increment_values(e=e.control),
                                content=ft.Icon(
                                    icon=ft.Icons.ADD_ROUNDED
                                )
                            ),
                        ]
                    ),

                    ft.Text(
                        value='Min: 1 ● Max: 20',
                        style=ft.TextStyle(
                            font_family='Pixel',
                            color='#78787a',
                            size=16
                        )
                    )
                ]
            )
        )

    def create_length_settings(self):

        self.length_field = ft.TextField(
            bgcolor='#191c20',
            value=str(self.MAX_COMMENT_CHAR),
            border_color='#27282a',
            cursor_color='#F5980A',
            border_radius=0,
            height=45,
            width=120,
            text_align=ft.TextAlign.CENTER,
            text_style=ft.TextStyle(
                font_family='Pixel'
            ),
            text_size=18
        )

        return ft.Container(
            padding=ft.Padding.only(top=10),
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(
                                icon=ft.Icons.CIRCLE_ROUNDED,
                                color="#F5980A",
                                size=10
                            ),
                            ft.Text(
                                value="Max Comment Length",
                                font_family="Pixel",
                                size=22,
                            )
                        ]
                    ),

                    ft.Text(
                        value='Set the maximum length (in characters) for a comment.',
                        font_family='Pixel',
                        color="#78787a",
                        size=16
                    ),

                    ft.Row(
                        spacing=0,
                        controls=[
                            ft.Container(
                                border=ft.Border.all(
                                    color='#595957',
                                    width=2
                                ),
                                bgcolor='#191c20',
                                border_radius=8,
                                width=45,
                                height=45,
                                data=-2,
                                on_click=lambda e: self.increment_values(e=e.control),
                                content=ft.Icon(
                                    icon=ft.Icons.REMOVE_ROUNDED
                                )
                            ),

                            self.length_field,

                            ft.Container(
                                border=ft.Border.all(
                                    color='#595957',
                                    width=2
                                ),
                                bgcolor='#191c20',
                                border_radius=8,
                                width=45,
                                height=45,
                                data=2,
                                on_click=lambda e: self.increment_values(e=e.control),
                                content=ft.Icon(
                                    icon=ft.Icons.ADD_ROUNDED
                                )
                            ),
                        ]
                    ),

                    ft.Text(
                        value='Min: 50 ● Max: 1000',
                        style=ft.TextStyle(
                            font_family='Pixel',
                            color='#78787a',
                            size=16
                        )
                    )
                ]
            )
        )

    def background_video_selection(self):
        return ft.Container(
            padding=ft.Padding.only(top=10),
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(
                                icon=ft.Icons.CIRCLE_ROUNDED,
                                color="#F5980A",
                                size=10
                            ),
                            ft.Text(
                                value="Background Video",
                                font_family="Pixel",
                                size=22,
                            )
                        ]
                    ),

                    ft.Text(
                        value='Choose the background video for your short.',
                        font_family='Pixel',
                        color="#78787a",
                        size=16
                    ),

                    ft.ResponsiveRow(
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        columns=9,
                        controls=[
                            ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=5,
                                col=3,
                                controls=[
                                    ft.Container(
                                        border_radius=12,
                                        border=ft.Border.all(
                                            width=2,
                                            color='#F5980A' if i==self.BACKGROUND_VIDEO else '#595957'
                                        ),
                                        data=i,
                                        on_click=lambda e: self.bg_video_change(e=e),
                                        content=ft.Image(
                                            src=f"{i}.png"
                                        ),
                                    ),
                                    ft.Text(
                                        value=i,
                                        font_family='Pixel',
                                        size=18,
                                        color='white',
                                    ),
                                ],
                            )
                            for i in self.Images
                        ]
                    )
                ]
            )
        )

    def create_action_buttons(self):

        button1 = ft.Container(
            bgcolor="#17191E",
            width=100,
            height=40,
            border_radius=15,
            on_click=lambda e: self.page.pop_dialog(),
            alignment=ft.alignment.Alignment.CENTER,
            border=ft.Border(
                right=ft.BorderSide(6, "white"),
                bottom=ft.BorderSide(4, "white"),
                top=ft.BorderSide(1.5, "white"),
                left=ft.BorderSide(1.5, "white"),
            ),
            content=ft.Text(
                "Cancel",
                size=20,
                color="white",
                font_family="Pixel",
            ),
        )

        button2 = ft.Container(
            bgcolor="orange",
            width=150,
            height=40,
            border_radius=15,
            alignment=ft.alignment.Alignment.CENTER,
            on_click=lambda e: self.save_settings(e),
            border=ft.Border(
                right=ft.BorderSide(6, "white"),
                bottom=ft.BorderSide(4, "white"),
                top=ft.BorderSide(1.5, "white"),
                left=ft.BorderSide(1.5, "white"),
            ),
            content=ft.Text(
                "Save Settings",
                size=18,
                color="white",
                font_family="Pixel",
            ),
        )

        return [button1, button2]

    def content_construction(self):

        return ft.Container(
            width=500,
            height=1000,
            content=ft.Column(
                controls=[
                    self.create_heading(),

                    self.create_subreddit_settings(),

                    ft.Divider(
                        color='#595957',
                        leading_indent=5,
                        trailing_indent=5
                    ),

                    self.create_comments_settings(),

                    ft.Divider(
                        color='#595957',
                        leading_indent=5,
                        trailing_indent=5
                    ),

                    self.create_length_settings(),

                    ft.Divider(
                        color='#595957',
                        leading_indent=5,
                        trailing_indent=5
                    ),

                    self.background_video_selection()
                ]
            )
        )

    def save_settings(self, e):

        subreddit = self.subreddit_field.value.strip()
        number_of_comments = int(self.comments_field.value)
        max_comment_char = int(self.length_field.value)

        with open(USER_SETTINGS_PATH,'w',encoding='utf-8') as file:
            new_data={
                "subreddit": subreddit,
                "number_of_comments": number_of_comments,
                "max_comment_char": max_comment_char,
                "background_video": self.SELECTED_VIDEO
            }
            dump(new_data,file)

        self.page.pop_dialog()

def main(page: ft.Page):
    RedditVideoMakerApp(page)


ft.run(main, assets_dir="assets")