import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const { role } = await request.json();

    if (!role || !['admin', 'developer', 'guest'].includes(role)) {
      return NextResponse.json({ success: false, message: 'Invalid role specified.' }, { status: 400 });
    }

    // Create a response
    const response = NextResponse.json({ success: true, message: `Role set to ${role}` });

    // Set the cookie on the response
    response.cookies.set('user-role', role, {
      httpOnly: true,
      path: '/',
    });

    return response;
  } catch (error) {
    const errorResponse = NextResponse.json({ success: false, message: 'An unexpected error occurred.' }, { status: 500 });
    return errorResponse;
  }
}
