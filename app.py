from flask import Flask, render_template, request, jsonify, session
import pandas as pd
import plotly.graph_objs as go
import plotly.utils
import json
import io
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 設置一個秘密鍵，用於session

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
                
                # 將DataFrame轉換為JSON並存儲在session中
                session['data'] = df.to_json()
                columns = df.columns.tolist()
                return render_template('chart.html', columns=columns)
            except Exception as e:
                return jsonify({'error': str(e)})
    return render_template('index.html')

@app.route('/plot', methods=['POST'])
def plot():
    try:
        data = request.json
        # 從session中獲取數據並轉換回DataFrame
        df = pd.read_json(session['data'])

        x_column = data['x_column']
        y_column = data['y_column']
        chart_type = data['chart_type']
        color = data['color']

        if chart_type == 'bar':
            fig = go.Figure(data=[go.Bar(x=df[x_column], y=df[y_column], marker_color=color)])
        elif chart_type == 'line':
            fig = go.Figure(data=[go.Scatter(x=df[x_column], y=df[y_column], mode='lines', line=dict(color=color))])
        elif chart_type == 'pie':
            fig = go.Figure(data=[go.Pie(labels=df[x_column], values=df[y_column], marker=dict(colors=[color]))])
        else:
            return jsonify({'error': 'Unsupported chart type'})

        fig.update_layout(title=f'{y_column} vs {x_column}')
        
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify(graphJSON)
    except Exception as e:
        return jsonify({'error': str(e)})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv', 'xls', 'xlsx'}

if __name__ == '__main__':
    app.run(debug=True)
