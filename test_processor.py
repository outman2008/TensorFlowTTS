import sys
sys.path.append("..")

import tensorflow as tf
import IPython.display as ipd

from tensorflow_tts.inference import TFAutoModel
from tensorflow_tts.inference import AutoProcessor

fastspeech2 = TFAutoModel.from_pretrained("tensorspeech/tts-fastspeech2-baker-ch", name="fastspeech2")
mb_melgan = TFAutoModel.from_pretrained("tensorspeech/tts-mb_melgan-baker-ch", name="mb_melgan")
processor = AutoProcessor.from_pretrained("tts-fastspeech2-baker-ch.mapper.json")
text = input("请输入：")
input_ids = processor.text_to_sequence(text, inference=True)
mel_before, mel_outputs, duration_outputs, _, _ = fastspeech2.inference(
    input_ids=tf.expand_dims(tf.convert_to_tensor(input_ids, dtype=tf.int32), 0),
    speaker_ids=tf.convert_to_tensor([0], dtype=tf.int32),
    speed_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
    f0_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
    energy_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
)
# melgan inference (mel-to-wav)
output = mb_melgan.inference(mel_outputs)[0, :, 0]
ipd.Audio(output, rate=22050)