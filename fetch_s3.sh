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
mkdir -p app/static/kekule
curl https://s3.amazonaws.com/chem-struct-data/kekule/algorithm.min.js > app/static/kekule/algorithm.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/calculation.min.js > app/static/kekule/calculation.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/chemWidget.min.js > app/static/kekule/chemWidget.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/common.min.js > app/static/kekule/common.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/core.min.js > app/static/kekule/core.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/data.min.js > app/static/kekule/data.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/emscripten.min.js > app/static/kekule/emscripten.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/html.min.js > app/static/kekule/html.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/inchi.min.js > app/static/kekule/inchi.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/indigo.min.js > app/static/kekule/indigo.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/io.min.js > app/static/kekule/io.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/kekule.js > app/static/kekule/kekule.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/kekule.loaded.js > app/static/kekule/kekule.loaded.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/kekule.min.js > app/static/kekule/kekule.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/localization.min.js > app/static/kekule/localization.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/localizationData.zh.min.js > app/static/kekule/localizationData.zh.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/openbabel.min.js > app/static/kekule/openbabel.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/package.json > app/static/kekule/package.json
curl https://s3.amazonaws.com/chem-struct-data/kekule/render.min.js > app/static/kekule/render.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/root.min.js > app/static/kekule/root.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/widget.min.js > app/static/kekule/widget.min.js

mkdir -p app/static/kekule/extra
curl https://s3.amazonaws.com/chem-struct-data/kekule/extra/inchi.js > app/static/kekule/extra/inchi.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/extra/indigo.js > app/static/kekule/extra/indigo.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/extra/indigoAdapter.js > app/static/kekule/extra/indigoAdapter.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/extra/openbabel.js > app/static/kekule/extra/openbabel.js

mkdir -p app/static/kekule/extra/workers
curl https://s3.amazonaws.com/chem-struct-data/kekule/extra/workers/kekule.worker.obStructure3DGenerator.js > app/static/kekule/extra/workers/kekule.worker.obStructure3DGenerator.js

mkdir -p app/static/kekule/themes/default
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/chemWidget.css > app/static/kekule/themes/default/chemWidget.css
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/chemWidgetColor.css > app/static/kekule/themes/default/chemWidgetColor.css
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/default.css > app/static/kekule/themes/default/default.css
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/defaultColor.css > app/static/kekule/themes/default/defaultColor.css
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/kekule.css > app/static/kekule/themes/default/kekule.css

mkdir -p app/static/kekule/themes/default/images/cursors
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/images/cursors/rotate.cur > app/static/kekule/themes/default/images/cursors/rotate.cur
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/images/cursors/rotate.png > app/static/kekule/themes/default/images/cursors/rotate.png
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/images/cursors/rotateNE.cur > app/static/kekule/themes/default/images/cursors/rotateNE.cur
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/images/cursors/rotateNE.png > app/static/kekule/themes/default/images/cursors/rotateNE.png
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/images/cursors/rotateNW.cur > app/static/kekule/themes/default/images/cursors/rotateNW.cur
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/images/cursors/rotateNW.png > app/static/kekule/themes/default/images/cursors/rotateNW.png
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/images/cursors/rotateSE.cur > app/static/kekule/themes/default/images/cursors/rotateSE.cur
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/images/cursors/rotateSE.png > app/static/kekule/themes/default/images/cursors/rotateSE.png
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/images/cursors/rotateSW.cur > app/static/kekule/themes/default/images/cursors/rotateSW.cur
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/images/cursors/rotateSW.png > app/static/kekule/themes/default/images/cursors/rotateSW.png

mkdir -p app/static/kekule/themes/default/sprite
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/sprite/chemWidgetColor.png > app/static/kekule/themes/default/sprite/chemWidgetColor.png
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/sprite/defaultColor.png > app/static/kekule/themes/default/sprite/defaultColor.png
