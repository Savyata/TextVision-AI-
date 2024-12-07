from flask import Flask, render_template
import boto3

app = Flask(_name_)

# Initialize the S3 client
s3_client = boto3.client('s3')

# Define your S3 bucket name
bucket_name = 'your-s3-bucket-name'

# Function to fetch the list of .txt files from the S3 bucket
def get_txt_file_key():
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    
    # Look for a .txt file in the S3 bucket
    for obj in response.get('Contents', []):
        if obj['Key'].endswith('.txt'):
            return obj['Key']
    
    return None  # Return None if no .txt file is found

# Function to fetch the text file content from S3
def get_text_from_s3(file_key):
    response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    text_data = response['Body'].read().decode('utf-8')
    return text_data

@app.route('/')
def home():
    # Get the .txt file key automatically
    text_file_key = get_txt_file_key()
    
    if text_file_key is None:
        return "No .txt file found in the S3 bucket"
    
    # Fetch the text content from S3
    text_content = get_text_from_s3(text_file_key)
    
    # Render the text content in an HTML page
    return render_template('index.html', text=text_content)

if _name_ == "_main_":
    app.run(host='0.0.0.0', port=5000, debug=True)