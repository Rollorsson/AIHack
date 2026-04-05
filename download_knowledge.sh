#!/bin/bash
set -e

cd "$(dirname "$0")"
mkdir -p rag/ingest/sources
cd rag/ingest/sources

echo "📥 Descargando base de conocimiento para RAG..."

git clone --depth=1 https://github.com/swisskyrepo/PayloadsAllTheThings.git PayloadsAllTheThings
echo "✅ PayloadsAllTheThings"

git clone --depth=1 https://github.com/HackTricks-wiki/hacktricks.git HackTricks
echo "✅ HackTricks"

git clone --depth=1 https://github.com/csb21jb/Pentesting-Notes.git OSCP-Notes
echo "✅ OSCP Notes"

git clone --depth=1 https://github.com/SrivathsanNayak/ethical-hacking-notes.git CTF-Notes
echo "✅ CTF Notes"

git clone --depth=1 https://github.com/GTFOBins/GTFOBins.github.io.git GTFOBins
echo "✅ GTFOBins"

git clone --depth=1 https://github.com/shiahalan/Ethical-Hacking-Cheat-Sheet.git Cheatsheets
echo "✅ Cheatsheets"

echo "\n🧠 Base de conocimiento lista. Ahora corré python3 rag/ingest/ingest.py"
