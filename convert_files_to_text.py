import os
import speech_recognition as sr
from docx import Document
from pydub import AudioSegment

# lista todos os arquivos de áudio na pasta 'audio'
audio_files = [f for f in os.listdir("audio") if f.endswith('.mp3')]
# 

# cria a pasta recordsWav caso não exista
if not os.path.exists('recordsWav'):
    os.makedirs('recordsWav')

# Reconhecimento de fala para cada arquivo de áudio na lista
r = sr.Recognizer()
for audio_file in audio_files:
    # convertendo o áudio mp3 para WAV e salvando em recordsWav
    sound = AudioSegment.from_mp3(os.path.join('audio', audio_file))
    sound.export(os.path.join('recordsWav', audio_file.replace('.mp3', '.wav')), format="wav")

    # reconhecendo o áudio
    with sr.AudioFile(os.path.join('recordsWav', audio_file.replace('.mp3', '.wav'))) as source:
        audio = r.record(source)

    try:
        # transformando o áudio em texto
        text = r.recognize_google(audio, language='pt-BR')
        # print("Áudio: {}, Texto: {}".format(audio_file, text))
        print("Áudio: {} | Está sendo formatado...".format(audio_file, text))


        # gera o arquivo .docx
        filename = "texto.docx"
        if not os.path.exists(filename):
            doc = Document()
            doc.save(filename)
        doc = Document(filename)
        doc.add_paragraph(text)
        doc.save(filename)

    except sr.UnknownValueError:
        print("Não foi possível entender o áudio: {}".format(audio_file))
    except sr.RequestError as e:
        print(
            "Não foi possível acessar o serviço de reconhecimento de fala; {0}".format(e))