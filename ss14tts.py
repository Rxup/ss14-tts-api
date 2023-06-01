import base64, os, io

from src.SpeakerPatch import SpeakerPatch,SpeakerPatchInit
from src.WarmUp import WarmUp
from src.SoundEffects import add_echo, add_radio_effect

import torch
import torchaudio

torch.set_num_threads(int(os.environ.get("threads","4")))

language = 'ru'
model_id = 'v3_1_ru'
deviceName = "cuda" if torch.cuda.is_available() else "cpu"
device = torch.device(deviceName)

ApiToken = os.environ.get("apitoken","test")

local_file = 'model.pt'
if not os.path.isfile(local_file):
    print("Start download silero models")
    torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/v3_1_ru.pt',
                                   local_file)  

model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
example_text = "В недрах тундры выдры в г+етрах т+ырят в вёдра ядра кедров."
#model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
#    model='silero_tts',
#    language=language,
#    speaker=model_id, 
#    trust_repo=True,
#    verbose=False
#)

model.to(device)  # gpu or cpu

from flask import Flask, request, jsonify, abort

app = Flask(__name__)

#import logging
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)
#app.logger.disabled = True
#log.disabled = True


# доступные спикера
speakers = model.speakers # ['aidar', 'baya', 'kseniya', 'xenia', 'eugene', 'random']

SpeakerPatchInit(model,example_text)

# Docker HealthCheck
@app.route('/health', methods=['GET'])
def doHEALTH():
    return "OK"

# TTS вход
@app.route('/tts', methods=['POST'])
def doTTS():
    req = request.json
    if request.json['api_token'] != ApiToken:
        abort(403)
        return
    audio = None
    speaker = request.json['speaker']

    speaker, voiceFile = SpeakerPatch(speaker,speakers)

    if request.json['ssml']:
        audio = model.apply_tts(ssml_text=request.json['text'],
            speaker=speaker,
            sample_rate=request.json['sample_rate'],
            put_accent=request.json['put_accent'],
            put_yo=request.json['put_yo'],
            voice_path=voiceFile
        )
    else:
        audio = model.apply_tts(text=request.json['text'],
            speaker=speaker,
            sample_rate=request.json['sample_rate'],
            put_accent=request.json['put_accent'],
            put_yo=request.json['put_yo'],
            voice_path=voiceFile
        )
    # Saving to bytes buffer
    buffer_ = io.BytesIO()
    torchaudio.save(buffer_, audio.unsqueeze(0), request.json['sample_rate'], format=req["format"])
    buffer_.seek(0)

    effect = req.json['effect'] or None

    if effect == "Echo": 
        # метро: (для аннонсов)
        delay = 0.03  # Задержка в секундах (30 миллисекунд)
        decay = 0.7  # Затухание
        buffer_ = add_echo(buffer_, delay, decay)
    elif effect == "Radio":
        cutoff_freq_low = 2000  # Частота среза для фильтра низких частот (Гц)
        cutoff_freq_high = 3000  # Частота среза для фильтра высоких частот (Гц)
        noise_level = 0.1  # Уровень шума
        buffer_ = add_radio_effect(buffer_, cutoff_freq_low, cutoff_freq_high, noise_level)

    return jsonify({'results': [{'Audio': base64.b64encode(buffer_.getvalue()).decode()}]})

if __name__ == '__main__':
    WarmUp(model,speakers)
    app.run(host= '0.0.0.0',debug=False,port=int(os.environ.get("PORT","5000")))