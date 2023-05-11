import os

# Get the current working directory
cwd = os.getcwd()
dynVoices = cwd + "/voices"

# float_val = config.getfloat('section_a', 'pi_val')

if not os.path.exists(dynVoices):
    os.makedirs(dynVoices)

# фикс не доступных спикеров
speakers_not_avaible = {
    # free: 'aidar','eugene'
    'Male': ['arthas', 'thrall', 'kael', 'rexxar', 'furion', 'illidan', 'kelthuzad', 'narrator', 'cairne', 'garithos',
             'anubarak', 'uther', 'grunt', 'medivh', 'villagerm', 'illidan_f', 'peon', 'chen', 'dread_bm', 'priest',
             'acolyte', 'muradin', 'dread_t', 'mannoroth', 'peasant', 'wheatley', 'barney', 'raynor', 'tusk', 'earth',
             'wraith', 'bristle', 'gyro', 'treant', 'lancer', 'clockwerk', 'batrider', 'kotl', 'kunkka', 'pudge',
             'juggernaut', 'vort_e2', 'omni', 'sniper', 'skywrath', 'huskar', 'bloodseeker', 'shaker', 'storm', 'tide',
             'riki', 'witchdoctor', 'doom', 'bandit', 'pantheon', 'tychus', 'breen', 'kleiner', 'father', 'tosh',
             'stetmann', 'hanson', 'swann', 'hill', 'gman_e2', 'valerian', 'gman', 'vort', 'aradesh', 'dornan',
             'harris', 'cabbot', 'decker', 'dick', 'officer', 'frank', 'gizmo', 'hakunin', 'harold', 'harry', 'maxson',
             'killian', 'lieutenant', 'loxley', 'lynette', 'marcus', 'master', 'morpheus', 'overseer', 'rhombus', 'set',
             'sulik', 'dude', 'archmage', 'demoman', 'engineer', 'heavy', 'medic', 'scout', 'soldier', 'spy', 'admiral',
             'alchemist', 'archimonde', 'breaker', 'captain', 'footman', 'grom', 'hh', 'keeper', 'naga_m', 'naga_rg',
             'rifleman', 'satyr', 'voljin', 'sidorovich'],
    # free 'kseniya','xenia'
    'Female': ['maiev', 'tyrande', 'jaina', 'ladyvashj', 'naisha', 'sylvanas', 'sorceress', 'alyx', 'glados',
               'announcer', 'kerrigan', 'lina', 'luna', 'windranger', 'templar', 'ranger', 'mortred', 'queen',
               'evelynn', 'elder', 'jain', 'laura', 'nicole', 'tandi', 'vree', 'huntress', 'peasant_w', 'sylvanas_w'],
    # free 'baya'
    'Unsexed': ['meepo', 'bounty', 'antimage', 'yuumi', 'myron', 'dryad', 'elf_eng']
}

# рандомизация не доступных спикеров

speakers_rnd = {}


def SpeakerPatchInit(model, example_text):
    for idx, value in enumerate(speakers_not_avaible['Male']):
        if (idx % 2) == 0:
            speakers_rnd[value] = 1
        else:
            speakers_rnd[value] = 2
        # if not os.path.isfile(dynVoices+"/"+value+".pt"):
        #    model.apply_tts(text=example_text, speaker="random", sample_rate=24000, put_accent=False, put_yo=False)
        #   model.save_random_voice(dynVoices+"/"+value+".pt")
    for idx, value in enumerate(speakers_not_avaible['Female']):
        if (idx % 2) == 0:
            speakers_rnd[value] = 1
        else:
            speakers_rnd[value] = 2

        # if not os.path.isfile(dynVoices+"/"+value+".pt"):
        #    model.apply_tts(text=example_text, speaker="random", sample_rate=24000, put_accent=False, put_yo=False)
        #    model.save_random_voice(dynVoices+"/"+value+".pt")


def SpeakerPatch(speaker, speakers):
    voiceFile = dynVoices + "/" + speaker + ".pt"
    if os.path.exists(voiceFile):
        return "random", voiceFile
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
    return speaker, voiceFile
