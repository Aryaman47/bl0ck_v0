const titleElement = document.getElementById("shuffleTitle");

const options = {
    0: ['b', 'B'],
    1: ['l', 'L', '1'],
    2: ['o', 'O', '0'],
    3: ['c', 'C', '{', '(', '['],
    4: ['k', 'K', '|<'],
    5: ['c', 'C', '{', '(', '['],
    6: ['h', 'H', '|-|'],
    7: ['a', 'A'],
    8: ['i', 'I'],
    9: ['n', 'N'],
};

const allChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

function generateVariations() {
    const keys = Object.keys(options);
    const allVariations = [];

    function build(current = "", index = 0) {
        if (index === keys.length) {
            allVariations.push(current);
            return;
        }
        for (const char of options[index]) {
            build(current + char, index + 1);
        }
    }

    build();
    return allVariations;
}

const variations = generateVariations();

function randomChar() {
    return allChars[Math.floor(Math.random() * allChars.length)];
}

async function hackerShuffle(newText) {
    const delay = (ms) => new Promise((res) => setTimeout(res, ms));
    const shuffleRounds = 10;
    const shuffleSpeed = 100;

    for (let round = 0; round < shuffleRounds; round++) {
        let tempText = '';
        for (let i = 0; i < newText.length; i++) {
            // Show correct char if in final round, else random
            tempText += (round === shuffleRounds - 1) ? newText[i] : randomChar();
        }
        titleElement.textContent = tempText;
        await delay(shuffleSpeed);
    }
}

async function startLoop() {
    let previousIndex = -1;
    while (true) {
        let index;
        do {
            index = Math.floor(Math.random() * variations.length);
        } while (index === previousIndex);

        previousIndex = index;
        await hackerShuffle(variations[index]);
        await new Promise(res => setTimeout(res, 3000)); // Wait before next shuffle
    }
}

startLoop();