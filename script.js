async function uploadPDF() {
  const input = document.getElementById('pdfInput');
  const file = input.files[0];

  if (!file) {
    alert("Please upload a PDF");
    return;
  }

  const formData = new FormData();
  formData.append("pdf", file);

  const output = document.getElementById('output');
  output.innerText = "Analyzing document...";

  try {
    const response = await fetch("http://127.0.0.1:5000/analyze", {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();
    output.innerText = data.summary;
  } catch (err) {
    output.innerText = "Error: " + err.message;
    console.error(err);
  }
}
