from random import uniform
from pathlib import Path

from moviepy import (
    AudioFileClip,
    CompositeVideoClip,
    ImageClip,
    VideoFileClip,
    concatenate_videoclips,
)

from src.config import (
    IMAGES,
    AUDIOS,
    MINECRAFT_VIDEO,
    OUTPUT_PATH,
    )


class VideoEditor:
    def __init__(self,callback=None) -> None:
        self.callback=callback

        self.audio_clips: list[AudioFileClip] = []
        self.video_clips: list = []

        self.story = None
        self.background = None
        self.final_video = None

    def run(self) -> None:
        try:
            self.story = self.create_story()

            self.background = self.create_background(self.story.duration)

            self.final_video = self.combine_story_and_background(
                self.story,
                self.background,
            )

            self.export_video(self.final_video)

            self.notify_process('Editing Video...')

        finally:
            self.cleanup()


    def notify_process(self,message:str):
        if self.callback:
            self.callback(message)

    def load_assets(self) -> tuple[list[Path], list[Path]]:

        images =  sorted(Path(IMAGES).glob("*.png")) # type: ignore
        audios =  sorted(Path(AUDIOS).glob("*.mp3")) # type: ignore

        return images, audios

    def create_story(self) -> CompositeVideoClip:

        images, audios = self.load_assets()

        clips = []

        for image_path, audio_path in zip(images, audios):

            audio = AudioFileClip(str(audio_path))
            self.audio_clips.append(audio)

            clip = (
                ImageClip(str(image_path))
                .with_duration(audio.duration)
                .with_audio(audio)
            )

            self.video_clips.append(clip)
            clips.append(clip)

        return concatenate_videoclips(clips) # type: ignore

    def create_background(
        self,
        duration: float,
    ) -> VideoFileClip:

        minecraft = VideoFileClip(str(MINECRAFT_VIDEO))
        self.video_clips.append(minecraft)

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


        story = (
            story
            .resized(1.30)
            .with_position(("center", "center"))
        )
        self.video_clips.append(story)

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
        
    def cleanup(self):
        for audio in self.audio_clips:
            try:
                audio.close()
            except Exception as e:
                print(f"Failed to close clip: {e}")

        for clip in self.video_clips:
            try:
                clip.close()
            except Exception as e:
                print(f"Failed to close clip: {e}")

        if self.story:
            self.story.close()

        if self.final_video:
            self.final_video.close()

        self.audio_clips.clear()
        self.video_clips.clear()

if __name__ == "__main__":
    editor = VideoEditor()
    editor.run()