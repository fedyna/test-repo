export const dynamic = 'force-dynamic';

type TrendRow = {
  yt_video_id: string;
  title: string;
  channel_title: string;
  region: string;
  score_total: number;
  explanation_json?: { why?: string };
};

const demoRows: TrendRow[] = [
  {
    yt_video_id: 'demo1',
    title: 'Claude Code + n8n: автопилот для саппорта',
    channel_title: 'Automation Lab RU',
    region: 'RU',
    score_total: 3.42,
    explanation_json: { why: '24h views growth: +12 400; velocity +2.1σ vs baseline' },
  },
  {
    yt_video_id: 'demo2',
    title: 'Codex Agents for DevOps Workflows',
    channel_title: 'US Agentic Ops',
    region: 'US',
    score_total: 2.88,
    explanation_json: { why: 'Stable 48h acceleration with strong engagement velocity' },
  },
];

async function getData(): Promise<TrendRow[]> {
  const base = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';
  try {
    const res = await fetch(`${base}/api/trending?region=MIX`, {
      cache: 'no-store',
      headers: { Authorization: 'Basic ' + Buffer.from('admin:admin').toString('base64') },
    });
    return res.ok ? res.json() : demoRows;
  } catch {
    return demoRows;
  }
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
          {rows.map((r) => (
            <tr key={r.yt_video_id}>
              <td>{r.title}</td><td>{r.channel_title}</td><td>{r.region}</td><td>{Number(r.score_total).toFixed(2)}</td><td>{r.explanation_json?.why}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
