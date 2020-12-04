"""
Defines two dictionaries for converting 
between text and integer sequences.
"""
# List of all the characters in dataset
char_map_str = """
<SPACE>
ं 
् 
ा 
ि 
ु 
ृ 
े 
ै 
ो 
ौ 
अ 
आ 
इ 
उ 
ए 
ऐ 
ओ 
औ 
क 
ख 
ग 
घ 
ङ 
च 
छ 
ज 
झ 
ञ 
त 
थ 
द 
ध 
न 
प 
फ 
भ 
म 
य 
र 
ल 
व 
स 
ह 
"""
# Initialize all variables
char_map ={}
index_map = {}
char_map_list = char_map_str.strip().split('\n')
char_map_list=[char_map_list[i].strip() for i in range(len(char_map_list))]   

# Create dictionaries to map letters to integers and vice versa
for char in char_map_list:
    index = char_map_list.index(char)
    char_map[char] = index
    index_map[index]=char
