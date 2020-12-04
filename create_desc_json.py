# Importing Dependencies 
import csv
import os 
import re
import json
import wave
from sys import argv, exit

# Function to calculate duration of audio file
def get_audio_duration(audio_path):
    audio = wave.open(audio_path)
    duration = float(audio.getnframes()) / audio.getframerate()
    audio.close()
    return duration

# Main Function 
def main(data_directory, output_file):
    # Key-words to drop line
    numbers = ['१', '२', '३', '४', '५', '६', '७', '८', '९', '०']
    # Open tsv file
    transcript= open("./dev-clean/Nepali/utt_spk_text_small.tsv", "r")
    transcript_reader=csv.reader(transcript, delimiter="\t" )
    
    file_names=list()
    labels=list()

    # Check and drop lines containing numbers
    for row in transcript_reader:
        drop_line=False
        for letter in row[2]:
            if letter in numbers:
                drop_line=True
                break
        # If not dropped check for audio file 
        if not drop_line:
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

    # Dump contents as dictionary in json
    with open(output_file, 'w') as out_file:
        for i in range(len(paths)):
            line = json.dumps({'path': paths[i],'duration':durations[i],'text': texts[i]}, ensure_ascii=False)
            out_file.write(line + '\n')

# Main function call
if __name__ == "__main__":
    if len(argv) !=3:
        print("Error in command, exiting...")
        exit()
    data_directory = argv[1]
    output_file = argv[2]
    main(data_directory, output_file)

    