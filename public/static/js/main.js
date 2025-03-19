console.log("JavaScript file loaded successfully!");

function login() {
    var username = document.getElementById('loginUsername').value;
    var password = document.getElementById('loginPassword').value;
    var csrf = document.getElementById('csrf').value;

    if (username === '' || password === '') {
        alert('You must enter both username and password.');
        return;
    }

    var data = {
        'username': username,
        'password': password
    };

    fetch('/api/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf,
        },
        body: JSON.stringify(data)
    })
    .then(result => result.json())
    .then(response => {
        if (response.status === 200) {
            window.location.href = '/';
        } else {
            alert(response.message);
        }
    })
    .catch(error => console.error('Error:', error));
}

function register() {
    var username = document.getElementById('loginUsername').value;
    var password = document.getElementById('loginPassword').value;
    var csrf = document.getElementById('csrf').value;

    if (username === '' || password === '') {
        alert('You must enter both username and password.');
        return;
    }

    var data = {
        'username': username,
        'password': password
    };

    fetch('/api/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf,
        },
        body: JSON.stringify(data)
    })
    .then(result => result.json())
    .then(response => {
        console.log(response);
        if (response.status === 200) {
            alert("Registration successful! Redirecting to login...");
            window.location.href = "/login/";
        } else {
            alert(response.message);
        }
    })
    .catch(error => console.error('Error:', error));
}