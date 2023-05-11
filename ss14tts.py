import base64, os, io

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

from src.SpeakerPatch import SpeakerPatch, SpeakerPatchInit
from src.WarmUp import WarmUp

import torch
import torchaudio

torch.set_num_threads(int(os.environ.get("threads", "4")))
deviceName = "cuda" if torch.cuda.is_available() else "cpu"
device = torch.device(deviceName)

# init .ini parser
config = ConfigParser()
# parse config
config.read('config.ini')
# read values from a section
language = config.get('main', 'language')
model_id = config.get('main', 'model_id')
speakers = config.get('main', 'speakers')
ApiToken = os.environ.get("apitoken", "test")

local_file = 'model.pt'
if not os.path.isfile(local_file):
    print("Start download silero models")
    torch.hub.download_url_to_file(f'https://models.silero.ai/models/tts/{language}/{model_id}.pt',
                                   local_file)

model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
example_text = "В недрах тундры выдры в г+етрах т+ырят в вёдра ядра кедров."
# model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
#    model='silero_tts',
#    language=language,
#    speaker=model_id, 
#    trust_repo=True,
#    verbose=False
# )

model.to(device)  # gpu or cpu

from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# import logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)
# app.logger.disabled = True
# log.disabled = True


# доступные спикера
# speakers = ['aidar', 'baya', 'kseniya', 'xenia', 'eugene', 'random']

SpeakerPatchInit(model, example_text)


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

    speaker, voiceFile = SpeakerPatch(speaker, speakers)

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

    return jsonify({'results': [{'Audio': base64.b64encode(buffer_.getvalue()).decode()}]})


if __name__ == '__main__':
    WarmUp(model, speakers)
    app.run(host='0.0.0.0', debug=False, port=int(os.environ.get("PORT", "5000")))
