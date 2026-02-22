#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timedelta
import re

repo = Path('.')
reports = repo / 'reports'
web = repo / 'web'
pat = re.compile(r'^(x_top_news|threads_top_news)_(\d{8})_(\d{4})(?:_.*)?\.(md|html)$')
cutoff = datetime.now() - timedelta(days=7)

items = []
for p in list(reports.glob('*.md')) + list(web.glob('*.html')):
    m = pat.match(p.name)
    if not m:
        continue
    kind, d, t, ext = m.groups()
    dt = datetime.strptime(d+t, '%Y%m%d%H%M')
    if dt < cutoff:
        continue
    items.append((dt, kind, ext, p))

# group by stem
group = {}
for dt, kind, ext, p in items:
    key = p.stem
    g = group.setdefault(key, {'dt':dt,'kind':kind,'md':None,'html':None})
    if dt > g['dt']:
        g['dt'] = dt
    if ext == 'md':
        g['md'] = p
    else:
        g['html'] = p

def build_rows(target_kind):
    rows = []
    sub = [(k,v) for k,v in group.items() if v['kind']==target_kind]
    sub.sort(key=lambda kv: kv[1]['dt'], reverse=True)
    for key, g in sub:
        dt = g['dt'].strftime('%Y-%m-%d %H:%M')
        md_link = f"[MD](./{g['md'].as_posix()})" if g['md'] else '-'
        html_link = f"[HTML](./{g['html'].as_posix()})" if g['html'] else '-'
        page_link = f"[網頁版](https://gaskhuang.github.io/social-media-report/{g['html'].as_posix()})" if g['html'] else '-'
        rows.append(f"| {dt} | `{key}` | {md_link} | {html_link} | {page_link} |")
    if not rows:
        rows = ["| - | - | - | - | - |"]
    return rows

x_rows = build_rows('x_top_news')
th_rows = build_rows('threads_top_news')

readme = [
"# Social Media Report",
"",
"這個 repo 用來集中保存社群情報報告（X / Threads）。",
"",
"## 自動維護規則",
"- 每次上傳報告時更新 README",
"- README 僅保留 **最近 7 天** 的報告索引",
"",
"## X 報告（最近一週）",
"| 時間 | 檔名 | Markdown | HTML | 直接瀏覽 |",
"|---|---|---|---|---|",
]
readme.extend(x_rows)
readme.extend([
"",
"## Threads 報告（最近一週）",
"| 時間 | 檔名 | Markdown | HTML | 直接瀏覽 |",
"|---|---|---|---|---|",
])
readme.extend(th_rows)

(repo/'README.md').write_text('\n'.join(readme)+'\n', encoding='utf-8')
print('README updated')
