export class ChatRoomWidget {
    constructor(options) {
        this.socket = io.connect(options.serverUrl);
        this.username = options.username;
        this.room = options.room;
        this.containerId = options.containerId;
        this.sendcontainerId = options.sendcontainerId;
        this.inputId=options.inputId;

        this.init();
    }

    init() {
        this.socket.on('connect', () => {
            this.socket.emit('join_room', {
                username: this.username,
                room: this.room
            });

            const messageInput = document.getElementById(this.inputId);
            document.getElementById(this.sendcontainerId).onsubmit = (e) => {
                e.preventDefault();
                const message = messageInput.value.trim();
                if (message.length) {
                    this.socket.emit('send_message', {
                        username: this.username,
                        room: this.room,
                        message: message
                    });
                }
                messageInput.value = '';
                messageInput.focus();
            };
        });

        this.socket.on('receive_message', (data) => {
            console.log(data);
            const newNode = document.createElement('div');
            newNode.classList.add('message');
            newNode.innerHTML = `<b>${data.username}:&nbsp;</b> ${data.message}`;
            document.getElementById(this.containerId).appendChild(newNode);
        });

        this.socket.on('join_room_announce', (data) => {
            console.log(data);
            const newNode = document.createElement('div');
            newNode.classList.add('announce');
            newNode.innerHTML = `<b>${data.username}</b> has joined the room`;
            document.getElementById(this.containerId).appendChild(newNode);
        });
    }
}


