document.addEventListener("DOMContentLoaded", function () {
    const signupBtn = document.getElementById("signupBtn");
    const loginBtn = document.getElementById("loginBtn");
    const signupForm = document.getElementById("signupForm");
    const loginForm = document.getElementById("loginForm");
    const formContainer = document.querySelector(".form-container");
    const formBox = document.getElementById("formBox");
    const switchToLogin = document.getElementById("switchToLogin");
    const switchToSignup = document.getElementById("switchToSignup");

    // Show Signup Form when clicking "Sign Up"
    signupBtn.addEventListener("click", function () {
        document.body.classList.add("show-form"); // Add blur effect
        formContainer.style.display = "flex";
        signupForm.style.display = "block";
        loginForm.style.display = "none";
    });

    // Show Login Form when clicking "Login"
    loginBtn.addEventListener("click", function () {
        document.body.classList.add("show-form"); // Add blur effect
        formContainer.style.display = "flex";
        signupForm.style.display = "none";
        loginForm.style.display = "block";
    });

    // Switch to Login Form inside the box
    switchToLogin.addEventListener("click", function () {
        signupForm.style.display = "none";
        loginForm.style.display = "block";
    });

    // Switch to Signup Form inside the box
    switchToSignup.addEventListener("click", function () {
        signupForm.style.display = "block";
        loginForm.style.display = "none";
    });

    // Close form and remove blur when clicking outside
    formContainer.addEventListener("click", function (event) {
        if (event.target === formContainer) {
            formContainer.style.display = "none";
            document.body.classList.remove("show-form"); // Remove blur effect
        }
    });
});

let mediaRecorder;
let audioChunks = [];

// 📸 Start Camera
function startCamera() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            document.getElementById('video').srcObject = stream;
        });
}

// 📸 Capture Image
function captureImage() {
    const canvas = document.getElementById('canvas');
    const video = document.getElementById('video');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);

    canvas.toBlob(blob => {
        const formData = new FormData();
        formData.append('image', blob, 'capture.png');

        fetch('/detect-mood-image', {
            method: 'POST',
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById('moodResult').innerText = 
                `Mood: ${data.mood} | Recommendation: ${data.recommendation}`;
        })
        .catch(err => alert("Error detecting mood."));
    });
}

// 🎙️ Start Recording
function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();

            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });
        });
}

// 🎙️ Stop Recording
function stopRecording() {
    mediaRecorder.stop();
    mediaRecorder.addEventListener("stop", () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.wav');

        fetch('/detect-mood-audio', {
            method: 'POST',
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById('moodResult').innerText = 
                `Mood: ${data.mood} | Recommendation: ${data.recommendation}`;
        })
        .catch(err => alert("Error detecting mood."));
    });
}

