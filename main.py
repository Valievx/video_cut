from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips
from colorama import Fore
from colorama import init

import os
import sys
import time
import math
from dataclasses import dataclass

from time_range import range_random, full_time_clip

init()
working_dir = os.path.sep.join(sys.argv[0].split(os.path.sep)[:-1])


@dataclass
class VideoEditor:
    """Basic VideoEditor Class."""
    path_file: str
    audio_duration: float
    path_directory: str
    result_name: str
    path_futage: str

    def video_cut(self) -> None:
        """Cut the video."""
        if (os.path.split(self.path_file)[-1].endswith(".mp4")
                or os.path.split(self.path_file)[-1].endswith(".avi")):
            print(Fore.CYAN + '[+] Начинаю вырезку фрагмента видео')

            for i, (start_time, end_time) in enumerate(range_random()):
                clip = VideoFileClip(self.path_file)
                clip_clip = clip.subclip(start_time, end_time)
                print(Fore.CYAN + '[+] Записываю фрагмент видео...\n')
                clip_clip.write_videofile(
                    f'{working_dir}\\media\\clip_{i}.mp4',
                    codec='libx264'
                )
                clip.reader.close()
                clip.audio.reader.close_proc()

            print(Fore.GREEN + '\n[+] Видео успешно сохранены')

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
                print(
                    Fore.YELLOW + f'[+] Найдено файлов: {len(clip_to_merge)}')

                print(Fore.LIGHTMAGENTA_EX + 'Начинаю генерировать новое видео')
                clip_to_merge = (clip_to_merge * math.trunc(
                    self.audio_duration / full_time_clip))
                merge_final = concatenate_videoclips(
                    clip_to_merge, method='compose'
                )
                print(Fore.YELLOW + (
                    f'[+] Длительность объединяемого видео: '
                    f'{time.strftime("%H:%M:%S", time.gmtime(merge_final.duration))}'
                    f'\n[+] Начинаю объединение файлов...\n'))
                merge_final.write_videofile(f'{self.result_name}.mp4')
                print(Fore.GREEN + '\n[+] Объединение файлов завершено')
                print(
                    Fore.GREEN + f'[+] Видео {self.result_name}.mp4 сохранено')

    def add_fx(self):
        """Adding futage to video."""
        print(Fore.LIGHTMAGENTA_EX + '[+] Накладываем футаж')

        video = VideoFileClip(f'{working_dir}\\{self.result_name}.mp4')
        futage = VideoFileClip(self.path_futage).set_duration(video.duration).set_opacity(0.5)
        final = CompositeVideoClip([video, futage])
        final.write_videofile(f'{working_dir}\\{self.result_name}_fx.mp4')

    def add_audio(self):
        """Adding an audio track to a video."""
        print(Fore.LIGHTMAGENTA_EX + '[+] Заменяем Аудио')

        video_path = f'{working_dir}\\{self.result_name}_fx.mp4'
        audio_path = f'{working_dir}\\song.mp3'
        final_path = f'{working_dir}\\{self.result_name}_master.mp4'

        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)

        duration = video.duration
        start_time = 0
        end_time = duration

        audio_cut = audio.subclip(start_time, end_time)
        video_without_audio = video.without_audio()
        video_with_new_audio = video_without_audio.set_audio(audio_cut)
        video_with_new_audio.write_videofile(final_path)


def main() -> None:
    """Main Function."""
    video = VideoEditor(
        input(Fore.LIGHTMAGENTA_EX + '(Пример: '
                                     'C:\\desktop\\video\\video.mp4)\n'
                                     'Введите полный путь видеофайла: '),
        int(AudioFileClip(input('(Пример: '
                                'C:\\desktop\\music\\song.mp3)\n '
                                'Введите полный путь аудиофайла: ')).duration),
        f'{working_dir}\\media',
        input('Введите название нового видео: '),
        f'{working_dir}\\futage.mp4'
    )
    video.video_cut()
    video.video_merge()
    video.add_fx()
    video.add_audio()


if __name__ == "__main__":
    main()
