#! bash
cd "$(dirname "$0")"
# if ! [ $(find "$search_dir" -name "$filename") ]; then
#   echo "$filename is found in $search_dir"
# else
#   echo "$filename not found"
# fi

mkdir -p data
mkdir -p app/static

# apt-get update -y
# apt-get install curl -y
sudo yum update -y
sudo yum install curl -y

curl http://downloads.emolecules.com/free/2018-03-01/version.smi.gz > data/version.smi.gz
curl ftp://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/chembl_23_postgresql.tar.gz > data/chembl_23_postgresql.tar.gz
curl http://deepchem.io.s3-website-us-west-1.amazonaws.com/datasets/delaney-processed.csv > data/delaney-processed.csv
# curl http://deepchem.io.s3-website-us-west-1.amazonaws.com/datasets/SAMPL.csv > data/SAMPL.csv
curl http://deepchem.io.s3-website-us-west-1.amazonaws.com/datasets/Lipophilicity.csv > data/Lipophilicity.csv

curl http://partridgejiang.github.io/Kekule.js/download/files/kekule.js.zip > app/static/kekule.js.zip
curl https://raw.githubusercontent.com/DmitryBaranovskiy/raphael/master/raphael.min.js > app/static/raphael.min.js
curl https://threejs.org/build/three.min.js > three.js.zip

cd app/static/
unzip kekule.js.zip
cd "$(dirname "$0")"
