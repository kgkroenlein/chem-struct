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

curl http://downloads.emolecules.com/free/2018-03-01/version.smi.gz > data/version.smi.gz
curl ftp://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/chembl_23_postgresql.tar.gz > data/chembl_23_postgresql.tar.gz
curl http://deepchem.io.s3-website-us-west-1.amazonaws.com/datasets/delaney-processed.csv > data/delaney-processed.csv
curl http://deepchem.io.s3-website-us-west-1.amazonaws.com/datasets/SAMPL.csv > data/SAMPL.csv
curl http://deepchem.io.s3-website-us-west-1.amazonaws.com/datasets/Lipophilicity.csv > data/Lipophilicity.csv
