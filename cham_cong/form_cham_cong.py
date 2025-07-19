import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os

try:
    from tkcalendar import DateEntry, Calendar
    TKCALENDAR_AVAILABLE = True
except Exception as e:
    print("Lỗi import tkcalendar:", e)
    TKCALENDAR_AVAILABLE = False

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except Exception as e:
    print("Lỗi import Pillow:", e)
    PIL_AVAILABLE = False

current_user = {
    "username": "admin1",
    "role": "admin",
    "department": "Ngoại tổng hợp"
}

root = tk.Tk()
root.title("🏥 Chấm Công - Bệnh Viện Đa Khoa Long An")
root.state('zoomed')  # Windows: full màn hình
root.attributes('-fullscreen', True)  # Full màn hình trên mọi hệ điều hành

# --- Fix: define open_create_user before using it ---
def open_create_user():
    top = tk.Toplevel(root)
    top.title("Tạo User mới")
    tk.Label(top, text="Tên đăng nhập:").grid(row=0, column=0, pady=5)
    entry_username = tk.Entry(top)
    entry_username.grid(row=0, column=1, pady=5)
    tk.Label(top, text="Vai trò:").grid(row=1, column=0, pady=5)
    combo_role = ttk.Combobox(top, values=["admin", "user"])
    combo_role.current(1)
    combo_role.grid(row=1, column=1, pady=5)
    tk.Label(top, text="Khoa:").grid(row=2, column=0, pady=5)
    entry_dept = tk.Entry(top)
    entry_dept.grid(row=2, column=1, pady=5)

    def save_user():
        username = entry_username.get()
        role = combo_role.get()
        dept = entry_dept.get()
        print(f"User mới: {username}, Role: {role}, Khoa: {dept}")
        messagebox.showinfo("Thành công", "Đã tạo user mới!")
        top.destroy()

    tk.Button(top, text="Lưu", command=save_user).grid(row=3, column=0, columnspan=2, pady=10)

# Đặt đoạn này trước khi tạo sidebar!
sidebar = tk.Frame(root, bg="#34495E", width=220)
sidebar.pack(side="left", fill="y")

tk.Label(sidebar, text="⚙️ MENU", bg="#34495E", fg="white", font=("Arial", 14, "bold")).pack(pady=20)

def menu_action(name):
    print(f"👉 Đã chọn chức năng: {name}")

# Python
if current_user["role"] == "admin":
    for item in ["Tạo User", "Sửa User", "Xóa User", "Sửa phiếu chấm công"]:
        if item == "Tạo User":
            tk.Button(sidebar, text=item, width=20, bg="#2C3E50", fg="white",
                      command=open_create_user).pack(pady=5)
        else:
            tk.Button(sidebar, text=item, width=20, bg="#2C3E50", fg="white",
                      command=lambda i=item: menu_action(i)).pack(pady=5)

tk.Button(sidebar, text="🔒 Đăng xuất", width=20, bg="#E74C3C", fg="white",
          command=root.quit).pack(pady=30)

main_area = tk.Frame(root, bg="#ECF0F1")
main_area.pack(expand=True, fill="both")

# === Logo bệnh viện ===
logo_path = "logo_longan.jpg"
if not os.path.exists(logo_path):
    # Thử đường dẫn tương đối từ thư mục cha
    logo_path = os.path.join("cham_cong", "logo_longan.jpg")

if PIL_AVAILABLE:
    try:
        img = Image.open(logo_path).resize((100, 100))
        logo_img = ImageTk.PhotoImage(img)
        logo_label = tk.Label(main_area, image=logo_img, bg="#ECF0F1")
        logo_label.image = logo_img  # giữ tham chiếu
        logo_label.pack(pady=10)
    except Exception as e:
        print("Lỗi khi tải logo:", e)
        tk.Label(main_area, text="🏥 [Không tìm thấy logo]", font=("Arial", 16), bg="#ECF0F1").pack(pady=10)
else:
    tk.Label(main_area, text="🏥 [Logo]", font=("Arial", 24), bg="#ECF0F1").pack(pady=10)

tk.Label(main_area, text="PHIẾU CHẤM CÔNG", font=("Arial", 24, "bold"), bg="#ECF0F1", fg="#2C3E50").pack()
tk.Label(main_area, text=f"Nhân viên: {current_user['username']} | Khoa: {current_user['department']}",
         bg="#ECF0F1", font=("Arial", 12)).pack(pady=5)

form_frame = tk.Frame(main_area, bg="#ECF0F1")
form_frame.pack(pady=20)

tk.Label(form_frame, text="Ngày làm việc:", bg="#ECF0F1", font=("Arial", 10)).grid(row=0, column=0, sticky="e", pady=5)

if TKCALENDAR_AVAILABLE:
    entry_ngay = DateEntry(form_frame, width=15, background='darkblue',
                           foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    entry_ngay.set_date(datetime.now())
else:
    entry_ngay = tk.Entry(form_frame)
    entry_ngay.insert(0, datetime.now().strftime("%Y-%m-%d"))
entry_ngay.grid(row=0, column=1, padx=5)

def open_calendar():
    if not TKCALENDAR_AVAILABLE:
        messagebox.showerror("Lỗi", "Chưa cài tkcalendar!")
        return
    top = tk.Toplevel(root)
    top.title("Chọn ngày làm việc")
    cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(padx=10, pady=10)
    def select_date():
        entry_ngay.set_date(cal.get_date())
        top.destroy()
    tk.Button(top, text="Chọn", command=select_date).pack(pady=5)

btn_calendar = tk.Button(form_frame, text="📅", command=open_calendar)
btn_calendar.grid(row=0, column=2, padx=5)

tk.Label(form_frame, text="Ca làm:", bg="#ECF0F1", font=("Arial", 10)).grid(row=1, column=0, sticky="e", pady=5)
combo_ca = ttk.Combobox(form_frame, values=["Sáng", "Chiều", "Đêm"])
combo_ca.current(0)
combo_ca.grid(row=1, column=1, padx=5)

def gui_du_lieu():
    du_lieu = {
        "user": current_user["username"],
        "dept": current_user["department"],
        "ngay": entry_ngay.get(),
        "ca": combo_ca.get()
    }
    print("📤 Dữ liệu gửi:", du_lieu)
    tk.Label(main_area, text="✅ Đã ghi nhận!", fg="green", bg="#ECF0F1", font=("Arial", 10)).pack()

tk.Button(main_area, text="📤 Gửi phiếu chấm công", command=gui_du_lieu,
          bg="#2ECC71", fg="white", font=("Arial", 12)).pack(pady=10)

root.mainloop()