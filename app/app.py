from flask import Flask, request, render_template, jsonify
import psycopg2
import os

app = Flask(__name__)
conn = psycopg2.connect(database='chemstruct',
                        user='postgres',
                        host=os.environ['DB_PORT_5432_TCP_ADDR'],
                        port=os.environ['DB_PORT_5432_TCP_PORT'],
                        )

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/closest', methods=['GET','POST'])
def closest():
    sql = '''
    WITH func AS (
        SELECT  molregno,m,similarity
        FROM    get_mfp2_neighbors(%s)
    )
    SELECT  md.pref_name,
            func.m,
            func.similarity
    FROM    func
        JOIN molecule_dictionary AS md
        ON   md.molregno=func.molregno
    LIMIT   30;
    '''
    cmp = 'Cc1ccc2nc(-c3ccc(NC(C4N(C(c5cccs5)=O)CCC4)=O)cc3)sc2c1'

    cur = conn.cursor()
    cur.execute(sql, (cmp,))
    results = []
    for row in cur:
        results += [{'name': row[0],
                     'smiles': row[1],
                     'similarity': row[2],
                  }]

    return render_template('closest.html', items = results)

@app.errorhandler(404)
def page_not_found(error):
    return 'There seems to have been a problem: ' + error

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
