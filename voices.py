import gtts

def is_english(x):
    return ('English' in x['LanguageName'])

def is_neural(x):
    return 'neural' in x['SupportedEngines']

def is_standard(x):
    return 'standard' in x['SupportedEngines']

tts = gtts.TTS()
all_voices = tts.get_voices()

english_voices = list(filter(is_english, all_voices))
neural_voice_names = [x['Name'] for x in filter(is_neural, english_voices)]
standard_voice_names = [x['Name'] for x in filter(is_standard, english_voices)]

print(standard_voice_names)

#for voice in standard_voices:
#    name = voice['Name']
#    lang = voice['LanguageName']
#    engines = voice['SupportedEngines']
#    print (f"{name}, {lang} {engines}")
    