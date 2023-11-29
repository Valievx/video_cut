from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from colorama import Fore
from colorama import init

import os
import sys
import time
from dataclasses import dataclass


init()
working_dir = os.path.sep.join(sys.argv[0].split(os.path.sep)[:-1])


@dataclass
class VideoEditor:
    """Basic VideoEditor Class."""
    path_file: str
    path_directory: str
    result_name: str

    NUM_REPEATS = 5

    def video_cut(self) -> None:
        """Cut the video."""

        time_range = [(36, 46), (72, 82), (96, 106), (134, 149)]

        if os.path.isfile(self.path_file):
            if os.path.split(self.path_file)[-1].endswith(".mp4") or os.path.split(self.path_file)[-1].endswith(".avi"):
                print(Fore.CYAN + '[+] Начинаю вырезку фрагмента видео')

                for i, (start_time, end_time) in enumerate(time_range):
                    clip = VideoFileClip(self.path_file)
                    clip_clip = clip.subclip(start_time, end_time)
                    print(Fore.CYAN + '[+] Записываю фрагмент видео...\n')
                    clip_clip.write_videofile(f'{working_dir}\\sample\\Clip_{i}.mp4', codec='h264')
                    clip.reader.close()
                    clip.audio.reader.close_proc()

                print(Fore.GREEN + f'\n[+] Видео успешно сохранены')

    def video_merge(self):
        """Merge the video."""
        if os.path.exists(self.path_directory):
            print(Fore.CYAN + '[+] Сканирование директории')
            clip_in_dir = os.listdir(self.path_directory)

            clip_to_merge = []
            for clip in clip_in_dir:
                if clip.endswith(".mp4") or clip.endswith(".avi"):
                    VideoFileClip(os.path.join(self.path_directory, clip))
                    clip_to_merge.append(
                        VideoFileClip(os.path.join(self.path_directory, clip)))

            if len(clip_to_merge) <= 1:
                print(
                    Fore.RED + '[-] В указанной директории нечего объединять')
            else:
                print(Fore.YELLOW + f'[+] Найдено файлов: {len(clip_to_merge)}')

                print(Fore.YELLOW + 'Происходит зацикливание видео')
                audio_file = AudioFileClip(f'{working_dir}\\AMNESIA (no tag).mp3')
                audio_duration = int(audio_file.duration)
                clip_to_merge = clip_to_merge * int(audio_duration / 45)

                merge_final = concatenate_videoclips(clip_to_merge, method='compose')
                print(Fore.YELLOW + f'[+] Длительность объединяемого видео: '
                                    f'{time.strftime("%H:%M:%S", time.gmtime(merge_final.duration))}'
                                    f'\n[+] Начинаю объединение файлов...\n')
                merge_final.write_videofile(f'{self.result_name}.mp4')

                print(Fore.GREEN + '\n[+] Объединение файлов завершено')
                print(Fore.GREEN + f'[+] Видео {self.result_name}.mp4 сохранено')

    def add_audio(self):
        print(Fore.CYAN + '[+] Заменяем Аудио')
        video_path = f'{working_dir}\\{self.result_name}.mp4'
        audio_path = f'{working_dir}\\Название аудио'
        final_path = f'{working_dir}\\{self.result_name}_mastering.mp4'

        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)

        duration = video.duration
        start_time = 0
        end_time = duration

        audio_cut = audio.subclip(start_time, end_time)
        video_without_audio = video.without_audio()
        video_with_new_audio = video_without_audio.set_audio(audio_cut)
        video_with_new_audio.write_videofile(final_path)

    def add_fx(self):
        pass


def main() -> None:
    """Main Function."""
    video = VideoEditor(
        f'{working_dir}\\Название видео',
        f'{working_dir}\\sample',
        input('Введите название нового видео: ')
    )
    video.video_cut()
    video.video_merge()
    video.add_audio()


if __name__ == "__main__":
    main()
