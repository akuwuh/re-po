export type WorkflowOptions = {
  user: string;
  format: 'txt' | 'svg';
  theme: string;
  output: string;
};

export function buildWorkflowYaml(options: WorkflowOptions): string {
  const { user, format, theme, output } = options;
  return `name: Update re-po card
on:
  schedule:
    - cron: "0 0 * * *"
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: akuwuh/re-po/actions/re-po-action@main
        with:
          user: ${user}
          format: ${format}
          theme: ${theme}
          out: ${output}
      - name: Commit card
        run: |
          git config user.name "re-po bot"
          git config user.email "re-po@users.noreply.github.com"
          git add ${output}
          git commit -m "Update re-po card" || echo "Nothing to commit"
          git push
`;
}
