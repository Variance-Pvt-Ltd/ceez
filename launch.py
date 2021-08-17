import json

from flask import Flask, render_template, request, redirect

from bin.orders import Order

app = Flask(__name__)
orders = []
with open('usr/orders.json') as f:
    all = json.load(f)
f.close()


def unique(id):
    for x in all.keys():
        print(x)
        if all[x] == id:
            return False
    return True


@app.route("/")
def dashboard():
    with open('usr/orders.json') as f:
        all = json.load(f)
    f.close()
    for each in all:
        orders.append(all[each])
    return render_template('onept.html', list=orders, len=not (bool(len(orders))))


@app.route('/save', methods=['POST'])
def save():
    id = 0

    while not unique(id):
        id += 1
    if request.method == 'POST':
        symbol = request.form['symbol']
        type = request.form["type"]
        take_profit = request.form['take_profit']
        quantity = request.form["quantity"]
        order = Order(id, symbol, type, take_profit, quantity)
        with open('usr/orders.json') as f:
            orders = dict(json.load(f))
            f.close()
        return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):
    with open('usr/orders.json') as jn:
        j = dict(json.load(jn))
    jn.close()
    del j[str(id)]
    with open('usr/orders.json', 'w') as jn:
        json.dump(j, jn)
    jn.close()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
