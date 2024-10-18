from transformers import AutoModelForCausalLM, AutoTokenizer
import pickle
import console

# Start by initalizing the model
checkpoint = "bigcode/starcoder2-3b"
device = "cuda"

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device)

# Load the generated dataset
with open("dataset.pkl", "rb") as f:
    dataset = pickle.load(f)

# Start writing the report
output = "# Report\n\n"

for prefix, suffix, expected in dataset:
    
    # Generate the prediction
    input_text = f"<fim_prefix>{prefix}<fim_suffix>{suffix}<fim_middle>"
    inputs = tokenizer.encode(input_text, return_tensors="pt").to(device)
    outputs = model.generate(inputs, max_new_tokens=100, pad_token_id=tokenizer.eos_token_id)

    # Extract the prediction
    prediction = tokenizer.decode(outputs[0])
    prediction = prediction[prediction.find("<fim_middle>")+12:]
    prediction = prediction[:prediction.find("\n")]

    # Generate the console output & write to the report
    input_line = prefix[prefix.rfind("\n")+1:].lstrip()

    console.print(f"[bright_black italic]{input_line}", expected.lstrip(), sep="")
    console.print(f"[bright_black italic]{input_line}", prediction.lstrip(), sep="")
    console.print("="*50)
    
    output += f"`{input_line}`\n"
    output += f"> Expected \t`{expected.lstrip()}`\n"
    output += f"> Predicted\t`{prediction.lstrip()}`\n\n"

# Save the report
with open("report.md", "w") as f:
    f.write(output)