'use client'

import { useState } from 'react';

export default function Home() {
  const [url, setUrl] = useState('');
  const [qrCodeUrl, setQrCodeUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setQrCodeUrl('');

    try {
      // Call the NextJS API route (not the Python API directly)
      // This route will proxy the request to the Python backend
      const response = await fetch('/api/qr', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to generate QR code');
      }

      const data = await response.json();
      console.log('QR Code generated:', data);
      
      // Set the QR code URL from the response
      setQrCodeUrl(data.qr_code_url);
      
    } catch (err) {
      console.error('Error generating QR Code:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>QR Code Generator</h1>
      
      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter URL like https://example.com"
          style={styles.input}
          required
        />
        <button 
          type="submit" 
          style={{
            ...styles.button,
            backgroundColor: loading ? '#555' : '#0070f3',
            cursor: loading ? 'not-allowed' : 'pointer',
          }}
          disabled={loading}
        >
          {loading ? 'Generating...' : 'Generate QR Code'}
        </button>
      </form>

      {error && (
        <div style={styles.error}>
          <p style={{ margin: 0, fontWeight: 'bold' }}>Error:</p>
          <p style={{ margin: '5px 0 0 0' }}>{error}</p>
        </div>
      )}

      {qrCodeUrl && (
        <div style={styles.qrCodeContainer}>
          <img src={qrCodeUrl} alt="QR Code" style={styles.qrCode} />
          <a 
            href={qrCodeUrl} 
            download 
            style={styles.downloadButton}
            target="_blank"
            rel="noopener noreferrer"
          >
            Download QR Code
          </a>
        </div>
      )}
    </div>
  );
}

// Styles
const styles = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#121212',
    color: 'white',
    padding: '20px',
  },
  title: {
    margin: '0 0 40px 0',
    lineHeight: '1.15',
    fontSize: '4rem',
    textAlign: 'center',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    width: '100%',
    maxWidth: '400px',
  },
  input: {
    padding: '10px',
    borderRadius: '5px',
    border: 'none',
    marginTop: '20px',
    width: '100%',
    color: '#121212',
    fontSize: '16px',
  },
  button: {
    padding: '10px 20px',
    marginTop: '20px',
    border: 'none',
    borderRadius: '5px',
    backgroundColor: '#0070f3',
    color: 'white',
    cursor: 'pointer',
    fontSize: '16px',
    fontWeight: 'bold',
    transition: 'background-color 0.3s',
    width: '100%',
  },
  error: {
    marginTop: '20px',
    padding: '15px',
    backgroundColor: '#ff4444',
    borderRadius: '5px',
    maxWidth: '400px',
    width: '100%',
    textAlign: 'center',
  },
  qrCodeContainer: {
    marginTop: '30px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '20px',
  },
  qrCode: {
    marginTop: '20px',
    border: '5px solid white',
    borderRadius: '10px',
    maxWidth: '100%',
    height: 'auto',
  },
  downloadButton: {
    padding: '10px 20px',
    backgroundColor: '#00b894',
    color: 'white',
    textDecoration: 'none',
    borderRadius: '5px',
    fontSize: '16px',
    fontWeight: 'bold',
    transition: 'background-color 0.3s',
  },
};