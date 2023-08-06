from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.utils.logger import get_logger
import logging
logger = get_logger(log_level=logging.CRITICAL)
logger.setLevel(logging.CRITICAL)

import soundfile

waveform, sample_rate = soundfile.read("/home/gzf/huiyi_pianduan.wav")
waveform, sample_rate = soundfile.read("/home/gzf/2.wav")
# fs = 16000

inference_pipeline_vad = pipeline(
    task=Tasks.voice_activity_detection,
    model='damo/speech_fsmn_vad_zh-cn-16k-common-pytorch',
    model_revision=None,
)
inference_pipeline = pipeline(
    task=Tasks.auto_speech_recognition,
    model='damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch')

inference_pipeline_punc = pipeline(
    task=Tasks.punctuation,
    model='damo/punc_ct-transformer_zh-cn-common-vad_realtime-vocab272727',
    model_revision=None,
)

segments_result = inference_pipeline_vad(audio_in=waveform)
param_punc_dict = {"cache": []}
for i, segments in enumerate(segments_result["text"]):
    beg_idx = segments[0] * sample_rate/1000
    end_idx = segments[1] * sample_rate/1000
    waveform_slice = waveform[int(beg_idx):int(end_idx)]
    result_segments = inference_pipeline(audio_in=waveform_slice)
    result_segments_withpunc = inference_pipeline_punc(text_in=result_segments['text'], param_dict=param_punc_dict)
    print(result_segments_withpunc['text'])
