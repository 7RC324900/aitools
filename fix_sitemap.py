import urllib.parse
import os

articles_dir = "articles"
files = sorted(os.listdir(articles_dir))
html_files = [f for f in files if f.endswith(".html") and f != "index.html"]

lines = []
lines.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
lines.append("<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">")

lines.append("  <url>")
lines.append("    <loc>https://7RC324900.github.io/aitools/</loc>")
lines.append("    <changefreq>daily</changefreq>")
lines.append("    <priority>1.0</priority>")
lines.append("  </url>")

lines.append("  <url>")
lines.append("    <loc>https://7RC324900.github.io/aitools/articles/</loc>")
lines.append("    <changefreq>daily</changefreq>")
lines.append("    <priority>0.9</priority>")
lines.append("  </url>")

for i, fname in enumerate(html_files):
    name_without_ext = fname.replace(".html", "")
    encoded_name = urllib.parse.quote(name_without_ext)
    url = "https://7RC324900.github.io/aitools/articles/" + encoded_name + ".html"
    month = "0" + str(i // 10 + 1) if i // 10 + 1 < 10 else str(i // 10 + 1)
    day = "%02d" % (i % 28 + 1)
    lines.append("  <url>")
    lines.append("    <loc>" + url + "</loc>")
    lines.append("    <lastmod>2026-" + month + "-" + day + "</lastmod>")
    lines.append("    <changefreq>monthly</changefreq>")
    lines.append("    <priority>0.7</priority>")
    lines.append("  </url>")

lines.append("</urlset>")

with open("sitemap.xml", "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines) + "\n")

print("Done! " + str(len(html_files)) + " articles")
with open("sitemap.xml", "r", encoding="utf-8") as f:
    c = f.read()
for line in c.split("\n"):
    if "<loc>" in line:
        print(line.strip())
        break