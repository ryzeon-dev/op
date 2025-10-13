#!/bin/bash 

if [ "$(whoami)" != "root" ]; then
  echo "Execution requires root privilegies"
  exit 1
fi 

python3 -m venv venv
source venv/bin/activate
pip install pyinstaller
pyinstaller --onefile ./src/main.py --name op
deactivate

mkdir -p ./bin
cp ./dist/op ./bin/op
rm -rf ./dist ./build ./venv ./op.spec


cp ./bin/op /usr/local/bin
