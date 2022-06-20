from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import re

from tempfile import gettempdir

MAX_TTS_LEN = 2900

class TTSException(Exception):
    pass

class SegmentException(Exception):
    pass
    
def segment_by_punctuation(to_segment):

    sentences = re.split('([\.;:\?\!])',to_segment)

    s = ""
    for x in sentences:
        if MAX_TTS_LEN <= len(x):
            print("cannot segment: this sentence is too long! " + s) 
            raise SegmentException

    paragraphs = []
    paragraph = "" 

    for x in sentences:
        if len(paragraph) + len(x) > MAX_TTS_LEN:
            paragraphs.append(paragraph)
            paragraph = ""
        paragraph = paragraph + x
    paragraphs.append(paragraph)
    
    return paragraphs

def is_english(x):
    return ('English' in x['LanguageName'])

def is_neural(x):
    return 'neural' in x['SupportedEngines']

def is_standard(x):
    return 'standard' in x['SupportedEngines']

class TTS:

    def set_voice(self, voice, neural):
        if self.is_valid_voice(voice, neural):
            self.voice =  voice
            self.neural = neural
        else:
            engine_type = "neural" if neural else "standard"
            raise TTSException(f"invalid voice/engine combo ({voice}/{engine_type}).")
        
    def __init__(self, voice="Joanna", neural=True):
        self.set_voice(voice, neural)
        
    def is_valid_voice(self, voice, neural):
       
        all_voices = self.get_voices()

        english_voices = list(filter(is_english, all_voices))
        
        if neural:
            voice_names = [x['Name'] for x in filter(is_neural, english_voices)]
        else:
            voice_names = [x['Name'] for x in filter(is_standard, english_voices)]

        return (voice in voice_names)

    def list_voices(self):
        all_voices = self.get_voices()    
        english_voices = list(filter(lambda x: ('English' in x['LanguageName']), all_voices))

        for voice in english_voices:
            name = voice['Name']
            lang = voice['LanguageName']
            engines = voice['SupportedEngines']
            print (f"{name}, {lang} {engines}")        
        
    def get_client(self):
        session = Session(profile_name="adminuser")
        p = session.client("polly", region_name='us-west-2')
        return p
        
    def get_voices(self):
        return self.get_client().describe_voices()['Voices']

    def speak_to_files(self, text_to_process, out_file_prefix):
        segments = segment_by_punctuation(text_to_process)
        for i, segment in enumerate(segments):
            out_file_name = f"{out_file_prefix}_{i+1:04}.mp3"
            self.speak_to_file(segment, out_file_name)
         
    def speak_to_file(self, text_to_process, out_file_name):

        polly = self.get_client()
        engine = "neural" if self.neural else "standard"
        
        try:
            response = polly.synthesize_speech(Text=text_to_process, OutputFormat="mp3", VoiceId=self.voice, Engine=engine)
        except (BotoCoreError, ClientError) as error:
            raise TTSException(error)
            
        if "AudioStream" in response:
            # Closing the stream is important; service throttles on # of parallel connections.
                with closing(response["AudioStream"]) as stream:
                   try:
                        with open(out_file_name, "wb") as file:
                           file.write(stream.read())
                   except IOError as error:
                      raise TTSException(error)
        else:
            raise TTSException("no stream found in response")
