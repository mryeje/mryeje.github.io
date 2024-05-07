import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import subprocess
import sys

class FileMoverApp:
    def __init__(self, master):
        self.master = master
        master.title("File Mover and Converter")
        master.geometry("675x450")  # Window size

        self.model_label = tk.Label(master, text="Model Number", font=("Arial", 12))
        self.model_label.pack(pady=10)

        self.model_entry = tk.Entry(master, font=("Arial", 12))
        self.model_entry.pack(pady=10)

        self.load_file_btn = tk.Button(master, text="Load File", font=("Arial", 12), command=self.load_file)
        self.load_file_btn.pack(pady=10)

        self.success_button = tk.Button(master, text="", font=("Arial", 10), fg="blue", command=self.open_destination)
        self.success_button.pack(pady=(5, 0))
        self.success_button.pack_forget()  # Hide initially

        self.convert_and_move_btn = tk.Button(master, text="Convert and Move to DXF", command=self.convert_and_move, state='disabled')
        self.convert_and_move_btn.pack(pady=10)

        self.file_path = ""
        self.destination_path = "C:/Users/jsmith/Blender/GE CAD files"
        self.external_exe_path = "C:\\Program Files\\ODA\\ODAFileConverter 24.12.0\\ODAFileConverter.exe"

    def load_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.convert_and_move_btn['state'] = 'normal'
            self.hide_success_button()
            print(f"File loaded: {self.file_path}")

    def convert_and_move(self):
        model_number = self.model_entry.get()
        if self.file_path and os.path.exists(self.file_path) and model_number:
            file_extension = os.path.splitext(self.file_path)[1]
            new_file_name = model_number + file_extension
            destination_file_path = os.path.join(self.destination_path, new_file_name)
            shutil.move(self.file_path, destination_file_path)
            self.file_path = destination_file_path  # Update file_path to new location
            print(f"File moved to: {destination_file_path}")
            self.show_success_button(f"Successfully moved {new_file_name} to {self.destination_path}")
            self.convert_to_dxf()
            self.convert_and_move_btn['state'] = 'disabled'
        else:
            messagebox.showerror("Error", "No file selected, file does not exist, or model number is not specified.")

    def convert_to_dxf(self):
        if self.file_path and os.path.exists(self.file_path):
            self.run_external_exe(self.file_path)

    def run_external_exe(self, file_path):
        input_folder = os.path.dirname(file_path)
        output_folder = self.destination_path + "\\Output"
        output_version = "ACAD2018"
        output_file_type = "DXF"
        recurse = "0"
        audit = "1"

        command = [
            self.external_exe_path,
            input_folder,  # Properly formatted input
            output_folder,
            output_version,
            output_file_type,
            recurse,
            audit
        ]

        print("Running command:", ' '.join(command))  # Debugging output

        try:
            subprocess.run(command, check=True)
            messagebox.showinfo("Success", "File was successfully converted and saved as DXF!")
            clear_directory_files(self.destination_path)  # Clear the directory of files after conversion
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Execution Error", f"Failed to execute the process: {e}")

    def open_destination(self):
        try:
            os.startfile(self.destination_path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open the directory: {e}")

    def show_success_button(self, message):
        self.success_button['text'] = message
        self.success_button.pack()  # Show the button with the success message

    def hide_success_button(self):
        self.success_button.pack_forget()  # Hide the success button

def clear_directory_files(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
            print(f"Deleted file: {item_path}")
        else:
            print(f"Skipped directory: {item_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileMoverApp(root)
    root.mainloop()
