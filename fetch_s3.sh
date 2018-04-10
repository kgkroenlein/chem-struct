#! bash
cd "$(dirname "$0")"
# if ! [ $(find "$search_dir" -name "$filename") ]; then
#   echo "$filename is found in $search_dir"
# else
#   echo "$filename not found"
# fi

mkdir -p data

# apt-get update -y
# apt-get install curl -y
sudo yum update -y
sudo yum install curl -y

curl https://s3.amazonaws.com/chem-struct-data/version.smi.gz > data/version.smi.gz
curl https://s3.amazonaws.com/chem-struct-data/chembl_23_postgresql.tar.gz > data/chembl_23_postgresql.tar.gz
curl https://s3.amazonaws.com/chem-struct-data/delaney-processed.csv > data/delaney-processed.csv
curl https://s3.amazonaws.com/chem-struct-data/Lipophilicity.csv > data/Lipophilicity.csv

# Pull in kekule libraries
mkdir -p app/static
curl https://s3.amazonaws.com/chem-struct-data/kekule.zip > app/static/kekule.zip
curl https://s3.amazonaws.com/chem-struct-data/raphael-min.2.0.1.js > app/static/raphael-min.2.0.1.js
curl https://s3.amazonaws.com/chem-struct-data/Three.js > app/static/Three.js

cd app/static/
unzip kekule.zip
cd "$(dirname "$0")"
