const windowHref = window.location.href;
console.log(windowHref);

fetch('http://127.0.0.1:5000/post', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({url: windowHref})
}).then(response => console.log(response));

// add event listener to video element

const getScreenshot = (video) => {
    console.log("video was paused. Taking screenshot");
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataURL = canvas.toDataURL('image/png');
    console.log(dataURL);

    fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({dataURL})
    }).then(response => console.log(response));
}

let interval = setInterval(() => {
    video = document.querySelector('video');
    if (video) {
        clearInterval(interval);
        video.addEventListener('pause', () => getScreenshot(video));
        console.log("Added event listener");
    }
}, 500);