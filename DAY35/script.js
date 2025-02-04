const SECRET_KEY = "b'_PF_42Uu7dKlQnfphgaVCKp9Fd_b32JZJ2ti337E5PY='"; 

function encryptMessage(message) {
    return CryptoJS.AES.encrypt(message, SECRET_KEY).toString();
}

function decryptMessage(encryptedMessage) {
    let bytes = CryptoJS.AES.decrypt(encryptedMessage, SECRET_KEY);
    return bytes.toString(CryptoJS.enc.Utf8);
}

let ws = new WebSocket("ws://127.0.0.1:8000");

ws.onopen = () => {
    console.log("WebSocket connected!");

    let encryptedMessage = encryptMessage("Hello, Server!");
    console.log("Sending Encrypted:", encryptedMessage);

    ws.send(encryptedMessage);
};

ws.onmessage = (event) => {
    let decryptedMessage = decryptMessage(event.data);
    console.log("Message from server:", decryptedMessage);
};
