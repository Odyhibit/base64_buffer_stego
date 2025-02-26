 const base64Alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

        function getMessage(paddingBits) {
            let size = parseInt(paddingBits.slice(0, 16), 2) * 7;
            let binMessage = paddingBits.slice(16, 16 + size);
            let message = "";
            for (let i = 0; i < binMessage.length; i += 7) {
                message += String.fromCharCode(parseInt(binMessage.slice(i, i + 7), 2));
            }
            return message;
        }

        function base64PaddingDecoder(base64Strings) {
            let output = "";
            let lines = base64Strings.split("\n");
            for (let line of lines) {
                let binaryLine = "";
                for (let char of line.trim()) {
                    let index = base64Alphabet.indexOf(char);
                    if (index !== -1) {
                        binaryLine += index.toString(2).padStart(6, '0');
                    }
                }
                let paddingCharacters = binaryLine.length % 8;
                if (paddingCharacters !== 0) {
                    output += binaryLine.slice(-paddingCharacters);
                }
            }
            return getMessage(output);
        }

        function decodeMessage() {
            let inputText = document.getElementById("input").value;
            let decodedMessage = base64PaddingDecoder(inputText);
            document.getElementById("output").innerText = "Decoded Message: " + decodedMessage;
        }

        function encodeMessage() {
            let text = document.getElementById("input").value;
            let secret = document.getElementById("secret").value;
            let words = text.split(" ");
            let wordsB64 = words.map(word => btoa(unescape(encodeURIComponent(word + " "))));
            let secretBits = secret.length.toString(2).padStart(16, '0');
            secretBits += secret.split('').map(c => c.charCodeAt(0).toString(2).padStart(7, '0')).join('');
            let maxSecretLength = wordsB64.reduce((sum, word) => sum + (word.match(/=/g) || []).length * 2, 0);
            if (secretBits.length > maxSecretLength) {
                alert("Error: Text is too short to encode the secret message.");
                return;
            }
            secretBits = secretBits.padEnd(maxSecretLength, '0');
            let encodedList = wordsB64.map((word) => {
                let paddingCount = (word.match(/=/g) || []).length;
                if (paddingCount > 0) {
                    let secretPart = secretBits.slice(0, 2 * paddingCount);
                    secretBits = secretBits.slice(2 * paddingCount);
                    let firstEqual = word.indexOf('=');
                    let toModify = word[firstEqual - 1];
                    let delta = parseInt(secretPart, 2) || 0;
                    let newIndex = base64Alphabet.indexOf(toModify) + delta;
                    if (newIndex >= base64Alphabet.length) newIndex -= base64Alphabet.length;
                    let encodedChar = base64Alphabet[newIndex];
                    return word.slice(0, firstEqual - 1) + encodedChar + word.slice(firstEqual);
                }
                return word;
            });
            document.getElementById("encodedOutput").value = encodedList.join("\n");
        }