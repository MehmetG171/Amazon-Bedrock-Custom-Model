import pandas as pd
from datasets import load_dataset

# Load the dataset from the huggingface hub
dataset = load_dataset("knkarthick/dialogsum")

# Convert the dataset to a pandas DataFrame
dft = dataset['train'].to_pandas()

# Drop the columns that are not required for fine-tuning
dft = dft.drop(columns=['id', 'topic'])

# Rename the columns to prompt and completion as required for fine-tuning.
# Ref: https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization-prereq.html#model-customization-prepare
dft = dft.rename(columns={"dialogue": "prompt", "summary": "completion"})

# Limit the number of rows to 10,000 for fine-tuning
dft = dft.sample(10000,
    random_state=42)

# Save DataFrame as a JSONL file, with each line as a JSON object
dft.to_json('dialogsum-train-finetune.jsonl', orient='records', lines=True)