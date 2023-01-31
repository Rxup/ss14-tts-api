import base64
import io
import torch
import torchaudio

torch.set_num_threads(4)

language = 'ru'
model_id = 'v3_1_ru'
device = torch.device('cpu')

model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                     model='silero_tts',
                                     language=language,
                                     speaker=model_id, 
                                     trust_repo=True)

from flask import Flask, request, jsonify

app = Flask(__name__)

#import logging
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)
#app.logger.disabled = True
#log.disabled = True

speakers = ['aidar', 'baya', 'kseniya', 'xenia', 'eugene', 'random']

speakers_not_avaible = {
    #free: 'aidar','eugene'
    'Male': ['arthas','thrall','kael','rexxar','furion','illidan','kelthuzad','narrator','cairne','garithos','anubarak','uther','grunt','medivh','villagerm','illidan_f','peon','chen','dread_bm','priest','acolyte','muradin','dread_t','mannoroth','peasant','wheatley','barney','raynor','tusk','earth','wraith','bristle','gyro','treant','lancer','clockwerk','batrider','kotl','kunkka','pudge','juggernaut','vort_e2','omni','sniper','skywrath','huskar','bloodseeker','shaker','storm','tide','riki','witchdoctor','doom','bandit','pantheon','tychus','breen','kleiner','father','tosh','stetmann','hanson','swann','hill','gman_e2','valerian','gman','vort','aradesh','dornan','harris','cabbot','decker','dick','officer','frank','gizmo','hakunin','harold','harry','maxson','killian','lieutenant','loxley','lynette','marcus','master','morpheus','overseer','rhombus','set','sulik','dude','archmage','demoman','engineer','heavy','medic','scout','soldier','spy','admiral','alchemist','archimonde','breaker','captain','footman','grom','hh','keeper','naga_m','naga_rg','rifleman','satyr','voljin','sidorovich'], 
    #free 'kseniya','xenia'
    'Female': ['maiev','tyrande','jaina','ladyvashj','naisha','sylvanas','sorceress','alyx','glados','announcer','kerrigan','lina','luna','windranger','templar','ranger','mortred','queen','evelynn','elder','jain','laura','nicole','tandi','vree','huntress','peasant_w','sylvanas_w'],
    #free 'baya'
    'Unsexed': ['meepo','bounty','antimage','yuumi','myron','dryad','elf_eng']
}
speakers_rnd = {}
for idx, value in enumerate(speakers_not_avaible['Male']):
    if (idx % 2) == 0:
        speakers_rnd[value] = 1
    else:
        speakers_rnd[value] = 2
for idx, value in enumerate(speakers_not_avaible['Female']):
    if (idx % 2) == 0:
        speakers_rnd[value] = 1
    else:
        speakers_rnd[value] = 2

@app.route('/tts', methods=['POST'])
def get_tasks():
    req = request.json
    if request.json['api_token'] != "test":
        return
    audio = None
    speaker = request.json['speaker']
    if speaker not in speakers:
        if speaker in speakers_not_avaible['Male']:
            if speakers_rnd[speaker] == 1:
                speaker = 'aidar'
            else:
                speaker = 'eugene'
        elif speaker in speakers_not_avaible['Female']:
            if speakers_rnd[speaker] == 1:
                speaker = 'xenia'
            else:
                speaker = 'kseniya'
        elif speaker in speakers_not_avaible['Unsexed']:
            speaker = 'baya'
    if speaker not in speakers:
        speaker = 'baya'
    
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

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=False)