from flask import Flask, render_template, request
from captcha import * 
from emmision import emmision_test

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        reg_num = request.form['reg_num']
        res = traffic_fine(reg_num)
        res = res.return_function()
        res["emmision"] = emmision_test(reg_num).extract_emmision_data()
        return res
    else:
        return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0") 