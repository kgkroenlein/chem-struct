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
curl https://s3.amazonaws.com/chem-struct-data/kekule/algorithm.min.js > app/static/kekulealgorithm.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/calculation.min.js > app/static/kekulecalculation.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/chemWidget.min.js > app/static/kekulechemWidget.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/common.min.js > app/static/kekulecommon.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/core.min.js > app/static/kekulecore.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/data.min.js > app/static/kekuledata.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/emscripten.min.js > app/static/kekuleemscripten.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/extra > app/static/kekuleextra
curl https://s3.amazonaws.com/chem-struct-data/kekule/html.min.js > app/static/kekulehtml.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/inchi.min.js > app/static/kekuleinchi.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/indigo.min.js > app/static/kekuleindigo.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/io.min.js > app/static/kekuleio.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/kekule.js > app/static/kekulekekule.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/kekule.loaded.js > app/static/kekulekekule.loaded.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/kekule.min.js > app/static/kekulekekule.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/localization.min.js > app/static/kekulelocalization.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/localizationData.zh.min.js > app/static/kekulelocalizationData.zh.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/openbabel.min.js > app/static/kekuleopenbabel.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/package.json > app/static/kekulepackage.json
curl https://s3.amazonaws.com/chem-struct-data/kekule/render.min.js > app/static/kekulerender.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/root.min.js > app/static/kekuleroot.min.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes > app/static/kekulethemes
curl https://s3.amazonaws.com/chem-struct-data/kekule/widget.min.js > app/static/kekulewidget.min.js

mkdir -p app/static/kekule/extra
curl https://s3.amazonaws.com/chem-struct-data/kekule/extra/inchi.js > app/static/kekule/extrainchi.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/extra/indigo.js > app/static/kekule/extraindigo.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/extra/indigoAdapter.js > app/static/kekule/extraindigoAdapter.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/extra/openbabel.js > app/static/kekule/extraopenbabel.js
curl https://s3.amazonaws.com/chem-struct-data/kekule/extra/workers > app/static/kekule/extraworkers

mkdir -p app/static/kekule/extra/workers
curl https://s3.amazonaws.com/chem-struct-data/kekule/extra/workers/kekule.worker.obStructure3DGenerator.js > app/static/kekule/extra/workerskekule.worker.obStructure3DGenerator.js

mkdir -p app/static/kekule/themes
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default > app/static/kekule/themesdefault

mkdir -p app/static/kekule/themes/default
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/chemWidget.css > app/static/kekule/themes/defaultchemWidget.css
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/chemWidgetColor.css > app/static/kekule/themes/defaultchemWidgetColor.css
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/default.css > app/static/kekule/themes/defaultdefault.css
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/defaultColor.css > app/static/kekule/themes/defaultdefaultColor.css
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/images > app/static/kekule/themes/defaultimages
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/kekule.css > app/static/kekule/themes/defaultkekule.css
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/sprite > app/static/kekule/themes/defaultsprite

mkdir -p app/static/kekule/themes/default/images
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/images/cursors > app/static/kekule/themes/default/imagescursors

mkdir -p app/static/kekule/themes/default/images/cursors
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/images/cursors/rotate.cur > app/static/kekule/themes/default/images/cursorsrotate.cur
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/images/cursors/rotate.png > app/static/kekule/themes/default/images/cursorsrotate.png
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/images/cursors/rotateNE.cur > app/static/kekule/themes/default/images/cursorsrotateNE.cur
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/images/cursors/rotateNE.png > app/static/kekule/themes/default/images/cursorsrotateNE.png
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/images/cursors/rotateNW.cur > app/static/kekule/themes/default/images/cursorsrotateNW.cur
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/images/cursors/rotateNW.png > app/static/kekule/themes/default/images/cursorsrotateNW.png
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/images/cursors/rotateSE.cur > app/static/kekule/themes/default/images/cursorsrotateSE.cur
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/images/cursors/rotateSE.png > app/static/kekule/themes/default/images/cursorsrotateSE.png
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/images/cursors/rotateSW.cur > app/static/kekule/themes/default/images/cursorsrotateSW.cur
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/images/cursors/rotateSW.png > app/static/kekule/themes/default/images/cursorsrotateSW.png

mkdir -p app/static/kekule/themes/default/sprite
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/sprite/chemWidgetColor.png > app/static/kekule/themes/default/spritechemWidgetColor.png
curl https://s3.amazonaws.com/chem-struct-data/kekule/themes/default/sprite/defaultColor.png > app/static/kekule/themes/default/spritedefaultColor.png
