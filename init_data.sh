#!bash

apt-get update -y
apt-get install curl -y
curl http://downloads.emolecules.com/free/2018-03-01/version.smi.gz > version.smi.gz
curl ftp://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/chembl_23_postgresql.tar.gz > chembl_23_postgresql.tar.gz


createdb -U postgres emolecules
psql -U postgres -f build-sql/table_creates.sql emolecules
zcat version.smi.gz                            \
| sed '1d; s/\\/\\\\/g'                        \
| psql  -U postgres -f build-sql/stream.sql emolecules
psql -U postgres -f build-sql/feature_gen.sql emolecules
