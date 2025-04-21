# Factorio Mod Title List

A simple Python script that extracts and lists the titles of enabled Factorio mods. The result is exported to a text file.

## 🚀 Features
- Extracts enabled mods from Factorio's `mod-list.json`.
- Supports both mod folders and mod `.zip` files.
- Exports the mod titles to a plain text file.

## 📦 Requirements
- **Windows** (for the precompiled `.exe` version)
- **Python** (if running the script version)

## 💻 Usage

### Option 1: Using the `.exe` file
1. Download the latest `.exe` release from the [Releases](https://github.com/Ctyann/factorio-mod-title-list/releases) page.
2. Place the `.exe` file in any folder.
3. Double-click the `.exe` file to run it.
4. The list of enabled mod titles will be saved in `enabled_mods.txt` in the same directory.

### Option 2: Running the script with Python
1. Clone or download this repository.
2. Install Python (if not already installed) from [python.org](https://www.python.org/).
3. Install required dependencies (if needed):
    ```bash
    pip install -r requirements.txt
    ```
4. Run the script:
    ```bash
    python list_enabled_mods.py
    ```
5. The list of enabled mod titles will be saved in `enabled_mods.txt`.

## 🔧 How it works
- The script reads `mod-list.json` from your Factorio mod directory.
- It looks for enabled mods and fetches the title from either the `info.json` file or the `zip` files.
- The resulting list is saved as a plain text file (`enabled_mods.txt`).

## ⚠️ Notes
- Make sure Factorio is installed and you have the `mod-list.json` file in the expected directory:  
  - On Windows: `C:\Users\<YourUsername>\AppData\Roaming\Factorio\mods\mod-list.json`


