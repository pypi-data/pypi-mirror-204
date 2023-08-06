import os

import torch

from lecture_automator.settings import get_app_dir


MODEL_URL = 'https://models.silero.ai/models/tts/ru/v3_1_ru.pt'
MODEL_FILENAME = 'v3_1_ru.pt'
SPEAKER = 'xenia'
SAMPLE_RATE = 48000


def text_to_speech(text: str, out_path: str, device: str = 'cpu') -> str:
    """Синтез речи.

    Args:
        text (str): текст для синтеза речи.
        out_path (str): путь для сохранения сгенерированной речи.
        device (str, optional): устройство для вычислений (cuda, cpu и т.д.). Defaults to 'cpu'.

    Returns:
        str: название файла формата wav со сгенерированной речью по тексту.
    """

    model_path = os.path.join(get_app_dir(), MODEL_FILENAME)

    if not os.path.exists(model_path):
        torch.hub.download_url_to_file(
            MODEL_URL,
            model_path
        )

    model = torch.package.PackageImporter(model_path).load_pickle(
        "tts_models", "model"
    )
    model.to(device)

    curr_dir = os.getcwd()
    os.chdir(os.path.dirname(out_path))
    audio_path = model.save_wav(
        text=text,
        speaker=SPEAKER,
        sample_rate=SAMPLE_RATE
    )
    os.rename(audio_path, os.path.basename(out_path))
    os.chdir(curr_dir)

    return out_path



def texts_to_speeches(texts: list, out_dir: str, basename: str = 'Sound') -> list:
    audio_paths = []
    for index, text in enumerate(texts, start=1):
        audio_path = os.path.join(out_dir, '{}_{}.wav'.format(basename, index))
        text_to_speech(
            text, audio_path
        )
        audio_paths.append(audio_path)

    return audio_paths


if __name__ == '__main__':
    # text_to_speech('Зачем ты запустил код?', "./example.wav")
    audio_paths = texts_to_speeches(['Привет', 'Пока'], '.')
    print(audio_paths)