#! bash
cd "$(dirname "$0")"
# if ! [ $(find "$search_dir" -name "$filename") ]; then
#   echo "$filename is found in $search_dir"
# else
#   echo "$filename not found"
# fi

mkdir -p data

apt-get update -y
apt-get install curl -y

curl http://downloads.emolecules.com/free/2018-03-01/version.smi.gz > data/version.smi.gz
curl ftp://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/chembl_23_postgresql.tar.gz > data/chembl_23_postgresql.tar.gz
# ACS moves the link for no apparent reason
# Just cache the file for the sake of simplicity
#curl https://pubs.acs.org/doi/suppl/10.1021/ci034243x/suppl_file/ci034243xsi20040112_053635.txt > data/ESOL.csv
