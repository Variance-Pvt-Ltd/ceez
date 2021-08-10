# from bin._binance_ import Z_Binance
from flask import Flask, render_template

#binance = Z_Binance()
app = Flask(__name__)


@app.route("/")
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)
