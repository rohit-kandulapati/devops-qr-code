// This is a Next.js 13+ App Router API route
// It runs on the server, not in the browser

export async function POST(request) {
  try {
    // Get the API URL from environment variable
    const API_URL = process.env.API_URL || 'http://localhost:8000';
    
    // Parse the incoming request body
    const body = await request.json();
    
    console.log(`[NextJS API Route] Proxying request to: ${API_URL}/generate`);
    console.log(`[NextJS API Route] Request body:`, body);

    // Make the request to the Python FastAPI backend
    const response = await fetch(`${API_URL}/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    // Check if the response is ok
    if (!response.ok) {
      const errorText = await response.text();
      console.error(`[NextJS API Route] API Error: ${response.status} - ${errorText}`);
      return Response.json(
        { error: 'Failed to generate QR code', details: errorText },
        { status: response.status }
      );
    }

    // Parse and return the successful response
    const data = await response.json();
    console.log(`[NextJS API Route] Success:`, data);
    
    return Response.json(data, { status: 200 });

  } catch (error) {
    console.error('[NextJS API Route] Error:', error);
    return Response.json(
      { error: 'Failed to connect to QR code service', details: error.message },
      { status: 500 }
    );
  }
}