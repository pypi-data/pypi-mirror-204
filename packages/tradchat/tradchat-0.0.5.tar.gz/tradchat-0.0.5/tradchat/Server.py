from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO
import secrets
from datetime import*
from flask_wtf import FlaskForm
from wtforms import FileField
from contextlib import suppress
import shutil
import smtplib
from email.message import EmailMessage
import ssl
from threading import Thread as T
import socket
import os

Color = '#61b3a2'
password = 'Charity'

class Upload(FlaskForm):
    file = FileField('File')

def capitalize_username(string):
    groups = string.split(' ') # spliting diffenent parts of username at spaces so I can capitialize them all
    for group in groups:
        groups[groups.index(group)] = group.lower().capitalize()
    username = ' '.join(groups)
    return username

try:
    rooms = eval(open('rooms.txt').read())
except Exception:
    rooms = {'mainroom': ['Server', 'mainroom']}

app = Flask(__name__)
app.secret_key = secrets.token_hex(64)
Server = SocketIO(app)

try:
    accounts = eval(open('accounts.txt').read())
except Exception:
    accounts = {'Server': [secrets.token_hex(64), 'computer', Color, '1970-01-01', 'JavaScript', 'Pythonsin', 'mainroom', 'tradchatforkids@gmail.com']}

@app.route('/control/', methods=['POST'])
def control():
    password = request.form['password']
    if password == control_panel_password:
        return render_template('control.html', password=password)
    else:
        return 'Please don`t try anything smart. We want no hackers on tradchat'


@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/login/')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    with suppress(KeyError):
        print(session['username'])
        return redirect('/mainpage/')

    if request.method == 'POST':
        if request.form['password'].lower() != accounts[capitalize_username(request.form['username'])][0].lower():return 'Please don`t try anything smart. We want no hackers on tradchat'
        session['username'] = capitalize_username(request.form['username'])
        return redirect('/mainpage/')
    return render_template('login.html', color = Color)

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    os.chdir(os.path.split(__file__)[0])
    with suppress(KeyError):
        print(session['username'])
        return redirect('/mainpage/')
    if request.method == 'POST':
        if capitalize_username(request.form['username']) in accounts: return 'Please don`t try anything smart. We want no hackers on tradchat'
        session['username'] = capitalize_username(request.form['username'])
        if (request.form['gender'] == 'male'):
            shutil.copy('static/graphics/defaultBoy.png', 'static/savedPictures/'+session['username'])
        else:
            shutil.copy('static/graphics/defaultGirl.png', 'static/savedPictures/'+session['username'])
        accounts[session['username']] = [request.form['password'], request.form['gender'], request.form['color'], request.form['birthday'], request.form['first_name'], request.form['last_name'], 'mainroom', request.form['email']]
        file = open('accounts.txt', 'w')
        for thing in list(str(accounts)):
            try:
                file.write(thing)
            except UnicodeEncodeError:
                file.write(' _emoji_ ')
        file.close()
        return redirect('/mainpage/')
    try:
        assert session['I am a trad'] == True
    except Exception:
        return redirect('/checkIfClientKnowsPassword/')
    return render_template('signup.html', color = Color)

@app.route('/mainpage/', methods=['GET', 'POST'])
def mainpage():
    try:
        username = session['username']
    except KeyError:
        return redirect('/login/')
    form = Upload()
    return render_template('mainpage.html', name=username, color=accounts[session['username']][2], gender=accounts[session['username']][1], form=form, room=accounts[session['username']][6])

@app.route('/checkIfClientKnowsPassword/', methods=['GET', 'POST'])
def checkIfClientKnowsPassword():
    alert = 'false'
    if request.method == 'POST':
        alert = 'true'
        if request.form['password'].lower() == password.lower():
            session['I am a trad'] = True
            return redirect('/signup/')
    return render_template('trad.html', alert=alert)

