#!/bin/bash

# Entferne mögliche Lock-Datei
if [ -f .git/index.lock ]; then
    echo "Entferne alte Lock-Datei ..."
    rm .git/index.lock
fi

# Füge alle Änderungen dem Git-Index hinzu
echo "Füge Dateien hinzu ..."
git add .

# Commit mit automatisch generierter Nachricht inkl. Zeitstempel
echo "Committe Änderungen ..."
git commit -m "Automatisierter Commit am $(date +'%Y-%m-%d %H:%M:%S')"

# Optionaler Push
echo -n "Möchtest du pushen? (y/n): "
read answer
if [ "$answer" == "y" ]; then
    echo "Pushe zum Remote-Repository ..."
    git push
else
    echo "Push übersprungen."
fi

echo "Fertig!"
