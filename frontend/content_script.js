const windowHref = window.location.href;
console.log(windowHref);
let ws = new WebSocket('ws://127.0.0.1:5000/ws');

fetch('http://127.0.0.1:5000/post', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({url: windowHref})
}).then(response => console.log(response.text()));

const getScreenshot = (video) => {
    console.log("video was paused. Taking screenshot");
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataURL = canvas.toDataURL('image/jpg');
    console.log(dataURL);

    fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({dataURL})
    }).then(response => console.log(response));
}

let video_interval = setInterval(() => {
    video = document.querySelector('video');
    if (video) {
        clearInterval(video_interval);
        // video.addEventListener('pause', () => getScreenshot(video));
        // console.log("Added event listener");
    }
}, 500);

const create_message = (chat, message, is_user=true) => {
    const p = document.createElement('p');
    p.innerText = message;
    p.style.width = "50%";
    if (is_user) {
        p.style.marginLeft = "auto";
    } else {
        p.style.marginRight = "auto";
    }
    p.style.backgroundColor = "#F4F4F4";
    p.style.padding = "10px";
    p.style.fontSize = "16px";
    p.style.marginBottom = "10px";
    chat.appendChild(p);
}

const initialize_interface = () => {
    const interface = document.createElement('section');
    interface.style.width = "100%";
    interface.style.height = "572px";
    interface.style.boxSizing = "border-box";
    interface.style.backgroundColor = "white";

    const chat = document.createElement('section');
    chat.id = "chat";
    chat.style.width = "calc(100% - 30px)";
    chat.style.height = "calc(100% - 65px)";
    chat.style.paddingTop = "15px";
    chat.style.paddingLeft = "15px";
    chat.style.paddingRight = "15px";
    chat.style.overflowY = "scroll";
    chat.style.flex = "1";
    chat.style.flexDirection = "column";

    interface.appendChild(chat);

    const input = document.createElement('input');
    input.id = "chat-input";
    input.style.boxSizing = "border-box";
    input.style.width = "100%";
    input.style.height = "50px";
    input.addEventListener("keydown", (e) => {
        if(e.key == "Enter") {
            create_message(chat, input.value);
            if (ws.OPEN) {
                ws.send(JSON.stringify({
                    url: windowHref,
                    message: input.value
                }));
            } else {
                console.log("Error. Websocket not open.");
            }
            input.disabled = true;
            input.value = '';

        }
    });

    interface.appendChild(input);

    items.insertBefore(interface, items.firstChild);
}

ws.addEventListener("message", (evt) => {
    const { data } = evt;
    console.log(data);

    const chat = document.querySelector('#chat');
    create_message(chat, data, false);

    const chat_input = document.querySelector('#chat-input');
    chat_input.disabled = false;
});

let items;
let interface_interval = setInterval(() => {
    items = document.querySelector('#items.style-scope.ytd-watch-next-secondary-results-renderer');
    if (items) {
        clearInterval(interface_interval);
        initialize_interface();
        console.log("Mounted interface.");
    }
}, 500);
