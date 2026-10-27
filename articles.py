"""Reviewed editorial content rendered with the site's existing shared templates.

The registry contains approved editorial prose and explicit publication dates.
Empty input creates no article routes, index or navigation links.
"""
from datetime import date
from pathlib import Path
from html import escape
import re
from urllib.parse import urlsplit

def load_article():
    text=(Path(__file__).parent/'content'/'smarter-medical-transportation-iteration.md').read_text(encoding='utf-8')
    title,body=text.split('\n',1)
    parts=re.split(r'^## (.+)$',body,flags=re.M)
    blocks=lambda s:[p.strip() for p in s.strip().split('\n\n') if p.strip()]
    return dict(slug='smarter-medical-transportation-iteration',title=title.removeprefix('# '),
        seo_title='Smarter Medical Transportation Software',
        summary='How clearer ride requests, accessible forms and careful testing can improve transportation tools without promising unbuilt dispatch or tracking features.',
        status='published',published_on='2026-10-27',research_on='2026-10-27',intro=blocks(parts[0]),
        sections=[(parts[i],blocks(parts[i+1])) for i in range(1,len(parts),2)],sources=[])

ARTICLES = (load_article(),)

def inline(text):
    # Deliberately small editorial syntax: emphasis and HTTPS links; never raw HTML.
    pattern=r'\*\*([^*]+)\*\*|\[([^\]]+)\]\((https://[^\s)]+)\)'
    output=[];end=0
    for match in re.finditer(pattern,text):
        output.append(escape(text[end:match.start()]))
        if match.group(1):output.append('<strong>'+escape(match.group(1))+'</strong>')
        else:
            url=match.group(3);parsed=urlsplit(url)
            if not parsed.netloc or parsed.username or parsed.password:raise ValueError('Invalid article link')
            output.append('<a href="'+escape(url,quote=True)+'">'+escape(match.group(2))+'</a>')
        end=match.end()
    return ''.join(output)+escape(text[end:])

def block(text):
    lines=text.splitlines()
    if all(line.startswith('- ') for line in lines):
        return '<ul>'+''.join('<li>'+inline(line[2:])+'</li>' for line in lines)+'</ul>'
    return '<p>'+inline(text)+'</p>'

def published_articles(articles, today=None):
    """Only explicitly published entries whose publication date has arrived."""
    today = today or date.today()
    entries=[]
    for article in articles:
        status=article.get('status','draft')
        if status not in ('draft','published'):
            raise ValueError('Article status must be draft or published.')
        if status == 'published' and date.fromisoformat(article['published_on']) <= today:
            entries.append(article)
    return entries

def render_articles(articles, document, write):
    articles=published_articles(articles)
    if not articles:
        return []
    seen=set()
    # Validate the whole collection before generating any pages.
    for article in articles:
        slug=article['slug']
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug) or slug in seen:
            raise ValueError('Article slugs must be unique, safe path segments.')
        seen.add(slug)
        date.fromisoformat(article['published_on'])
        if not article['title'].strip() or not article['summary'].strip() or not article['sections']:
            raise ValueError('Final article title, summary and sections are required.')
        for heading, paragraphs in article['sections']:
            if not heading.strip() or not paragraphs or any(not p.strip() for p in paragraphs):
                raise ValueError('Each section requires a heading and nonempty paragraphs.')
        for label,url in article['sources']:
            parsed=urlsplit(url)
            if not label.strip() or parsed.scheme!='https' or not parsed.netloc or parsed.username or parsed.password:
                raise ValueError('Sources require labeled HTTPS URLs without credentials.')
    paths=[]
    items=[]
    for article in articles:
        path='/articles/'+article['slug']+'/'
        title=escape(article['title'])
        summary=escape(article['summary'])
        published=escape(article['published_on'])
        intro=''.join(block(p) for p in article.get('intro',[]))
        sections=''.join('<h2>'+escape(h)+'</h2>'+''.join(block(p) for p in paragraphs)
                         for h,paragraphs in article['sections'])
        sources=''.join('<li><a href="'+escape(url,quote=True)+'">'+escape(label)+'</a></li>'
                        for label,url in article['sources'])
        references='<h2>Sources</h2><ul>'+sources+'</ul>' if sources else ''
        body=('<section class="page-hero wrap"><a class="breadcrumb" href="/articles/">Articles /</a>'
              '<p class="eyebrow">RIDE PRIMETIME ARTICLES</p><h1>'+title+'</h1><p class="lead">'+summary+'</p>'
              '<p class="fine">Published by Primetime Medical Transportation / RidePrimetime. Prepared with AI drafting assistance.</p>'
              '<p class="fine">Published <time datetime="'+published+'">'+published+'</time>. Research checked '+escape(article.get('research_on',article['published_on']))+'.</p></section>'
              '<article class="section wrap prose">'+intro+sections+references+'</article>')
        write(path,document(article.get('seo_title',article['title']),article['summary'],path,body))
        paths.append(path)
        items.append('<li><h2><a href="'+path+'">'+title+'</a></h2><p>'+summary+'</p></li>')
    index='/articles/'
    write(index,document('Articles','Planning and service perspectives from Ride Primetime.',index,
          '<section class="page-hero wrap"><a class="breadcrumb" href="/">Home /</a><p class="eyebrow">ARTICLES</p>'
          '<h1>Perspectives on planned transportation.</h1></section><section class="section wrap prose"><ul class="site-map">'
          +''.join(items)+'</ul></section>'))
    return [index]+paths

def reconcile_article_output(public, paths):
    """Remove stale generated article HTML, never editorial sources or other assets."""
    public=Path(public).resolve()
    archive=public/'articles'
    if archive.is_symlink():
        raise ValueError('Article output directory must not be a symbolic link.')
    if not archive.exists():return
    keep={public/path.strip('/')/'index.html' for path in paths}
    candidates=[archive/'index.html']
    for child in archive.iterdir():
        if child.is_dir() and not child.is_symlink() and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',child.name):
            candidates.append(child/'index.html')
    for page in candidates:
        if page.is_symlink():raise ValueError('Article output must not be a symbolic link.')
        if page.is_file() and page not in keep:
            page.unlink()
