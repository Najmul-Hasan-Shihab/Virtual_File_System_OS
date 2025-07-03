### futuristic_vfs_app.py
import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog
from vfs_core import VFS

class VFSApp:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()  # Hide main window during splash
        self.splash_screen()

    def splash_screen(self):
        splash = ttk.Toplevel()
        splash.title("Welcome :: Virtual File System")
        splash.geometry("500x300+500+250")
        splash.resizable(False, False)
        splash.overrideredirect(True)

        splash_frame = ttk.Frame(splash, padding=30)
        splash_frame.pack(fill=BOTH, expand=YES)

        ttk.Label(
            splash_frame,
            text="\u269B Virtual File System",
            font=("Courier New", 24, "bold"),
            bootstyle="info"
        ).pack(pady=10)

        ttk.Label(
            splash_frame,
            text="Loading futuristic workspace...",
            font=("Consolas", 12),
            bootstyle="secondary"
        ).pack(pady=20)

        splash.after(1800, lambda: (splash.destroy(), self.show_main()))

    def show_main(self):
        self.root.deiconify()
        self.root.title("\u269B Virtual File System :: NeoUI")
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        # self.root.iconbitmap(default="favicon.ico")

        self.vfs = VFS()

        self.style = ttk.Style("darkly")
        font_header = ("Courier New", 18, "bold")
        font_normal = ("Consolas", 11)

        menubar = ttk.Menu(self.root)

        filemenu = ttk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Create File", command=self.create_file)
        filemenu.add_command(label="Read File", command=self.read_file)
        filemenu.add_command(label="Update File", command=self.update_file)
        filemenu.add_command(label="Delete File", command=self.delete_file)
        filemenu.add_command(label="Search File", command=self.search_file)
        filemenu.add_separator()
        filemenu.add_command(label="Set Shared Directory", command=self.set_shared_directory)
        filemenu.add_command(label="Exit", command=self.on_exit)
        menubar.add_cascade(label="\u2699 File Ops", menu=filemenu)

        thememenu = ttk.Menu(menubar, tearoff=0)
        for theme in ["darkly", "superhero", "cyborg", "solar", "morph"]:
            thememenu.add_command(
                label=theme.capitalize(),
                command=lambda th=theme: self.change_theme(th)
            )
        menubar.add_cascade(label="\U0001F3A8 Theme", menu=thememenu)

        self.root.config(menu=menubar)

        frame = ttk.Frame(self.root, padding=30)
        frame.pack(fill=BOTH, expand=YES)

        ttk.Label(
            frame,
            text="Welcome to the Virtual File System",
            font=font_header,
            bootstyle="info",
            anchor="center",
            justify="center"
        ).pack(pady=15)

        desc = (
            "Interact with a virtual environment that emulates file system operations.\n"
            "Use the menu to create, update, read or search files.\n\n"
            "Credits:\n"
            "- Mohammed Fahimul Hoque\n"
            "- Omar Faruque\n"
            "- Tonmoy Mutsuddy\n"
            "- Md. Najmul Hasan Shihab\n\n"
            "Course Teacher: Mohammed Arfat"
        )

        ttk.Label(
            frame,
            text=desc,
            font=font_normal,
            bootstyle="secondary",
            anchor="center",
            justify="center"
        ).pack(pady=10)

        self.status = ttk.Label(
            self.root,
            text="Ready...",
            font=("Consolas", 9),
            anchor="w",
            bootstyle="inverse-dark",
            relief="ridge"
        )
        self.status.pack(side="bottom", fill="x")

        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

    def change_theme(self, theme):
        self.style.theme_use(theme)
        self.status.config(text=f"Theme changed to: {theme}")

    def on_exit(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.root.quit()

    def show_dialog(self, title, content_frame):
        dialog = ttk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("450x350")
        dialog.resizable(False, False)
        content_frame(dialog).pack(fill=BOTH, expand=True)
        return dialog

    def create_file(self):
        def layout(dialog):
            frame = ttk.Frame(dialog, padding=10)
            ttk.Label(frame, text="File Name:").pack(pady=5)
            name_entry = ttk.Entry(frame, width=40)
            name_entry.pack()

            ttk.Label(frame, text="File Content:").pack(pady=5)
            content_box = ttk.Text(frame, height=8)
            content_box.pack()

            def save():
                fname = name_entry.get()
                content = content_box.get("1.0", "end").strip()
                if fname:
                    try:
                        self.vfs.create_file(fname, content)
                        self.status.config(text=f"Created: {fname}")
                        dialog.destroy()
                    except Exception as e:
                        messagebox.showerror("Error", str(e))
                else:
                    messagebox.showerror("Error", "Filename cannot be empty.")

            ttk.Button(frame, text="Save File", command=save, bootstyle="success-outline").pack(pady=10)
            return frame

        self.show_dialog("Create File", layout)

    def read_file(self):
        def layout(dialog):
            frame = ttk.Frame(dialog, padding=10)
            ttk.Label(frame, text="File Name:").pack(pady=5)
            name_entry = ttk.Entry(frame, width=40)
            name_entry.pack()

            result_box = ttk.Text(frame, height=8)
            result_box.pack(pady=5)

            def read():
                fname = name_entry.get()
                if fname:
                    try:
                        content = self.vfs.read_file(fname)
                        result_box.delete("1.0", "end")
                        result_box.insert("1.0", content)
                        self.status.config(text=f"Read: {fname}")
                    except Exception as e:
                        messagebox.showerror("Error", str(e))

            ttk.Button(frame, text="Read", command=read, bootstyle="info-outline").pack(pady=5)
            return frame

        self.show_dialog("Read File", layout)

    def update_file(self):
        def layout(dialog):
            frame = ttk.Frame(dialog, padding=10)
            ttk.Label(frame, text="File Name:").pack(pady=5)
            name_entry = ttk.Entry(frame, width=40)
            name_entry.pack()

            ttk.Label(frame, text="New Content:").pack(pady=5)
            content_box = ttk.Text(frame, height=8)
            content_box.pack()

            def update():
                fname = name_entry.get()
                content = content_box.get("1.0", "end").strip()
                if fname:
                    try:
                        self.vfs.update_file(fname, content)
                        self.status.config(text=f"Updated: {fname}")
                        dialog.destroy()
                    except Exception as e:
                        messagebox.showerror("Error", str(e))

            ttk.Button(frame, text="Update", command=update, bootstyle="warning-outline").pack(pady=10)
            return frame

        self.show_dialog("Update File", layout)

    def delete_file(self):
        def layout(dialog):
            frame = ttk.Frame(dialog, padding=10)
            ttk.Label(frame, text="File Name:").pack(pady=5)
            name_entry = ttk.Entry(frame, width=40)
            name_entry.pack()

            def delete():
                fname = name_entry.get()
                if fname:
                    try:
                        self.vfs.delete_file(fname)
                        self.status.config(text=f"Deleted: {fname}")
                        dialog.destroy()
                    except Exception as e:
                        messagebox.showerror("Error", str(e))

            ttk.Button(frame, text="Delete", command=delete, bootstyle="danger-outline").pack(pady=10)
            return frame

        self.show_dialog("Delete File", layout)

    def search_file(self):
        def layout(dialog):
            frame = ttk.Frame(dialog, padding=10)
            ttk.Label(frame, text="File Name:").pack(pady=5)
            name_entry = ttk.Entry(frame, width=40)
            name_entry.pack()

            result_box = ttk.Text(frame, height=8)
            result_box.pack(pady=5)

            def search():
                fname = name_entry.get()
                found, meta = self.vfs.search_files(fname)
                if found:
                    info = (
                        f"Size: {meta['size']} bytes\n"
                        f"Created: {meta['creation_time']}\n\n"
                        f"Content:\n{meta['content']}"
                    )
                    result_box.delete("1.0", "end")
                    result_box.insert("1.0", info)
                    self.status.config(text=f"Searched: {fname}")
                else:
                    messagebox.showerror("Not Found", f"File '{fname}' not found.")

            ttk.Button(frame, text="Search", command=search, bootstyle="primary-outline").pack(pady=5)
            return frame

        self.show_dialog("Search File", layout)

    def set_shared_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            try:
                self.vfs.set_root_directory(directory)
                self.status.config(text=f"Directory set: {directory}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = ttk.Window(themename="darkly")
    VFSApp(app)
    app.mainloop()
