# ===============================================================================
#  GF2ePRNGTool - Verilog Generator for PRNGs over GF(2^e)
# -------------------------------------------------------------------------------
# @author      : Davi Moreno
# @affiliation : Universidade Federal de Pernambuco (UFPE), PPGEE
# 
# A graphical interface for generating Verilog code and testbenches for Pseudorandom
# Number Generators (PRNGs) based on affine recurrence relations over the finite field GF(2^e).
#
#  FEATURES:
#     - Input polynomial parameters a(x), c(x), and h(x) in multiple formats:
#         - Integer   (e.g., 19)
#         - Binary    (e.g., 0b10011)
#         - Hex       (e.g., 0x13)
#         - Algebraic (e.g., x^4 + x + 1)
#     - Directory selection for project output.
#     - Console log with runtime messages and error handling.
#     - Designed for researchers and engineers working with FPGA/ASIC designs.
#
# ===============================================================================

from tkinter import ttk, filedialog, messagebox
from gf2_poly_utils import poly_degree, poly_mod, str_poly_to_int, int_poly_to_str

import gf2e_prng_tool
import os
import sys
import tkinter as tk
import traceback

class ConsoleRedirector:
    """
    Used to redirect stdout/stderr to the app Console logs
    """
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.config(state="normal")
        self.text_widget.insert("end", message)
        self.text_widget.see("end")
        self.text_widget.config(state="disabled")

    def flush(self):
        pass

