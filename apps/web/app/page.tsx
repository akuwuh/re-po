import Link from 'next/link';

export default function HomePage() {
  return (
    <div style={{ display: 'grid', gap: '1.5rem', maxWidth: '640px' }}>
      <h1>re-po</h1>
      <p>
        Render GitHub statistics cards with a shared Python core, FastAPI delivery, and a reusable GitHub Action. Visit the{' '}
        <Link href="/builder">builder</Link> to configure an embed or workflow.
      </p>
    </div>
  );
}
