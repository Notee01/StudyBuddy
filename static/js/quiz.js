const quizBox = document.getElementById('quiz-box');
const resultBox = document.getElementById('result-box');
const scoreBox = document.getElementById('score-box');
let questionCounter = 1; // Initialize question counter

window.addEventListener("DOMContentLoaded", (event) => {
    let timer;
    const quizStart = document.getElementById('quiz_start');
    const timerBox = document.getElementById('timer-box');
    const back_btn = document.getElementById('back_btn');
    const csrf = document.getElementsByName('csrfmiddlewaretoken');
    const quizForm = document.getElementById('quiz-form')

    const sendData = () => {
        const element = [...document.getElementsByClassName('ans')]
        const data = {}
        data['csrfmiddlewaretoken'] = csrf[0].value
        element.forEach(el => {
            if (el.checked) {
                data[el.name] = el.value
            } else {
                if (!data[el.name]) {
                    data[el.name] = null
                }
            }
        })

        $.ajax({
            type: 'POST',
            url: `${url}submit/`,
            data: data,
            success: function (response) {
                // console.log(response)
                const results = response.results
                console.log(results)
                quizForm.classList.add('hidden')
                scoreBox.innerHTML += `${response.pass ? 'Congratulations!' : 'Failed!'} Your score is ${response.score.toFixed(2)}%`

                results.forEach(result => {
                    const resultDiv = document.createElement('div');

                    // Add a container class and apply padding and text color
                    resultDiv.classList.add('result-container', 'p-4', 'text-white', 'rounded-md');

                    for (const [question, resp] of Object.entries(result)) {
                        // Add the question as a paragraph element with bottom margin for spacing
                        resultDiv.innerHTML += `<p class="pb-2"><strong>${question}</strong></p>`;

                        if (resp == 'no answer') {
                            // Handle case when no answer is provided
                            resultDiv.innerHTML += '- No answer';
                            resultDiv.classList.add('bg-danger');
                        } else {
                            const answer = resp['answer'];
                            const correct = resp['correct_answer'];

                            if (answer == correct) {
                                // Handle correct answer case
                                resultDiv.classList.add('bg-success');
                                resultDiv.innerHTML += `Answered: ${answer}`;
                            } else {
                                // Handle incorrect answer case
                                resultDiv.classList.add('bg-danger');
                                resultDiv.innerHTML += `Correct answer: ${correct} | Answered: ${answer}`;
                            }
                        }
                    }

                    // Append the resultDiv to the resultBox (assuming resultBox is defined)
                    resultBox.appendChild(resultDiv);


                    // Log the created resultDiv to ensure it's being appended correctly
                    console.log('Appended resultDiv:', resultDiv);
                });

            },
            error: function (error) {
                console.log(error)
            }
        })
    }

    const activateTimer = (time) => {
        if (time.toString().length < 2) {
            timerBox.innerHTML = `<b>0${time}:00</b>`
        }
        else {
            timerBox.innerHTML = `<b>${time}:00</b>`
        }
        let minutes = time - 1;
        let seconds = 60;
        let displaySeconds
        let displayMinutes

        timer = setInterval(() => {
            seconds--;
            if (seconds < 0) {
                seconds = 59;
                minutes--
            }
            if (minutes.toString().length < 2) {
                displayMinutes = '0' + minutes;
            } else {
                displayMinutes = minutes;
            }
            if (seconds.toString().length < 2) {
                displaySeconds = '0' + seconds;
            } else {
                displaySeconds = seconds;
            }
            if (minutes === 0 && seconds === 0) {
                timerBox.innerHTML = "<b>00:00</b>"
                setTimeout(() => {
                    clearInterval(timer)
                    alert('timer ended')
                    sendData()
                })
            }
            timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`
        }, 1000)
    }

    const stopTimer = () => {
        clearInterval(timer); // Clear the interval
    }

    const url = window.location.href;
    if (quizStart) {
        $.ajax({
            type: 'GET',
            url: `${url}data`,
            success: function (response) {
                const data = response.data;

                data.forEach(element => {
                    const question = element.question;
                    const answers = element.answers;
                    const imageUrl = element.image_url; // New image URL field

                    quizBox.innerHTML += `
                        <div class="p-2 bg-gray-700 text-white rounded-md mb-4 mt-4">
                            <b style="font-weight: bold;">${questionCounter}.</b> ${question}
                        </div>
                    `;

                    if (imageUrl) {
                        // If image URL exists, display the image
                        quizBox.innerHTML += `
                            <div class="ml-4 pl-4 mb-2 ">
                                <img src="${imageUrl}" alt="Question Image" style="max-width: 200px;">
                            </div>
                        `;
                    }

                    answers.forEach(answer => {
                        quizBox.innerHTML += `
                            <div class="ml-4 pl-4 flex items-center text-gray-300 ">
                                <input type="radio" class="ans mr-2 cursor-pointer" id="${question}-${answer}" name="${question}" value="${answer}">
                                <label for="${question}" style="font-weight: normal;" class="text-gray-300">${answer}</label>
                            </div>
                        `;
                    });
                    questionCounter++; // Increment question counter
                });

                activateTimer(response.time)
            },
            error: function (error) {
                console.log(error);
            }
        });


        quizForm.addEventListener('submit', e => {
            e.preventDefault();
            stopTimer();
            sendData();
        })
    }
});


window.addEventListener("DOMContentLoaded", (event) => {
    const videoPlayer = document.getElementById("videoPlayer");
    if (videoPlayer) {
        const url = window.location.href; // Get the base URL
        videoPlayer.addEventListener("ended", function () {
            const data = { 'data': "success" }
            console.log(url)
            const csrftoken = getCookie('csrftoken');
            location.reload();
            $.ajax({
                type: "POST",
                url: `${url}/update-activity-status`,
                data: data,
                headers: {
                    "X-CSRFToken": csrftoken
                },
                success: function (response) {
                    // Handle success response
                    console.log(response);

                },
                error: function (error) {
                    // Log the entire error object
                    console.error(error);
                },
            });
        });
    }
});

function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
}





