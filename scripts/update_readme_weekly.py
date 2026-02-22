#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timedelta
import re

repo = Path('.')
reports = repo / 'reports'
web = repo / 'web'
cutoff = datetime.now() - timedelta(days=7)

# filename time parsers
p1 = re.compile(r'(\d{8})_(\d{4})')
p2 = re.compile(r'(\d{8})_(\d{6})')
p3 = re.compile(r'(\d{4}-\d{2}-\d{2})_(\d{2})-(\d{2})')
p4 = re.compile(r'(\d{4}-\d{2}-\d{2})')

def extract_dt(name: str):
    m = p2.search(name)
    if m:
        return datetime.strptime(m.group(1)+m.group(2), '%Y%m%d%H%M%S')
    m = p1.search(name)
    if m:
        return datetime.strptime(m.group(1)+m.group(2), '%Y%m%d%H%M')
    m = p3.search(name)
    if m:
        return datetime.strptime(m.group(1)+m.group(2)+m.group(3), '%Y-%m-%d%H%M')
    m = p4.search(name)
    if m:
        return datetime.strptime(m.group(1)+'0000', '%Y-%m-%d%H%M')
    return None

def kind_of(stem: str):
    if stem.startswith('x_top_news_'):
        return 'x'
    if stem.startswith('threads_top_news_'):
        return 'threads'
    if stem.startswith('reddit_'):
        return 'reddit'
    return None

# gather md/html by stem
group = {}
for p in list(reports.glob('*.md')) + list(web.glob('*.html')):
    stem = p.stem
    kind = kind_of(stem)
    if not kind:
        continue
    dt = extract_dt(stem)
    if not dt or dt < cutoff:
        continue
    g = group.setdefault(stem, {'dt': dt, 'kind': kind, 'md': None, 'html': None})
    if dt > g['dt']:
        g['dt'] = dt
    if p.suffix == '.md':
        g['md'] = p
    else:
        g['html'] = p


def rows_for(kind):
    rows = []
    items = [(k, v) for k, v in group.items() if v['kind'] == kind]
    items.sort(key=lambda kv: kv[1]['dt'], reverse=True)
    for key, g in items:
        dt = g['dt'].strftime('%Y-%m-%d %H:%M')
        md_link = f"[MD](./{g['md'].as_posix()})" if g['md'] else '-'
        html_link = f"[HTML](./{g['html'].as_posix()})" if g['html'] else '-'
        page_link = f"[網頁版](https://gaskhuang.github.io/social-media-report/{g['html'].as_posix()})" if g['html'] else '-'
        rows.append(f"| {dt} | `{key}` | {md_link} | {html_link} | {page_link} |")
    if not rows:
        rows = ["| - | - | - | - | - |"]
    return rows

x_rows = rows_for('x')
th_rows = rows_for('threads')
rd_rows = rows_for('reddit')

readme = [
    '# Social Media Report',
    '',
    '這個 repo 用來集中保存社群情報報告（X / Threads / Reddit）。',
    '',
    '## 自動維護規則',
    '- 每次上傳報告時更新 README',
    '- README 僅保留 **最近 7 天** 的報告索引',
    '',
    '## X 報告（最近一週）',
    '| 時間 | 檔名 | Markdown | HTML | 直接瀏覽 |',
    '|---|---|---|---|---|',
]
readme.extend(x_rows)
readme.extend([
    '',
    '## Threads 報告（最近一週）',
    '| 時間 | 檔名 | Markdown | HTML | 直接瀏覽 |',
    '|---|---|---|---|---|',
])
readme.extend(th_rows)
readme.extend([
    '',
    '## Reddit 報告（最近一週）',
    '| 時間 | 檔名 | Markdown | HTML | 直接瀏覽 |',
    '|---|---|---|---|---|',
])
readme.extend(rd_rows)

(repo / 'README.md').write_text('\n'.join(readme) + '\n', encoding='utf-8')
print('README updated')
