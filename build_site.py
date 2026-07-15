import os, sys

# Load generate_articles.py data
with open("generate_articles.py", "r", encoding="utf-8") as f:
    src = f.read()
lines = src.split("\n")
while lines and lines[-1].strip() == '':
    lines.pop()
if lines and 'print("Script ready")' in lines[-1]:
    lines.pop()
src_clean = "\n".join(lines)

ns = {}
exec(src_clean.lstrip('﻿'), ns)

SITE_URL = ns["SITE_URL"]
ARTICLES_DIR = ns["ARTICLES_DIR"]
CATEGORIES = ns["CATEGORIES"]
TOOLS = ns["TOOLS"]
mkarticle = ns["mkarticle"]


def mkpage(title, desc, body, canonical, is_article=False, css=None, home=None, arts=None, js=None):
    if css is None:
        css = "../" if is_article else ""
    if home is None:
        home = "../" if is_article else "."
    if arts is None:
        arts = "../articles/" if is_article else "articles/"
    if js is None:
        js = "../" if is_article else ""
    schema = ""
    if is_article:
        schema = '<script type="application/ld+json">\n{"@context":"https://schema.org","@type":"Article","headline":"' + title + '","datePublished":"2026-01-15"}\n</script>\n'
    return '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>' + title + '</title>\n<meta name="description" content="' + desc + '">\n<link rel="canonical" href="' + canonical + '">\n<link rel="stylesheet" href="' + css + 'css/style.css">\n<meta property="og:title" content="' + title + '">\n<meta property="og:description" content="' + desc + '">\n<meta property="og:type" content="' + ('article' if is_article else 'website') + '">\n' + schema + '</head>\n<body>\n<header class="site-header" style="background:linear-gradient(135deg,#1a1a2e,#16213e);color:#fff;padding:16px 0;position:sticky;top:0;z-index:100">\n<div class="container" style="max-width:1200px;margin:0 auto;padding:0 20px;display:flex;align-items:center;justify-content:space-between">\n<a href="' + home + '" class="site-logo" style="font-size:1.5rem;font-weight:800;color:#fff">AI<span style="color:#60a5fa">\u5de5\u5177</span>\u5bfc\u822a</a>\n<button class="nav-toggle" onclick="document.querySelector(\'.nav-list\').classList.toggle(\'open\')" style="background:none;border:none;color:#fff;font-size:1.5rem;cursor:pointer;display:none">\u2630</button>\n<nav>\n<ul class="nav-list" style="display:flex;list-style:none;gap:24px;margin:0;padding:0">\n<li><a href="' + home + '" style="color:#cbd5e1;text-decoration:none;font-size:0.9rem">\u9996\u9875</a></li>\n<li><a href="' + arts + '" style="color:#cbd5e1;text-decoration:none;font-size:0.9rem">\u5168\u90e8\u6587\u7ae0</a></li>\n</ul>\n</nav>\n</div>\n</header>\n<main>\n' + body + '\n</main>\n<footer class="site-footer" style="background:#1a1a2e;color:#94a3b8;text-align:center;padding:2rem 0;font-size:0.85rem">\n<div class="container">\n<p>&copy; 2025 AI\u5de5\u5177\u5bfc\u822a - \u4e3a\u81ea\u7531\u804c\u4e1a\u8005\u7cbe\u9009AI\u5de5\u5177\u8bc4\u6d4b | <a href="' + SITE_URL + '/sitemap.xml" style="color:#60a5fa">\u7f51\u7ad9\u5730\u56fe</a></p>\n</div>\n</footer>\n<script src="' + js + 'js/main.js"></script>\n</body>\n</html>'


