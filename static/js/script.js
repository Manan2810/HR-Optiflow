document.addEventListener('DOMContentLoaded', function () {
    const videoPreview = document.getElementById('video-preview');
    const startRecordingButton = document.getElementById('start-recording');
    const stopRecordingButton = document.getElementById('stop-recording');
    let mediaRecorder;
    let recordedChunks = [];

    // Sample questions
    const questions = [
        "Please introduce yourself and tell us about your experience.",
        "What skills do you possess that make you a good fit for this position?"
    ];

    let currentQuestionIndex = 0;

    // Access the camera and start video preview
    navigator.mediaDevices.getUserMedia({ video: true, audio: true })
        .then(stream => {
            videoPreview.srcObject = stream;
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = event => {
                if (event.data.size > 0) {
                    recordedChunks.push(event.data);
                }
            };

            mediaRecorder.onstop = () => {
                const timestamp = new Date().toISOString().replace(/[-T:\.Z]/g, "");
                const questionNumber = currentQuestionIndex + 1;
                const questionText = questions[currentQuestionIndex].replace(/\s+/g, "_"); // Remove spaces and replace with underscores
                const filename = `question${questionNumber}_${questionText}_${timestamp}.webm`;

                const blob = new Blob(recordedChunks, { type: 'video/webm' });
                const url = URL.createObjectURL(blob);
                
                downloadFile(url, filename).then(() => {
                    // Move to the next question or finish if all questions have been asked
                    currentQuestionIndex++;

                    if (currentQuestionIndex < questions.length) {
                        // If there are more questions, display the next question
                        showQuestion(questions[currentQuestionIndex]);
                    } else {
                        // If all questions are done, you might want to redirect or perform another action
                        alert("Interview completed!");
                    }
                });
            };
        })
        .catch(error => console.error('Error accessing camera:', error));

    // Start recording
    startRecordingButton.addEventListener('click', () => {
        recordedChunks = [];
        mediaRecorder.start();
        startRecordingButton.disabled = true;
        stopRecordingButton.disabled = false;
    });

    // Stop recording
    stopRecordingButton.addEventListener('click', () => {
        mediaRecorder.stop();
        startRecordingButton.disabled = false;
        stopRecordingButton.disabled = true;
    });

    // Initial display of the first question
    showQuestion(questions[currentQuestionIndex]);
});

function showQuestion(question) {
    // Update the HTML to display the current question
    const questionDisplay = document.getElementById('question-display');
    questionDisplay.textContent = question;
}

function downloadFile(url, filename) {
    return new Promise((resolve, reject) => {
        const a = document.createElement('a');
        a.href = url;

        // Set a unique download filename
        a.download = filename;

        document.body.appendChild(a);
        a.click();

        // Remove the temporary anchor element
        document.body.removeChild(a);

        resolve();
    });
}
