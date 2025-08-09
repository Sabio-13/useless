document.addEventListener('DOMContentLoaded', () => {
    const qrForm = document.getElementById('qrForm');
    const resultContainer = document.getElementById('resultContainer');
    const qrResult = document.getElementById('qrResult');
    const downloadBtn = document.getElementById('downloadBtn');
    
    qrForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(qrForm);
        const url = formData.get('url');
        
        if (!url) {
            alert('Please enter a valid URL');
            return;
        }
        
        try {
            const response = await fetch('/generate_qr', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error('Failed to generate QR code');
            }
            
            const blob = await response.blob();
            const objectURL = URL.createObjectURL(blob);
            
            // Display QR code
            qrResult.innerHTML = `<img src="${objectURL}" alt="Generated QR Code">`;
            resultContainer.classList.remove('hidden');
            
            // Set up download button
            downloadBtn.onclick = () => {
                const a = document.createElement('a');
                a.href = objectURL;
                a.download = 'qr-code.png';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            };
            
        } catch (error) {
            console.error('Error:', error);
            alert('Error generating QR code. Please try again.');
        }
    });
});