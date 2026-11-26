export function speakManeuver(instructionText) {
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(instructionText);
    utterance.rate = 1.05;
    utterance.volume = 0.85;
    window.speechSynthesis.speak(utterance);
  }
}
