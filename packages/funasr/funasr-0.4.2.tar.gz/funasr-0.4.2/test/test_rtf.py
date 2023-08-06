
import time
import sys
import librosa
backend=sys.argv[1]
model_dir=sys.argv[2]
wav_file=sys.argv[3]

from torch_paraformer import Paraformer
if backend == "onnxruntime":
	from rapid_paraformer import Paraformer
	
# model_dir = "/home/gzf/export/damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch"
#model_dir ="/home/gzf/workspace/amp_int8/libtorch_fb20"
#model_dir ="/home/gzf/workspace/amp_int8/onnx_dynamic"

model = Paraformer(model_dir, batch_size=1, device_id="-1")

# wav_path = ["/nfs/zhifu.gzf/export/damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch/example/asr_example.wav", "/nfs/zhifu.gzf/export/damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch/example/asr_example.wav"]
# wav_path = ["/home/gzf/export/damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch/example/asr_example.wav"]

wav_file_f = open(wav_file, 'r')
wav_files = wav_file_f.readlines()

# warm-up
total = 0.0
num = 100
wav_path = wav_files[0].strip()
for i in range(num):
	beg_time = time.time()
	result = model(wav_path)
	end_time = time.time()
	duration = end_time-beg_time
	total += duration
	print(result)
	print("num: {}, time, {}, avg: {}, rtf: {}".format(len(wav_path), duration, total/(i+1), (total/(i+1))/5.53))

# infer time
beg_time = time.time()
for i, wav_path in enumerate(wav_files):
	wav_path = wav_path.strip()
	result = model(wav_path)
end_time = time.time()
duration = end_time-beg_time
print("total_time_comput: {}".format(duration))

duration_time = 0.0
for i, wav_path in enumerate(wav_files):
	waveform, _ = librosa.load(wav_path, sr=16000)
	duration_time += len(waveform)/16000.0
print("total_time_wav: {}".format(duration_time))

print("total_rtf: {}".format(duration/duration_time))
