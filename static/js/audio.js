// static/js/audio.js
const clickAudio = new Audio('/soundreality-ding-411634.mp3');
const winAudio = new Audio('/universfield-interface-124464.mp3');

function playSound(audio) {
    audio.currentTime = 0;
    audio.play().catch(e => console.warn('Audio blocked:', e));
}

document.addEventListener('click', function(e) {
    if (e.target.tagName === 'BUTTON') {
        const btnText = e.target.innerText.trim();
        if (btnText === 'X' || btnText === 'O') {
            playSound(clickAudio);
        }
    }
}, true);

const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        mutation.addedNodes.forEach(function(node) {
            if (node.textContent && node.textContent.includes('Congratulations')) {
                playSound(winAudio);
            }
        });
    });
});
observer.observe(document.body, { childList: true, subtree: true });
