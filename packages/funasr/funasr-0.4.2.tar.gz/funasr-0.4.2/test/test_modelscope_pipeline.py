from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

if __name__ == '__main__':
#    audio_in = 'https://isv-data.oss-cn-hangzhou.aliyuncs.com/ics/MaaS/ASR/test_audio/asr_example_zh.wav'
    audio_in = '/data/mengzhe.cmz/post-processing_transformer/easyspeech_pytorch/test_env_punc/video.wav'
    audio_in="/home/gzf/video.wav"
    output_dir = None
    inference_pipeline = pipeline(
        task=Tasks.auto_speech_recognition,
        model='damo/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
        #vad_model='damo/speech_fsmn_vad_zh-cn-16k-common-pytorch',
        #punc_model='damo/punc_ct-transformer_zh-cn-common-vocab272727-pytorch',
        ngpu=0,
        ncpu=8,
    )
    rec_result = inference_pipeline(audio_in=audio_in)
    print(rec_result)
