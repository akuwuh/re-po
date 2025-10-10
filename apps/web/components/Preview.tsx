'use client';

import { useEffect, useState } from 'react';

type PreviewProps = {
  url: string;
  format: 'txt' | 'svg';
};

export function Preview({ url, format }: PreviewProps) {
  const [content, setContent] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let abort = false;
    setLoading(true);
    setError(null);

    fetch(url)
      .then(async (response) => {
        if (!response.ok) {
          throw new Error(`Request failed: ${response.status}`);
        }
        return response.text();
      })
      .then((text) => {
        if (!abort) {
          setContent(text);
        }
      })
      .catch((err) => {
        if (!abort) {
          setError(err.message);
        }
      })
      .finally(() => {
        if (!abort) {
          setLoading(false);
        }
      });

    return () => {
      abort = true;
    };
  }, [url]);

  if (loading) {
    return <p>Loading preview…</p>;
  }

  if (error) {
    return <p style={{ color: '#f87171' }}>Error: {error}</p>;
  }

  if (!content) {
    return <p>No data yet.</p>;
  }

  if (format === 'txt') {
    return <pre>{content}</pre>;
  }

  return (
    <div
      style={{
        maxWidth: '100%',
        borderRadius: '1rem',
        overflow: 'hidden',
        backgroundColor: 'rgba(0, 0, 0, 0.3)',
        padding: '1rem',
      }}
      dangerouslySetInnerHTML={{ __html: content }}
    />
  );
}
