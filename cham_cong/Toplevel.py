import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

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

USERS = {
    "admin1": {"password": "123456", "role": "admin", "department": "Ngoại tổng hợp"},
    "user1": {"password": "userpass", "role": "user", "department": "Khoa nội"}
}

current_user = None

def show_main_app():
    root = tk.Tk()
    root.title("🏥 Chấm Công - Bệnh Viện Đa Khoa Long An")
    root.state('zoomed')
    root.configure(bg="#f5f6fa")

    # Sidebar
    sidebar = tk.Frame(root, bg="#273c75", width=240)
    sidebar.pack(side="left", fill="y")

    # Logo ở góc trái trên sidebar
    logo_path = "logo_longan.jpg"
    if PIL_AVAILABLE:
        try:
            img = Image.open(logo_path).resize((80, 80))
            logo_img = ImageTk.PhotoImage(img)
            logo_label = tk.Label(sidebar, image=logo_img, bg="#273c75")
            logo_label.image = logo_img
            logo_label.pack(pady=(30,10))
        except Exception as e:
            tk.Label(sidebar, text="🏥", font=("Arial", 32), bg="#273c75", fg="white").pack(pady=(30,10))
    else:
        tk.Label(sidebar, text="🏥", font=("Arial", 32), bg="#273c75", fg="white").pack(pady=(30,10))

    tk.Label(sidebar, text="MENU", bg="#273c75", fg="white", font=("Arial", 16, "bold")).pack(pady=(0,20))

    def menu_action(name):
        print(f"👉 Đã chọn chức năng: {name}")

    if current_user["role"] == "admin":
        for item in ["Tạo User", "Sửa User", "Xóa User", "Sửa phiếu chấm công"]:
            tk.Button(sidebar, text=item, width=20, bg="#40739e", fg="white",
                      font=("Arial", 12, "bold"), relief="flat", bd=0,
                      activebackground="#00a8ff", activeforeground="white",
                      command=lambda i=item: menu_action(i)).pack(pady=7, ipadx=4, ipady=4)

    tk.Button(sidebar, text="🔒 Đăng xuất", width=20, bg="#e84118", fg="white",
              font=("Arial", 12, "bold"), relief="flat", bd=0,
              activebackground="#c23616", activeforeground="white",
              command=root.quit).pack(pady=30, ipadx=4, ipady=4)

    # Main area
    main_area = tk.Frame(root, bg="#f5f6fa")
    main_area.pack(expand=True, fill="both")

    # Tên bệnh viện căn giữa phía trên
    tk.Label(main_area, text="BỆNH VIỆN ĐA KHOA LONG AN", font=("Arial", 24, "bold"),
             bg="#f5f6fa", fg="#273c75").pack(pady=(30,10))

    # Thông tin người dùng
    tk.Label(main_area, text=f"Nhân viên: {current_user['username']} | Khoa: {current_user['department']}",
             bg="#f5f6fa", font=("Arial", 13), fg="#353b48").pack(pady=5)

    # Form chấm công
    form_frame = tk.Frame(main_area, bg="#f5f6fa", bd=2, relief="groove")
    form_frame.pack(pady=30)

    tk.Label(form_frame, text="PHIẾU CHẤM CÔNG", font=("Arial", 20, "bold"),
             bg="#f5f6fa", fg="#192a56").grid(row=0, column=0, columnspan=3, pady=(0,20))

    tk.Label(form_frame, text="Ngày làm việc:", bg="#f5f6fa", font=("Arial", 12)).grid(row=1, column=0, sticky="e", pady=8)
    if TKCALENDAR_AVAILABLE:
        entry_ngay = DateEntry(form_frame, width=15, background='#273c75',
                               foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        entry_ngay.set_date(datetime.now())
    else:
        entry_ngay = tk.Entry(form_frame, font=("Arial", 12))
        entry_ngay.insert(0, datetime.now().strftime("%Y-%m-%d"))
    entry_ngay.grid(row=1, column=1, padx=5)

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
        tk.Button(top, text="Chọn", command=select_date, font=("Arial", 12), bg="#00a8ff", fg="white").pack(pady=5)

    btn_calendar = tk.Button(form_frame, text="📅", command=open_calendar, font=("Arial", 12),
                             bg="#40739e", fg="white", relief="flat", bd=0, activebackground="#00a8ff")
    btn_calendar.grid(row=1, column=2, padx=5)

    tk.Label(form_frame, text="Ca làm:", bg="#f5f6fa", font=("Arial", 12)).grid(row=2, column=0, sticky="e", pady=8)
    combo_ca = ttk.Combobox(form_frame, values=["Sáng", "Chiều", "Đêm"], font=("Arial", 12))
    combo_ca.current(0)
    combo_ca.grid(row=2, column=1, padx=5)

    def gui_du_lieu():
        du_lieu = {
            "user": current_user["username"],
            "dept": current_user["department"],
            "ngay": entry_ngay.get(),
            "ca": combo_ca.get()
        }
        print("📤 Dữ liệu gửi:", du_lieu)
        tk.Label(main_area, text="✅ Đã ghi nhận!", fg="#44bd32", bg="#f5f6fa", font=("Arial", 12)).pack()

    tk.Button(form_frame, text="📤 Gửi phiếu chấm công", command=gui_du_lieu,
              bg="#44bd32", fg="white", font=("Arial", 14, "bold"),
              relief="flat", bd=0, activebackground="#4cd137").grid(row=3, column=0, columnspan=3, pady=20, ipadx=10, ipady=6)

    root.mainloop()

def show_login():
    login_win = tk.Tk()
    login_win.title("Đăng nhập hệ thống")
    login_win.configure(bg="#f5f6fa")
    login_win.state('zoomed')
    login_win.resizable(True, True)

    # Frame chứa toàn bộ nội dung, căn giữa màn hình
    main_frame = tk.Frame(login_win, bg="#f5f6fa")
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Logo và tên bệnh viện
    top_frame = tk.Frame(main_frame, bg="#f5f6fa")
    top_frame.pack(side="top", fill="x", pady=(0,10))

    logo_path = "logo_longan.jpg"
    logo_img = None
    logo_label = None
    logo_side = tk.Frame(top_frame, bg="#f5f6fa")
    logo_side.pack(side="left", padx=(0,20))
    if PIL_AVAILABLE:
        try:
            img = Image.open(logo_path).resize((90, 90))
            logo_img = ImageTk.PhotoImage(img)
            logo_label = tk.Label(logo_side, image=logo_img, bg="#f5f6fa")
            logo_label.image = logo_img
            logo_label.pack()
        except Exception:
            tk.Label(logo_side, text="🏥", font=("Arial", 32), bg="#f5f6fa", fg="#273c75").pack()
    else:
        tk.Label(logo_side, text="🏥", font=("Arial", 32), bg="#f5f6fa", fg="#273c75").pack()

    tk.Label(top_frame, text="BỆNH VIỆN ĐA KHOA LONG AN", font=("Arial", 24, "bold"),
             bg="#f5f6fa", fg="#273c75").pack(side="left", padx=(10,0))

    # Form đăng nhập bo tròn, căn giữa
    form_frame = tk.Frame(main_frame, bg="#dff9fb", bd=2, relief="groove")
    form_frame.pack(pady=(30,0))

    tk.Label(form_frame, text="ĐĂNG NHẬP", font=("Arial", 15, "bold"), bg="#dff9fb", fg="#192a56").pack(pady=(10,8))
    tk.Label(form_frame, text="Tên đăng nhập:", font=("Arial", 12), bg="#dff9fb").pack(pady=(0,3))
    entry_user = tk.Entry(form_frame, font=("Arial", 12), bd=2, relief="groove")
    entry_user.pack(pady=(0,8), ipadx=10)

    tk.Label(form_frame, text="Mật khẩu:", font=("Arial", 12), bg="#dff9fb").pack(pady=(0,3))
    entry_pass = tk.Entry(form_frame, show="*", font=("Arial", 12), bd=2, relief="groove")
    entry_pass.pack(pady=(0,8), ipadx=10)

    def do_login(event=None):
        username = entry_user.get()
        password = entry_pass.get()
        if username in USERS and USERS[username]["password"] == password:
            global current_user
            current_user = {"username": username,
                            "role": USERS[username]["role"],
                            "department": USERS[username]["department"]}
            login_win.destroy()
            show_main_app()
        else:
            messagebox.showerror("Lỗi đăng nhập", "Sai tên đăng nhập hoặc mật khẩu!")

    login_btn = tk.Button(form_frame, text="Đăng nhập", command=do_login, font=("Arial", 13, "bold"),
              bg="#273c75", fg="white", relief="flat", bd=0,
              activebackground="#00a8ff", activeforeground="white")
    login_btn.pack(pady=10, ipadx=10, ipady=4)

    login_win.bind('<Return>', do_login)
    entry_user.focus_set()

    login_win.mainloop()

if __name__ == "__main__":
    show_login()