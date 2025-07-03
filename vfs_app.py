### futuristic_vfs_app.py
import os
import shutil
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog
from vfs_core import VFS
from tkinter import Listbox, Text


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

        version_menu = ttk.Menu(menubar, tearoff=0)
        version_menu.add_command(label="View File Versions", command=self.view_file_versions)
        menubar.add_cascade(label="\U0001F5C3 Versioning", menu=version_menu)

        trash_menu = ttk.Menu(menubar, tearoff=0)
        trash_menu.add_command(label="View Trash Bin", command=self.view_trash_bin)
        menubar.add_cascade(label="🗑️ Trash", menu=trash_menu)

        tree_menu = ttk.Menu(menubar, tearoff=0)
        tree_menu.add_command(label="Open Directory Tree", command=self.open_directory_tree)
        menubar.add_cascade(label="📂 Navigation", menu=tree_menu)

        batch_menu = ttk.Menu(menubar, tearoff=0)
        batch_menu.add_command(label="Batch File Manager", command=self.open_batch_file_manager)
        menubar.add_cascade(label="🧰 Batch Ops", menu=batch_menu)

        analytics_menu = ttk.Menu(menubar, tearoff=0)
        analytics_menu.add_command(label="Open Analytics Panel", command=self.open_analytics_panel)
        menubar.add_cascade(label="📊 Analytics", menu=analytics_menu)




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
            font=("Consolas", 11),
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

    def view_file_versions(self):
        def layout(dialog):
            import os
            from tkinter import Listbox, Text

            frame = ttk.Frame(dialog, padding=10)
            frame.pack(fill=BOTH, expand=True)

            ttk.Label(frame, text="File Name: ").pack(pady=5)
            name_entry = ttk.Entry(frame, width=40)
            name_entry.pack()

            ttk.Button(frame, text="Load Versions", bootstyle="info-outline", command=lambda: fetch_versions(name_entry.get())).pack(pady=5)

            version_list = Listbox(frame, height=5)
            version_list.pack(fill=BOTH, expand=True, padx=5, pady=5)

            content_area = Text(frame, height=7, wrap="word")
            content_area.pack(fill=BOTH, expand=True, padx=5, pady=5)

            button_frame = ttk.Frame(frame)
            button_frame.pack(fill=X, pady=5)
            ttk.Button(
                button_frame,
                text="Restore Selected Version",
                bootstyle="warning-outline",
                command=lambda: restore_version(version_list)
            ).pack(pady=5)

            def fetch_versions(fname):
                versions = self.vfs.get_file_versions(fname)
                version_list.delete(0, 'end')
                content_area.delete("1.0", END)
                if versions:
                    for v in versions:
                        version_list.insert(END, v)
                else:
                    messagebox.showinfo("No Versions", f"No versions found for '{fname}'.")

            def show_version_content(evt):
                selected = version_list.curselection()
                if selected:
                    version_path = version_list.get(selected[0])
                    try:
                        with open(version_path, "r") as f:
                            content = f.read()
                        content_area.delete("1.0", END)
                        content_area.insert("1.0", content)
                    except Exception as e:
                        messagebox.showerror("Error", str(e))

            def restore_version(vlist):
                selected = vlist.curselection()
                if selected:
                    version_path = vlist.get(selected[0])
                    target_name = os.path.basename(version_path).split("_v")[0]
                    try:
                        with open(version_path, "r") as vfile:
                            data = vfile.read()
                        self.vfs.update_file(target_name, data)
                        messagebox.showinfo("Success", f"'{target_name}' restored from version.")
                    except Exception as e:
                        messagebox.showerror("Error", str(e))

            version_list.bind("<<ListboxSelect>>", show_version_content)

            return frame

        self.show_dialog("View File Versions", layout)

    
    def view_trash_bin(self):
        def layout(dialog):
            from tkinter import Listbox

            frame = ttk.Frame(dialog, padding=10)
            frame.pack(fill=BOTH, expand=True)

            trash_list = Listbox(frame, height=10)
            trash_list.pack(fill=BOTH, expand=True, padx=5, pady=5)

            def load_trash():
                trash_list.delete(0, END)
                trashed_files = self.vfs.list_trashed_files()
                if trashed_files:
                    for f in trashed_files:
                        trash_list.insert(END, f)
                else:
                    trash_list.insert(END, "<Trash is empty>")

            def restore_selected():
                selected = trash_list.curselection()
                if selected:
                    fname = trash_list.get(selected[0])
                    if "Trash is empty" in fname:
                        return
                    try:
                        self.vfs.restore_file(fname)
                        messagebox.showinfo("Success", f"'{fname}' restored.")
                        load_trash()
                    except Exception as e:
                        messagebox.showerror("Error", str(e))

            def delete_selected():
                selected = trash_list.curselection()
                if selected:
                    fname = trash_list.get(selected[0])
                    if "Trash is empty" in fname:
                        return
                    try:
                        self.vfs.permanently_delete_file(fname)
                        messagebox.showinfo("Deleted", f"'{fname}' permanently removed.")
                        load_trash()
                    except Exception as e:
                        messagebox.showerror("Error", str(e))

            ttk.Button(frame, text="Restore", bootstyle="success-outline", command=restore_selected).pack(pady=5)
            ttk.Button(frame, text="Delete Permanently", bootstyle="danger-outline", command=delete_selected).pack(pady=5)

            load_trash()
            return frame

        self.show_dialog("Trash Bin", layout)


    def open_directory_tree(self):
        import os
        from ttkbootstrap import Treeview

        def layout(dialog):
            frame = ttk.Frame(dialog, padding=10)
            frame.pack(fill=BOTH, expand=True)

            tree = Treeview(frame)
            tree.pack(fill=BOTH, expand=True)

            def populate_tree(parent, path):
                try:
                    for entry in os.listdir(path):
                        full_path = os.path.join(path, entry)
                        is_dir = os.path.isdir(full_path)
                        node = tree.insert(parent, "end", text=entry, open=False)
                        if is_dir:
                            populate_tree(node, full_path)
                except PermissionError:
                    pass

            def on_node_double_click(event):
                selected = tree.focus()
                node_path = get_full_path(tree, selected)
                if os.path.isfile(node_path):
                    try:
                        content = self.vfs.read_file(os.path.relpath(node_path, self.vfs.root_directory))
                        messagebox.showinfo("File Preview", content[:500] + ("\n\n...[truncated]" if len(content) > 500 else ""))
                    except Exception as e:
                        messagebox.showerror("Error", str(e))

            def get_full_path(tree, node):
                path = []
                while node:
                    path.insert(0, tree.item(node)["text"])
                    node = tree.parent(node)
                return os.path.join(self.vfs.root_directory, *path)

            tree.bind("<Double-1>", on_node_double_click)
            populate_tree("", self.vfs.root_directory)

            return frame

        self.show_dialog("Directory Tree", layout)


    def open_batch_file_manager(self):
        import os
        from tkinter import Listbox, MULTIPLE

        def layout(dialog):
            frame = ttk.Frame(dialog, padding=10)
            frame.pack(fill=BOTH, expand=True)

            ttk.Label(frame, text="Select files to operate on:").pack(pady=5)

            file_listbox = Listbox(frame, selectmode=MULTIPLE, height=12)
            file_listbox.pack(fill=BOTH, expand=True, padx=5, pady=5)

            all_files = [
                f for f in os.listdir(self.vfs.root_directory)
                if os.path.isfile(os.path.join(self.vfs.root_directory, f))
            ]
            for f in all_files:
                file_listbox.insert(END, f)

            def get_selected_files():
                return [file_listbox.get(i) for i in file_listbox.curselection()]

            def batch_delete():
                for fname in get_selected_files():
                    try:
                        self.vfs.delete_file(fname)
                    except Exception as e:
                        messagebox.showerror("Error", str(e))
                refresh()

            def batch_copy():
                dest = filedialog.askdirectory(title="Select Destination Folder")
                if dest:
                    for fname in get_selected_files():
                        src = os.path.join(self.vfs.root_directory, fname)
                        dst = os.path.join(dest, fname)
                        try:
                            shutil.copy2(src, dst)
                        except Exception as e:
                            messagebox.showerror("Copy Failed", str(e))

            def batch_move():
                dest = filedialog.askdirectory(title="Select Destination Folder")
                if dest:
                    for fname in get_selected_files():
                        src = os.path.join(self.vfs.root_directory, fname)
                        dst = os.path.join(dest, fname)
                        try:
                            shutil.move(src, dst)
                        except Exception as e:
                            messagebox.showerror("Move Failed", str(e))
                    refresh()

            def refresh():
                file_listbox.delete(0, END)
                current = [
                    f for f in os.listdir(self.vfs.root_directory)
                    if os.path.isfile(os.path.join(self.vfs.root_directory, f))
                ]
                for f in current:
                    file_listbox.insert(END, f)

            button_frame = ttk.Frame(frame)
            button_frame.pack(pady=5)

            ttk.Button(button_frame, text="Delete", bootstyle="danger-outline", command=batch_delete).pack(side=LEFT, padx=5)
            ttk.Button(button_frame, text="Copy To...", bootstyle="info-outline", command=batch_copy).pack(side=LEFT, padx=5)
            ttk.Button(button_frame, text="Move To...", bootstyle="warning-outline", command=batch_move).pack(side=LEFT, padx=5)

            return frame

        self.show_dialog("Batch File Operations", layout)


    def open_analytics_panel(self):
        import os
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        def layout(dialog):
            frame = ttk.Frame(dialog, padding=20)
            frame.pack(fill=BOTH, expand=True)

            stats, filetype_data, date_data = self.collect_file_stats(
                return_filetypes=True,
                return_dates=True
            )

            # Text stats (left)
            text_frame = ttk.Frame(frame)
            text_frame.pack(side=LEFT, fill=Y, padx=10)

            for key, value in stats.items():
                ttk.Label(
                    text_frame,
                    text=f"{key}: {value}",
                    font=("Consolas", 10),
                    bootstyle="info"
                ).pack(anchor="w", pady=2)

            # Charts (right)
            chart_frame = ttk.Frame(frame)
            chart_frame.pack(side=RIGHT, fill=BOTH, expand=True)

            fig = Figure(figsize=(6, 4), dpi=100)
            ax1 = fig.add_subplot(211)  # Pie chart
            ax2 = fig.add_subplot(212)  # Timeline

            if filetype_data:
                labels = list(filetype_data.keys())
                sizes = list(filetype_data.values())
                ax1.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
                ax1.set_title("File Type Distribution", fontsize=10)

            if date_data:
                dates = sorted(date_data.keys())
                counts = [date_data[d] for d in dates]
                ax2.plot(dates, counts, marker="o", linestyle="-", color="steelblue")
                ax2.set_title("File Creation Timeline", fontsize=10)
                ax2.set_xlabel("Date")
                ax2.set_ylabel("Files Created")
                fig.autofmt_xdate(rotation=45)

            canvas = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH, expand=True)

            return frame

        self.show_dialog("📊 VFS Analytics Panel", layout)


    def collect_file_stats(self, return_filetypes=False, return_dates=False):
        import os
        from collections import defaultdict
        from datetime import datetime

        files = [
            f for f in os.listdir(self.vfs.root_directory)
            if os.path.isfile(os.path.join(self.vfs.root_directory, f))
        ]

        total_files = len(files)
        total_size = 0
        largest_file = ("", 0)
        last_modified = ("", 0)
        extensions = {}
        created_dates = defaultdict(int)

        for f in files:
            path = os.path.join(self.vfs.root_directory, f)
            size = os.path.getsize(path)
            mtime = os.path.getmtime(path)
            ctime = os.path.getctime(path)

            total_size += size
            if size > largest_file[1]:
                largest_file = (f, size)
            if mtime > last_modified[1]:
                last_modified = (f, mtime)

            ext = os.path.splitext(f)[1] or "None"
            extensions[ext] = extensions.get(ext, 0) + 1

            date_str = datetime.fromtimestamp(ctime).strftime("%Y-%m-%d")
            created_dates[date_str] += 1

        size_mb = round(total_size / (1024 * 1024), 2)
        largest_name = largest_file[0] or "N/A"
        largest_size = round(largest_file[1] / 1024, 2)
        modified_name = last_modified[0] or "N/A"

        stat_text = {
            "Total Files": total_files,
            "Total Size": f"{size_mb} MB",
            "Largest File": f"{largest_name} ({largest_size} KB)",
            "Last Modified": modified_name
        }

        result = [stat_text]
        if return_filetypes:
            result.append(extensions)
        if return_dates:
            result.append(dict(created_dates))

        return tuple(result) if len(result) > 1 else result[0]




    def show_dialog(self, title, content_frame):
        dialog = ttk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("700x500")
        dialog.resizable(True, True)
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
