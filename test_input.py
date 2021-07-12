import sys
sys.path.append("..")
from tensorflow_tts.inference import AutoProcessor
processor = AutoProcessor.from_pretrained("tts-fastspeech2-baker-ch.mapper.json")
str = input("请输入：")
print(str)
processor.set_english_dict(str)