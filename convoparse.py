
import re

class DialogLine:
    def __init__(self, raw_text):
        self.parse(raw_text)
    
    #format is SPEAKER: TEXT
    def parse(self, raw_text):
        raw_text = raw_text.strip()

        separator = raw_text.find(':')

        if separator == -1:
            self.speaker = None
            self.text = raw_text
        else:
            self.speaker = raw_text[:separator].strip()
            self.text = raw_text[separator+1:].strip()

    def append(self, text):
        self.text = self.text + text    

def get_aliases(self):
  
    if self.speaker is None:    
        return []
    else:

        aliases = [self.speaker.upper()]

        if self.speaker.find(' ') != -1:
            #add acronym of speaker's name to aliases
            acronym = ''
            for name in self.speaker.split(' '):
                acronym += name[0]
            aliases.append(acronym)

              #add speakers first name to aliases
            aliases.append(self.speaker.split(' ')[0])

        return aliases

def parse_conversation(conversation):

    conversation = re.sub(r'\n+', '\n', conversation)
    
    lines = []

    for paragraph in conversation.split('\n'):
        line = DialogLine(paragraph)
        if line.speaker is None: 
            #this is a continuation of the previous line
            if len(lines) == 0:
                raise Exception("No previous line to append to")
            last_line = lines[-1]   
            last_line.append(line.text)
        else:
            lines.append(line)  
    
    return lines
                 


text = open("playboyconvo.txt", "r").read()

convo = parse_conversation(text)

for line in convo:
    print(f'{line.speaker} said, "{line.text}"')

