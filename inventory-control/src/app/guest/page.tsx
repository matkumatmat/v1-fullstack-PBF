import { redirect } from 'next/navigation';

export default function GuestPage() {
  redirect('/guest/dashboard/overview');
}
