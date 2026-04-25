# index.py
import io
import base64
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR Code Generator</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: linear-gradient(135deg, #f5f7fe 0%, #e9eef8 100%);
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }

        .card {
            max-width: 1200px;
            width: 100%;
            background: white;
            border-radius: 48px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15);
            overflow: hidden;
            transition: transform 0.2s ease;
        }

        .card-content {
            padding: 3rem;
        }

        /* Header Section */
        .header {
            text-align: center;
            margin-bottom: 3rem;
        }

        .badge {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 1rem;
        }

        h1 {
            font-size: 2.8rem;
            font-weight: 800;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            margin-bottom: 1rem;
        }

        .subtitle {
            color: #5a6874;
            font-size: 1.1rem;
            max-width: 500px;
            margin: 0 auto;
            line-height: 1.5;
        }

        /* Features Grid */
        .features {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.5rem;
            margin-bottom: 3rem;
        }

        .feature-item {
            text-align: center;
            padding: 1rem;
            background: #f8fafc;
            border-radius: 24px;
            transition: all 0.2s ease;
        }

        .feature-item:hover {
            background: #f1f5f9;
            transform: translateY(-2px);
        }

        .feature-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }

        .feature-title {
            font-weight: 600;
            color: #1e293b;
            font-size: 0.9rem;
        }

        /* Main Generator Area */
        .generator-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 3rem;
            margin-bottom: 2rem;
        }

        /* Input Section */
        .input-section {
            background: #f8fafc;
            border-radius: 32px;
            padding: 1.5rem;
        }

        .section-label {
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
            color: #64748b;
            margin-bottom: 1rem;
        }

        .url-input {
            width: 100%;
            padding: 1rem 1.25rem;
            font-size: 1rem;
            border: 2px solid #e2e8f0;
            border-radius: 24px;
            font-family: 'Inter', monospace;
            transition: all 0.2s ease;
            background: white;
            margin-bottom: 1rem;
        }

        .url-input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .design-options {
            margin-bottom: 1.5rem;
        }

        .color-picker-group {
            display: flex;
            gap: 1rem;
            margin-bottom: 1rem;
            flex-wrap: wrap;
        }

        .color-field {
            flex: 1;
        }

        .color-field label {
            display: block;
            font-size: 0.75rem;
            font-weight: 500;
            color: #475569;
            margin-bottom: 0.25rem;
        }

        .color-input {
            width: 100%;
            height: 48px;
            border: 2px solid #e2e8f0;
            border-radius: 16px;
            cursor: pointer;
            padding: 4px;
            background: white;
        }

        .color-input:focus {
            outline: none;
            border-color: #667eea;
        }

        .generate-btn {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 1rem;
            font-size: 1rem;
            font-weight: 600;
            border-radius: 40px;
            cursor: pointer;
            transition: transform 0.1s ease, box-shadow 0.2s ease;
            font-family: 'Inter', sans-serif;
            letter-spacing: 0.5px;
        }

        .generate-btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 20px -5px rgba(102, 126, 234, 0.4);
        }

        .generate-btn:active {
            transform: translateY(1px);
        }

        /* QR Code Display */
        .output-section {
            background: #f8fafc;
            border-radius: 32px;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
        }

        .qr-container {
            background: white;
            padding: 1.5rem;
            border-radius: 24px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
            margin-bottom: 1rem;
            display: inline-block;
        }

        .qr-image {
            max-width: 220px;
            height: auto;
            display: block;
        }

        .placeholder-qr {
            width: 220px;
            height: 220px;
            background: #f1f5f9;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #94a3b8;
            font-size: 0.85rem;
            text-align: center;
            flex-direction: column;
            gap: 0.5rem;
        }

        .download-btn {
            background: white;
            border: 2px solid #e2e8f0;
            padding: 0.75rem 1.5rem;
            border-radius: 40px;
            font-weight: 600;
            color: #1e293b;
            cursor: pointer;
            transition: all 0.2s ease;
            font-family: 'Inter', sans-serif;
            margin-top: 0.5rem;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }

        .download-btn:hover {
            border-color: #667eea;
            background: #f8fafc;
        }

        .example-hint {
            font-size: 0.75rem;
            color: #94a3b8;
            margin-top: 0.5rem;
        }

        /* Footer */
        .footer {
            text-align: center;
            padding-top: 2rem;
            border-top: 1px solid #e2e8f0;
            margin-top: 1rem;
            color: #94a3b8;
            font-size: 0.8rem;
        }

        @media (max-width: 768px) {
            .card-content {
                padding: 1.5rem;
            }
            .generator-grid {
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }
            .features {
                grid-template-columns: repeat(2, 1fr);
                gap: 1rem;
            }
            h1 {
                font-size: 1.8rem;
            }
        }

        .loader {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 0.6s linear infinite;
            margin-right: 8px;
            vertical-align: middle;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="card">
        <div class="card-content">
            <div class="header">
                <div class="badge">QR CODE GENERATOR</div>
                <h1>Create custom QR codes</h1>
                <p class="subtitle">for URLs, text, contacts, Wi-Fi and more in just a few clicks.</p>
            </div>

            <div class="features">
                <div class="feature-item">
                    <div class="feature-icon">⚡</div>
                    <div class="feature-title">Instant Generation</div>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">🔗</div>
                    <div class="feature-title">URL & Text Support</div>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">🎨</div>
                    <div class="feature-title">Customizable Design</div>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">📥</div>
                    <div class="feature-title">Download High Quality</div>
                </div>
            </div>

            <div class="generator-grid">
                <div class="input-section">
                    <div class="section-label">📝 CONTENT & DESIGN</div>
                    <input type="text" id="qrData" class="url-input" placeholder="https://example.com" value="https://example.com">
                    <div class="design-options">
                        <div class="color-picker-group">
                            <div class="color-field">
                                <label>🎨 QR Color</label>
                                <input type="color" id="fillColor" class="color-input" value="#1a1a2e">
                            </div>
                            <div class="color-field">
                                <label>⬜ Background</label>
                                <input type="color" id="backColor" class="color-input" value="#ffffff">
                            </div>
                        </div>
                    </div>
                    <button id="generateBtn" class="generate-btn">✨ GENERATE QR CODE</button>
                    <div class="example-hint">Try: https://github.com, mailto:hello@example.com, or any text</div>
                </div>

                <div class="output-section">
                    <div class="section-label">📱 YOUR QR CODE</div>
                    <div id="qrDisplay" class="qr-container">
                        <div class="placeholder-qr">
                            <span>⬚</span>
                            <span>Your QR code will appear here</span>
                        </div>
                    </div>
                    <a id="downloadLink" class="download-btn" download="qrcode.png" style="pointer-events: none; opacity: 0.5;">📸 Download PNG</a>
                </div>
            </div>
            <div class="footer">
                Free • Instant • Customizable QR Codes
            </div>
        </div>
    </div>

    <script>
        const generateBtn = document.getElementById('generateBtn');
        const qrDataInput = document.getElementById('qrData');
        const fillColorPicker = document.getElementById('fillColor');
        const backColorPicker = document.getElementById('backColor');
        const qrDisplay = document.getElementById('qrDisplay');
        const downloadLink = document.getElementById('downloadLink');

        async function generateQRCode() {
            const data = qrDataInput.value.trim();
            if (!data) {
                alert('Please enter a URL or text');
                return;
            }

            const fillColor = fillColorPicker.value;
            const backColor = backColorPicker.value;

            // Show loading state
            generateBtn.innerHTML = '<span class="loader"></span> Generating...';
            generateBtn.disabled = true;

            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        data: data,
                        fill_color: fillColor,
                        back_color: backColor
                    })
                });

                if (!response.ok) {
                    throw new Error('Generation failed');
                }

                const result = await response.json();
                const qrImageUrl = result.qr_image;
                
                // Update display
                qrDisplay.innerHTML = `<img src="${qrImageUrl}" class="qr-image" alt="QR Code">`;
                
                // Enable download link
                downloadLink.href = qrImageUrl;
                downloadLink.style.pointerEvents = 'auto';
                downloadLink.style.opacity = '1';
                
            } catch (error) {
                console.error('Error:', error);
                qrDisplay.innerHTML = '<div class="placeholder-qr"><span>⚠️</span><span>Error generating QR code. Please try again.</span></div>';
                alert('Failed to generate QR code. Make sure the server is running.');
            } finally {
                generateBtn.innerHTML = '✨ GENERATE QR CODE';
                generateBtn.disabled = false;
            }
        }

        generateBtn.addEventListener('click', generateQRCode);
        
        // Allow Enter key to generate
        qrDataInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                generateQRCode();
            }
        });
        
        // Auto-generate on color change (optional, but convenient)
        let debounceTimer;
        function autoGenerate() {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                if (qrDataInput.value.trim()) {
                    generateQRCode();
                }
            }, 500);
        }
        
        fillColorPicker.addEventListener('input', autoGenerate);
        backColorPicker.addEventListener('input', autoGenerate);
        
        // Initial generation on page load
        window.addEventListener('load', () => {
            generateQRCode();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    content = data.get('data', '')
    fill_color = data.get('fill_color', '#1a1a2e')
    back_color = data.get('back_color', '#ffffff')
    
    if not content:
        return jsonify({'error': 'No content provided'}), 400
    
    # Create QR Code instance
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(content)
    qr.make(fit=True)
    
    # Create styled image
    try:
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            color_mask=SolidFillColorMask(
                back_color=back_color,
                front_color=fill_color
            )
        )
    except Exception:
        # Fallback to standard QR if styled fails
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
    
    # Save to bytes and encode as base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return jsonify({
        'qr_image': f'data:image/png;base64,{image_base64}'
    })

if __name__ == '__main__':
    import threading
    import webbrowser

    def open_browser():
        webbrowser.open('http://127.0.0.1:5000')

    threading.Timer(1.0, open_browser).start()
    app.run(debug=True, host='0.0.0.0', port=5000)