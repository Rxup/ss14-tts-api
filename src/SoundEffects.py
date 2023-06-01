import numpy as np
import librosa
import soundfile as sf
import io

def add_echo(input_buffer, delay, decay):
    # Загрузка звукового файла из буфера
    audio, sr = librosa.load(input_buffer, sr=None, mono=True)

    # Расчет параметров эхо
    delay_samples = int(delay * sr)
    decay_factor = decay

    # Создание пустого массива для выходного звука
    output = np.zeros_like(audio)

    # Добавление эффекта эхо
    for i in range(len(audio)):
        if i < delay_samples:
            output[i] = audio[i]
        else:
            output[i] = audio[i] + decay_factor * output[i - delay_samples]

    # Запись результата в новый буфер
    output_buffer = io.BytesIO()
    sf.write(output_buffer, output, sr, format='OGG', subtype='VORBIS')

    return output_buffer

def add_radio_effect(input_buffer, cutoff_freq_low, cutoff_freq_high, noise_level):
    # Загрузка звукового файла из буфера
    audio, sr = librosa.load(input_buffer, sr=None, mono=True)

    # Применение фильтра низких частот
    filtered_low = librosa.lowpass_filter(audio, sr, cutoff_freq_low)

    # Применение фильтра высоких частот
    filtered_high = librosa.highpass_filter(filtered_low, sr, cutoff_freq_high)

    # Добавление шума
    noise = np.random.normal(scale=noise_level, size=len(filtered_high))
    output = filtered_high + noise

    # Запись результата в новый буфер
    output_buffer = io.BytesIO()
    sf.write(output_buffer, output, sr, format='OGG', subtype='VORBIS')

    return output_buffer