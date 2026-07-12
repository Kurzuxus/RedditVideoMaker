from scraper import DataScraper
from video_editor import VideoEditor


def main() -> None:
    scraper = DataScraper()

    try:
        scraper.run()
    finally:
        scraper.close()

    editor = VideoEditor()
    editor.run()


if __name__ == "__main__":
    main()