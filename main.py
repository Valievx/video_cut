from colorama import Fore
from colorama import init
from moviepy.editor import (VideoFileClip,
                            AudioFileClip,
                            CompositeVideoClip,
                            concatenate_videoclips)

import os
import sys
import time
from dataclasses import dataclass

from time_range import range_random

init()
working_dir = os.path.sep.join(sys.argv[0].split(os.path.sep)[:-1])


@dataclass
class VideoEditor:
    """Basic VideoEditor Class."""
    path_video: str
    path_audio: str
    path_directory: str
    path_futage: str
    result_name: str
    resolution_selection: str

    def video_cut(self) -> None:
        """Cut the video."""
        if (os.path.split(self.path_video)[-1].endswith(".mp4")
                or os.path.split(self.path_video)[-1].endswith(".avi")):
            print(Fore.CYAN + '[+] Начинаю вырезку фрагмента видео')

            # Создаем директорию, если она не существует
            output_dir = os.path.join(working_dir, 'media')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            for i, (start_time, end_time) in enumerate(range_random()):
                clip = VideoFileClip(self.path_video)
                clip_clip = clip.subclip(start_time, end_time)
                print(Fore.CYAN + '[+] Записываю фрагмент видео...\n')
                clip_clip.write_videofile(
                    f'{working_dir}\\media\\clip_{i}.mp4',
                    codec='libx264',
                    audio=False
                )
                clip.reader.close()
                clip.audio.reader.close_proc()

            print(Fore.GREEN + '\n[+] Видео успешно сохранены')

    def video_merge(self) -> None:
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

                merge_final = concatenate_videoclips(
                    clip_to_merge,
                    method='compose'
                )

                print(Fore.YELLOW + (
                    f'[+] Длительность объединяемого видео: '
                    f'{time.strftime("%H:%M:%S", time.gmtime(merge_final.duration))}'
                    f'\n[+] Начинаю объединение файлов...\n'))

                merge_final.write_videofile(
                    f'{self.result_name}.mp4',
                    codec='libx264',
                    audio=False
                )
                print(Fore.GREEN + '\n[+] Объединение файлов завершено')
                print(
                    Fore.GREEN + f'[+] Видео {self.result_name}.mp4 сохранено')

    def add_fx(self) -> None:
        """Adding futage to video."""
        print(Fore.LIGHTMAGENTA_EX + '[+] Добавляем футаж')

        video = VideoFileClip(f'{self.result_name}.mp4')
        futage = VideoFileClip(
            self.path_futage).set_duration(video.duration).set_opacity(0.5)
        video_with_futage = CompositeVideoClip([video, futage])
        video_with_futage.write_videofile(f'{self.result_name}_fx.mp4')
        os.remove(f'{self.result_name}.mp4')

    def full_video_generation(self) -> None:
        """Adding an audio track to a video."""
        print(
            Fore.LIGHTMAGENTA_EX + '[+] Генерируем видео и добавляем аудио')

        video_path = f'{working_dir}\\{self.result_name}_fx.mp4'
        audio_path = self.path_audio
        output_path = f'{working_dir}\\{self.result_name}.mp4'

        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)

        video_duration = video_clip.duration
        audio_duration = audio_clip.duration

        # Вычисление количества повторений видео,
        # чтобы оно было не короче аудио
        num_repeats = int(audio_duration / video_duration)

        # Зацикливание видео
        looped_video_clips = [video_clip] * num_repeats

        # Вычисление остаточной длительности видео для последнего повторения
        remaining_duration = audio_duration - (num_repeats * video_duration)
        if remaining_duration > 0:
            last_clip = video_clip.subclip(0, remaining_duration)
            looped_video_clips.append(last_clip)

        final_video_clip = concatenate_videoclips(looped_video_clips)

        # Изменение разрешения
        new_resolution = (1440, 1080)
        if self.resolution_selection == 'y':
            final_video_clip = final_video_clip.resize(new_resolution)
            print(
                Fore.LIGHTMAGENTA_EX + (f'\nРазрешение изменено '
                                        f'на {new_resolution}.'))
        else:
            print(
                Fore.LIGHTMAGENTA_EX + '\nРазрешение оставлено без изменений.')

        final_clip = final_video_clip.set_audio(audio_clip)
        final_clip.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac'
        )

        video_clip.reader.close()
        video_clip.audio.reader.close_proc()
        os.remove(f'{self.result_name}_fx.mp4')


def main() -> None:
    """Main Function."""
    video = VideoEditor(
        input(Fore.LIGHTMAGENTA_EX + '(Пример: '
                                     'C:\\desktop\\video\\video.mp4)\n'
                                     'Введите полный путь видеофайла: '),
        input(Fore.LIGHTMAGENTA_EX + '(Пример: '
                                     'C:\\desktop\\music\\song.mp3)\n'
                                     'Введите полный путь аудиофайла: '),
        os.path.join(working_dir, 'media'),
        f'{working_dir}\\futage.mp4',
        input('Введите название нового видео: '),
        input(
            "Желаете изменить разрешение видео на 1440x1080? (Y/N): ").lower()
    )
    video.video_cut()
    video.video_merge()
    video.add_fx()
    video.full_video_generation()


if __name__ == "__main__":
    main()
