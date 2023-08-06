import os
import glob
import tempfile

import click

from lecture_automator.parser import parse_md
from lecture_automator.marp_api import generate_marp_slides
from lecture_automator.gen_speech import texts_to_speeches
from lecture_automator.gen_video import generate_video


@click.command()
@click.argument(
    'input_md', 
    type=click.STRING,
)
@click.argument(
    'out_path', 
    type=click.STRING,
)
@click.option(
    '--scale', 
    type=click.FLOAT, 
    default=1.5, 
    help=(
        'Коэффициент масштабирования генерируемого видео, '
        'по умолчанию равен 1.5, что соответствует разрешению 1920x1080,'
        'значение 1 соответствует разрешению 1280x720.'
    )
)
def convert_md_to_mp4(input_md, out_path, scale):
    md_data = parse_md(input_md)

    with tempfile.TemporaryDirectory() as tmpdirname:
        generate_marp_slides(tmpdirname, md_data['md_text'], scale=scale)
        slide_images = glob.glob(os.path.join(tmpdirname, 'Slide.*'))
        audio_paths = texts_to_speeches(md_data['speech'], tmpdirname)
        generate_video(slide_images, audio_paths, out_path)


if __name__ == '__main__':
    convert_md_to_mp4()