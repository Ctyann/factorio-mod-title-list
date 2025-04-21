import json
import os
import zipfile

FACTORIO_MOD_DIR = os.path.join(os.environ["APPDATA"], "Factorio", "mods")
MOD_LIST_PATH = os.path.join(FACTORIO_MOD_DIR, "mod-list.json")
OUTPUT_PATH = os.path.join(os.getcwd(), "enabled_mods.txt")

with open(MOD_LIST_PATH, "r", encoding="utf-8") as f:
    mod_list = json.load(f)

enabled_mods = [mod["name"] for mod in mod_list["mods"] if mod["enabled"] and mod["name"] != "base"]
mod_titles = []

for mod_name in enabled_mods:
    found = False

    # 解凍フォルダを探す
    for item in os.listdir(FACTORIO_MOD_DIR):
        if item.startswith(mod_name + "_") and os.path.isdir(os.path.join(FACTORIO_MOD_DIR, item)):
            info_path = os.path.join(FACTORIO_MOD_DIR, item, "info.json")
            if os.path.exists(info_path):
                with open(info_path, "r", encoding="utf-8") as info_file:
                    info = json.load(info_file)
                    title = info.get("title", info.get("name", mod_name))
                    mod_titles.append(title)
                    found = True
            break

    if not found:
        # zipファイル内を探す
        for item in os.listdir(FACTORIO_MOD_DIR):
            if item.startswith(mod_name + "_") and item.endswith(".zip"):
                zip_path = os.path.join(FACTORIO_MOD_DIR, item)
                with zipfile.ZipFile(zip_path, "r") as zip_file:
                    # info.jsonのパスを探す
                    info_json_path = next(
                        (f for f in zip_file.namelist() if f.endswith("info.json") and f.count("/") == 1),
                        None
                    )
                    if info_json_path:
                        with zip_file.open(info_json_path) as info_file:
                            info = json.load(info_file)
                            title = info.get("title", info.get("name", mod_name))
                            mod_titles.append(title)
                            found = True
                break

    if not found:
        mod_titles.append(mod_name + "（info.jsonが見つかりませんでした）")

# 結果を表示
print("有効なModのタイトル一覧:")
for title in mod_titles:
    print(f"- {title}")

# テキストファイルに出力
with open(OUTPUT_PATH, "w", encoding="utf-8") as out_file:
    out_file.write("有効なModのタイトル一覧:\n")
    for title in mod_titles:
        out_file.write(f"- {title}\n")

print(f"\n→ 結果を '{OUTPUT_PATH}' に保存しました。")
