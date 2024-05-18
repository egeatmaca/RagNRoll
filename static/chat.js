function getInput() {
    const inputElement = document.getElementById("input-text");
    const input = inputElement.value;
    inputElement.value = "";
    return input;
}

function displayInput(input) {
    if (input.trim() == "") {
        return;
    }

    const messages = document.querySelector(".messages");
    const message = document.createElement("div");
    message.classList.add("message");
    message.classList.add("user-message");
    message.innerText = input;
    messages.appendChild(message);
    messages.scroll(0, messages.scrollHeight);
}

async function getAnswer(prompt) {
    if (prompt.trim() == "") {
        return;
    }

    const url = new URL("/chat", window.location.href);
    url.searchParams.append("prompt", prompt);

    const response = await fetch(url, { method: "POST" });

    return await response.json();
}

function displayAnswer(answer) {
    const answerFormatted = formatAnswer(answer);

    const responseMessage = document.createElement("div");
    responseMessage.classList.add("message");
    responseMessage.classList.add("bot-message");

    const answerContainer = document.createElement("div");
    answerContainer.classList.add("answer-container");
    const answerParagraph = document.createElement("span");
    answerParagraph.classList.add("answer");
    answerParagraph.innerHTML = answerFormatted;
    answerContainer.appendChild(answerParagraph);
    responseMessage.appendChild(answerContainer);

    const messages = document.querySelector(".messages");
    messages.appendChild(responseMessage);
    
    messages.scroll(0, messages.scrollHeight);
}

function formatAnswer(answer) {
    if (answer.startsWith('"')) {
        answer = answer.substring(1, answer.length);
    }

    if (answer.endsWith('"')) {
        answer = answer.substring(0, answer.length - 1);
    }

    while (answer.includes("\\n")) {
        answer = answer.replace("\\n", "<br>");
    }

    while (answer.includes('\\"')) {
        answer = answer.replace('\\"', '"');
    }

    return answer;
}

function displayLoadingMessage() {
    const loadingMessage = document.createElement("div");
    loadingMessage.classList.add("message");
    loadingMessage.classList.add("bot-message");
    loadingMessage.classList.add("loading-message");
    loadingMessage.innerHTML = "Writing, please wait</span><span>.</span><span>.</span>";
    
    const messages = document.querySelector(".messages");
    messages.appendChild(loadingMessage);
    
    messages.scroll(0, messages.scrollHeight);
}

function removeLoadingMessage() {
    document.querySelectorAll(".loading-message").forEach((e) => e.remove())
}

async function onAsk() {
    const input = getInput();
    displayInput(input);
    displayLoadingMessage();
    const answer = await getAnswer(input);
    removeLoadingMessage();
    displayAnswer(answer);
}

function initialize() {
    document.getElementById("ask-button").addEventListener("click", onAsk);

    document
        .getElementById("input-text")
        .addEventListener("keypress", function (e) {
            if (e.key === "Enter") {
                onAsk();
            }
        });
}

document.addEventListener("DOMContentLoaded", initialize);
