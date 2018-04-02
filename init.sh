#!bash
# Build images
docker image build -t rdkit-app -f Dockerfile-rdkit .
docker image build -t rdkit-db -f Dockerfile-postgres .

# Initialize database
docker run -d -p 5432:5432 --name postgresdb rdkit-db
