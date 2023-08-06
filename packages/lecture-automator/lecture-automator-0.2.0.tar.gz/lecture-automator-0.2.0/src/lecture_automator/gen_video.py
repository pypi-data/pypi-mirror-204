import tempfile
import os
from typing import List

import ffmpeg

from lecture_automator.marp_api import generate_marp_slides


def generate_video(path_images: List[str], path_wavs: List[str], output_name: str) -> None:
    """Генерация видео на основе изображений и звука к каждому из них.

    Args:
        path_images (List[str]): список путей к изображениям в файловой системе.
        path_wavs (List[str]): список путей к звукам в файловой системе (каждый звук соответствует изображению с таким же индексом).
        output_name (str): название выходного видео.
    """

    files = []
    for path_image, path_wav in zip(path_images, path_wavs):
        files.extend([ffmpeg.input(path_image), ffmpeg.input(path_wav)])

    joined = ffmpeg.concat(*files, v=1, a=1).node
    ffmpeg.output(
        joined[0], joined[1], output_name, 
        f='mp4', vcodec='libx264', acodec='aac'
    ).run(overwrite_output=True)


if __name__ == '__main__':
    # with open('examples/Example_2.md') as file:
    #     md_text = file.read()
    # generate_marp_slides("examples", md_text)
    path_to_image = "/Users/donsangre/PycharmProjects/lecture-automator/examples/Example.001.png"
    path_to_image_2 = "/Users/donsangre/PycharmProjects/lecture-automator/examples/Example.002.png"
    path_to_audio = "/Users/donsangre/PycharmProjects/lecture-automator/examples/Example.wav"

    generate_video([path_to_image, path_to_image_2], [path_to_audio, path_to_audio], 'examples/output.mp4')

    # input_still = ffmpeg.input(path_to_image)
    # input_audio = ffmpeg.input("/Users/donsangre/PycharmProjects/lecture-automator/examples/Example.wav")

    # (
    #     ffmpeg
    #     .concat(input_still, input_audio, v=1, a=1)
    #     .output("output.mp4")
    #     .run(overwrite_output=True)
    # )
