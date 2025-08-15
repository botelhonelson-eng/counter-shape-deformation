
function startCalculation() {
  document.getElementById('upload-panel').classList.add('hidden');
  document.getElementById('viewer-panel').classList.remove('hidden');
}

function downloadTxt() {
  const element = document.createElement("a");
  const file = new Blob(["Resultado do cálculo de superfície deformada"], {type: 'text/plain'});
  element.href = URL.createObjectURL(file);
  element.download = "resultado.txt";
  document.body.appendChild(element);
  element.click();
}
