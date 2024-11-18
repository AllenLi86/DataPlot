from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import pandas as pd
import plotly.graph_objs as go
import plotly.utils
import json
import io
import os

app = Flask(__name__)

# Configure server-side session storage
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        if file and allowed_file(file.filename):
            try:
                if file.filename.endswith('.csv'):
                    df = pd.read_csv(file)
                elif file.filename.endswith(('.xls', '.xlsx')):
                    df = pd.read_excel(file)
                else:
                    return jsonify({'error': 'Unsupported file format'})
                
                # Store DataFrame in server-side session
                session['data'] = df.to_dict()
                columns = df.columns.tolist()
                return render_template('chart.html', columns=columns)
            except Exception as e:
                return jsonify({'error': str(e)})
    return render_template('index.html')

@app.route('/plot', methods=['POST'])
def plot():
    try:
        data = request.json
        df = pd.DataFrame.from_dict(session['data'])
        
        traces = []
        for line in data['lines']:
            trace = go.Scatter(
                x=df[line['x_column']], 
                y=df[line['y_column']], 
                mode='lines+markers',
                name=f"{line['y_column']} vs {line['x_column']}",
                line=dict(color=line['color'])
            )
            traces.append(trace)
            
        fig = go.Figure(data=traces)
        fig.update_layout(
            title='Multiple Lines Chart',
            height=800,
            autosize=True
        )
        
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify(graphJSON)
    except Exception as e:
        return jsonify({'error': str(e)})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv', 'xls', 'xlsx'}

if __name__ == '__main__':
    app.run(debug=True)
