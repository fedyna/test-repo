export const dynamic = 'force-dynamic';

async function getData() {
  const base = process.env.NEXT_PUBLIC_API_BASE || 'http://api:8000';
  const res = await fetch(`${base}/api/trending?region=MIX`, { cache: 'no-store', headers: { Authorization: 'Basic ' + Buffer.from('admin:admin').toString('base64') } });
  return res.ok ? res.json() : [];
}

export default async function TrendingPage() {
  const rows = await getData();
  return (
    <div>
      <h2>Trending Videos</h2>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr><th>Title</th><th>Channel</th><th>Region</th><th>Score</th><th>Why trending</th></tr>
        </thead>
        <tbody>
          {rows.map((r: any) => (
            <tr key={r.yt_video_id}>
              <td>{r.title}</td><td>{r.channel_title}</td><td>{r.region}</td><td>{Number(r.score_total).toFixed(2)}</td><td>{r.explanation_json?.why}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
