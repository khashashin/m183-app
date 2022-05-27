document.addEventListener('DOMContentLoaded', main(), false);

let timeout = 0;

function main() {
    const form = document.getElementById('run');
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        if (timeout > 0) {
            return;
        }

        timeout = 7;

        const errorElement = document.getElementById('results');
        errorElement.innerHTML = '';
        const input = document.getElementById('command').value;
        const output = document.getElementById('output');
        output.innerHTML = '';

        // The Input will be validated by the server,
        // so we don't want to share with you the validation logic.
        const response = await fetch('/-_/run/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                input: input
            })
        });
        if (response.ok) {
            const data = await response.json();
            console.log(data);
            if (data.output.length > 0) {
                let line = `<span class="line" style="color: white">${data.output}</span><br>`;
                output.innerHTML = line;
            }
            if (data.error.length > 0) {
                let line = `<span class="line" style="color: red">${data.error}</span><br>`;
                output.innerHTML = line;
            }
        }
        if (response.status >= 400) {
            const error = await response.json();
            errorElement.innerHTML = '<span class="line" style="color: red">' + error.error + '</span>';
        }
    });

    setInterval(function () {
        const submitButton = document.getElementById('submit');
        if (timeout > 0) {
            timeout--;
            submitButton.classList.add('disabled');
            submitButton.innerHTML = timeout;
        } else {
            submitButton.classList.remove('disabled');
            submitButton.innerHTML = 'Run';
        }
    }, 1000);
}