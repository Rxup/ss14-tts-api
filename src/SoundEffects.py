import numpy as np
import librosa
from pydub import AudioSegment
from pydub.effects import normalize
import io
from scipy.signal import butter, lfilter

def add_echo(input_buffer, new_pitch, decay):
    input_buffer.seek(0)
    # Загрузка звукового файла
    audio = AudioSegment.from_file(input_buffer, format='ogg')

    # Применение питча
    audio_with_pitch = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * new_pitch)
    })

    # Применение реверберации
    audio_with_reverb = audio_with_pitch.fade_in(50).fade_out(50).normalize().apply_gain(-10).apply_gain_stereo(-1, 1).normalize()

    # Запись измененного аудио в буфер
    output_buffer = io.BytesIO()
    audio_with_reverb.export(output_buffer, format='ogg')

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
    soundfile.write(output_buffer, mixed_audio, sr, format='OGG', subtype='VORBIS')

    return output_buffer
