function detectPneumonia() {
    const input = document.getElementById('imageUpload');
    const file = input.files[0];
    const formData = new FormData();
    formData.append('file', file);

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        document.getElementById('result').innerText = data.result;

        // Update medicines container
        var medicinesContainer = document.getElementById('medicinesContainer');
        medicinesContainer.innerHTML = ''; // Clear previous content

        // Display button for possible medications if result indicates pneumonia
        if (data.result === "Pneumonia Detected Please seek Medical Advice") {
            var medicationsButton = document.createElement('button');
            medicationsButton.textContent = 'Possible Medications';
            medicationsButton.onclick = function() {
                fetchMedications();
            };
            medicinesContainer.appendChild(medicationsButton);
        }
    })
    .catch(error => console.error('Error:', error));
}

function fetchMedications() {
    // Fetch medications from the server
    fetch('/medications')
        .then(response => response.json())
        .then(data => {
            displayMedications(data.medications);
        })
        .catch(error => console.error('Error:', error));
}

function displayMedications(medications) {
    // Update medicines container with medications list
    var medicinesContainer = document.getElementById('medicinesContainer');
    medicinesContainer.innerHTML = ''; // Clear previous content

    var medicinesList = document.createElement('ul');
    medications.forEach(function(medicine) {
        var listItem = document.createElement('li');
        listItem.textContent = `${medicine.name} - Substitute: ${medicine.substitute}`;
        medicinesList.appendChild(listItem);
    });
    medicinesContainer.appendChild(medicinesList);
}