from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import pandas as pd
import plotly.graph_objs as go


app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
# app.secret_key = 'abc123'

@app.route('/', methods=['GET', 'POST'])
def test_post():
    if request.method == "POST":
        if "excel_file" in request.files:
            file = request.files["excel_file"]
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
    else:
        return render_template("index_for_post.html")
    
@app.route('/plot', methods=['POST'])
def plot():
    x = request.form["line_x"]
    y = request.form["line_y"]
    df = pd.DataFrame.from_dict(session['data'])
    x_data = df[x]
    y_data = df[y]
    
    # Create plotly figure
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=x_data, y=y_data, mode='lines+markers')
        )
    
    # Customize layout if needed
    fig.update_layout(
        title=f'{y} vs {x}',
        xaxis_title=x,
        yaxis_title=y
    )
    
    fig.write_html('templates/xy_chart.html')
    return render_template("xy_chart.html")
    
    # return jsonify({"x": x_data.tolist(), "y": y_data.tolist()})
    
if __name__ == '__main__':
    app.run(debug=True)
