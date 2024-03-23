import cs50
import re

text = cs50.get_string("Text: ")

# Use a dictionary to keep track. Start with word count 1 to
# avoid the off-by-one error also encounters in the C version
lws = {
    "letters": 0,
    "words": 1,
    "sentences": 0,
}

for i in range(len(text)):
    if re.match("[a-zA-Z]", text[i]):
        lws["letters"] += 1
    elif re.match(" ", text[i]):
        lws["words"] += 1
    elif re.match("\.|\?|!", text[i]):
        lws["sentences"] += 1

l = lws["letters"] / lws["words"] * 100
s = lws["sentences"] / lws["words"] * 100
index = round(0.0588 * l - 0.29 * s - 15.8)

if index > 16:
    print("Grade 16+")
elif index > 1 and index < 16:
    print(f"Grade {index}")
else:
    print("Before Grade 1")
