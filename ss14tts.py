import base64
import io
import torch
import torchaudio

language = 'ru'
model_id = 'v3_1_ru'
device = torch.device('cpu')

model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                     model='silero_tts',
                                     language=language,
                                     speaker=model_id)

from flask import Flask, request, jsonify

app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app.logger.disabled = True
log.disabled = True

speakers = ['aidar', 'baya', 'kseniya', 'xenia', 'eugene', 'random']


@app.route('/tts', methods=['POST'])
def get_tasks():
    req = request.json
    if request.json['api_token'] != "test":
        return
    audio = None
    speaker = request.json['speaker']
    if speaker not in speakers:
        if speaker == 'garithos':
            speaker = 'aidar'
        else:
            speaker = 'eugene'

    if request.json['ssml']:
        audio = model.apply_tts(ssml_text=request.json['text'],
            speaker=speaker,
            sample_rate=request.json['sample_rate'],
            put_accent=request.json['put_accent'],
            put_yo=request.json['put_yo']
        )
    else:
        audio = model.apply_tts(text=request.json['text'],
            speaker=speaker,
            sample_rate=request.json['sample_rate'],
            put_accent=request.json['put_accent'],
            put_yo=request.json['put_yo']
        )
    # Saving to bytes buffer
    buffer_ = io.BytesIO()
    torchaudio.save(buffer_, audio.unsqueeze(0), request.json['sample_rate'], format=req["format"])
    buffer_.seek(0)

    return jsonify({'results': [{'Audio': base64.b64encode(buffer_.getvalue()).decode()}]})


app.run(host= '0.0.0.0',debug=False)