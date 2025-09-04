import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  const role = request.cookies.get('user-role')?.value || 'guest';
  const { pathname } = request.nextUrl;
  const isDevelopment = process.env.NODE_ENV === 'development';

  const getRedirectUrl = () => {
    return isDevelopment ? '/dev/sign-in' : '/auth/sign-in';
  };

  // Rule for admin routes
  if (pathname.startsWith('/admin')) {
    if (role !== 'admin') {
      return NextResponse.redirect(new URL(getRedirectUrl(), request.url));
    }
  }

  // Rule for developer routes
  if (pathname.startsWith('/developer')) {
    if (role !== 'admin' && role !== 'developer') {
      return NextResponse.redirect(new URL(getRedirectUrl(), request.url));
    }
  }

  // For guest routes, no specific check is needed as it's the lowest access level.
  // Anyone can access guest routes.

  return NextResponse.next();
}

export const config = {
  matcher: [
    // Skip Next.js internals and all static files, unless found in search params
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    // Always run for API routes
    '/(api|trpc)(.*)'
  ]
};
