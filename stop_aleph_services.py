#!/usr/bin/env python3
"""
Script pentru oprirea/deconectarea serviciilor ALEPH
- Închide toate procesele Catalog.exe
- Închide sesiunile web browser pentru catalog online
- Deconectare din sesiunea ALEPH online
"""

import os
import sys
import subprocess
import psutil
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import logging
import time

# Configurare logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('stop_aleph_services.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Configurații
CATALOG_EXE = "Catalog.exe"
CATALOG_URL = "http://87.176.171.72:8991/F"
LOGOUT_PATTERN = "func=logout"  # Pattern pentru deconectare ALEPH

class AlephServicesStopper:
    def __init__(self):
        self.stopped_processes = []
        self.closed_sessions = []
        
    def stop_catalog_exe(self):
        """Oprește toate procesele Catalog.exe."""
        logging.info("=" * 60)
        logging.info("OPRIRE CATALOG.EXE")
        logging.info("=" * 60)
        
        found_processes = False
        
        try:
            # Caută toate procesele Catalog.exe
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    # Verifică dacă procesul este Catalog.exe
                    if proc.info['name'] and CATALOG_EXE.lower() in proc.info['name'].lower():
                        found_processes = True
                        pid = proc.info['pid']
                        logging.info(f"Găsit proces: {proc.info['name']} (PID: {pid})")
                        
                        # Încearcă să oprească procesul elegant
                        try:
                            proc.terminate()
                            proc.wait(timeout=5)
                            logging.info(f"✓ Proces oprit: PID {pid}")
                            self.stopped_processes.append(pid)
                        except psutil.TimeoutExpired:
                            # Dacă nu se oprește elegant, forțează oprirea
                            logging.warning(f"Proces nu răspunde, forțare oprire: PID {pid}")
                            proc.kill()
                            logging.info(f"✓ Proces forțat să se oprească: PID {pid}")
                            self.stopped_processes.append(pid)
                        except Exception as e:
                            logging.error(f"✗ Eroare la oprirea procesului PID {pid}: {e}")
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            
            if not found_processes:
                logging.info("Nu s-au găsit procese Catalog.exe active")
                return False
            else:
                logging.info(f"✓ Total procese oprite: {len(self.stopped_processes)}")
                return True
                
        except Exception as e:
            logging.error(f"✗ Eroare la oprirea Catalog.exe: {e}")
            return False
    
    def close_browser_sessions(self):
        """Închide sesiunile browser care au deschis catalogul online."""
        logging.info("=" * 60)
        logging.info("ÎNCHIDERE SESIUNI BROWSER CATALOG ONLINE")
        logging.info("=" * 60)
        
        browser_processes = ['chrome.exe', 'firefox.exe', 'msedge.exe', 'iexplore.exe', 'opera.exe']
        found_browsers = False
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['name'] and any(browser in proc.info['name'].lower() for browser in browser_processes):
                        # Verifică dacă browser-ul are URL-ul catalogului în cmdline
                        cmdline = proc.info.get('cmdline', [])
                        if cmdline and any('87.176.171.72:8991' in str(arg) for arg in cmdline):
                            found_browsers = True
                            pid = proc.info['pid']
                            logging.info(f"Găsit browser cu catalog: {proc.info['name']} (PID: {pid})")
                            
                            try:
                                proc.terminate()
                                proc.wait(timeout=3)
                                logging.info(f"✓ Browser închis: PID {pid}")
                                self.closed_sessions.append(pid)
                            except psutil.TimeoutExpired:
                                proc.kill()
                                logging.info(f"✓ Browser forțat să se închidă: PID {pid}")
                                self.closed_sessions.append(pid)
                            except Exception as e:
                                logging.error(f"✗ Eroare la închiderea browser PID {pid}: {e}")
                                
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            
            if not found_browsers:
                logging.info("Nu s-au găsit browsere cu catalog online deschis")
                return False
            else:
                logging.info(f"✓ Total browsere închise: {len(self.closed_sessions)}")
                return True
                
        except Exception as e:
            logging.error(f"✗ Eroare la închiderea browserelor: {e}")
            return False
    
    def logout_web_session(self):
        """Încearcă să deconecteze sesiunea web ALEPH."""
        logging.info("=" * 60)
        logging.info("DECONECTARE SESIUNE WEB ALEPH")
        logging.info("=" * 60)
        
        try:
            # Creează o sesiune cu retry
            session = requests.Session()
            retry = Retry(
                total=3,
                read=3,
                connect=3,
                backoff_factor=0.3,
                status_forcelist=(500, 502, 504)
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            
            # Încearcă să acceseze pagina principală pentru a obține sesiunea
            logging.info(f"Accesare {CATALOG_URL} pentru deconectare...")
            response = session.get(CATALOG_URL, timeout=10)
            
            if response.status_code == 200:
                # Caută link-ul de logout în pagină
                if 'logout' in response.text.lower() or 'deconect' in response.text.lower():
                    # Încearcă să găsească URL-ul de logout
                    import re
                    logout_match = re.search(r'(http[s]?://[^"\']+(?:logout|func=logout)[^"\']*)', response.text)
                    
                    if logout_match:
                        logout_url = logout_match.group(1)
                        logging.info(f"Găsit URL logout: {logout_url}")
                        
                        # Accesează URL-ul de logout
                        logout_response = session.get(logout_url, timeout=10)
                        if logout_response.status_code == 200:
                            logging.info("✓ Deconectare reușită din sesiunea web")
                            return True
                        else:
                            logging.warning(f"Răspuns neașteptat la logout: {logout_response.status_code}")
                    else:
                        logging.info("Nu s-a găsit link de logout în pagină")
                else:
                    logging.info("Pagina nu pare să aibă opțiune de logout")
                    
            else:
                logging.warning(f"Server răspuns cu status: {response.status_code}")
            
            # Închide sesiunea
            session.close()
            return False
            
        except requests.exceptions.Timeout:
            logging.error("✗ Timeout la accesarea paginii de deconectare")
            return False
        except requests.exceptions.ConnectionError:
            logging.error("✗ Nu se poate conecta la server pentru deconectare")
            return False
        except Exception as e:
            logging.error(f"✗ Eroare la deconectarea sesiunii web: {e}")
            return False
    
    def stop_all(self):
        """Oprește toate serviciile ALEPH."""
        logging.info("=" * 60)
        logging.info("OPRIRE COMPLETĂ SERVICII ALEPH")
        logging.info("=" * 60)
        logging.info(f"Data/Ora: {time.strftime('%d.%m.%Y %H:%M:%S')}")
        logging.info("=" * 60)
        
        results = {
            'catalog_exe': False,
            'browser_sessions': False,
            'web_logout': False
        }
        
        # 1. Oprește Catalog.exe
        logging.info("\n[1/3] Oprire Catalog.exe...")
        results['catalog_exe'] = self.stop_catalog_exe()
        time.sleep(1)
        
        # 2. Închide sesiunile browser
        logging.info("\n[2/3] Închidere sesiuni browser...")
        results['browser_sessions'] = self.close_browser_sessions()
        time.sleep(1)
        
        # 3. Deconectare sesiune web
        logging.info("\n[3/3] Deconectare sesiune web...")
        results['web_logout'] = self.logout_web_session()
        
        # Raport final
        logging.info("\n" + "=" * 60)
        logging.info("RAPORT FINAL")
        logging.info("=" * 60)
        logging.info(f"Catalog.exe oprit: {'✓ DA' if results['catalog_exe'] else '✗ NU'}")
        logging.info(f"Browsere închise: {'✓ DA' if results['browser_sessions'] else '✗ NU'}")
        logging.info(f"Sesiune web deconectată: {'✓ DA' if results['web_logout'] else '✗ NU'}")
        logging.info(f"Total procese oprite: {len(self.stopped_processes)}")
        logging.info(f"Total browsere închise: {len(self.closed_sessions)}")
        logging.info("=" * 60)
        
        return any(results.values())

def main():
    """Funcția principală."""
    print("=" * 60)
    print("OPRIRE SERVICII ALEPH")
    print("=" * 60)
    print()
    
    stopper = AlephServicesStopper()
    success = stopper.stop_all()
    
    print()
    if success:
        print("✓ Servicii ALEPH oprite cu succes!")
        print(f"  - Procese Catalog.exe oprite: {len(stopper.stopped_processes)}")
        print(f"  - Browsere închise: {len(stopper.closed_sessions)}")
    else:
        print("✗ Nu s-au găsit servicii ALEPH active")
    
    print()
    print("Vezi detalii în: stop_aleph_services.log")
    print("=" * 60)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())

