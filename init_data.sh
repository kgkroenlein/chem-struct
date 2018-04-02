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
| psql  -U postgres -d chemstruct -c           \
"COPY raw_data (smiles, emol_id, parent_id) FROM stdin WITH DELIMITER ' '"
tar -xzf chembl_23_postgresql.tar.gz
PATH_CACHE=`psql -U postgres -tc 'SHOW search_path'`
psql -U postgres -d chemstruct -c              \
"ALTER ROLE postgres SET search_path TO chembl;"
pg_restore --no-owner -U postgres -d chemstruct \
    chembl_23/chembl_23_postgresql/chembl_23_postgresql.dmp
psql -U postgres -d chemstruct -c              \
"ALTER ROLE postgres SET search_path TO $PATH_CACHE;"
psql -U postgres -f build-sql/feature_gen.sql -d chemstruct
