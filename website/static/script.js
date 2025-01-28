// Handle form submission and multiple file upload
document.getElementById('uploadForm').addEventListener('submit', async function(e) {
    e.preventDefault();  // Prevent the default form submission

    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();

    // Append all selected files to FormData
    for (const file of fileInput.files) {
        formData.append('files', file);
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/upload/', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('File upload failed');
        }

        const data = await response.json();
        if (data.extracted_data) {
            // Display the extracted data for each file
            document.getElementById('result').style.display = 'block';
            document.getElementById('extractedData').textContent = JSON.stringify(data.extracted_data, null, 2);
        } else {
            alert('No extracted data available');
        }
    } catch (error) {
        alert('Error uploading file: ' + error.message);
    }
});
