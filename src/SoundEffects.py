import numpy as np
import librosa
import soundfile as sf
import io
from scipy.signal import butter, lfilter

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

    # Создание фильтров низких и высоких частот для эффекта рации
    nyquist_freq = 0.5 * sr
    b_low, a_low = butter(10, cutoff_freq_low / nyquist_freq, btype='low')
    b_high, a_high = butter(10, cutoff_freq_high / nyquist_freq, btype='high')

    # Применение фильтров к звуковому файлу
    filtered_audio_low = lfilter(b_low, a_low, audio)
    filtered_audio_high = lfilter(b_high, a_high, audio)

    # Генерация шума
    noise = np.random.normal(scale=noise_level, size=len(audio))
    
    # Нормализация аудио
    filtered_audio_low = librosa.util.normalize(filtered_audio_low)
    filtered_audio_high = librosa.util.normalize(filtered_audio_high)
    noise = librosa.util.normalize(noise)

    # Применение эффекта рации
    radio_effect = filtered_audio_low + filtered_audio_high + noise

    # Смешивание оригинального аудио и эффекта рации
    mixed_audio = audio + radio_effect

    # Запись результата в новый буфер
    output_buffer = io.BytesIO()
    sf.write(output_buffer, mixed_audio, sr, format='OGG', subtype='VORBIS')

    return output_buffer
