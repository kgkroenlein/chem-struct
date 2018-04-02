#!bash
cd "$(dirname "$0")"

apt-get update -y
apt-get install curl -y
curl http://downloads.emolecules.com/free/2018-03-01/version.smi.gz > version.smi.gz
curl ftp://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/chembl_23_postgresql.tar.gz > chembl_23_postgresql.tar.gz

createdb -U postgres chemstruct
psql -U postgres -f build-sql/table_creates.sql -d chemstruct
zcat version.smi.gz                            \
| sed '1d; s/\\/\\\\/g'                        \
| psql  -U postgres -f build-sql/stream.sql -d chemstruct
psql -U postgres -f build-sql/feature_gen.sql -d chemstruct
