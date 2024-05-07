import tkinter as tk
from tkinter import filedialog, messagebox
from zipfile import ZipFile
import os
import tempfile
import shutil
import zipfile

def load_zip_file():
    global zip_path
    zip_path = filedialog.askopenfilename(filetypes=[("Zip files", "*.zip")])
    if zip_path:
        status_label.config(text="Zip file loaded: " + os.path.basename(zip_path))
    else:
        status_label.config(text="No zip file selected.")

def search_for_other_folder():
    if not zip_path:
        status_label.config(text="No zip file selected. Please load a zip file first.")
        return
    
    with ZipFile(zip_path, 'r') as zip_ref:
        other_folder_exists = any('other/' in member.filename for member in zip_ref.infolist())
        if other_folder_exists:
            zip_files_in_other = [member for member in zip_ref.infolist() if 'other/' in member.filename and member.filename.endswith('.zip')]
            if zip_files_in_other:
                status_label.config(text=f"Zip files found in 'other' folder. {len(zip_files_in_other)} files found. Extracting...")
                extract_zip_files(zip_ref, zip_files_in_other)
            else:
                status_label.config(text="No zip files found in 'other' folder.")
        else:
            # The 'other' folder is not found, search for a DXF file in the zip root
            status_label.config(text="The 'other' folder is NOT found. Searching for DXF file...")
            dxf_files_in_root = [member for member in zip_ref.infolist() if member.filename.lower().endswith('.dxf') and '/' not in member.filename]
            if dxf_files_in_root:
                extract_path = "C:\\Users\\jsmith\\Blender\\extracted bosch files"
                if not os.path.exists(extract_path):
                    os.makedirs(extract_path, exist_ok=True)
                # Extract found DXF files
                for dxf_file in dxf_files_in_root:
                    zip_ref.extract(dxf_file, extract_path)
                messagebox.showinfo("DXF Extraction Complete", f"DXF files have been extracted to: {extract_path}")
                os.startfile(extract_path)
            else:
                status_label.config(text="No DXF files found in the zip file's root.")

def extract_zip_files(zip_ref, zip_files):
    extract_path = "C:\\Users\\jsmith\\Blender\\extracted bosch files"
    
    if not os.path.exists(extract_path):
        os.makedirs(extract_path, exist_ok=True)
    
    temp_dir = tempfile.mkdtemp()
    try:
        for zip_file in zip_files:
            zip_ref.extract(zip_file, temp_dir)
            nested_zip_path = os.path.join(temp_dir, zip_file.filename)
            
            if not zipfile.is_zipfile(nested_zip_path):
                print(f"Warning: {nested_zip_path} is not a zip file or is corrupted.")
                continue

            with ZipFile(nested_zip_path, 'r') as nested_zip:
                nested_zip.extractall(extract_path)
        
        messagebox.showinfo("Extraction Complete", "ZIP files have been extracted to: " + extract_path)
        os.startfile(extract_path)
    finally:
        shutil.rmtree(temp_dir)

# Set up the GUI
root = tk.Tk()
root.title("Zip File Browser")

zip_path = ''

status_label = tk.Label(root, text="Load a zip file to search for 'other' folder.", wraplength=300)
status_label.pack(pady=10)

load_zip_btn = tk.Button(root, text="Load Zip File", command=load_zip_file)
load_zip_btn.pack(pady=5)

search_btn = tk.Button(root, text="Search for 'other' folder", command=search_for_other_folder)
search_btn.pack(pady=5)

root.mainloop()
