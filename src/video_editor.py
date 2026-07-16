from random import uniform
from pathlib import Path

from moviepy import (
    AudioFileClip,
    CompositeVideoClip,
    ImageClip,
    VideoFileClip,
    concatenate_videoclips,
)

from .config import (
    IMAGES,
    AUDIOS,
    MINECRAFT_VIDEO,
    OUTPUT_PATH,
    )


class VideoEditor:
    def run(self) -> None:
        story = self.create_story()

        background = self.create_background(story.duration)

        final_video = self.combine_story_and_background(
            story,
            background,
        )

        self.export_video(final_video)

    def load_assets(self) -> tuple[list[Path], list[Path]]:

        images =  sorted(Path(IMAGES).glob("*.png")) # type: ignore
        audios =  sorted(Path(AUDIOS).glob("*.mp3")) # type: ignore

        return images, audios

    def create_story(self) -> CompositeVideoClip:

        images, audios = self.load_assets()

        clips = []

        for image_path, audio_path in zip(images, audios):

            audio = AudioFileClip(str(audio_path))

            clip = (
                ImageClip(str(image_path))
                .with_duration(audio.duration)
                .with_audio(audio)
            )

            clips.append(clip)

        return concatenate_videoclips(clips) # type: ignore

    def create_background(
        self,
        duration: float,
    ) -> VideoFileClip:

        minecraft = VideoFileClip(str(MINECRAFT_VIDEO))

        max_start = minecraft.duration - duration

        start = uniform(0, max_start)

        return minecraft.subclipped(
            start,
            start + duration,
        )

    def combine_story_and_background(
        self,
        story,
        background,
    ) -> CompositeVideoClip:


        story = story.with_position(
            ("center", "center")
        )

        return CompositeVideoClip(
            [
                background,
                story,
            ]
        )

    def export_video(
        self,
        video: CompositeVideoClip,
    ) -> None:

        video.write_videofile(
            str(OUTPUT_PATH),
            fps=30,
            codec="libx264",
            audio_codec="aac",
        )


if __name__ == "__main__":
    editor = VideoEditor()
    editor.run()