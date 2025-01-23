from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import pandas as pd
import plotly.graph_objs as go
import json
import plotly.utils


app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
# app.secret_key = 'abc123'

@app.route('/', methods=['GET', 'POST'])
def test_post():
    if request.method == "POST":
        if "file" in request.files:
            file = request.files["file"]
            if file.filename == "":
                return jsonify({"Error": "No file selected"})
            elif file.filename[-5:] == ".xlsx":
                df = pd.read_excel(file)
            elif file.filename.endswith(".csv"):
                df = pd.read_csv(file)
            else:
                return jsonify({"Error": "Invalid file format"})
            
            session['data'] = df.to_dict()
            columns = df.columns.tolist()
            return render_template("for_chart.html", columns=columns)
        return jsonify({"Error": "No file part"})  # Add this line
    else:
        return render_template("index_test.html")
    
@app.route('/plot', methods=['POST'])
def plot():
    data = request.json
    df = pd.DataFrame.from_dict(session['data'])
    
    # data = {
    #     lines: [
    #         {x_column: "freq", y_column: "s21", color: "#0000FF"},
    #         {x_column: "freq", y_column: "s21", color: "#0000FF"},
    #     ]
    #     chart_type: 'line' 
    # }
    
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
        
    fig = go.Figure(traces)
    fig.update_layout(
        title='Multiple Lines Chart',
        # height=800,
        autosize=True
    )
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return jsonify(graphJSON)
    
    
    
if __name__ == '__main__':
    app.run(debug=True)
