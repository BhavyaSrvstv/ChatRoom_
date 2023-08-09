
import { ChatRoomWidget } from './widget.js';

const queryParams = new URLSearchParams(window.location.search);

const username = queryParams.get('username');
const room = queryParams.get('roomid');

const chatWidgetOptions = {
        serverUrl: 'http://127.0.0.1:5000',
        username: username,
        room: room,
        containerId: 'container',
        sendcontainerId:'send-container',
        inputId: 'inputbox'
};

const chatWidget = new ChatRoomWidget(chatWidgetOptions);
