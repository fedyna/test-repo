export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ru">
      <body style={{ fontFamily: 'Inter, sans-serif', margin: 20, background: '#0a0a0a', color: '#f5f5f5' }}>
        <h1>YouTube Trend Radar</h1>
        {children}
      </body>
    </html>
  );
}
