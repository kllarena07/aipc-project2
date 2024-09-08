const windowHref = window.location.href;
console.log(windowHref);

fetch('http://127.0.0.1:5000/post', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({url: windowHref})
});