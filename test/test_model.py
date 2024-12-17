import os
import cv2
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from ultralytics import YOLO

# Konfigurasi model YOLO
model_path = 'models/yolo11m.pt'
output_folder = 'outputs'

# Pastikan folder output ada
os.makedirs(output_folder, exist_ok=True)

# Inisialisasi model YOLO
model = YOLO(model_path)
print("Model berhasil dimuat.")

def process_video_to_output(video_path, output_video_path):
    """Proses video dengan YOLO dan simpan hasilnya sebagai video."""
    # Baca video menggunakan OpenCV
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    fps = cap.get(cv2.CAP_PROP_FPS)  # Ambil FPS video asli
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))   # Lebar frame
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Tinggi frame

    # Siapkan VideoWriter untuk menyimpan hasil
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec untuk output video
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

        # Proses frame menggunakan YOLO
        results = model.predict(source=frame, save=True)
        
        # Ambil hasil deteksi dan simpan dalam output video
        # Menggunakan frame hasil deteksi langsung
        output_frame = results[0].plot()  # Dapatkan frame dengan hasil deteksi

        # Tulis frame yang sudah diproses ke output video
        out.write(output_frame)

    cap.release()
    out.release()
    print(f"Video hasil deteksi disimpan di: {output_video_path}")

def select_file_and_process():
    """Pilih file secara fleksibel dan proses menggunakan YOLO."""
    print("Pilih file gambar atau video untuk diproses...")
    root = Tk()
    root.withdraw()  # Sembunyikan jendela utama Tkinter

    # Filter file yang bisa dipilih: gambar dan video
    file_path = askopenfilename(
        title="Pilih file gambar atau video",
        filetypes=[("Image and Video Files", "*.png;*.jpg;*.jpeg;*.mp4")]
    )

    if not file_path:
        print("Tidak ada file yang dipilih. Program selesai.")
        return

    print(f"File yang dipilih: {file_path}")

    # Tentukan apakah file gambar atau video
    if file_path.lower().endswith(('png', 'jpg', 'jpeg')):
        process_image(file_path)  # Proses gambar (misal: jika ada pilihan gambar)
    elif file_path.lower().endswith('mp4'):
        # Tentukan nama output video
        output_video_path = os.path.join(output_folder, 'output_video.mp4')
        process_video_to_output(file_path, output_video_path)  # Proses video

if __name__ == "__main__":
    select_file_and_process()
