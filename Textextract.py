import os
import boto3
import pytesseract
from PIL import Image
from io import BytesIO

# Set the Tesseract command path
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

# Set the TESSDATA_PREFIX environment variable
os.environ['TESSDATA_PREFIX'] = '/usr/local/share/tessdata/'

# Initialize the S3 client
s3_client = boto3.client('s3')

# Define the S3 bucket name
bucket_name = 'your-s3-bucket-name'

def extract_text_from_image(s3_bucket, image_key):
    # Download the image from S3
    response = s3_client.get_object(Bucket=s3_bucket, Key=image_key)
    image_data = response['Body'].read()
    
    # Open the image using PIL
    image = Image.open(BytesIO(image_data))
    
    # Use Tesseract to extract text from the image
    extracted_text = pytesseract.image_to_string(image)
    
    return extracted_text

def upload_text_to_s3(s3_bucket, text, text_file_key):
    # Upload the extracted text to S3 as a text file
    s3_client.put_object(Body=text, Bucket=s3_bucket, Key=text_file_key)

def main():
    # List all objects in the S3 bucket
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    
    if 'Contents' not in response:
        print(f"No objects found in bucket {bucket_name}.")
        return
    
    image_keys = [obj['Key'] for obj in response['Contents'] if obj['Key'].lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif'))]
    
    for image_key in image_keys:
        print(f"Processing image: {image_key}")
        # Extract text from the image
        extracted_text = extract_text_from_image(bucket_name, image_key)
        
        # Create a key for the text file to store in S3
        text_file_key = image_key.rsplit('.', 1)[0] + '.txt'
        
        # Upload the extracted text to S3
        upload_text_to_s3(bucket_name, extracted_text, text_file_key)
        
        print(f"Text extracted and uploaded to S3 as {text_file_key}")

if _name_ == "_main_":
    main()