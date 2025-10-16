# Monitor Server ALEPH - Auto Login

## 🚀 Versiune Simplificată - Fără Autentificare

Această versiune este o variantă simplificată a Monitorului Server ALEPH care se loghează automat fără cerințe de autentificare.

## ✨ Caracteristici

### 🔑 **Auto Login**
- **Fără formular de autentificare**
- **Buton direct "Pornire Monitor"**
- **Utilizator implicit**: `admin` / `admin123`
- **Credențiale SSH integrate**: `root` / `YOUR-PASSWORD`

### 🛡️ **Securitate**
- Credențialele SSH sunt integrate în executabil
- Parola SSH `YOUR-PASSWORD` este CRITICĂ - fără ea nu poți accesa serverul
- Conectare automată la server `87.176.171.72`

### 📋 **Funcționalități**
- Monitorizare automată la fiecare 2 minute
- Repornire automată când serverul cade
- Secvența corectă: catalog online → Catalog.exe → resetare dată
- Autentificare automată în Catalog.exe
- Log detaliat al tuturor operațiunilor

## 🔧 **Instalare și Compilare**

### Pasul 1: Instalare Dependențe
```bash
pip install paramiko requests pyautogui pyinstaller pillow
```

### Pasul 2: Compilare Executabil
```bash
python build_exe_autologin.py
```

### Pasul 3: Distribuire
Executabilul va fi generat în `dist/AlephMonitor-AutoLogin.exe`

## 🚀 **Utilizare**

1. **Rulare Executabil**:
   - Dublu-click pe `AlephMonitor-AutoLogin.exe`
   - Se deschide direct ecranul principal

2. **Pornire Monitorizare**:
   - Apasă butonul **"🚀 Pornire Monitor"**
   - Monitorizarea pornește automat cu utilizatorul implicit

3. **Monitorizare Automată**:
   - Verifică serverul la fiecare 2 minute
   - Dacă serverul cade, pornește automat secvența de repornire
   - Browser-ul se deschide automat pentru catalog online
   - Catalog.exe se lansează și se autentifică automat

## 📝 **Secvența de Repornire**

1. **Conectare SSH** cu `root` / `YOUR-PASSWORD`
2. **Setare dată în trecut** (2012) pentru licență
3. **Așteptare 30 secunde** pentru inițializare servicii
4. **Deschidere catalog ONLINE** în browser
5. **Lansare Catalog.exe** cu autentificare automată
6. **Resetare la data curentă**
7. **Redeschidere catalog online**
8. **Verificare finală**

## ⚠️ **Cerințe Sistem**

- Windows OS
- Catalog.exe instalat la: `C:\TUR00\catalog\bin\batalog.exe`
- Acces la server SSH: `87.176.171.72`
- Browser web pentru catalog online

## 🔍 **Credențiale Integrate**

### SSH (Pentru Server)
- **Server**: `87.176.171.72`
- **Utilizator**: `root`
- **Parolă**: `YOUR-PASSWORD` ← **CRITICĂ**

### Catalog (Pentru Aplicație)
- **Utilizator**: `admin`
- **Parolă**: `admin123`

## 📧 **Contact și Suport**

Pentru probleme sau sugestii, contactați administratorul de sistem.

## 🔄 **Diferențe față de Versiunea Standard**

| Caracteristică | Versiune Standard | Auto Login |
|---|---|---|
| Autentificare | Formular cu user/pass | Automată |
| Utilizatori | Lista autorizați | Unul implicit |
| Securitate | Credențiale individuale | Credențiale integrate |
| Complexitate | Medie | Simplă |
| Distribuire | Mai complexă | Simplă |
