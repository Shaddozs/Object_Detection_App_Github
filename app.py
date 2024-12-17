import os
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import glob
import shutil

# Load environment variables
load_dotenv()

# Konfigurasi Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

app = Flask(__name__)
CORS(app)

# Path model dan folder
MODEL_PATH = 'models/last.pt'
UPLOAD_FOLDER = '/tmp/uploads'
OUTPUT_FOLDER = '/tmp/outputs'

# Buat folder lokal
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load model YOLO
model = YOLO(MODEL_PATH)

def upload_to_cloudinary(file_path, folder='object-detection'):
    """Upload file to Cloudinary"""
    try:
        # Upload file dan dapatkan response
        upload_result = cloudinary.uploader.upload(
            file_path, 
            folder=folder,
            unique_filename=True,
            overwrite=True
        )
        return upload_result
    except Exception as e:
        print(f"Cloudinary upload error: {e}")
        return None

@app.route('/detect', methods=['POST'])
def detect_objects():
    # Periksa apakah ada file yang diunggah
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Generate unique filename
    unique_filename = str(uuid.uuid4()) + '_' + file.filename
    
    # Simpan file yang diunggah
    input_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    file.save(input_path)

    # Jalankan deteksi objek
    results = model.predict(
        source=input_path, 
        save=True, 
        save_dir=OUTPUT_FOLDER, 
        project=OUTPUT_FOLDER, 
        name="", 
        exist_ok=True
    )

    # Path hasil deteksi lokal
    output_filename = f"{unique_filename}"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    predict_folder = os.path.join(OUTPUT_FOLDER, 'predict')
    output_files = glob.glob(os.path.join(predict_folder, '*'))

    print(f"Predict folder: {predict_folder}")
    print(f"Output files found: {output_files}")

     # Jika ada file, gunakan file pertama
    if output_files:
        output_path = output_files[0]
    else:
        return jsonify({
            'error': 'No output file found',
            'details': f'Checked folder: {predict_folder}'
        }), 500
    
    try:
        # Upload input file ke Cloudinary
        input_upload = upload_to_cloudinary(input_path, folder='object-detection/inputs')
        
        # Upload output file ke Cloudinary
        output_upload = upload_to_cloudinary(output_path, folder='object-detection/outputs')
        
        # Siapkan response
        response = {
            'message': 'Detection completed',
            'input_file': {
                'name': unique_filename,
                'url': input_upload['secure_url'] if input_upload else None,
                'public_id': input_upload['public_id'] if input_upload else None
            },
            'output_file': {
                'name': os.path.basename(output_path),
                'url': output_upload['secure_url'] if output_upload else None,
                'public_id': output_upload['public_id'] if output_upload else None
            }
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'error': 'Upload to Cloudinary failed',
            'details': str(e)
        }), 500
    finally:
        # Hapus file lokal
        try:
            os.remove(input_path)
            shutil.rmtree(os.path.join(OUTPUT_FOLDER, 'predict'), ignore_errors=True)
        except Exception as cleanup_error:
            print(f"Cleanup error: {cleanup_error}")

@app.route('/')
def home():
    return "Welcome to the Object Detection API! Use the /detect endpoint to upload files."

if __name__ == '__main__':
    app.run(debug=True)