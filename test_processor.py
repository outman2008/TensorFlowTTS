import sys
sys.path.append("..")
# import tensorflow as tf
# import IPython.display as ipd
from tensorflow_tts.models import TFFastSpeech2
from tensorflow_tts.inference import AutoConfig
from tensorflow_tts.configs import FastSpeech2Config

# from tensorflow_tts.inference import TFAutoModel
# from tensorflow_tts.inference import AutoProcessor

# fastspeech2 = TFAutoModel.from_pretrained("tensorspeech/tts-fastspeech2-baker-ch", name="fastspeech2")
# mb_melgan = TFAutoModel.from_pretrained("tensorspeech/tts-mb_melgan-baker-ch", name="mb_melgan")
# processor = AutoProcessor.from_pretrained("tts-fastspeech2-baker-ch.mapper.json")

config = {
    "encoder_hidden_size": 384,
    "encoder_num_hidden_layers": 4,
    "encoder_num_attention_heads": 2,
    "encoder_attention_head_size": 192,
    "encoder_intermediate_size": 1024,
    "encoder_intermediate_kernel_size": 3,
    "encoder_hidden_act": "mish",
    "decoder_hidden_size": 384,
    "decoder_num_hidden_layers": 4,
    "decoder_num_attention_heads": 2,
    "decoder_attention_head_size": 192,
    "decoder_intermediate_size": 1024,
    "decoder_intermediate_kernel_size": 3,
    "decoder_hidden_act": "mish",
    "variant_prediction_num_conv_layers": 2,
    "variant_predictor_filter": 256,
    "variant_predictor_kernel_size": 3,
    "variant_predictor_dropout_rate": 0.5,
    "num_mels": 80,
    "hidden_dropout_prob": 0.2,
    "attention_probs_dropout_prob": 0.1,
    "max_position_embeddings": 2048,
    "initializer_range": 0.02,
    "output_attentions": False,
    "output_hidden_states": False
}
fastspeech2_config = FastSpeech2Config(**config)
tf_model = TFFastSpeech2(
    config=fastspeech2_config, name="fastspeech2"
)
print('num_hidden_layers', fastspeech2_config.encoder_self_attention_params.num_hidden_layers)
tf_model = TFFastSpeech2(fastspeech2_config)
tf_model._build()
tf_var = tf_model.trainable_variables
all_keys = []
for i, var in enumerate(tf_var):
    all_keys.append(var.name)
print('all_keys len', len(all_keys))
print('all_keys', all_keys)
#
# text = input("请输入：")
# input_ids = processor.text_to_sequence(text, inference=True)
# mel_before, mel_outputs, duration_outputs, _, _ = fastspeech2.inference(
#     input_ids=tf.expand_dims(tf.convert_to_tensor(input_ids, dtype=tf.int32), 0),
#     speaker_ids=tf.convert_to_tensor([0], dtype=tf.int32),
#     speed_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
#     f0_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
#     energy_ratios=tf.convert_to_tensor([1.0], dtype=tf.float32),
# )
# # melgan inference (mel-to-wav)
# output = mb_melgan.inference(mel_outputs)[0, :, 0]
# ipd.Audio(output, rate=22050)