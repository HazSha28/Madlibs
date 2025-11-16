import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from utils.parser import extract_placeholders, load_template, render_story, random_fill_value       



class MadLibApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # ---- Window Icon ----
        icon_path = os.path.join(os.path.dirname(__file__), "../assets/logo.png")
        try:
            self.iconphoto(False, tk.PhotoImage(file=icon_path))
        except Exception as e:
            print("Icon load failed:", e)

        self.title("MadLibs — Story Generator")
        self.geometry("900x580")
        self.minsize(750, 480)

        self.templates_path = os.path.join(os.path.dirname(__file__), "templates")

        # Load template names
        self.templates = [
            f for f in os.listdir(self.templates_path)
            if f.endswith(".txt")
        ]

        self._build_layout()
        self.template_select.set(self.templates[0])
        self.on_template_change(None)

    # ---------------- UI ----------------
    def _build_layout(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self._build_left()
        self._build_right()

    def _build_left(self):
        left = ttk.Frame(self, padding=12)
        left.grid(row=0, column=0, sticky="nsew")

        title = ttk.Label(left, text="MadLib Story Maker", font=("Arial", 20, "bold"))
        title.pack(anchor="w")

        ttk.Label(left, text="Choose a template and fill the words").pack(anchor="w", pady=(4, 12))

        # Template selector
        self.template_select = tk.StringVar()
        template_box = ttk.Combobox(left, textvariable=self.template_select,
                                    values=self.templates, state="readonly")
        template_box.pack(fill="x")
        template_box.bind("<<ComboboxSelected>>", self.on_template_change)

        ttk.Button(left, text="Random Fill", command=self.random_fill).pack(pady=6, anchor="w")
        ttk.Button(left, text="Clear", command=self.clear_inputs).pack(pady=2, anchor="w")

        # Scrollable input area
        input_frame = ttk.LabelFrame(left, text="Fill the Blanks")
        input_frame.pack(fill="both", expand=True, pady=(10, 0))

        canvas = tk.Canvas(input_frame)
        scrollbar = ttk.Scrollbar(input_frame, orient="vertical", command=canvas.yview)
        self.form_frame = ttk.Frame(canvas)

        self.form_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.form_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set, height=300)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _build_right(self):
        right = ttk.Frame(self, padding=12)
        right.grid(row=0, column=1, sticky="nsew")

        ttk.Label(right, text="Live Preview", font=("Arial", 16, "bold")).pack(anchor="w")

        box = ttk.Frame(right)
        box.pack(fill="both", expand=True, pady=8)
        box.rowconfigure(0, weight=1)
        box.columnconfigure(0, weight=1)

        self.preview = tk.Text(box, wrap="word", state="disabled")
        self.preview.grid(row=0, column=0, sticky="nsew")

        # Actions
        actions = ttk.Frame(right)
        actions.pack(fill="x", pady=4)

        ttk.Button(actions, text="Copy to Clipboard", command=self.copy_text).pack(side="left")
        ttk.Button(actions, text="Save Story", command=self.save_story).pack(side="right")

    # ---------------- Template Logic ----------------
    def on_template_change(self, event):
        for widget in self.form_frame.winfo_children():
            widget.destroy()

        template_file = os.path.join(self.templates_path, self.template_select.get())
        self.template_text = load_template(template_file)
        placeholders = extract_placeholders(self.template_text)

        self.inputs = {}

        for ph in placeholders:
            row = ttk.Frame(self.form_frame)
            row.pack(fill="x", pady=3)

            ttk.Label(row, text=ph + ":", width=18).pack(side="left")
            var = tk.StringVar()
            ttk.Entry(row, textvariable=var).pack(side="left", fill="x", expand=True)

            self.inputs[ph] = var

        self.update_preview()

    def gather_values(self):
        result = {}
        for key, var in self.inputs.items():
            value = var.get().strip()
            result[key] = value if value else f"<{key}>"
        return result

    def update_preview(self):
        story = render_story(self.template_text, self.gather_values())

        self.preview.config(state="normal")
        self.preview.delete("1.0", tk.END)
        self.preview.insert(tk.END, story)
        self.preview.config(state="disabled")

    def random_fill(self):
        for key, var in self.inputs.items():
            var.set(random_fill_value(key))
        self.update_preview()

    def clear_inputs(self):
        for var in self.inputs.values():
            var.set("")
        self.update_preview()

    # ---------------- Actions ----------------
    def copy_text(self):
        story = render_story(self.template_text, self.gather_values())
        self.clipboard_clear()
        self.clipboard_append(story)
        messagebox.showinfo("Copied", "Story copied to clipboard!")

    def save_story(self):
        story = render_story(self.template_text, self.gather_values())
        file = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt")])
        if file:
            with open(file, "w", encoding="utf-8") as f:
                f.write(story)
            messagebox.showinfo("Saved", "Story saved successfully!")


if __name__ == "__main__":
    app = MadLibApp()
    app.mainloop()
