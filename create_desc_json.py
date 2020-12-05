# Importing Dependencies 
import csv
import os 
import re
import json
import wave
from numpy import random
from sys import argv, exit

# Function to calculate duration of audio file
def get_audio_duration(audio_path):
    audio = wave.open(audio_path)
    duration = float(audio.getnframes()) / audio.getframerate()
    audio.close()
    return duration

# Main Function 
def main(data_directory):
    # Open tsv file
    transcript= open("./sample_dataset/utt_spk_text_clean.tsv", "r")
    transcript_reader=csv.reader(transcript, delimiter="\t" )
    
    file_names=list()
    labels=list()

    # Check and drop lines containing numbers
    for row in transcript_reader:
        file_names.append(row[0])
        labels.append(row[2])

    transcript.close()

    # Bind file name and corresponding label
    zipped_list = list(zip(file_names, labels))
    sorted_zip = sorted(zipped_list, key = lambda x: x[0]) 

    paths = list()
    texts = list()
    durations= list()

    for file_name, label in sorted_zip:
        # For file name beginning with 0-7, Audio_0_7 directory 
        if re.match("(^[0-7])", file_name):
            audio_path=os.path.join(data_directory, "Audio_0_7", file_name+".wav")
            duration=get_audio_duration(audio_path)
            paths.append(audio_path)
            durations.append(duration)
            texts.append(label)
        # Else, directory Audio_8_f
        else:
            audio_path=os.path.join(data_directory,"Audio_8_f", file_name+".wav")
            duration=get_audio_duration(audio_path)
            paths.append(audio_path)
            durations.append(duration)
            texts.append(label)

    # Dump contents randomly into two json
    size = len(paths)
    print(size)
    
    fv = open("valid_corpus.json", "w")
    ft = open("train_corpus.json", "w")
    fm = open("main_corpus.json", "w")
    threshold = int(0.2 * size)
    while(True):
        distribution = random.binomial(n=1, p=0.2, size=size)

        if list(distribution).count(1)==threshold:
            for index, value in enumerate(distribution):
                line = json.dumps({'path': paths[index],'duration':durations[index],'text': texts[index]}, ensure_ascii=False)
                fm.write(line+"\n")
                if value==1:
                    fv.write(line +"\n")
                else:
                    ft.write(line + "\n")
        
            fv.close()
            ft.close()
            fm.close()
            break

# Main function call
if __name__ == "__main__":
    if len(argv) !=2:
        print("Error in command, exiting...")
        exit()
    data_directory = argv[1]
    main(data_directory)

    