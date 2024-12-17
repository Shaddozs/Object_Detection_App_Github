# Plant Disease Object Detection API

## Project Overview
This is a Flask-based object detection API using Ultralytics YOLO for detecting plant diseases, with image storage powered by Cloudinary.

## Prerequisites
- Python 3.11
- Docker (optional)
- Cloudinary Account

## Setup and Installation

### Local Development

1. Clone the repository
```bash
git clone <your-repository-url>
cd <project-directory>
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Setup Cloudinary Credentials
Create a `.env` file in the project root with your Cloudinary credentials:
```
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

5. Run the application
```bash
flask run
```

### Docker Deployment

1. Build the Docker image
```bash
docker build -t plant-disease-detection .
```

2. Run the Docker container
```bash
docker run -p 5000:5000 \
  -e CLOUDINARY_CLOUD_NAME=your_cloud_name \
  -e CLOUDINARY_API_KEY=your_api_key \
  -e CLOUDINARY_API_SECRET=your_api_secret \
  plant-disease-detection
```

### IBM Cloud Code Engine Deployment

1. Create a new project in IBM Cloud Code Engine

2. Set the following environment variables:
- `CLOUDINARY_CLOUD_NAME`
- `CLOUDINARY_API_KEY`
- `CLOUDINARY_API_SECRET`

3. Deploy using the Docker image or source code

## API Endpoint

### Detect Plant Diseases

- **Endpoint**: `/detect`
- **Method**: POST
- **Content-Type**: `multipart/form-data`
- **Request Parameter**: `file` (image file)

#### Response
```json
{
    "message": "Detection completed",
    "input_file": {
        "name": "filename.jpg",
        "url": "cloudinary_input_url",
        "public_id": "cloudinary_public_id"
    },
    "output_file": {
        "name": "filename.jpg",
        "url": "cloudinary_output_url",
        "public_id": "cloudinary_public_id"
    }
}
```

## Model Training

The YOLO model (`last.pt`) should be placed in the `models/` directory. Ensure the model is trained on your specific plant disease dataset.

## Troubleshooting

- Ensure Cloudinary credentials are correct
- Check Docker build and runtime environments
- Verify model file is present in `models/` directory

## Technologies Used
- Flask
- Ultralytics YOLO
- Cloudinary
- Docker