def main():
    os.makedirs(ARTICLES_DIR, exist_ok=True)
    
    # Build articles data
    articles = []
    idx = 0
    for cat_zh, cat_en in CATEGORIES.items():
        for tool_title, tool_name in TOOLS.get(cat_en, []):
            content_html, slug, desc, month, day = mkarticle(cat_zh, tool_title, tool_name, idx)
            articles.append((cat_zh, tool_title, tool_name, slug, desc, month, day, content_html))
            idx += 1
    
    print(f"Total: {len(articles)} articles")
    
    # Generate individual article pages
    for cat_zh, tool_title, tool_name, slug, desc, month, day, content_html in articles:
        filename = slug + ".html"
        filepath = os.path.join(ARTICLES_DIR, filename)
        canonical = SITE_URL + "/" + ARTICLES_DIR + "/" + filename
        title = tool_title + " - \u81ea\u7531\u804c\u4e1a\u8005AI\u5de5\u5177\u8bc4\u6d4b"
        page = mkpage(title, desc, content_html, canonical, is_article=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(page)
        print("  ok " + filename)
    
    # Generate articles listing
    items = ""
    for cat_zh, tool_title, tool_name, slug, desc, month, day, content_html in articles:
        items += f'''    <li>
      <a href="{slug}.html" style="font-size:1.1rem;font-weight:600;color:#2563eb">{tool_title}</a>
      <span class="desc" style="display:block;color:#64748b;font-size:0.9rem;margin:4px 0">{desc}</span>
      <span class="cat-tag" style="display:inline-block;background:#e0e7ff;color:#4338ca;padding:2px 10px;border-radius:12px;font-size:0.8rem">{cat_zh}</span>
    </li>
'''
    body = f'''<div class="container-narrow" style="padding-top:3rem;padding-bottom:3rem;max-width:800px;margin:0 auto;padding:3rem 20px">
  <h1 style="font-size:2rem;font-weight:800;margin-bottom:1rem">\u5168\u90e8AI\u5de5\u5177\u8bc4\u6d4b</h1>
  <p style="margin:0 0 2rem;color:#64748b;font-size:1.1rem">\u6d4f\u89c8{len(articles)}\u6b3eAI\u5de5\u5177\u6df1\u5ea6\u8bc4\u6d4b\uff0c\u8986\u76d6\u5199\u4f5c\u3001\u8bbe\u8ba1\u3001\u7f16\u7a0b\u3001\u8425\u9500\u3001\u6548\u7387\u7b49\u7c7b\u522b\u3002</p>
  <input type="text" id="search-input" placeholder="\u641c\u7d22AI\u5de5\u5177..." style="width:100%;padding:12px 16px;border:2px solid #e2e8f0;border-radius:8px;font-size:1rem;margin-bottom:2rem;outline:none">
  <ul id="article-list" style="list-style:none;padding:0;display:grid;gap:1.2rem">
{items}  </ul>
  <p style="margin-top:2rem;color:#94a3b8;text-align:center;font-size:0.85rem">\u6570\u636e\u6765\u6e90\uff1aGartner 2025 AI\u5e02\u573a\u62a5\u544a\u3001McKinsey Global Institute\u7814\u7a76</p>
</div>
<script>
function filterArticles(q){{q=q.toLowerCase().trim();document.querySelectorAll('#article-list li').forEach(function(l){{var t=l.textContent.toLowerCase();l.style.display=(!q||t.indexOf(q)>-1)?'':'none';}})}}
document.addEventListener('DOMContentLoaded',function(){{var e=document.getElementById('search-input');if(e)e.addEventListener('input',function(){{filterArticles(this.value)}})}});
</script>'''
    with open(os.path.join(ARTICLES_DIR, "index.html"), 'w', encoding='utf-8') as f:
        f.write(mkpage("\u5168\u90e8AI\u5de5\u5177\u8bc4\u6d4b - AI\u5de5\u5177\u5bfc\u822a", "\u6d4f\u89c8100\u6b3eAI\u5de5\u5177\u6df1\u5ea6\u8bc4\u6d4b", body, SITE_URL + "/" + ARTICLES_DIR + "/", is_article=False, css="../", home="..", arts="articles/", js="../"))
    print("  ok articles/index.html")
    
    # Generate main index
    featured = ""
    for i, (cat_zh, tool_title, tool_name, slug, desc, month, day, content_html) in enumerate(articles):
        if i >= 6: break
        featured += f'''    <article class="post-card" style="background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.1)">
      <div class="post-card-body" style="padding:1.5rem">
        <span style="display:inline-block;background:#e0e7ff;color:#4338ca;padding:2px 10px;border-radius:12px;font-size:0.8rem;margin-bottom:0.5rem">{cat_zh}</span>
        <h3 style="margin:0 0 0.5rem;font-size:1.15rem"><a href="{ARTICLES_DIR}/{slug}.html" style="color:#1e293b;text-decoration:none">{tool_title}</a></h3>
        <p style="color:#64748b;font-size:0.9rem;margin:0">{desc[:80]}...</p>
      </div>
    </article>
'''
    cat_boxes = ""
    for cat_zh, cat_en in CATEGORIES.items():
        ct = [(t[2], t[3]) for t in articles if t[0] == cat_zh]
        links = " \u00b7 ".join(f'<a href="{ARTICLES_DIR}/{s}.html" style="color:#475569;text-decoration:none">{n}</a>' for n, s in ct[:3])
        cat_boxes += f'''  <div class="cat-card" style="background:#f1f5f9;border-radius:8px;padding:1.5rem">
    <h3 style="margin-bottom:0.75rem;font-size:1.1rem;color:#1e293b">{cat_zh}</h3>
    <p style="margin:0;font-size:0.85rem;line-height:1.8;color:#475569">{links}</p>
  </div>
'''
    pbody = f'''<section class="hero" style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);color:#fff;padding:4rem 0;text-align:center">
  <div class="container" style="max-width:700px;margin:0 auto;padding:0 20px">
    <h1 style="font-size:2.8rem;font-weight:800;margin-bottom:1rem">AI<span style="color:#60a5fa">\u5de5\u5177</span>\u5bfc\u822a</h1>
    <p style="font-size:1.2rem;color:#94a3b8;margin-bottom:2rem">\u4e3a\u81ea\u7531\u804c\u4e1a\u8005\u548c\u72ec\u7acb\u5f00\u53d1\u8005\u7cbe\u9009\u7684AI\u5de5\u5177\u8bc4\u6d4b\u4e0e\u4f7f\u7528\u6307\u5357\u3002\u8986\u76d6\u5199\u4f5c\u3001\u8bbe\u8ba1\u3001\u7f16\u7a0b\u3001\u8425\u9500\u7b49\u9886\u57df\uff0c\u52a9\u4f60\u63d0\u5347\u6548\u738710\u500d\u3002</p>
    <a href="{ARTICLES_DIR}/" style="display:inline-block;background:#2563eb;color:#fff;padding:14px 36px;border-radius:8px;font-weight:600;font-size:1rem;text-decoration:none">\u6d4f\u89c8\u5168\u90e8{len(articles)}\u6b3e\u5de5\u5177</a>
  </div>
</section>
<section class="featured-articles" style="padding:3rem 0">
  <div class="container" style="max-width:1200px;margin:0 auto;padding:0 20px">
    <h2 style="text-align:center;margin-bottom:2rem;font-size:1.8rem;font-weight:700;color:#1e293b">\u7cbe\u9009AI\u5de5\u5177\u8bc4\u6d4b</h2>
    <div id="featured-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1.5rem">
{featured}    </div>
  </div>
</section>
<section class="categories" style="padding:3rem 0;background:#fff">
  <div class="container" style="max-width:1200px;margin:0 auto;padding:0 20px">
    <h2 style="text-align:center;margin-bottom:2rem;font-size:1.8rem;font-weight:700;color:#1e293b">\u5de5\u5177\u5206\u7c7b</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:1.2rem">
{cat_boxes}  </div>
  </div>
</section>'''
    with open("index.html", 'w', encoding='utf-8') as f:
        f.write(mkpage("AI\u5de5\u5177\u5bfc\u822a - \u4e3a\u81ea\u7531\u804c\u4e1a\u8005\u7cbe\u9009\u6700\u4f73AI\u5de5\u5177", "\u63a2\u7d22\u4e13\u4e3a\u81ea\u7531\u804c\u4e1a\u8005\u7cbe\u62fe\u7ec6\u9009\u7684AI\u5de5\u5177\u8bc4\u6d4b", pbody, SITE_URL + "/"))
    print("  ok index.html")
    
    # Generate sitemap.xml
    sm_items = f'''  <url>
    <loc>{SITE_URL}/</loc>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>{SITE_URL}/{ARTICLES_DIR}/</loc>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>
'''
    for cat_zh, tool_title, tool_name, slug, desc, month, day, content_html in articles:
        sm_items += f'''  <url>
    <loc>{SITE_URL}/{ARTICLES_DIR}/{slug}.html</loc>
    <lastmod>2026-{month}-{day}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
'''
    with open("sitemap.xml", 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + sm_items + '</urlset>\n')
    print("  ok sitemap.xml")
    
    # Generate 404.html
    body404 = '<div class="container-narrow" style="text-align:center;padding:6rem 0;max-width:800px;margin:0 auto;padding:6rem 20px">\n<h1 style="font-size:4rem;margin-bottom:1rem;font-weight:800;color:#1e293b">404</h1>\n<p style="font-size:1.2rem;color:#64748b;margin-bottom:2rem">\u62b1\u6b49\uff0c\u9875\u9762\u4e0d\u5b58\u5728\u3002</p>\n<a href="./" style="display:inline-block;background:#2563eb;color:#fff;padding:14px 36px;border-radius:8px;font-weight:600;text-decoration:none">\u8fd4\u56de\u9996\u9875</a>\n</div>'
    with open("404.html", 'w', encoding='utf-8') as f:
        f.write(mkpage("\u9875\u9762\u672a\u627e\u5230 - AI\u5de5\u5177\u5bfc\u822a", "\u60a8\u8bbf\u95ee\u7684\u9875\u9762\u4e0d\u5b58\u5728", body404, SITE_URL + "/404.html"))
    print("  ok 404.html")
    
    print(f"\nDone! {len(articles)} articles + pages generated.")


if __name__ == "__main__":
    main()