@app.route('/profile/', methods=['GET', 'POST'])
def settings():
    try:
        color = accounts[session['username']][2]
    except KeyError:
        return redirect('/login/')
    if request.method == 'POST':
        accounts[session['username']][2] = request.form['color']
        accounts[session['username']][0] = request.form['password'].replace('#39;', "'")
        file = open('accounts.txt', 'w')
        for thing in list(str(accounts)):
            try:
                file.write(thing)
            except UnicodeEncodeError:
                file.write(' _emoji_ ')
        file.close()
        return redirect('/mainpage/')
    form = Upload()
    return render_template('settings.html', color=color, password = accounts[session['username']][0], form=form, name=session['username'])

@app.route('/')
def index():
    try:
        print(session['username'])
        return redirect('/mainpage/')
    except KeyError:
        return redirect('/login/')

def heighst(li):
    try:
        heighst = li[0]
    except IndexError:
        return 0
    for i in li:
        if i > heighst:
            heighst = i
    return heighst

@app.route('/shareAudio/', methods=['POST'])
def shareAudio():
    form = Upload()
    values = []
    if form.validate_on_submit():
        File = form.file.data
        for file in os.listdir('static/sharedAudio'):
            with suppress(ValueError):
                values.append(int(file))
        name = str(heighst(values)+1)
        File.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/sharedAudio', name))
        day = date.today()
        time = datetime.today()
        compounded = ['Audio', [[request.form['username'], f'static/sharedAudio/{name}'], f'{months[int(day.month)-1]} {day.day}, {day.year} at {time.hour}:{time.minute}']]
        try:
            messages[request.form['room']].append(compounded)
        except KeyError:
            Server.send(str(['you better switch to this room', request.form['username'], 'mainroom']), broadcast=True)
        Server.send(str([request.form['room'], compounded]), broadcast=True)
        file = open('chat.txt', 'w')
        for thing in list(str(messages)):
            try:
                file.write(thing)
            except UnicodeEncodeError:
                file.write(' _emoji_ ')
        file.close()
    try:
        assert session['I am a trad'] == True
        return redirect('/signup/')
    except Exception:
        return redirect('/mainpage/')
control_panel_password = 'JavaScopeRuntime'
@app.route('/sharePicture/', methods=['POST'])
def sharePicture():
    form = Upload()
    values = []
    if form.validate_on_submit():
        File = form.file.data
        for file in os.listdir('static/sharedPictures'):
            with suppress(ValueError):
                values.append(int(file))
        name = str(heighst(values)+1)
        File.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/sharedPictures', name))
        day = date.today()
        time = datetime.today()
        compounded = ['Picture', [[request.form['username'], f'static/sharedPictures/{name}'], f'{months[int(day.month)-1]} {day.day}, {day.year} at {time.hour}:{time.minute}']]
        try:
            messages[request.form['room']].append(compounded)
        except KeyError:
            Server.send(str(['you better switch to this room', request.form['username'], 'mainroom']), broadcast=True)
        Server.send(str([request.form['room'], compounded]), broadcast=True)
        file = open('chat.txt', 'w')
        for thing in list(str(messages)):
            try:
                file.write(thing)
            except UnicodeEncodeError:
                file.write(' _emoji_ ')
        file.close()
    try:
        assert session['I am a trad'] == True
        return redirect('/signup/')
    except Exception:
        return redirect('/mainpage/')

@app.route('/sharePrivateAudio/', methods=['POST'])
def sharePrivateAudio():
    form = Upload()
    values = []
    if form.validate_on_submit():
        File = form.file.data
        for file in os.listdir('static/sharedAudio'):
            with suppress(ValueError):
                values.append(int(file))
        name = str(heighst(values)+1)
        File.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/sharedAudio', name))
        day = date.today()
        time = datetime.today()
        compounded = ['PrivateAudio', [[request.form['username'], f'static/sharedAudio/{name}'], f'{months[int(day.month)-1]} {day.day}, {day.year} at {time.hour}:{time.minute}'], request.form['receiver']]
        messages['mainroom'].append(compounded)
        Server.send(str(['mainroom', compounded]), broadcast=True)
        file = open('chat.txt', 'w')
        for thing in list(str(messages)):
            try:
                file.write(thing)
            except UnicodeEncodeError:
                file.write(' _emoji_ ')
        file.close()
        session['chatterWith'] = request.form['receiver']
    return redirect('/messenger/')

