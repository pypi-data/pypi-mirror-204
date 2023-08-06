#from torch_paraformer import Paraformer
from funasr_torch import Paraformer
import time

model_dir = "/home/gzf/FunASR/export/damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch"
#model_dir ="/home/gzf/workspace/amp_int8/libtorch_fb20"
#model_dir ="/home/gzf/workspace/amp_int8/onnx_dynamic"
model = Paraformer(model_dir, batch_size=1, device_id=0)

wav_path = ["/home/gzf/FunASR/export/damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch/example/asr_example.wav"]

total = 0.0
num = 100
result = model(wav_path)
for i in range(num):
  beg_time = time.time()
  result = model(wav_path)
  end_time = time.time()
  duration = end_time-beg_time
  total += duration
  print(result)
  print("num: {}, time, {}, avg: {}, rtf: {}".format(len(wav_path), duration, total/(i+1), (total/(i+1))/5.53))
print(result)
