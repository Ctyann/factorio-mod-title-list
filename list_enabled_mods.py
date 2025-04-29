import json
import os
import zipfile
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

def extract_titles(include_version=False, include_link=False):
    try:
        mods_path = Path(os.getenv('APPDATA')) / 'Factorio' / 'mods'
        mod_list_path = mods_path / 'mod-list.json'

        with open(mod_list_path, encoding='utf-8') as f:
            mod_list = json.load(f)['mods']

        enabled_mods = [mod["name"] for mod in mod_list if mod.get('enabled') and mod['name'] != 'base']

        lines = []
        for mod_id in enabled_mods:
            found = False
            title = mod_id
            version = ""
            link = ""

            # 解凍フォルダを探す
            for item in os.listdir(mods_path):
                if item.startswith(mod_id + "_") and os.path.isdir(os.path.join(mods_path, item)):
                    info_path = os.path.join(mods_path, item, "info.json")
                    if os.path.exists(info_path):
                        with open(info_path, "r", encoding="utf-8") as info_file:
                            info = json.load(info_file)
                            title = info.get("title", mod_id)
                            version = info.get('version', "")
                            link = f"https://mods.factorio.com/mod/{mod_id}"
                            found = True
                    break

            if not found:
                # zipファイル内を探す
                for item in os.listdir(mods_path):
                    if item.startswith(mod_id + "_") and item.endswith(".zip"):
                        zip_path = os.path.join(mods_path, item)
                        with zipfile.ZipFile(zip_path, "r") as zip_file:
                            # info.jsonのパスを探す
                            info_json_path = next(
                                (f for f in zip_file.namelist() if f.endswith("info.json") and f.count("/") == 1),
                                None
                            )
                            if info_json_path:
                                with zip_file.open(info_json_path) as info_file:
                                    info = json.load(info_file)
                                    title = info.get("title", mod_id)
                                    version = info.get('version', "")
                                    link = f"https://mods.factorio.com/mod/{mod_id}"
                                    found = True
                        break

            if mod_id == 'elevated-rails':
                title = f"Elevated Rails"
                version = f"Official"
                link = f"https://factorio.com/blog/post/fff-378"
                found = True
            if mod_id == 'quality':
                title = f"Quality"
                version = f"Official"
                link = f"https://factorio.com/blog/post/fff-375"
                found = True
            if mod_id == 'space-age':
                title = f"Space Age"
                version = f"Official"
                link = f"https://factorio.com/blog/post/fff-373"
                found = True

            if not found:
                title += f" [info.json not found]"

            line = f"- {title}"
            if include_version and version:
                line += f" ({version})"
            lines.append(line)
            if include_link:
                lines.append(f"    {link}")
                lines.append("")  # 空行

        output = "\n".join(lines)
        with open("enabled_mods.txt", "w", encoding="utf-8") as f:
            f.write(output)
        messagebox.showinfo("Success", "Mod list extraction completed.")
        os.startfile("enabled_mods.txt")
        return True
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return False

def run_gui():
    root = tk.Tk()
    root.title("Factorio Mod Title Extractor")

    # パディングをつけるための Frame を使用
    frame = tk.Frame(root, padx=80, pady=10)
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Choose your output options").pack(pady=5)

    version_var = tk.BooleanVar()
    link_var = tk.BooleanVar()

    tk.Checkbutton(frame, text="Show Mod Version", variable=version_var).pack(anchor='w', pady=(0, 5))
    tk.Checkbutton(frame, text="Add a link to the Mod Portal", variable=link_var).pack(anchor='w', pady=(0, 5))

    def on_run():
        success = extract_titles(
            include_version=version_var.get(),
            include_link=link_var.get(),
        )
        if success:
            root.destroy()

    button_style = {"font": ("Arial", 14), "width": 10, "height": 2}
    tk.Button(frame, text="Run", command=on_run, **button_style).pack(pady=10)
    root.resizable(False, False)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
