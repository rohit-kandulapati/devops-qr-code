import { NextResponse } from 'next/server';

export async function POST(req) {
	  const { url } = await req.json();

	  try {
		      const backendResponse = await fetch(
			            `${process.env.API_BASE_URL}/generate-qr/?url=${encodeURIComponent(url)}`,
			            { method: 'POST' }
			          );

		      const data = await backendResponse.json();
		      return NextResponse.json(data);
		    } catch (err) {
			        console.error(err);
			        return NextResponse.json(
					      { message: 'Backend error' },
					      { status: 500 }
					    );
			      }
}
