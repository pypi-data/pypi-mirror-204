# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lecture_automator']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'ffmpeg-python>=0.2.0,<0.3.0',
 'numpy>=1.24.2,<2.0.0',
 'torch>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['lecture-automator = '
                     'lecture_automator.cli:convert_md_to_mp4']}

setup_kwargs = {
    'name': 'lecture-automator',
    'version': '0.2.0',
    'description': '',
    'long_description': "# Lecture Automator\n\nLecture Automator позволяет автоматически генерировать презентации с озвучкой для каждого из слайдов. Всё, что вам нужно сделать - написать текстовый файл Markdown со специальной разметкой, а остальное за вас сделает Lecture Automator.\n\n## Установка\n\nС помощью pip (также необходимо установить ffmpeg и [Marp](https://github.com/marp-team/marp-cli)):\n```\npip install lecture-automator\n```\n\n## Использование\n\nДля использование необходимо создать Markdown-файл с описаниями слайдов (см. [Marp](https://marp.app/#get-started)) и [управляющими конструкциями](#управляющие-конструкции):\n````md\n# Python\n\n```\nprint('Привет, мир')\n```\n\n/speech{На этом слайде представлена простейшая программа, написанная на языке програмирования Пайтон. Эта программа просто выводит указанные слова в терминал.}\n\n---\n\n# Python\n\n```\na = 2\nb = 4\nprint(a * b)\n```\n\n/speech{А здесь представлена другая программа, которая умножается число два на число четыре.}\n\n````\n\nЗатем для генерации необходимо использовать следующий CLI команду в терминале:\n```bash\nlecture-automator Example.md Example.mp4\n```\n\nПример сгенерированного видео:\n\n[Example.webm](https://user-images.githubusercontent.com/33065236/231875817-1d3aae09-2a63-4bb1-8380-8b7f024bbe45.webm)\n\n\n### Управляющие конструкции \n\nНа данный момент реализованы следующий управляющие конструкции:\n- `/speech{...}` - текст для озвучивания слайда (каждый слайд должен содержать данную конструкцию). \n",
    'author': 'CapBlood',
    'author_email': 'stalker.anonim@mail.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CapBlood/lecture-automator.git',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
