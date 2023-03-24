import json

input_file = "NRC-Emotion-Lexicon-Wordlevel-v0.92.txt"
output_file = "NRC-Emotion-Lexicon-Wordlevel-v0.92.json"

emotions = ["anger", "anticipation", "disgust", "fear", "joy", "negative", "positive", "sadness", "surprise", "trust"]

lexicon = {}

with open(input_file) as f:
    for line in f:
        if line.strip():
            word, emotion, value = line.strip().split("\t")
            if word not in lexicon:
                lexicon[word] = {e: 0 for e in emotions}
            lexicon[word][emotion] = int(value)

with open(output_file, "w") as f:
    json.dump(lexicon, f, indent=4)