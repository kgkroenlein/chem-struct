from flask import Flask, request, render_template, jsonify, abort
import psycopg2
import os
import lipo_model
from rdkit import Chem
from rdkit.Chem import AllChem
from collections import OrderedDict
from util import aws_context_db

'''
Initialize singleton global variables: App container and database connection
'''
app = Flask(__name__)

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
    n = 10

    conn = aws_context_db()

    base_cur = conn.cursor()
    if request.method == 'GET':
        if 'regno' not in request.args:
            abort(404, description="Required parameter is missing")

        regno = str(request.args['regno'])
        sql = '''
        SELECT  molfile
        FROM    compound_structures
        WHERE   molregno = %s
        '''

        base_cur.execute(sql, (regno,))
        mol   = None
        for (molfile,) in base_cur:
            mol = molfile

    else:
        if 'mol' not in request.form:
            abort(404, description="Required parameter is missing")

        mol = str(request.form['mol'])
        regno = None

    if not mol:
        abort(500, description="Server failed to identify a structure")

    search_cmp = {'molfile' : mol, 'regno' : regno}

    default_tol_sql = 'SET rdkit.tanimoto_threshold TO DEFAULT;'
    tol_sql = 'SET rdkit.tanimoto_threshold TO %s'

    # Prepare statment is necessary because a normal psycopg2 placeholder gets
    # confused by all the percents, I think
    neighbor_sql_tmpl = '''
    PREPARE neighbor_plan AS
    SELECT  fps.molregno AS molregno,
            tanimoto_sml(target, fps.{}) AS similarity,
            compound_structures.molfile AS molfile
    FROM    rdk.fps,
            compound_structures,
            {}(mol_from_ctab($1)) AS target
    WHERE   target%fps.{}
      AND   fps.molregno = compound_structures.molregno
    ORDER BY target<%>fps.{}
    LIMIT   {}
    '''

    fp_methods = {
        'mfp2': 'morganbv_fp',
        'ffp2': 'featmorganbv_fp',
        'rdkitbv': 'rdkit_fp',
        'atompair': 'atompairbv_fp',
        'torsionbv': 'torsionbv_fp',
        'maccs': 'maccs_fp',
    }
    fp_names = ('mfp2', 'ffp2', 'rdkitbv', 'atompair', 'torsionbv', 'maccs')

    rows = [{'n':i+1} for i in range(n)]
    for fp_name in fp_names:
        tol = 0.5
        neighbor_sql = neighbor_sql_tmpl.format( fp_name,
                            fp_methods[fp_name], fp_name, fp_name, n )
        base_cur.execute(neighbor_sql)

        success = False
        for _ in range(10):
            n_cur = conn.cursor()
            n_cur.execute('EXECUTE neighbor_plan (%s)', (mol,))
            for i, (n_id, similarity, molfile) in enumerate(n_cur):
                rows[i][fp_name] = {'regno':n_id,
                                    'similarity':similarity,
                                    'molfile':molfile
                                    }

            # Did we get enough?
            if fp_name in rows[-1]:
                success = True
                break

            # Lower the threshold and try again
            tol /= 2
            base_cur.execute(tol_sql, (tol,))

        # Reset tolerance if it changed
        if not success:
            abort(500, description="Failed to identify neighbors")

        if tol != 0.5:
            tol = 0.5
            base_cur.execute(default_tol_sql)

        base_cur.execute('DEALLOCATE neighbor_plan')

    fp_display = {
        'mfp2': 'Morgan',
        'ffp2': 'Morgan-Feature',
        'rdkitbv': 'Daylight',
        'atompair': 'Atom Pair',
        'torsionbv': 'Torsion',
        'maccs': 'MACCS',
    }
    fp_url = dict()
    fp_meta = []
    for fp_name in fp_names:
        this = dict()
        this['name'] = fp_name
        this['display'] = fp_display[fp_name]
        if fp_name in fp_url:
            this['url'] = fp_url[fp_name]
        fp_meta += [this]

    return render_template('closest.html', rows = rows, main=search_cmp, fps = fp_meta)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    '''
    Returns a tabulated list of closest neighbors

    Input, from composer widget on index page (thus required post)
    smiles {str}: What SMILES to compare with; default is:
                    'Cc1ccc2nc(-c3ccc(NC(C4N(C(c5cccs5)=O)CCC4)=O)cc3)sc2c1'
    '''

    conn = aws_context_db()

    base_cur = conn.cursor()
    if request.method == 'GET':
        if 'regno' not in request.args:
            abort(404, description="Required parameter is missing")

        regno = str(request.args['regno'])
        sql = '''
        SELECT  molfile
        FROM    compound_structures
        WHERE   molregno = %s
        '''

        base_cur.execute(sql, (regno,))
        ctab = None
        for (molfile,) in base_cur:
            ctab = molfile

    else:
        if 'mol' not in request.form:
            abort(404, description="Required parameter is missing")

        ctab = str(request.form['mol'])
        regno = None

        try: # Try structural optimization
            mol = Chem.MolFromMolBlock(ctab)
            mol = Chem.AddHs(mol)
            AllChem.EmbedMolecule(mol,AllChem.ETKDG())
            mol = Chem.RemoveHs(mol)
            ctab = Chem.MolToMolBlock(mol)
        except:
            pass # Swallow the failure

    if not ctab:
        abort(500, description="Server failed to identify a structure")

    pred, exp = lipo_model.predict(ctab)
    results = [{'link': 'https://en.wikipedia.org/wiki/Lipophilicity',
                'cat': 'Lipophilicity', 'pred': pred, 'exp': exp },
                ]
    for res in results:
        if res['pred']:
            res['pred'] = '{:0.4g}'.format(res['pred'])
        if res['exp']:
            res['exp'] = '{:0.4g}'.format(res['exp'])
    return render_template('predict.html', mol = ctab, items = results,
                            regno = regno
                            )

@app.errorhandler(404)
def page_not_found(error):
    '''
    Error handler; presently untested and stub
    '''
    return 'There seems to have been a problem: ' + str(error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