@app.route('/sharePrivatePicture/', methods=['POST'])
def sharePrivatePicture():
    form = Upload()
    values = []
    if form.validate_on_submit():
        File = form.file.data
        for file in os.listdir('static/sharedPictures'):
            with suppress(ValueError):
                values.append(int(file))
        name = str(heighst(values)+1)
        File.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/sharedPictures', name))
        day = date.today()
        time = datetime.today()
        compounded = ['PrivatePicture', [[request.form['username'], f'static/sharedPictures/{name}'], f'{months[int(day.month)-1]} {day.day}, {day.year} at {time.hour}:{time.minute}'], request.form['receiver']]
        messages['mainroom'].append(compounded)
        Server.send(str(['mainroom', compounded]), broadcast=True)
        file = open('chat.txt', 'w')
        for thing in list(str(messages)):
            try:
                file.write(thing)
            except UnicodeEncodeError:
                file.write(' _emoji_ ')
        file.close()
        session['chatterWith'] = request.form['receiver']
    return redirect('/messenger/')

@app.route('/showMeMyPassword/')
def sendEmail():
    return render_template('email.html', color=Color)

@app.route('/loadPicture/', methods=['POST'])
def loadPicture():
    form = Upload()
    if form.validate_on_submit():
        File = form.file.data
        File.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/savedPictures', request.form['username']))
    return redirect('/profile/')

@app.route('/messenger/')
def messagenger():
    try:
        username = session['username']
    except KeyError:
        return redirect('/login/')
    try:
        chatterer = session['chatterWith']
    except KeyError:
        chatterer = ''
    form = Upload()
    names = []
    for account in accounts:
        names.append(account)
    names.remove(username)
    names.remove('Server')
    return render_template('messagenger.html', names=str(names), name=username, color=accounts[session['username']][2], gender=accounts[session['username']][1], form=form, chatterer=chatterer)


@app.route('/learnYourFriends/', methods=['POST'])
def learnYourFriends():
    try:
        print(session['username'])
    except Exception:
        return redirect('/login/')
    try:
        username = request.form['username']
        return render_template('showMe.html', MyUsername=session['username'], username=username, gender=accounts[username][1], color=accounts[username][2], birthday=accounts[username][3], first_name=accounts[username][4], last_name=accounts[username][5], email=accounts[username][7])
    except Exception:
        username = 'Server'
    return render_template('showMe.html', MyUsername=session['username'], username=username, gender=accounts[username][1], color=accounts[username][2], birthday=accounts[username][3], first_name=accounts[username][4], last_name=accounts[username][5], email=accounts[username][7])


@app.route('/<other>/')
def other(other):
    return redirect('/')

@app.route('/<other>/<Other>/')
def Other(other, Other):
    return redirect('/')

@app.route('/<other>/<Other>/<_other>/')
def _other(other, Other, _other):
    return redirect('/')

@app.route('/<other>/<Other>/<_other>/<_Other>/')
def _Other(other, Other, _other, _Other):
    return redirect('/')

try:
    messages = eval(open('chat.txt').read())
except Exception:
    messages = {'mainroom': []}


@Server.on('connect')
def connect():
    Server.send(str(['Messages', messages]), broadcast=True)

months = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'Jun.', 'Jul.', 'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.']

def send_email(email, username):
    password = accounts[username][0]
    context = ssl.create_default_context()
    em = EmailMessage()
    em['From'] = 'tradchatforkids@gmail.com'
    em['To'] = email
    em['Subject'] = 'TradChat password recovery'
    body = f"""
    Your Tradchat Password for {username} is {password}
    """
    em.set_content(body)
    sender = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
    sender.login('tradchatforkids@gmail.com', 'zqclhcweonkehwwl')
    sender.send_message(em)
    sender.quit()

