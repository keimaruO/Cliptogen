const memoStyle = `
  position: fixed;
  bottom: 0;
  left: 0;
  background-color: white;
  z-index: 9999;
  padding: 20px;
  border: 1px solid #ccc;
  font-family: Meiryo;
  font-size: 16px;
`;

const memoContainer = document.createElement('div');
memoContainer.setAttribute('style', memoStyle);

const urlInput = document.createElement('input');
const startTimeInput = document.createElement('input');
const endTimeInput = document.createElement('input');

urlInput.placeholder = 'URL';
startTimeInput.placeholder = '開始時間';
endTimeInput.placeholder = '終了時間';

urlInput.value = location.href;

memoContainer.appendChild(urlInput);
memoContainer.appendChild(startTimeInput);
memoContainer.appendChild(endTimeInput);

const displayArea = document.createElement('div');
memoContainer.appendChild(displayArea);

document.body.appendChild(memoContainer);

const savedTimeSegments = [];

function getCurrentTime() {
  const video = document.querySelector('video');
  if (video) {
    const timeInSeconds = video.currentTime;
    const hours = Math.floor(timeInSeconds / 3600);
    const minutes = Math.floor((timeInSeconds % 3600) / 60);
    const seconds = Math.floor(timeInSeconds % 60);
    return (hours > 0 ? hours + ':' : '') + String(minutes).padStart(2, '0') + ':' + String(seconds).padStart(2, '0');
  }
  return null;
}

function updateDisplayArea() {
  displayArea.innerHTML = savedTimeSegments.join('<br>');
}

document.addEventListener('keydown', (event) => {
  if (event.ctrlKey) {
    switch (event.key) {
      case 'z':
      case 'Z':
        startTimeInput.value = getCurrentTime();
        break;
      case 'x':
      case 'X':
        endTimeInput.value = getCurrentTime();
        break;
      case 'c':
      case 'C':
        if (startTimeInput.value && endTimeInput.value) {
          savedTimeSegments.push(`${startTimeInput.value}-${endTimeInput.value}`);
          updateDisplayArea();
          startTimeInput.value = '';
          endTimeInput.value = '';
        }
        break;
      case 'q':
      case 'Q':
        if (savedTimeSegments.length > 0) {
          urlInput.value = location.href;
          const formattedTimeSegments = savedTimeSegments.join('\n');
          const fullOutput = `${urlInput.value}\n${formattedTimeSegments}`;
          navigator.clipboard.writeText(fullOutput);
          savedTimeSegments.length = 0;
          updateDisplayArea();
        }
        break;
    }
  }
});
