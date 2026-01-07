from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import qrcode
import boto3
import os
from io import BytesIO
from datetime import datetime
import re

# Loading Environment variable (AWS Access Key and Secret Key)
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Allowing CORS - now less critical since NextJS proxies requests
# But keeping it for flexibility
origins = [
    "http://localhost:3000",
    "*"  # Allow all origins since requests come from NextJS server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request validation
class QRRequest(BaseModel):
    url: HttpUrl  # Validates that it's a proper URL

# AWS S3 Configuration
# Updated to use environment variables properly
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", os.getenv("AWS_ACCESS_KEY")),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", os.getenv("AWS_SECRET_KEY")),
    region_name=os.getenv("AWS_REGION", "us-east-1")
)

# Get bucket name from environment variable with fallback
bucket_name = os.getenv("BUCKET_NAME", "YOUR_BUCKET_NAME")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "QR Code Generator API",
        "version": "1.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "generate": "/generate (POST with JSON body)",
            "generate_legacy": "/generate-qr/ (POST with query param - deprecated)"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint for Kubernetes probes"""
    return {
        "status": "healthy",
        "service": "qr-code-api",
        "bucket": bucket_name
    }

@app.post("/generate")
async def generate_qr_new(request: QRRequest):
    """
    Generate QR code and upload to S3
    Request body: {"url": "https://example.com"}
    
    This is the new recommended endpoint that accepts JSON body
    """
    try:
        url = str(request.url)
        
        # Generate QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save QR Code to BytesIO object
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        # Generate unique file name with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        # Sanitize URL for filename (remove special characters)
        safe_url = re.sub(r'[^\w\-_]', '_', url.split('//')[-1])[:50]  # Limit length
        file_name = f"qr_codes/{safe_url}_{timestamp}.png"

        # Upload to S3
        s3.put_object(
            Bucket=bucket_name, 
            Key=file_name, 
            Body=img_byte_arr, 
            ContentType='image/png', 
            # ACL='public-read'
        )
        
        # Generate the S3 URL
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
        
        return {
            "success": True,
            "qr_code_url": s3_url,
            "original_url": url,
            "file_name": file_name
        }
        
    except Exception as e:
        print(f"Error generating QR code: {str(e)}")  # Log for debugging
        raise HTTPException(status_code=500, detail=f"Error generating QR code: {str(e)}")

@app.post("/generate-qr/")
async def generate_qr_legacy(url: str):
    """
    Legacy endpoint for backward compatibility
    Usage: /generate-qr/?url=https://example.com
    
    DEPRECATED: Use /generate with JSON body instead
    """
    try:
        # Validate URL and convert to new format
        request = QRRequest(url=url)
        # Reuse the new endpoint logic
        return await generate_qr_new(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid URL provided: {str(e)}")