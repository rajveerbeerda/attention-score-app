import azure.cognitiveservices.speech as speechsdk
def detect_voice(audio_filename):
    speech_key, service_region = "3c48fa0556424fc48287a4225a91c03a", "centralindia"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_input = speechsdk.audio.AudioConfig(filename=audio_filename)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    result = speech_recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return True
    else:
        return False
