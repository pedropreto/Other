from flask import Flask, request, jsonify, render_template
from fontTools.misc.fixedTools import floatToFixed

app = Flask(__name__)

@app.route('/')
def form_page():
    return render_template("form.html")

@app.route('/area', methods=['POST'])
def calculate_area():
    width = request.form.get('width')
    height = request.form.get('height')

    # Validate
    if not width or not height:
        return render_template("result.html", error='Missing width or height')

    width = float(width)
    height = float(height)

    area = width * height

    return render_template("result.html",
        width=width,
       height=height,
        area=area
    )

if __name__ == '__main__':
    app.run(debug=True)