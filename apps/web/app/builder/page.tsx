'use client';

import { useMemo, useState } from 'react';
import Link from 'next/link';

import { buildWorkflowYaml } from '../../lib/yaml';
import { Preview } from '../../components/Preview';

const themes = [
  { id: 'terminal', label: 'Terminal (dark)' },
  { id: 'light', label: 'Terminal (light)' },
];

const formats = [
  { id: 'svg', label: 'SVG' },
  { id: 'txt', label: 'Text' },
];

export default function BuilderPage() {
  const [user, setUser] = useState('akuwuh');
  const [format, setFormat] = useState<'txt' | 'svg'>('svg');
  const [theme, setTheme] = useState('terminal');
  const [width, setWidth] = useState<number | undefined>(640);
  const [apiBase, setApiBase] = useState('http://localhost:8000');

  const embedUrl = useMemo(() => {
    const params = new URLSearchParams({ user, format, theme });
    if (format === 'svg' && width) {
      params.set('width', String(width));
    }
    return `${apiBase.replace(/\/$/, '')}/v1/card?${params.toString()}`;
  }, [apiBase, user, format, theme, width]);

  const workflowYaml = useMemo(
    () =>
      buildWorkflowYaml({
        user,
        format,
        theme,
        output: format === 'svg' ? 're-po.svg' : 're-po.txt',
      }),
    [user, format, theme],
  );

  return (
    <div style={{ display: 'grid', gap: '2rem', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))' }}>
      <section>
        <h1 style={{ marginBottom: '1rem' }}>re-po builder</h1>
        <p style={{ opacity: 0.8, lineHeight: 1.6 }}>
          Configure a GitHub stats card and preview it instantly. Copy the embed URL or drop the reusable workflow into your
          repository.
        </p>

        <fieldset>
          <label htmlFor="user">GitHub username</label>
          <input id="user" value={user} onChange={(event) => setUser(event.target.value)} placeholder="octocat" />
        </fieldset>

        <fieldset>
          <label htmlFor="format">Format</label>
          <select
            id="format"
            value={format}
            onChange={(event) => setFormat(event.target.value as 'txt' | 'svg')}
          >
            {formats.map((item) => (
              <option key={item.id} value={item.id}>
                {item.label}
              </option>
            ))}
          </select>
        </fieldset>

        <fieldset>
          <label htmlFor="theme">Theme</label>
          <select id="theme" value={theme} onChange={(event) => setTheme(event.target.value)}>
            {themes.map((item) => (
              <option key={item.id} value={item.id}>
                {item.label}
              </option>
            ))}
          </select>
        </fieldset>

        {format === 'svg' && (
          <fieldset>
            <label htmlFor="width">Width</label>
            <input
              id="width"
              type="number"
              min={320}
              max={1200}
              value={width ?? ''}
              onChange={(event) => setWidth(event.target.value ? Number(event.target.value) : undefined)}
            />
          </fieldset>
        )}

        <fieldset>
          <label htmlFor="api-base">API base URL</label>
          <input
            id="api-base"
            value={apiBase}
            onChange={(event) => setApiBase(event.target.value)}
            placeholder="https://api.example.com"
          />
        </fieldset>

        <fieldset>
          <label>Embed URL</label>
          <input readOnly value={embedUrl} onFocus={(event) => event.target.select()} />
        </fieldset>

        <fieldset>
          <label>Reusable workflow YAML</label>
          <textarea readOnly value={workflowYaml} rows={12} onFocus={(event) => event.target.select()} />
        </fieldset>

        <p style={{ opacity: 0.8 }}>
          Need help? See the <Link href="https://github.com/akuwuh/re-po">project README</Link> for full documentation.
        </p>
      </section>

      <section>
        <h2 style={{ marginBottom: '1rem' }}>Live preview</h2>
        <Preview url={embedUrl} format={format} />
      </section>
    </div>
  );
}
