from funasr_torch import Paraformer

model_dir = "/home/gzf/FunASR/export/damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch"

#model = Paraformer(model_dir, batch_size=2, plot_timestamp_to="./", pred_bias=0)  # cpu
model = Paraformer(model_dir, batch_size=2, plot_timestamp_to="./", pred_bias=0, device_id=0)  # gpu

# when using paraformer-large-vad-punc model, you can set plot_timestamp_to="./xx.png" to get figure of alignment besides timestamps
# model = Paraformer(model_dir, batch_size=1, plot_timestamp_to="test.png")


wav_path = "/home/gzf/FunASR/export/damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch/example/asr_example.wav"

for i in range(100):
    result = model(wav_path)
    print(result)
