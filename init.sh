#!bash
# Swap working directory to local
cd "$(dirname "$0")"

# Build images
docker image build -t rdkit-app -f Dockerfile-rdkit .
docker image build -t rdkit-db -f Dockerfile-postgres .

# Initialize database
DOCKERDB=`docker run -d -p 54321:5432 --name chemstructdb rdkit-db`
docker exec $DOCKERDB bash custom/init_data.sh

docker run -d -p 8080:8080 --link csdb:db --name csapp rdkit-app python app/app.py
