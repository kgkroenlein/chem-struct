#! bash
# Script for killing, rebuilding and restarting the web app

# Swap working directory to local
cd "$(dirname "$0")"

# Kill and remove old version
docker kill csapp
docker rm -v csapp

# Build image
docker image build -t rdkit-app -f Dockerfile-rdkit .

# Start app, with linking
docker run -d -p 8080:8080 --link csdb:db --name csapp rdkit-app python app/app.py
