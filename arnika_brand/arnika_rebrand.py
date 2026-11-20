import os
import re
import shutil

ROOT = os.getcwd()
BRAND_DIR = os.path.join(ROOT, "arnika_brand")
ICO_SRC = os.path.join(BRAND_DIR, "arnika_icon.ico")
PNG_SRC = os.path.join(BRAND_DIR, "arnika_icon.png")
SVG_SRC = os.path.join(BRAND_DIR, "arnika_icon.svg")

def copy_if_exists(src, rel_targets):
    if not os.path.isfile(src):
        print(f"[ARNIKA] Missing source asset: {src}")
        return
    for rel in rel_targets:
        dst = os.path.join(ROOT, rel)
        if os.path.isfile(dst):
            shutil.copy2(src, dst)
            print(f"[ARNIKA] Replaced icon: {rel}")

def patch_text(rel_path, replacements):
    path = os.path.join(ROOT, rel_path)
    if not os.path.isfile(path):
        return
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        data = f.read()
    orig = data
    for pattern, repl in replacements:
        data = re.sub(pattern, repl, data)
    if data != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(data)
        print(f"[ARNIKA] Patched text: {rel_path}")

def main():
    print("=== Applying Arnika White-Label Branding ===")

    # 1. ???????? ???? ????????? ??????? ???????? ???? ????? ? Flutter
    copy_if_exists(ICO_SRC, [
        "res/icon.ico",
        "res/tray-icon.ico",
        "flutter/windows/runner/resources/app_icon.ico",
        "flutter/assets/icon.ico",
    ])
    copy_if_exists(PNG_SRC, [
        "res/icon.png",
        "res/32x32.png",
        "res/64x64.png",
        "res/128x128.png",
        "res/128x128@2x.png",
        "flutter/assets/icon.png",
        "flutter/assets/logo.png",
    ])
    copy_if_exists(SVG_SRC, [
        "res/icon.svg",
        "flutter/assets/icon.svg",
        "flutter/assets/logo.svg",
    ])

    # 2. ????? ?????? ???? ?????? ?????? (Properties ? Task Manager)
    patch_text("flutter/windows/runner/Runner.rc", [
        (r'VALUE "CompanyName",\s*"[^"]*"', 'VALUE "CompanyName", "Arnika Systems"'),
        (r'VALUE "FileDescription",\s*"[^"]*"', 'VALUE "FileDescription", "Arnika Remote Core"'),
        (r'VALUE "ProductName",\s*"[^"]*"', 'VALUE "ProductName", "Arnika"'),
        (r'VALUE "LegalCopyright",\s*"[^"]*"', 'VALUE "LegalCopyright", "Copyright (C) Arnika. All rights reserved."'),
    ])

    # 3. ????? ????? ????? ???? ? ????? ????? ?? ??????
    patch_text("flutter/windows/runner/main.cpp", [
        (r'L"RustDesk"', 'L"Arnika"'),
    ])

    # 4. ????? ??? ?????? ???? ???? ????? (???? ??????? ? ????? ?? Arnika ????? ??????)
    patch_text("libs/hbb_common/src/config.rs", [
        (r'RwLock::new\("RustDesk"\.to_owned\(\)\)', 'RwLock::new("Arnika".to_owned())'),
    ])

    print("=== Arnika Branding Complete ===")

if __name__ == "__main__":
    main()
