#!/usr/bin/env python3
"""
Narion CoSD Framework - System Health Check
"""

import os
import sys
import subprocess

def check_python_version():
    """Python Version prüfen"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print("✅ Python Version: {}.{}.{}".format(version.major, version.minor, version.micro))
        return True
    else:
        print("❌ Python Version zu alt. Benötigt: 3.7+")
        return False

def check_packages():
    """Python-Pakete prüfen"""
    required = ['matplotlib', 'numpy', 'yaml', 'networkx']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package} installiert")
        except ImportError:
            print(f"❌ {package} fehlt")
            missing.append(package)
            
    return len(missing) == 0

def check_directories():
    """Verzeichnisstruktur prüfen"""
    dirs = ['analyzer', 'SKK', 'MIND', 'markers']
    all_present = True
    
    for d in dirs:
        if os.path.exists(d):
            print(f"✅ Verzeichnis {d}/ vorhanden")
        else:
            print(f"❌ Verzeichnis {d}/ fehlt")
            all_present = False
            
    return all_present

def check_files():
    """Wichtige Dateien prüfen"""
    files = [
        'analyzer/enhanced_drift_analyzer_v5.py',
        'SKK/skk_analyzer_standalone.py',
        'MIND/tools/mind_health_check.py',
        'start_narion.sh'
    ]
    
    all_present = True
    for f in files:
        if os.path.exists(f):
            print(f"✅ {f}")
        else:
            print(f"❌ {f} fehlt")
            all_present = False
            
    return all_present

def main():
    print("🏥 Narion CoSD Framework - System Health Check")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Python Pakete", check_packages),
        ("Verzeichnisse", check_directories),
        ("Dateien", check_files)
    ]
    
    all_ok = True
    for name, check_func in checks:
        print(f"\n{name}:")
        if not check_func():
            all_ok = False
            
    print("\n" + "=" * 50)
    if all_ok:
        print("✅ System vollständig funktionsfähig!")
    else:
        print("⚠️  Probleme gefunden. Bitte fehlende Komponenten installieren.")
        
if __name__ == "__main__":
    main()
