# src/SoundEffects.py
import subprocess
import io

# Убедись, что файлы существуют
RADIO1_PATH = "radio1.wav"
RADIO2_PATH = "radio2.wav"

def _run_ffmpeg(cmd, input_data):
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = proc.communicate(input=input_data)
    if proc.returncode != 0:
        raise RuntimeError(f"FFmpeg error: {stderr.decode()}")
    return stdout

def add_echo(input_buffer, output_format='ogg'):
    input_buffer.seek(0)
    cmd = [
        'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
        '-i', 'pipe:0',
        '-i', 'announce.wav',
        '-filter_complex',
        '[0] [1] afir=dry=10:wet=10 [reverb]; [0] [reverb] amix=inputs=2:weights=10 1 [out]; [out] volume=4',
        '-f', output_format, 'pipe:1'
    ]
    output = _run_ffmpeg(cmd, input_buffer.read())
    result = io.BytesIO(output)
    result.seek(0)
    return result

def add_radio_effect(input_buffer, hz=44100, format='ogg'):
    input_buffer.seek(0)
    input_data = input_buffer.read()

    # 1. Фильтрация → PCM (s16le)
    cmd_filter = [
        'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
        '-i', 'pipe:0',
        '-af', 'highpass=f=1000,lowpass=f=3000,acrusher=level_in=1:level_out=1:bits=8:mode=0:aa=1',
        '-ar', str(hz),
        '-ac', '1',
        '-f', 's16le', 'pipe:1'
    ]
    filtered = _run_ffmpeg(cmd_filter, input_data)  # ← PCM bytes

    # 2. Смешивание: radio1 + filtered (PCM) + radio2
    cmd_mix = [
        'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
        '-i', RADIO1_PATH,           # [0:a] wav
        '-f', 's16le', '-ar', str(hz), '-ac', '1', '-i', 'pipe:0',  # [1:a] ← PCM
        '-i', RADIO2_PATH,           # [2:a] wav
        '-filter_complex',
        '[0:a][1:a][2:a]concat=n=3:v=0:a=1[outa]',
        '-map', '[outa]',
        '-f', format,
        'pipe:1'
    ]

    result_bytes = _run_ffmpeg(cmd_mix, filtered)
    result = io.BytesIO(result_bytes)
    result.seek(0)
    return result

def add_robot(input_buffer, hz=44100, format='ogg'):
    input_buffer.seek(0)
    cmd = [
        'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
        '-i', 'pipe:0',
        '-filter:a', "afftfilt=real='hypot(re,im)*sin(0)':imag='hypot(re,im)*cos(0)':win_size=1024:overlap=0.5,deesser=i=0.4,volume=1.5",
        '-ar', str(hz),
        '-ac', '1',
        '-f', format, 'pipe:1'
    ]
    output = _run_ffmpeg(cmd, input_buffer.read())
    result = io.BytesIO(output)
    result.seek(0)
    return result