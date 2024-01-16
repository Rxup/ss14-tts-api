from ss14tts import model, speakers, add_echo, add_radio_effect
import torchaudio, io

example_text = "В н+едрах т+ундры в+ыдры в г+етрах т+ырят в в+ёдра +ядра к+едров."
audio = model.apply_tts(text=example_text, speaker="random", sample_rate=24000, put_accent=False, put_yo=False)
buffer_ = io.BytesIO()
torchaudio.save(buffer_, audio.unsqueeze(0), 24000, format="ogg")
buffer_.seek(0)
buffer_ = add_echo(buffer_, output_format="ogg")
buffer_ = add_radio_effect(buffer_, 24000, format="ogg")