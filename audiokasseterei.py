import ggpt
import gtts
import subprocess

import click

'''accept title and prompt as command line parameters'''

@click.command()
@click.option('--title', prompt='Title',
              help='The title of the text')
@click.option('--prompt', prompt='Prompt',
              help='The start of the text')
#optional parameter voice default "Aria"
@click.option('--voice', default='Aria',
              help='The voice of the reader')              
@click.option('--author', help="Enters e-book mode using the supplied author's name.")
@click.option('--neural/--standard', default=True)
              
#print title, prompt and voice 
def speak_text(title, prompt, voice, author, neural):
    
    if author is not None:
        prompt = f"{title}\nThe stunning best-seller by {author}\n\nChapter 1\n\n{prompt}"
        print(f'Writing "{title}" by {author}, as read by {voice}.')
    else:
        print(f'Writing "{title}", as read by {voice}.')
        
    gpt = ggpt.GPT()
    gpt.temperature = 1.1

    tts = gtts.TTS(voice, neural)
        

    pulls = 20
    MAX_MSG_LEN = 5000

    text_out = open(f"{title}.txt", "w", encoding="utf-8")
    text_out.write(prompt)

    text = prompt
    print(prompt)

    for i in range(pulls):
        #print(i)
        if len(text) < MAX_MSG_LEN: 
            text_end = text[:MAX_MSG_LEN-1]
        else:
            text_end = text
        new_text = gpt.predict(text_end)
        text_out.write(new_text)
        text_out.flush()
        text = text + new_text
        print(new_text)

    tts.speak_to_files(text, title)

    subprocess.run(f'sox "{title}_*.mp3" "{title}.mp3"' ,shell=True, check=True)


if __name__ == '__main__':
    speak_text()    

