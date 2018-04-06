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
done
sleep 1

createdb -U postgres chemstruct
psql -U postgres -f build-sql/table_creates.sql -d chemstruct

zcat data/version.smi.gz                                                       \
    | sed '1d; s/\\/\\\\/g'                                                    \
    | psql -U postgres -d chemstruct -c                                        \
    "COPY raw_data (smiles, emol_id, parent_id) FROM stdin WITH DELIMITER ' '"

psql -U postgres -d chemstruct -c                                              \
    "COPY solubility FROM stdin WITH DELIMITER ',' csv header"                 \
    < data/delaney-processed.csv

psql -U postgres -d chemstruct -c                                              \
    "COPY lipophilicity FROM stdin WITH DELIMITER ',' csv header"                 \
    < data/Lipophilicity.csv

tar -xzf data/chembl_23_postgresql.tar.gz --directory=data
PATH_CACHE=`psql -U postgres -tc 'SHOW search_path'`
psql -U postgres -d chemstruct -c                                              \
    "ALTER ROLE postgres SET search_path TO chembl;"
pg_restore --no-owner -U postgres -d chemstruct                                \
    data/chembl_23/chembl_23_postgresql/chembl_23_postgresql.dmp
# Import happens into public space for some unclear reason
psql -U postgres -d chemstruct -c                                              \
    "ALTER ROLE postgres SET search_path TO public;"
for TABLE in $( psql -U postgres -d chemstruct -tc "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';" ); do
    psql -U postgres -d chemstruct -c "ALTER TABLE $TABLE SET SCHEMA chembl;"
done
psql -U postgres -d chemstruct -c                                              \
    "ALTER ROLE postgres SET search_path TO $PATH_CACHE;"

psql -U postgres -f build-sql/feature_gen.sql -d chemstruct
