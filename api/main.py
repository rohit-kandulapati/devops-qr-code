from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import qrcode
import boto3
from botocore.exceptions import ClientError
import os
from io import BytesIO
from datetime import datetime
import re

# Loading Environment variable (AWS Access Key and Secret Key)
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Allowing CORS (this affects calls to YOUR API, not S3)
origins = [
    "http://localhost:3000"
]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Pydantic model for request validation
class QRRequest(BaseModel):
    url: HttpUrl


# AWS S3 Configuration
# This will auto-detect credentials in this order:
# 1. Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
# 2. IAM role from EC2 instance metadata (for EC2)
# 3. IAM role from EKS Service Account (IRSA)
# 4. AWS config file
def get_s3_client():
    """
    Initialize S3 client with automatic credential detection
    Supports both explicit credentials and IRSA
    """
    try:
        # Check if explicit credentials are provided (for local dev)
        access_key = os.getenv("AWS_ACCESS_KEY_ID") or os.getenv("AWS_ACCESS_KEY")
        secret_key = os.getenv("AWS_SECRET_ACCESS_KEY") or os.getenv("AWS_SECRET_KEY")

        region = os.getenv("AWS_REGION", "us-east-1")

        if access_key and secret_key:
            # Use explicit credentials (local development)
            print("Using explicit AWS credentials from environment")
            return boto3.client(
                "s3",
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region,
            )
        else:
            # Use IAM role (IRSA in EKS or instance profile in EC2)
            print("Using IAM role for authentication (IRSA or instance profile)")
            return boto3.client("s3", region_name=region)
    except Exception as e:
        print(f"Error initializing S3 client: {str(e)}")
        raise


s3 = get_s3_client()
bucket_name = os.getenv("BUCKET_NAME", "YOUR_BUCKET_NAME")

# How long the presigned URL should be valid (seconds)
PRESIGNED_URL_EXPIRES_IN = int(os.getenv("PRESIGNED_URL_EXPIRES_IN", "3600"))


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "QR Code Generator API",
        "version": "1.0",
        "status": "running",
        "auth_method": "IRSA" if not os.getenv("AWS_ACCESS_KEY_ID") else "Explicit Credentials",
        "endpoints": {
            "health": "/health",
            "generate": "/generate (POST with JSON body)",
            "generate_legacy": "/generate-qr/ (POST with query param)",
        },
    }


@app.get("/health")
async def health():
    """Health check endpoint for Kubernetes probes"""
    try:
        # Verify S3 access as part of health check
        s3.head_bucket(Bucket=bucket_name)
        s3_status = "accessible"
    except ClientError as e:
        s3_status = f"error: {str(e)}"
    except Exception as e:
        s3_status = f"error: {str(e)}"

    return {
        "status": "healthy",
        "service": "qr-code-api",
        "bucket": bucket_name,
        "s3_access": s3_status,
        "auth_method": "IRSA" if not os.getenv("AWS_ACCESS_KEY_ID") else "Explicit",
    }


@app.post("/generate")
async def generate_qr_new(request: QRRequest):
    """
    Generate QR code and upload to S3
    Request body: {"url": "https://example.com"}

    IMPORTANT:
    - Uploads the object privately.
    - Returns a presigned URL so the browser can access it without making the bucket public.
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
        img.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)

        # Generate unique file name with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        safe_url = re.sub(r"[^\w\-_]", "_", url.split("//")[-1])[:50]
        file_name = f"qr_codes/{safe_url}_{timestamp}.png"

        try:
            # Upload to S3 (private object; no ACL)
            s3.put_object(
                Bucket=bucket_name,
                Key=file_name,
                Body=img_byte_arr,
                ContentType="image/png",
            )

            # Generate a presigned URL for reading the object
            presigned_url = s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket_name, "Key": file_name},
                ExpiresIn=PRESIGNED_URL_EXPIRES_IN,
            )

            print(f"Successfully uploaded QR code to S3: {file_name}")

            return {
                "success": True,
                "qr_code_url": presigned_url,  # use this in the browser
                "original_url": url,
                "file_name": file_name,
                "expires_in": PRESIGNED_URL_EXPIRES_IN,
            }

        except ClientError as s3_error:
            print(f"S3 Upload Error: {str(s3_error)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload to S3: {str(s3_error)}",
            )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error generating QR code: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating QR code: {str(e)}")


@app.post("/generate-qr/")
async def generate_qr_legacy(url: str):
    """
    Legacy endpoint for backward compatibility
    Usage: /generate-qr/?url=https://example.com
    """
    try:
        request = QRRequest(url=url)
        return await generate_qr_new(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid URL provided: {str(e)}")
