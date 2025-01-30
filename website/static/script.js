let fileCount = 0;
let urlCount = 0;

// Toggle Dark/Day mode
document.querySelector('#toggleModeBtn').addEventListener('click', function () {
    document.body.classList.toggle('bg-dark');
    document.body.classList.toggle('text-light');
    const modeBtn = document.querySelector('#toggleModeBtn');
    modeBtn.textContent = modeBtn.textContent === 'Day' ? 'Night' : 'Day';
});

// Login button functionality
document.querySelector('#loginBtn').addEventListener('click', function() {
    alert('Redirecting to Login...');
    // Add login logic here
});

// Handle file upload
document.querySelector('#uploadBtn').addEventListener('click', function() {
    document.querySelector('#fileInput').click();  // Trigger the file input click
});

document.querySelector('#fileInput').addEventListener('change', function(event) {
    const uploadedFiles = document.querySelector('#uploadedFiles');
    const noFilesText = document.querySelector('#noFilesText');
    const fileCountDisplay = document.querySelector('#fileCount');
    
    const files = event.target.files;
    const totalFiles = fileCount + files.length;
    if (totalFiles <= 5) {
        Array.from(files).forEach(file => {
            const li = document.createElement('li');
            li.innerHTML = `${file.name} <button class="btn btn-danger btn-sm" onclick="removeFile(this)">❌</button>`;
            uploadedFiles.appendChild(li);
        });
        
        fileCount += files.length;
        fileCountDisplay.textContent = `Files: ${fileCount}`;
        
        if (fileCount > 0) {
            noFilesText.style.display = 'none';
            uploadedFiles.classList.add('active');
        }

        // Update URL placeholders based on file count
        updateUrlPlaceholders();
    }
});

// Remove file from list (optional)
function removeFile(button) {
    button.parentElement.remove();
    fileCount--;
    const uploadedFiles = document.querySelector('#uploadedFiles');
    const fileCountDisplay = document.querySelector('#fileCount');
    
    fileCountDisplay.textContent = `Files: ${fileCount}`;

    // Hide file list if no files left
    if (fileCount === 0) {
        document.querySelector('#noFilesText').style.display = 'block';
        uploadedFiles.classList.remove('active');
    }

    // Update URL placeholders
    updateUrlPlaceholders();
}

// Handle URL upload
document.querySelector('#uploadUrlBtn').addEventListener('click', function() {
    if (urlCount + fileCount < 5) {
        document.querySelector('#urlPlaceholders').style.display = 'block';
    }
});

// Update URL placeholders visibility based on file count
function updateUrlPlaceholders() {
    const remainingSlots = 5 - fileCount;
    const urlPlaceholders = document.querySelector('#urlPlaceholders');
    const urlInputs = urlPlaceholders.querySelectorAll('input');
    
    // Show only the remaining number of URL placeholders
    urlInputs.forEach((input, index) => {
        if (index < remainingSlots) {
            input.style.display = 'block';
        } else {
            input.style.display = 'none';
        }
    });

    // Update URL count display
    document.querySelector('#urlCount').textContent = `URLs: ${urlCount}`;
}

// Delete all files
document.querySelector('#deleteAllBtn').addEventListener('click', function() {
    const uploadedFiles = document.querySelector('#uploadedFiles');
    const fileCountDisplay = document.querySelector('#fileCount');
    
    uploadedFiles.innerHTML = '';  // Clear the list
    fileCount = 0;  // Reset file count
    fileCountDisplay.textContent = 'Files: 0';  // Reset file count
    document.querySelector('#noFilesText').style.display = 'block';  // Show 'No files uploaded' text

    // Update URL placeholders
    updateUrlPlaceholders();
});

// Toggle Sidebar visibility (☰ button)
document.querySelector('#toggleSidebarBtn').addEventListener('click', function() {
    const sidebar = document.getElementById('leftSidebar');
    const mainContent = document.getElementById('mainContent');
    sidebar.classList.toggle('open');
    mainContent.classList.toggle('open-sidebar');
});