@Server.on('message')
def Recv(msg):
    T(target=recv, args=(msg,)).start()

def sending_email_if_the_user_typed_an_email_vs_if_he_typed_a_username(email_he_typed):
    he_gave_a_valid_email_address = False
    for account in accounts:
        if accounts[account][7].lower() == email_he_typed.lower():
            he_gave_a_valid_email_address = True
            try:
                send_email(email_he_typed, account)
            except Exception:
                Server.send(str(['Something went wrong', email_he_typed]), broadcast=True)
                return
    if he_gave_a_valid_email_address:
        Server.send(str(['Message sent successfully', email_he_typed, f'Email(s) sent successfully to {email_he_typed}']), broadcast=True)
    else:
        Server.send(str(['Email no exist', email_he_typed]), broadcast=True)

def sending_email_if_the_user_typed_an_username_vs_if_he_typed_a_email(username_he_typed):
    username = capitalize_username(username_he_typed)
    if username in accounts:
        email = accounts[username][7]
        try:
            send_email(email, username)
            Server.send(str(['Message sent successfully', username_he_typed, f'Email sent successfully to {email}']), broadcast=True)
        except Exception:
            Server.send(str(['Something went wrong', username_he_typed]), broadcast=True)
    else:
        Server.send(str(['You are trying to send an email to a username that does not exist', username_he_typed]), broadcast=True)

