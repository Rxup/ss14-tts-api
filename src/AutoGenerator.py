import random
from src.SpeakerPatch import dynVoices

example_text = ["Съешь же ещё этих мягких французских булок, да выпей чаю.",
        "Клоун, прекрати разбрасывать банановые кожурки офицерам под ноги!",
        "Капитан, вы уверены что хотите назначить клоуна на должность главы персонала?",
        "Эс Бэ! Тут человек в сером костюме, с тулбоксом и в маске! Помогите!!"]
def Generate(model,ct):
    for idx in range(1, int(ct), 1):
        model.apply_tts(text=random.choice(example_text), speaker="random", sample_rate=24000, put_accent=False, put_yo=False)
        model.save_random_voice(dynVoices+"/Voice"+str(idx)+".pt")
        yield dynVoices+"/Voice"+str(idx)+".pt"

