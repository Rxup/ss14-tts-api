from pydub import AudioSegment
import subprocess
import io

# https://freesound.org/people/jorickhoofd/sounds/160144/
def add_echo(input_buffer, output_format='ogg'):
    # Создайте FFmpeg команду с указанными фильтрами
    cmd = [
        'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
        '-i', 'pipe:0',  # ввод из pipe (стандартного ввода)
        '-i', 'announce.wav',
        '-filter_complex', '[0] [1] afir=dry=3:wet=8 [out]; [out] volume=6',
        '-f', output_format,  # формат вывода (например, OGG)
        'pipe:1'  # вывод в pipe (стандартный вывод)
    ]

    # Запустите процесс FFmpeg с выводом ошибок в stderr
    ffmpeg_process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Прочитайте данные из входного буфера
    input_audio = input_buffer.read()

    # Выполните обработку аудио в FFmpeg и получите код завершения
    output_audio, err_output = ffmpeg_process.communicate(input_audio)
    return_code = ffmpeg_process.returncode

    # Закройте процесс FFmpeg
    ffmpeg_process.wait()

    # Если код завершения не равен нулю, выводите ошибку FFmpeg
    if return_code != 0:
        print("Ошибка FFmpeg:")
        print(err_output.decode("utf-8"))

    # Создайте буфер для измененного аудио и верните его
    output_buffer = io.BytesIO()
    output_buffer.write(output_audio)
    output_buffer.seek(0)

    return output_buffer

#https://freesound.org/people/Breviceps/sounds/457037/
radio1_audio = AudioSegment.from_file("radio1.wav")
radio2_audio = AudioSegment.from_file("radio2.wav")

def add_radio_effect(input_buffer, hz=44100, format='ogg'):
    input_buffer.seek(0)
    # Загрузка звукового файла
    audio = AudioSegment.from_file(input_buffer, format=format)

    # Примените эффект highpass
    audio = audio.high_pass_filter(1000)

    # Примените эффект lowpass
    audio = audio.low_pass_filter(3000)

    # Примените эффект acrusher
    audio = audio.set_frame_rate(hz)  # Установите желаемую частоту дискретизации
    audio = audio.set_channels(1)  # Установите желаемое количество каналов (1 для моно, 2 для стерео)
    audio = audio.set_sample_width(1)  # Установите желаемый размер выборки (1 байт)

    audio = radio1_audio + audio + radio2_audio

    # Запись измененного аудио в буфер
    output_buffer = io.BytesIO()
    audio.export(output_buffer, format=format)

    return output_buffer

def add_robot(input_buffer, output_format='ogg'):
    # Запустите FFmpeg с указанными фильтрами
    cmd = [
        'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
        '-i', 'pipe:0',  # ввод из pipe (стандартного ввода)
        '-filter:a', "afftfilt=real='hypot(re,im)*sin(0)':imag='hypot(re,im)*cos(0)':win_size=1024:overlap=0.5,deesser=i=0.4,volume=volume=1.5",
        '-f', output_format,  # формат вывода (OGG)
        'pipe:1'  # вывод в pipe (стандартный вывод)
    ]

    # Запустите процесс FFmpeg с выводом ошибок в stderr
    ffmpeg_process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Прочитайте данные из входного буфера
    input_audio = input_buffer.read()

    # Выполните обработку аудио в FFmpeg и получите код завершения
    output_audio, err_output = ffmpeg_process.communicate(input_audio)
    return_code = ffmpeg_process.returncode

    # Закройте процесс FFmpeg
    ffmpeg_process.wait()

    # Если код завершения не равен нулю, выводите ошибку FFmpeg
    if return_code != 0:
        print("Ошибка FFmpeg:")
        print(err_output.decode("utf-8"))

    # Создайте буфер для измененного аудио
    output_buffer = io.BytesIO()
    output_buffer.write(output_audio)
    output_buffer.seek(0)

    return output_buffer