from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_socketio import send, emit


# Init the server
app = Flask(__name__)
app.config['SECRET_KEY'] = 'some super secret key!'
socketio = SocketIO(app, logger=True)

# Send HTML!
@app.route('/')
def root():    
    return "Hello world!"

# Returns a random number
@app.route('/random')
def random():  
    from random import randint  
    html = str(randint(1, 100))
    return html

# Prints the user id
@app.route('/user/<id>')
def user_id(id):
    return str(id)

# Display the HTML Page & pass in a username parameter
@app.route('/html/<username>')
def html(username):
    return render_template('index.html', username=username)

# Receive a message from the front end HTML
@socketio.on('send_message')   
def message_recieved(data):
    print(data['text'])
    emit('message_from_server', {'text':'Message recieved!'})


@socketio.on('message')
def handle_message(message):
    send(message)

@socketio.on('my event')
def handle_my_custom_event(data):
    emit('my response', data, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)