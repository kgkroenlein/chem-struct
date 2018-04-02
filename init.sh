#!bash
# Build images
docker image build -t rdkit-app -f Dockerfile-rdkit .
docker image build -t rdkit-db -f Dockerfile-postgres .

# Initialize database
DOCKERDB=`docker run -d -p 54321:5432 --name chemstructdb rdkit-db`
docker exec -it $DOCKERDB bash custom/init_data.sh
