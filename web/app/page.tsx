import Link from 'next/link';

export default function Home() {
  return (
    <main>
      <p>Single-user dashboard for RU/US automation + AI trends.</p>
      <ul>
        <li><Link href="/dashboard">Dashboard</Link></li>
        <li><Link href="/trending">Trending Videos</Link></li>
        <li><Link href="/channels">Channels</Link></li>
        <li><Link href="/settings">Settings</Link></li>
      </ul>
    </main>
  );
}
