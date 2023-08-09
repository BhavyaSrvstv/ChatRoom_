from flask import Flask,render_template,request,session,redirect,url_for
from flask_socketio import SocketIO,emit,join_room,leave_room
from db import *

app=Flask(__name__)
app.config["SECRET_KEY"]="BQWERT"
socketio=SocketIO(app)


@app.route("/",methods=["POST","GET"])
def home():
     return render_template("index.html")


@app.route("/room",methods=["POST","GET"])
def room():
       username=request.args.get('username')
       room=request.args.get('roomid')

       if username and room:
            messages=get_messages(room)
            return render_template('room.html',username=username,room=room,messages=messages)
       else:
            return redirect(url_for('home'))
            
       
@socketio.on('join_room')
def handle_user_join(data):
     app.logger.info("{} has joined the room {}".format(data['username'],data['room']))
     join_room(data['room'])
     socketio.emit('join_room_announce',data)

@socketio.on('send_message')
def handle_send_message_event(data):
     app.logger.info("{} has sent message to the room {}: {}".format(data['username'],data['room'],data['message']))

     save_message(data['room'],data['message'],data['username'])

     socketio.emit('receive_message', data, room=data['room'])  #room is an argument of socket.emit function which checks what all sockets belong to the specified room and emit to only those sockets only




if __name__=="__main__":
    socketio.run(app,debug=True)