from flask import Flask, request, render_template, jsonify, abort
import psycopg2
import os
import lipo_model
from rdkit import Chem
from rdkit.Chem import AllChem

'''
Initialize singleton global variables: App container and database connection
'''
app = Flask(__name__)
conn = psycopg2.connect(database='chemstruct',
                        user='postgres',
                        host=os.environ['DB_PORT_5432_TCP_ADDR'],
                        port=os.environ['DB_PORT_5432_TCP_PORT'],
                        )

@app.route('/', methods=['GET'])
def index():
    '''
    Return landing page
    '''
    return render_template('index.html')

@app.route('/closest', methods=['GET','POST'])
def closest():
    '''
    Returns a tabulated list of closest neighbors

    Input, from cmp_search form
    smiles {str}: What SMILES to compare with; default is:
                    'Cc1ccc2nc(-c3ccc(NC(C4N(C(c5cccs5)=O)CCC4)=O)cc3)sc2c1'
    '''
    if 'smiles' in request.form:
        smiles = str(request.form['smiles'])
    else:
        smiles = 'Cc1ccc2nc(-c3ccc(NC(C4N(C(c5cccs5)=O)CCC4)=O)cc3)sc2c1'

    sql = '''
    SELECT  md.pref_name,
            func.m,
            func.similarity
    FROM    get_mfp2_neighbors(%s) AS func
        JOIN molecule_dictionary AS md
        ON   md.molregno=func.molregno
    LIMIT   30;
    '''

    cur = conn.cursor()
    cur.execute(sql, (smiles,))
    results = []
    for row in cur:
        results += [{'name': row[0],
                     'smiles': row[1],
                     'similarity': row[2],
                  }]

    return render_template('closest.html', items = results, smiles=smiles)

@app.route('/predict', methods=['POST'])
def predict():
    '''
    Returns a tabulated list of closest neighbors

    Input, from composer widget on index page (thus required post)
    smiles {str}: What SMILES to compare with; default is:
                    'Cc1ccc2nc(-c3ccc(NC(C4N(C(c5cccs5)=O)CCC4)=O)cc3)sc2c1'
    '''
    if 'mol' not in request.form:
        abort(404, description="Required parameter is missing")

    ctab = str(request.form['mol'])

    try: # Try structural optimization
        mol = Chem.MolFromMolBlock(ctab)
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol,AllChem.ETKDG())
        mol = Chem.RemoveHs(mol)
        ctab = Chem.MolToMolBlock(mol)
    except:
        pass # Swallow the failure

    pred, exp = lipo_model.predict(ctab)
    results = [{'link': 'https://en.wikipedia.org/wiki/Lipophilicity',
                'cat': 'Lipophilicity', 'pred': pred, 'exp': exp, },
                ]
    return render_template('predict.html', mol=ctab, items = results)

@app.errorhandler(404)
def page_not_found(error):
    '''
    Error handler; presently untested and stub
    '''
    return 'There seems to have been a problem: ' + error

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
