async function getTrending(region: string) {
  const base = process.env.NEXT_PUBLIC_API_BASE || 'http://api:8000';
  const res = await fetch(`${base}/api/trending?region=${region}`, { cache: 'no-store', headers: { Authorization: 'Basic ' + Buffer.from('admin:admin').toString('base64') } });
  return res.ok ? res.json() : [];
}

export default async function Dashboard() {
  const ru = await getTrending('RU');
  const us = await getTrending('US');
  const mix = await getTrending('MIX');
  return (
    <div>
      <h2>Dashboard</h2>
      <p>Top RU: {ru.length} | Top US: {us.length} | MIX: {mix.length}</p>
      <p>Use Trending page for detailed metrics and explainability.</p>
    </div>
  );
}
