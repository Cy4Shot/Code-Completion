import console
import os
import random
import pickle

# Select the file
files = os.listdir("src")
selected_file = console.choose(files, "Select file to process:")

# Read the file
with open(f"src/{selected_file}") as f:
    text = f.read()
    lines = text.split("\n")

# Ask for the number of predictions
num_pred = console.prompt_int(
    "How many predictions to ask?", default=len(lines))
results = []

# For each prediction, pick a random position in the text
for _ in range(num_pred):
    pos = random.randint(0, len(text))

    # We want to select all the text before, and all the text on the remaining lines
    prefix = text[:pos]
    after = text[pos:]
    suffix = after[after.find("\n")+1:]
    expected = after[:after.find("\n")]
    
    results.append((prefix, suffix, expected))

# Save the results
pickle.dump(results, open("dataset.pkl", "wb"))