# Streamline custom model creation and deployment for Amazon Bedrock using Terraform

## Scenario

This project employs Terraform to automate the end-to-end workflow of managing a public dataset from the Hugging Face Hub. 
The dataset is downloaded, converted into JSONL format, and uploaded to an Amazon Simple Storage Service (Amazon S3) bucket 
with a versioned prefix for traceability and management. Subsequently, the workflow involves the creation of an Amazon Bedrock 
custom model through fine-tuning, alongside the development of an additional model via continued pre-training to meet specific 
requirements.

## Prerequisites

- An AWS account. 
- Configured model access for Cohere `Command-Light` (if you plan to use that model).
- `Terraform v1.0.0` or newer installed.
- `Python v3.8` or newer installed.

## Tasks Overview

![complete](/pics/Overview.png)

1. The user runs the `terraform apply` The Terraform local-exec provisioner is used to run a Python script that downloads the 
public dataset DialogSum from the Hugging Face Hub. This is then used to create a fine-tuning training JSONL file.

2. An S3 bucket stores training, validation, and output data. The generated JSONL file is uploaded to the S3 bucket.

3. The FM defined in the Terraform configuration is used as the source for the custom model training job.

4. The custom model training job uses the fine-tuning training data stored in the S3 bucket to enrich the FM. Amazon Bedrock 
is able to access the data in the S3 bucket (including output data) due to the AWS Identity and Access Management (IAM) role 
defined in the Terraform configuration, which grants access to the S3 bucket.

5. When the custom model training job is complete, the new custom model is available for use.

## Demo

- Make sure that `dialogsum-dataset-finetune.py` is placed in the same directory with `main.tf`.

- Run the following command to create a virtual environment.

```bash
python3 -m venv venv
```

- Activate the virtual environment using the following command.

```bash
source venv/bin/activate
```

- Run the following command to install the datasets package.

```bash
pip3 install datasets
```

- The dataset is already divided into training, validation, and testing splits. This example uses just the training split.

- After checking the configurations in `main.tf`, initialize the Terraform.

```bash
terraform init
```

- Run the following command to validate the syntax for your Terraform files.

```bash
terraform validate
```

- Run the following command to create the resources. Enter `yes` to approve the changes.

```bash
terraform apply
```

- Enter `yes` to approve the changes.

- Notice the `training` status on the console. Wait for training to finish. It will take some time.

![training](/pics/Console-Training.png)

- After the training is finished, the model will be ready to use.

![complete](/pics/Console-Complete.png)

- If you want to delete the resources, run the following command.

```bash
terraform destroy
```

- Note that you need to delete S3 buckets manually because they are not empty.
