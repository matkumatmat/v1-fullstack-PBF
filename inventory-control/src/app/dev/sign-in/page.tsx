'use client';

import { useRouter } from 'next/navigation';

export default function DevSignInPage() {
  const router = useRouter();

  const handleSignIn = async (role: 'admin' | 'developer' | 'guest') => {
    try {
      const response = await fetch('/api/dev-auth', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ role }),
      });

      if (response.ok) {
        // Redirect to the appropriate dashboard after successful sign-in
        switch (role) {
          case 'admin':
            router.push('/admin');
            break;
          case 'developer':
            router.push('/developer');
            break;
          case 'guest':
            router.push('/guest');
            break;
        }
      } else {
        // Handle errors, e.g., show a message to the user
        console.error('Failed to set role:', await response.text());
        alert('There was an error signing in. Please try again.');
      }
    } catch (error) {
      console.error('An unexpected error occurred:', error);
      alert('An unexpected error occurred. Please try again.');
    }
  };

  // This page should only be available in development
  if (process.env.NODE_ENV !== 'development') {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <h1>404 - Not Found</h1>
        <p>This page is only available in the development environment.</p>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh', gap: '20px' }}>
      <h1>Development Sign-in</h1>
      <p>Click a button to sign in as a specific role.</p>
      <div style={{ display: 'flex', gap: '10px' }}>
        <button onClick={() => handleSignIn('admin')} style={{ padding: '10px 20px', fontSize: '16px' }}>
          Sign in as Admin
        </button>
        <button onClick={() => handleSignIn('developer')} style={{ padding: '10px 20px', fontSize: '16px' }}>
          Sign in as Developer
        </button>
        <button onClick={() => handleSignIn('guest')} style={{ padding: '10px 20px', fontSize: '16px' }}>
          Sign in as Guest
        </button>
      </div>
    </div>
  );
}
