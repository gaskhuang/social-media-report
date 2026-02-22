# Social Media Report

這個 repo 用來集中保存社群情報報告，主要收錄：

- `x_top_news_*`：X（Twitter）熱門貼文報告
- `threads_top_news_*`：Threads 熱門貼文報告
- `web/*.html`：可直接瀏覽的網頁版報告

## 目的

提供固定格式的社群監控產出，方便：

1. 每日追蹤 AI / OpenClaw / 產業熱門話題
2. 快速回顧每輪爬蟲結果與排序邏輯
3. 對外分享可點開瀏覽的 HTML 版本

## 報告規則（目前）

- 報告以繁體中文為主
- 非中文內容翻譯為繁體中文
- 排序規則：各分類依「愛心 + 分享 + 留言」總和由高到低

## 資料夾結構

```text
reports/
  x_top_news_*.md
  threads_top_news_*.md
web/
  x_top_news_*.html
```

## 備註

此 repo 為報告發布倉庫（public），用於彙整與瀏覽社群監控結果。
