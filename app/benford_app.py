#!/usr/bin/env python3

import os
import pathlib
import pandas as pd
from werkzeug.utils import secure_filename
from helpers import allowed_file, chisquare_plot
from flask import Flask, request, redirect, render_template

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(pathlib.Path(__file__).parent.resolve(),'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET','POST'])
@app.route('/index.html')
def index():
    return render_template('index.html', the_title='Benford\'s Law')


@app.route('/calculate.html', methods=['GET','POST'])
def calculate():
    
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template(
                'user_error.html',
                the_title='No File Uploaded',
                data='It appears no file was uploaded. Please attach a file.'
                )

        file = request.files['file']
        input_column = request.form['data_column']
        
        if file and not allowed_file(file.filename):
            return render_template(
                'user_error.html',
                the_title='File Type Error',
                data='Please use .tsv, .txt, or .csv file types'
                )
        
        elif not input_column or file.filename == '':
            return render_template(
                'user_error.html',
                the_title='Empty Form',
                data='Please ensure your data column is specified and filename is not empty string'
                )

        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_loc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_loc)
            file_ext = filename.split('.')[-1]
            septate = ',' if file_ext == 'csv' else '\t'
            
            import_file = pd.read_csv(file_loc, sep=septate).dropna()
            data_column = int(request.form['data_column'])-1 if int(request.form['data_column']) != 0 else 1
            
            if len(import_file.columns) < data_column+1:
                return render_template(
                    'user_error.html',
                    the_title='Column Index Error',
                    data='Check your column index. You may have specified too large an index'
                    )
                
            init_data = import_file.iloc[:,[data_column]]

            [graph_json, benford_fit, test_statistic, p_value] = chisquare_plot(init_data)
            
            if not test_statistic and not p_value:
                return render_template('chisquerror.html', the_title='Error with Dataset')
            
            calc_template = render_template(
                'benford_graph.html',               
                the_title='Your Results',           # Sends all calculated info to graph page
                graphJSON=graph_json,               # Graph data as JSON
                benford_fit=benford_fit,            # Boolean whether data fit Benford's law (p > 0.05)
                pvalue=p_value,                     # Testing null: are the submitted data and the  
                teststat=test_statistic,            # expected benford data from the same population?
                )
            return calc_template

    else:
        return render_template('/calculate.html', the_title='Calculating Fit to Benford\'s law')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)