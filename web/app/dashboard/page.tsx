async function getTrending(region: string) {
  const base = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';
  try {
    const res = await fetch(`${base}/api/trending?region=${region}`, {
      cache: 'no-store',
      headers: { Authorization: 'Basic ' + Buffer.from('admin:admin').toString('base64') },
    });
    return res.ok ? res.json() : [];
  } catch {
    return [];
  }
}

export default async function Dashboard() {
  const ru = await getTrending('RU');
  const us = await getTrending('US');
  const mix = await getTrending('MIX');
  const demo = ru.length + us.length + mix.length === 0;

  return (
    <div>
      <h2>Dashboard</h2>
      {demo ? (
        <p>Demo mode: API недоступен, показываем пустой дашборд (поднимите backend).</p>
      ) : (
        <p>Top RU: {ru.length} | Top US: {us.length} | MIX: {mix.length}</p>
      )}
      <p>Use Trending page for detailed metrics and explainability.</p>
    </div>
  );
}
