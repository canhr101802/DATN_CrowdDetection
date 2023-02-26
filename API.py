import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import subprocess
import cv2
from PIL import ImageTk, Image

# Tạo một cửa sổ giao diện
window = tk.Tk()
window.title("Ứng dụng phát hiện đám đông")

# Thiết lập kích thước của cửa sổ
window.geometry("600x300")
# Load image
bg_image = Image.open("/home/dinhcanh/Social-Distancing-using-YOLOv5/image.jpg")
bg_image = bg_image.resize((600, 300), Image.ANTIALIAS)

# Convert image to Tkinter compatible format
bg_image_tk = ImageTk.PhotoImage(bg_image)

# Set background image for window
bg_label = tk.Label(window, image=bg_image_tk)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Tạo một label "Chọn file video"
label = tk.Label(window, text="Chọn file video:", font=("Times New Roman", 14), fg="red", bg="#f0f0f0")
label.pack(pady=5)

# Tạo một button "Chọn file"
def select_file():
    filetypes = (
        ("Video files", "*.mp4"),
        ("All files", "*.*")
    )
    filename = filedialog.askopenfilename(
        title="Chọn file video",
        initialdir="./inference/videos/",
        filetypes=filetypes
    )
    text_box.delete(0, tk.END)
    text_box.insert(tk.END, filename)

select_file_button = tk.Button(window, text="Chọn file", command=select_file, bg="green", fg="white")
select_file_button.pack(pady=5)

# Tạo một text box để hiển thị đường dẫn file
text_box = tk.Entry(window, width=50, bg="#f0f0f0")
text_box.pack(pady=5)

# Tạo một button "Submit"
def run_cmd():
    filename = text_box.get()
    cmd = f"python detect.py --source {filename}"
    process = subprocess.Popen(cmd, shell=True)
    process.wait()
    messagebox.showinfo("Thông báo", "Nhận diện thành công!")
    path = filename
    start_index = path.rfind("/") + 1
    end_index = path.rfind(".mp4")
    fileOname = path[start_index:end_index]
    videoOut_path = f"/home/dinhcanh/Social-Distancing-using-YOLOv5/inference/output/{fileOname}.mp4"
    cap = cv2.VideoCapture(videoOut_path);
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (800, 600))
        cv2.imshow('Video Output', frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

submit_button = tk.Button(window, text="Submit", command=run_cmd)
submit_button.pack(pady=5)

# Chạy vòng lặp chính của giao diện

window.mainloop()
