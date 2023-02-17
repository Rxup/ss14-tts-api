import base64, os, io

from src.SpeakerPatch import SpeakerPatch,SpeakerPatchInit
from src.WarmUp import WarmUp

import torch
import torchaudio

torch.set_num_threads(int(os.environ.get("threads","4")))

language = 'ru'
model_id = 'v3_1_ru'
deviceName = "cuda" if torch.cuda.is_available() else "cpu"
device = torch.device(deviceName)

ApiToken = os.environ.get("apitoken","test")

model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                     model='silero_tts',
                                     language=language,
                                     speaker=model_id, 
                                     trust_repo=True)

model.to(device)  # gpu or cpu

from flask import Flask, request, jsonify, abort

app = Flask(__name__)

#import logging
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)
#app.logger.disabled = True
#log.disabled = True


# доступные спикера
speakers = ['aidar', 'baya', 'kseniya', 'xenia', 'eugene', 'random']

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

    return jsonify({'results': [{'Audio': base64.b64encode(buffer_.getvalue()).decode()}]})

if __name__ == '__main__':
    WarmUp(model,speakers)
    app.run(host= '0.0.0.0',debug=False,port=int(os.environ.get("PORT","5000")))