from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

model="/home/gzf/export/damo/speech_fsmn_vad_zh-cn-16k-common-pytorch"
inference_pipeline = pipeline(
    task=Tasks.voice_activity_detection,
    model=model,
    model_revision=None,
)
audio_in="/home/gzf/export/damo/speech_fsmn_vad_zh-cn-16k-common-pytorch/example/vad_example.wav"
segments_result = inference_pipeline(audio_in=audio_in)
print(segments_result)
