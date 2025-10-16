# build_exe_autologin.py
# Script pentru crearea executabilului ALEPH Monitor - Auto Login

"""
INSTRUCȚIUNI DE FOLOSIRE:

1. Instalează dependențele necesare:
   pip install paramiko requests pyautogui pyinstaller pillow

2. Rulează acest script:
   python build_exe_autologin.py

3. Executabilul va fi creat în folder-ul 'dist/AlephMonitor-AutoLogin.exe'

4. Distribuie executabilul - utilizatorii vor putea să-l ruleze fără Python instalat!
"""

import PyInstaller.__main__
import os
import sys

def create_icon():
    """Creează o iconiță simplă pentru aplicație."""
    try:
        from PIL import Image, ImageDraw

        # Creează o iconiță 256x256
        img = Image.new('RGBA', (256, 256), color=(52, 152, 219, 255))
        draw = ImageDraw.Draw(img)

        # Desenează un server/computer
        draw.rectangle([64, 80, 192, 176], fill=(255, 255, 255, 255))
        draw.rectangle([80, 96, 176, 112], fill=(46, 204, 113, 255))
        draw.rectangle([80, 128, 176, 144], fill=(52, 152, 219, 255))
        draw.ellipse([112, 188, 144, 220], fill=(255, 255, 255, 255))

        img.save('aleph_icon_autologin.ico', format='ICO')
        print("Iconita creata: aleph_icon_autologin.ico")
        return 'aleph_icon_autologin.ico'
    except Exception as e:
        print(f"Nu s-a putut crea iconita: {e}")
        return None

def build_executable():
    """Construiește executabilul folosind PyInstaller."""

    print("=" * 60)
    print("CREARE EXECUTABIL ALEPH MONITOR - AUTO LOGIN")
    print("=" * 60)

    # Creează iconița
    icon_path = create_icon()

    # Configurație PyInstaller
    pyinstaller_args = [
        'monitor-server-autologin.py',       # Fișierul principal
        '--onefile',                         # Un singur fișier executabil
        '--windowed',                        # Fără consolă (GUI mode)
        '--name=AlephMonitor-AutoLogin',     # Numele executabilului
        '--clean',                           # Curăță fișierele temporare
        '--noconfirm',                       # Nu cere confirmare
    ]

    # Adaugă iconița dacă există
    if icon_path and os.path.exists(icon_path):
        pyinstaller_args.append(f'--icon={icon_path}')

    # Adaugă metadata
    pyinstaller_args.extend([
        '--version-file=version_info_autologin.txt',  # Dacă există
    ])

    print("\nPornire build PyInstaller...\n")

    try:
        PyInstaller.__main__.run(pyinstaller_args)

        print("\n" + "=" * 60)
        print("EXECUTABIL CREAT CU SUCCES!")
        print("=" * 60)
        print(f"\nLocatie: {os.path.abspath('dist/AlephMonitor-AutoLogin.exe')}")
        print("\nINSTRUCTIUNI DISTRIBUIRI:")
        print("   1. Copiază fișierul 'dist/AlephMonitor-AutoLogin.exe' pe orice calculator")
        print("   2. La prima rulare, se va deschide direct ecranul principal")
        print("   3. Apasă 'Pornire Monitor' pentru a începe monitorizarea")
        print("   4. Monitorizarea va porni automat cu utilizatorul implicit")
        print("\nIMPORTANT:")
        print("   - Executabilul contine parola SSH (criptata in exe)")
        print("   - Utilizator implicit: admin / admin123")
        print("   - Catalog.exe trebuie să existe la: C:\\AL500\\catalog\\bin\\Catalog.exe")
        print("   - Browser-ul se va deschide automat pentru catalog online")
        print("\n" + "=" * 60)

    except Exception as e:
        print(f"\nEROARE la creare executabil: {e}")
        sys.exit(1)

def create_version_info():
    """Creează fișier cu informații despre versiune."""
    version_info = """# UTF-8
#
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 1, 0, 0),
    prodvers=(1, 1, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Biblioteca'),
        StringStruct(u'FileDescription', u'Monitor Server ALEPH - Auto Login'),
        StringStruct(u'FileVersion', u'1.1.0.0'),
        StringStruct(u'InternalName', u'AlephMonitor-AutoLogin'),
        StringStruct(u'LegalCopyright', u'© 2025'),
        StringStruct(u'OriginalFilename', u'AlephMonitor-AutoLogin.exe'),
        StringStruct(u'ProductName', u'ALEPH Server Monitor - Auto Login'),
        StringStruct(u'ProductVersion', u'1.1.0.0')])
      ]
    ),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""

    try:
        with open('version_info_autologin.txt', 'w', encoding='utf-8') as f:
            f.write(version_info)
        print("Fisier versiune creat: version_info_autologin.txt")
    except Exception as e:
        print(f"Nu s-a putut crea fisierul de versiune: {e}")

if __name__ == "__main__":
    # Verifică dacă fișierul principal există
    if not os.path.exists('monitor-server-autologin.py'):
        print("EROARE: Nu gasesc fisierul 'monitor-server-autologin.py'!")
        print("   Asigură-te că ești în folderul corect și că fișierul există.")
        sys.exit(1)

    # Creează fișierul de versiune
    create_version_info()

    # Construiește executabilul
    build_executable()
