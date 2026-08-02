from random import choice
from pathlib import Path

from selenium.webdriver.common.by import By
from seleniumbase import Driver

from config import (
    AUDIOS,
    IMAGES,
    MAX_COMMENT_CHAR,
    NUMBER_OF_COMMENTS,
    REDDIT_URL,
)
from tiktok_voice import Voice, tts
from concurrent.futures import ThreadPoolExecutor

class DataScraper:
    def __init__(self,callback=None) -> None:
        self.driver = Driver(uc=True,browser="brave")
        self.callback=callback

    def run(self) -> None:

        self.clear_generated_files()

        self.open_subreddit()
        self.open_random_post()
        self.notify_process('Scraping Reddit...')
        self.driver.fullscreen_window()

        self.process_post()
        self.notify_process('Generating Images & Audio...')

    def notify_process(self,message:str):
        if self.callback:
            self.callback(message)

    def open_subreddit(self) -> None:

        self.driver.get(REDDIT_URL)

    def open_random_post(self) -> None:

        if not self.driver.is_element_visible(By.TAG_NAME, "shreddit-post"):
            raise RuntimeError("No posts were found.")

        posts = self.driver.find_elements(By.TAG_NAME, "shreddit-post")

        random_post = choice(posts)
        random_post.uc_click()

    def process_post(self) -> None:

        title = self.grab_post_title()

        self.screenshot_post()

        comments = self.driver.find_elements(
            'shreddit-comment[depth="0"]'
        )

        self.process_comments(
            comments=comments,
            title=title,
        )

    def process_comments(self,comments: list,title: str) -> list[str]:

        accepted_comments = []

        tts_jobs = [(title,f"{AUDIOS}/audio0.mp3")]

        for index, comment in enumerate(comments, start=1):

            if len(accepted_comments) >= NUMBER_OF_COMMENTS:
                break

            paragraphs = comment.find_elements(By.TAG_NAME, "p")

            comment_text = " ".join(
                paragraph.text.strip()
                for paragraph in paragraphs
                if paragraph.text.strip()
            ).strip()

            if len(comment_text) >= MAX_COMMENT_CHAR:
                continue

            comment.screenshot(f"{IMAGES}/shot{index}.png")

            accepted_comments.append(comment_text)

            tts_jobs.append(
                (
                    comment_text,
                    f"{AUDIOS}/audio{index}.mp3",
                )
            )

        with ThreadPoolExecutor(max_workers=4) as executor:

            futures = [
                executor.submit(
                    self.transcribe_text,
                    text,
                    output_path,
                )
                for text, output_path in tts_jobs
            ]

            for future in futures:
                future.result()

        return accepted_comments

    def transcribe_text(
        self,
        text: str,
        output_path: str,
    ) -> None:

        tts(
            text=text,
            voice=Voice.US_MALE_1,
            output_file_path=output_path,
        )

    def screenshot_post(self) -> None:

        post = self.driver.find_element(By.TAG_NAME, "shreddit-post")

        post.screenshot(f"{IMAGES}/shot0.png")

    def grab_post_title(self) -> str:

        return self.driver.find_element(By.TAG_NAME, "h1").text

    def clear_generated_files(self) -> None:

        for folder in (IMAGES, AUDIOS):
            folder = Path(folder)

            if not folder.exists():
                continue

            for file in folder.iterdir():
                if file.is_file():
                    file.unlink()

    def close(self) -> None:

        self.driver.quit()


if __name__ == "__main__":
    scraper = DataScraper()

    try:
        scraper.run()
    finally:
        scraper.close()