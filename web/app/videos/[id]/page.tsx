export default async function VideoDetail({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return <div><h2>Video Detail</h2><p>Video ID: {id}</p><p>Snapshot charts and score breakdown can be rendered from /api endpoints.</p></div>;
}
