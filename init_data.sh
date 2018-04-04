#!bash
cd "$(dirname "$0")"

# There was a race condition condition around database start-up
while [ -z `which pg_isready` ]; do sleep 1; done
while [ true ]; do
  echo 'Polling database...';
  pg_isready -q;
  PG_STATUS=$?;
  sleep 1;
  if [ "$PG_STATUS" == 0 ]; then
    echo 'Ready';
    break;
  fi
  echo $PG_STATUS;
done
#pg_isready -q
#while [ $? != 0 ]; do pg_isready -q; sleep 1; done
#pg_isready
sleep 1

createdb -U postgres chemstruct
psql -U postgres -f build-sql/table_creates.sql -d chemstruct
zcat data/version.smi.gz                       \
| sed '1d; s/\\/\\\\/g'                        \
| psql  -U postgres -d chemstruct -c           \
"COPY raw_data (smiles, emol_id, parent_id) FROM stdin WITH DELIMITER ' '"
tar -xzf data/chembl_23_postgresql.tar.gz
PATH_CACHE=`psql -U postgres -tc 'SHOW search_path'`
psql -U postgres -d chemstruct -c              \
"ALTER ROLE postgres SET search_path TO chembl;"
pg_restore --no-owner -U postgres -d chemstruct \
    data/chembl_23/chembl_23_postgresql/chembl_23_postgresql.dmp
psql -U postgres -d chemstruct -c              \
"ALTER ROLE postgres SET search_path TO $PATH_CACHE;"
psql -U postgres -f build-sql/feature_gen.sql -d chemstruct
