#!/bin/bash

python3 -m venv .venv
source .venv/bin/activate

pip3 install -r requirements.txt

touch .env

echo "SPOTIFY_CLIENT_ID=        
SPOTIFY_CLIENT_SECRET=            
DB_URL=" >> .env