def recv(msg):
    try:
        message = eval(msg)
    except Exception:
        print(f'Error: {msg}')
        return
    if message[0] == 'I am ordering you to command':
        if message[1] == control_panel_password:
            Server.send(message[2], broadcast=True)
    if message[0] == 'I am ordering you to delete':
        if message[1] == control_panel_password:
            Server.send(str(["Command", message[2], "location.replace('/logout/')"]))
            del accounts[message[2]]
            file = open('accounts.txt', 'w')
            for thing in list(str(accounts)):
                try:
                    file.write(thing)
                except UnicodeEncodeError:
                    file.write(' _emoji_ ')
            file.close()
    if message[0] == "making sure it is alright to send a email":
        if '@' in list(message[1]):#they typed a email
            sending_email_if_the_user_typed_an_email_vs_if_he_typed_a_username(message[1])
            return
        else:#they typed a username
            sending_email_if_the_user_typed_an_username_vs_if_he_typed_a_email(message[1])
            return
    if message[0] == "Checking to see if my password is correct":
        if (capitalize_username(message[1]) in accounts) and (message[2].lower() == accounts[capitalize_username(message[1])][0].lower()):
            Server.send(str(["Checking to see if my password is correct", message[1], "you are good for takeoff"]), broadcast=True)
        else:
            Server.send(str(["Checking to see if my password is correct", message[1], "Error, something went wrong"]), broadcast=True)

    if message[0] == "Making sure that your username is not already claimed":
        if (capitalize_username(message[1]) in accounts):
            Server.send(str(["Making sure that your username is not already claimed", message[1], 'You have to quit that username as it is already taken']), broadcast=True)
        else:
            Server.send(str(["Making sure that your username is not already claimed", message[1], 'You are safe for takeoff bro, go make a new account to further expand tradchat']), broadcast=True)
    if message[0] == 'Requesting to join a room':
        for password in rooms:
            if password.lower() == message[2].lower():
                Server.send(str(['Requesting to join a room', message[1], 'you got the room right dude or thug or whatever you are', rooms[password][1]]))
                return
        Server.send(str(['Requesting to join a room', message[1], 'HOW DARE YOU GET THAT PASSWORD WRONG!!']))
        return
    if message[0] == 'Please oh please say `you better switch to this room` I know you can':
        for password in rooms:
            if rooms[password][1] == message[2]:
                Server.send(str(['you better switch to this room', message[1], message[2]]), broadcast=True)
                return
        Server.send(str(['ALERT ALERT HIGH ALERT!!  '*3, 'Someone is trying to hack tradchat!!!!']), broadcast=True)
    if message[0] == 'You nut, you have better give me all my rooms':
        li = []
        for password in rooms:
            if rooms[password][0] == message[1]:
                li.append([rooms[password][1], password])
        Server.send(str(['To the cashew that wanted his penut butter rooms', message[1], li]), broadcast=True)
        return
    if message[0] == 'Requesting to delete a room':
        for password in rooms:
            if rooms[password][1].lower() == message[1].lower():
                if rooms[password][0] == message[2]:
                    with suppress(KeyError):del messages[rooms[password][1]]
                    del rooms[password]
                    Server.send(str(['Sucsessfuul delete', message[2], message[1]]), broadcast=True)
                    return
                else:
                    Server.send(str(['Requesting to delete a room', message[2], 'you should not delete a room that does not belong to you']), broadcast=True)
                    return
        Server.send(str(['Requesting to delete a room', message[2], 'you should not delete a room that does not even EXIST']), broadcast=True)
        return
    if message[0] == "Then you better give me my messages buster":
        accounts[message[1]][6] = message[2]
        file = open('accounts.txt', 'w')
        for thing in list(str(accounts)):
            try:
                file.write(thing)
            except UnicodeEncodeError:
                file.write(' _emoji_ ')
        file.close()
        Server.send(str(['Messages', messages]), broadcast=True)
        return
    if message[0] == 'Requesting to make a new room':
        count = 0
        for password in rooms:
            name = rooms[password][0]
            if name == message[2]:
                count += 1
        if count > 2:
            Server.send(str(['Requesting to make a new room', message[2], 'you should not make more than 2 rooms']), broadcast=True)
            return
        for room in rooms:
            if room.lower() == message[1].lower():
                Server.send(str(['Requesting to make a new room', message[2], 'you should not take that claimed room']), broadcast=True)
                return
        for password in rooms:
            if rooms[password][1] == message[3]:
                Server.send(str(['Requesting to make a new room', message[2], 'you should not take that claimed room name']), broadcast=True)
                return
        messages[message[3]] = []
        rooms[message[1]] = [message[2], message[3]]
        file = open('rooms.txt', 'w')
        for thing in list(str(rooms)):
            try:
                file.write(thing)
            except UnicodeEncodeError:
                file.write(' _emoji_ ')
        file.close()
        Server.send(str(['Successful make', message[2], message[3]]), broadcast=True)
        print('hey hey')
        return
    if message[1] == 'PrivateText':
        day = date.today()
        time = datetime.today()
        compounded = ['PrivateText', [[message[0], message[3]], f'{months[int(day.month)-1]} {day.day}, {day.year} at {time.hour}:{time.minute}'], message[2]]
        messages['mainroom'].append(compounded)
        Server.send(str(['mainroom', compounded]), broadcast=True)
        file = open('chat.txt', 'w')
        for thing in list(str(messages)):
            try:
                file.write(thing)
            except UnicodeEncodeError:
                file.write(' _emoji_ ')
        file.close()
    if message[1] == 'Public':
        day = date.today()
        time = datetime.today()
        compounded = ['Public', [[message[0], message[3]], f'{months[int(day.month)-1]} {day.day}, {day.year} at {time.hour}:{time.minute}']]
        try:
            print(message[2])
            messages[message[2]].append(compounded)
        except KeyError:
            Server.send(str(['you better switch to this room', message[0], 'mainroom']), broadcast=True)
            return
        Server.send(str([message[2], compounded]), broadcast=True)
        file = open('chat.txt', 'w')
        for thing in list(str(messages)):
            try:
                file.write(thing)
            except UnicodeEncodeError:
                file.write(' _emoji_ ')
        file.close()
    

Server.run(app, host=socket.gethostbyname('raspberrypi'), port=777, debug=True)