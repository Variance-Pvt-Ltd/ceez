import json, os
from threading import Thread
from bin.bot import Bot
from subprocess import Popen
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
with open('usr/credentials.json') as f: 
    creds = json.load(f) 
    f.close() 

with open('usr/settings.json') as f: 
    settings = json.load(f) 
    f.close() 

with open('usr/alert.json') as f: 
    alert = json.load(f) 
    f.close() 

# Creating bot instance 
Bot1 = Bot(creds=creds, settings=settings) 
#Bot started in thread 

print("seeeeeeeeeeeeee") 

def take_response(): 
    if input() == '': 
        try:
            with open('usr/settings.json') as f: 
                settings = json.load(f) 
                f.close() 
            Bot1.update_attributes(settings=settings) 
            print("\n\tParameters updated!!\t\n") 
            #take_response()
        except: 
            print('Invalid inputs, check the settings.json') 
            take_response() 
    else:
        print('Enter valid input')
        take_response()


def unique(id):
    with open('usr/settings.json') as f:
        all = json.load(f)["take_profits"]
    f.close()
    for x in all.keys():
        print(all[x])
        if x == str(id):
            print(all)
            return False
    return True

@app.route("/")
def iniit():
    return render_template('init.html')

@app.route("/end")
def end():
    if Bot1.state:
        Bot1.stop()
    return render_template('init.html')

@app.route('/webhook', methods = ['POST'])
def Alert():
    #fetching data from webhook url
    if request.method == 'POST':
        try:
            data = json.loads(request.data.decode('utf-8'))
            print(data)
            global alert

            if (alert['passcode']==data['passcode']):
                alert=data

                if bool(settings['auto_trade']):
                    Bot1.read_alert(alert)
                    print('alert sent') 
                else: 
                    print('Alert received from webhoook please update settings.\n') 
                    val = input("Do you want to take this trade(y/n): ")
                    if val in ['y','Y']:
                        val = input("Do you want to update settings(y/n): ")
                        if val in ['y','Y']:
                            Popen('python run.py')
                        else:
                            pass 
                        take_response()
                        Bot1.read_alert(alert)   
                        print('alert sent')  
                    else:
                        print('You cancelled this trade.\n')

            else :
                print("error") 
            return data 
        except Exception as e:
            print(e)

@app.route("/dashboard")
def dashboard():
    with open('usr/settings.json') as f:
        settings = json.load(f)
        all = settings['take_profits']
    f.close()
    return render_template('dashboard.html', list=all, length=len(all), s=settings, len=not(bool(len(all))))

@app.route('/start', methods=['POST'])
def start():
    if request.method == 'POST':
        
        with open('usr/credentials.json') as f:
            c=json.load(f)
            f.close()
        c['api_key']=request.form['api_key']
        c['api_secret']=request.form['api_secret']
        c['tld']=request.form['tld']
        with open('usr/credentials.json', 'w') as f:
            json.dump(c,f)
            f.close()

    # from bin import app
    return redirect('/dashboard')
    

@app.route('/save', methods=['POST'])
def save():
    if request.method == 'POST':
        take_profit = request.form['take_profit']
        with open('usr/settings.json') as f:
            orders = dict(json.load(f))
            tf=orders['take_profits'] # list
            f.close()
        tf.append(float(take_profit))
        with open('usr/settings.json', 'w') as f:
            json.dump(orders,f)
            f.close()
    return redirect('/dashboard')


@app.route('/dashboard/delete/<int:i>',methods=['GET','POST'])
def delete(i):
    with open('usr/settings.json') as jn:
        j=dict(json.load(jn))
        tf = j['take_profits']
    jn.close()
    del tf[i]
    with open('usr/settings.json', 'w') as jn:
        json.dump(j, jn)
    jn.close()
    return redirect('/dashboard')

def run_bot(s):
    print('major')
    if Bot1.state:
        Bot1.update_attributes(s)
    else:
        Bot1.update_attributes(s)
        Bot1.run()

@app.route('/dashboard/update', methods=['POST','GET'])
def update():
    print('updating settings')
    with open('usr/settings.json') as settings:
        s = json.load(settings)
    settings.close()
    if request.method == 'POST':
        # s['auto_trade'] = request.form.get('auto_trade') #readonly
        s['margin_type'] = request.form['margin_type'] #dropdown
        s['type'] = request.form['type'] #dropdown
        s['time_in_force'] = request.form['time_in_force'] #dropdown
        s['enable_take_profits_upto'] = int(request.form['enabled_take_profit'])
        s['quantity'] = float(request.form['quantity'])
        s['quantity_per_take_profit'] = float(request.form['quantity_per_tk'])
        s['stoploss_type'] = request.form['stop_loss_type'] #dropdown
        s['stop_loss'] = float(request.form['stop_loss_rate'])
        s['stop_loss_switch'] = "True" if bool(request.form.get('stop_loss')) else "False"
    with open('usr/settings.json', 'w') as set:
        json.dump(s,set)
    set.close()
    t1 = Thread(target=run_bot, args=(s,))
    t1.start
    print('minor')
    
    return redirect('/dashboard')


if __name__ == '__main__':
        app.run(port=80)