class VerilogGeneratorGUI(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("GF2ePRNGTool - Verilog Generator for PRNGs over GF(2^e)")
        # self.geometry("600x400")
        self.resizable(False, False)

        self.format_options = ["int", "bin", "hex", "alg"]
        self.placeholders = {
            "int" : "e.g., 21",
            "bin" : "e.g., 0b10101",
            "hex" : "e.g., 0x15",
            "alg" : "e.g., x^4 + x^2 + 1"
        }

        self._create_widgets()

        # Dynamically size the window based on content
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())


    def _create_widgets(self):
        frame = ttk.Frame(self, padding="20")
        frame.pack(fill="both", expand=True)

        self.entries = {}
        self.format_vars = {}

        for idx, label in enumerate(["a(x)", "c(x)", "h(x)"]):
            ttk.Label(frame, text=f"Polynomial {label}:").grid(row=idx, column=0, sticky="w")

            # Format selection
            format_var = tk.StringVar(value="int")
            self.format_vars[label] = format_var

            format_menu = ttk.OptionMenu(
                frame, format_var, "int", *self.format_options,
                command=lambda fmt, l=label: self._update_placeholder(l, fmt)
            )
            format_menu.grid(row=idx, column=1, sticky="w", padx=5)

            # Entry with simulated placeholder
            entry = tk.Entry(frame, width=40, foreground="gray")
            default_fmt = format_var.get()
            placeholder = self.placeholders[default_fmt]
            entry.insert(0, placeholder)
            entry.bind("<FocusIn>", lambda e, l=label: self._clear_placeholder(l))
            entry.bind("<FocusOut>", lambda e, l=label: self._restore_placeholder(l))
            entry.grid(row=idx, column=2, pady=5)
            self.entries[label] = entry

        # Output directory
        ttk.Label(frame, text="Output Directory:").grid(row=3, column=0, sticky="w")
        self.dir_var = tk.StringVar(value=os.getcwd())
        self.dir_entry = ttk.Entry(frame, textvariable=self.dir_var, width=30)
        self.dir_entry.grid(row=3, column=2, sticky="w", pady=5)
        browse_button = ttk.Button(frame, text="Browse", command=self.browse_directory)
        browse_button.grid(row=3, column=3, padx=5)

        # Button row (Generate + Clear)
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=5)

        generate_button = ttk.Button(button_frame, text="Generate Project", command=self.generate_project)
        generate_button.pack(side="left", padx=10)

        clear_button = ttk.Button(button_frame, text="Clear Console", command=self.clear_output)
        clear_button.pack(side="left")

        # Output text area label
        ttk.Label(self, text="Console Output:").pack(anchor="w", padx=20)

        # Frame for text area + scrollbar
        text_frame = ttk.Frame(self)
        text_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Scrollbar
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        # Text widget (read-only style)
        self.output_text = tk.Text(text_frame, height=10, wrap="word", yscrollcommand=scrollbar.set)
        self.output_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.output_text.yview)

        # Redirect stderr to the Text widget that store the output logs
        # sys.stdout = ConsoleRedirector(self.output_text)
        sys.stderr = ConsoleRedirector(self.output_text)

        # Disable user editing
        self.output_text.config(state="disabled")


    def _update_placeholder(self, label, fmt):
        entry = self.entries[label]
        if entry.get() == "" or entry.cget("foreground") == "gray":
            entry.delete(0, tk.END)
            entry.insert(0, self.placeholders[fmt])
            entry.config(foreground="gray")

    def _clear_placeholder(self, label):
        entry = self.entries[label]
        if entry.cget("foreground") == "gray":
            entry.delete(0, tk.END)
            entry.config(foreground="black")

    def _restore_placeholder(self, label):
        entry = self.entries[label]
        if not entry.get():
            fmt = self.format_vars[label].get()
            entry.insert(0, self.placeholders[fmt])
            entry.config(foreground="gray")

    def clear_output(self):
        """
        Clears the contents of the console output text area.
        """
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state="disabled")


    def log_output(self, message: str):
        """
        Appends a message to the output text area.
        """
        self.output_text.config(state="normal")
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)  # auto-scroll to bottom
        self.output_text.config(state="disabled")


    def browse_directory(self):
        selected_dir = filedialog.askdirectory(initialdir=self.dir_var.get())
        if selected_dir:
            self.dir_var.set(selected_dir)

    def extract_poly_parameters(self):
        """
        Extract polynomial parameters given by user and save them in a dict
        Check for missing parameters too
        """
        missing_params = []
        inputs = {}
        for label in ["a(x)", "c(x)", "h(x)"]:
            value = self.entries[label].get()
            is_placeholder = self.entries[label].cget("foreground") == "gray"
            poly_format = self.format_vars[label].get()
            inputs[label] = ("" if is_placeholder else value, poly_format)
            if is_placeholder:
                missing_params.append(f"{label}")

        return inputs, missing_params

    def generate_project(self):

        # Extract polynomial parameters given by user
        inputs, missing_params = self.extract_poly_parameters()

        # Check if there are missing parameters        
        if len(missing_params) == 1:
            messagebox.showinfo("Error", f"Project missing parameter {missing_params[0]}!")
            return
        elif len(missing_params) > 1:
            messagebox.showinfo("Error", f"Project missing parameters {missing_params}!")
            return 

        # Extract dir to save project
        directory = self.dir_var.get()

        # Set arguments for project construction
        a = str_poly_to_int(poly_str=inputs["a(x)"][0], poly_format=inputs["a(x)"][1])
        c = str_poly_to_int(poly_str=inputs["c(x)"][0], poly_format=inputs["c(x)"][1])
        h = str_poly_to_int(poly_str=inputs["h(x)"][0], poly_format=inputs["h(x)"][1])
        save_dir = directory

        # Check if h(x) is irreducible
        # For now just checking that it is not 0
        if h == 0:
            messagebox.showinfo("Error", f"Polynomial h(x) cannot be {h}, it needs to be irreducible!")

        # Reduce polynomials a(x) and c(x) by h(x) if possible (reducing by h(x) doesn't affect PRNG)
        a = poly_mod(a, h)
        c = poly_mod(c, h)

        # Check if a(x) is not 0 (if it is the recursive relation of the PRNG will always output c(x))
        if a == 0:
            messagebox.showinfo("Error", f"Polynomial a(x) cannot be 0 (mod h(x))!")
            return

        # Contruct PRNG project inside save_dir
        gf2e_prng_tool.generate_project(a, c, h, save_dir)

        # Output project creation log
        e = poly_degree(h)
        project_dir = save_dir + f"/gf2_{e}_prng/"
        self.log_output("Generating project with:")
        a_alg = int_poly_to_str(a, "alg")
        c_alg = int_poly_to_str(c, "alg")
        h_alg = int_poly_to_str(h, "alg")
        self.log_output(f"  a(x): {a} (int) = {a_alg}")
        self.log_output(f"  c(x): {c} (int) = {c_alg}")
        self.log_output(f"  h(x): {h} (int) = {h_alg}")
        self.log_output(f"  Project directory: {project_dir}")

        # Print message box indicating that project was generated successfully
        messagebox.showinfo("Success", "Project generated successfully!")

if __name__ == "__main__":
    app = VerilogGeneratorGUI()
    app.mainloop()
