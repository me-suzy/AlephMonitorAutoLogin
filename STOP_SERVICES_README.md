# Script Oprire Servicii ALEPH

## 🛑 **Stop ALEPH Services**

Script Python pentru oprirea completă a serviciilor ALEPH:
- Închide toate procesele `Catalog.exe`
- Închide sesiunile browser cu catalog online deschis
- Deconectează sesiunea web de la [http://87.176.171.72:8991/F/](http://87.176.171.72:8991/F/)

## 📋 **Ce Face Scriptul**

### 1️⃣ **Oprire Catalog.exe**
- Caută toate procesele `Catalog.exe` active
- Încearcă oprire elegantă (terminate)
- Dacă nu răspunde → forțează oprirea (kill)
- Raportează numărul de procese oprite

### 2️⃣ **Închidere Browsere**
- Caută browsere cu catalog online deschis:
  - Chrome
  - Firefox
  - Edge
  - Internet Explorer
  - Opera
- Verifică dacă URL-ul conține `87.176.171.72:8991`
- Închide browserele găsite

### 3️⃣ **Deconectare Sesiune Web**
- Accesează pagina de catalog online
- Caută link-ul de deconectare ("Sfârșitul sesiunii")
- Execută deconectarea automată
- Închide sesiunea HTTP

## 🚀 **Utilizare**

### Instalare Dependențe
```bash
pip install psutil requests
```

### Rulare Script
```bash
python stop_aleph_services.py
```

### Rezultat
```
============================================================
OPRIRE SERVICII ALEPH
============================================================

[1/3] Oprire Catalog.exe...
Găsit proces: Catalog.exe (PID: 1234)
✓ Proces oprit: PID 1234

[2/3] Închidere sesiuni browser...
Găsit browser cu catalog: chrome.exe (PID: 5678)
✓ Browser închis: PID 5678

[3/3] Deconectare sesiune web...
Accesare http://87.176.171.72:8991/F pentru deconectare...
✓ Deconectare reușită din sesiunea web

============================================================
RAPORT FINAL
============================================================
Catalog.exe oprit: ✓ DA
Browsere închise: ✓ DA
Sesiune web deconectată: ✓ DA
Total procese oprite: 1
Total browsere închise: 1
============================================================

✓ Servicii ALEPH oprite cu succes!
  - Procese Catalog.exe oprite: 1
  - Browsere închise: 1

Vezi detalii în: stop_aleph_services.log
============================================================
```

## 📝 **Log-uri**

Scriptul creează fișierul `stop_aleph_services.log` cu detalii complete:
```
2025-10-16 00:30:00 - INFO - ============================================================
2025-10-16 00:30:00 - INFO - OPRIRE CATALOG.EXE
2025-10-16 00:30:00 - INFO - ============================================================
2025-10-16 00:30:01 - INFO - Găsit proces: Catalog.exe (PID: 1234)
2025-10-16 00:30:01 - INFO - ✓ Proces oprit: PID 1234
...
```

## 🔧 **Integrare cu Monitorul**

Acest script poate fi folosit independent sau integrat în monitorul ALEPH pentru:
- Cleanup înainte de repornire
- Oprire servicii la deconectare
- Maintenance periodic

## ⚠️ **Precauții**

- Scriptul va închide **TOATE** procesele `Catalog.exe` active
- Browserele vor fi închise **doar** dacă au catalog online deschis
- Se recomandă salvarea datelor înainte de rulare
- Necesită permisiuni pentru a opri procese

## 🔍 **Verificare Status**

Pentru a verifica ce servicii sunt active înainte de oprire:

**Windows Task Manager:**
```
Ctrl + Shift + Esc → Procese → Caută "Catalog.exe"
```

**Browser:**
```
Verifică tab-urile deschise pentru: 87.176.171.72:8991
```

## 📞 **Suport**

Pentru probleme sau întrebări, contactați administratorul de sistem.
