// detail.js
let answer = document.getElementById("answer")
let uuid = document.getElementById("question-uuid")
let csrftoken = getCookie('csrftoken');

answer.addEventListener("input", function() {
    //let newAnswer = answer.textContent  # is this unsafe? I think it might be
    let data = { answer: newAnswer }

    fetch('question/'+uuid+'/update/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify(data),
        credentials: 'same-origin',
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success: ', data)
    })
    .catch((error) => {
        console.error('My Error: ', error)
    })
}, false);

// The following function are copying from
// https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
function getCookie(answer) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, answer.length + 1) === (answer + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(answer.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
