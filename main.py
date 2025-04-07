import tkinter as tk
from tkinter import ttk
from collections import defaultdict

# Load and parse use flags from file
def load_useflags(filepath):
    categories = defaultdict(list)
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '#' in line:
                flag, comment = line.split('#', 1)
                flag = flag.strip()
                comment = comment.strip()
            else:
                flag = line
                comment = ''

            category = flag.split('-')[0] if '-' in flag else 'misc'
            categories[category].append((flag, comment))
    return categories

class UseFlagViewer:
    def __init__(self, root, flag_data):
        self.root = root
        self.root.title("Gentoo USE Flag Viewer")
        self.flag_data = flag_data

        self.setup_ui()

    def setup_ui(self):
        self.root.geometry("800x600")

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.left_frame = ttk.Frame(self.main_frame, width=200)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.category_list = tk.Listbox(self.left_frame)
        self.category_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.category_list.bind("<<ListboxSelect>>", self.on_category_select)

        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', self.update_flag_list)
        self.search_entry = ttk.Entry(self.right_frame, textvariable=self.search_var)
        self.search_entry.pack(fill=tk.X, padx=5, pady=5)

        self.flag_list = tk.Listbox(self.right_frame)
        self.flag_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.flag_list.bind("<<ListboxSelect>>", self.show_flag_info)

        self.flag_info = tk.Label(self.right_frame, anchor='w', justify='left')
        self.flag_info.pack(fill=tk.X, padx=5, pady=5)

        for cat in sorted(self.flag_data):
            self.category_list.insert(tk.END, cat)

    def on_category_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            self.current_category = event.widget.get(index)
            self.update_flag_list()

    def update_flag_list(self, *args):
        self.flag_list.delete(0, tk.END)
        self.flag_info.config(text="")

        if not hasattr(self, 'current_category'):
            return

        flags = self.flag_data[self.current_category]
        search_term = self.search_var.get().lower()

        for flag, comment in flags:
            if search_term in flag.lower() or search_term in comment.lower():
                self.flag_list.insert(tk.END, flag)

    def show_flag_info(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            flag_name = event.widget.get(index)
            for flag, comment in self.flag_data[self.current_category]:
                if flag == flag_name:
                    self.flag_info.config(text=f"{flag}: {comment if comment else 'No description'}")
                    break

if __name__ == '__main__':
    import os
    filepath = os.path.join(os.path.dirname(__file__), input('Enter filename of useflag file: '))
    flag_data = load_useflags(filepath)

    root = tk.Tk()
    app = UseFlagViewer(root, flag_data)
    root.mainloop()
