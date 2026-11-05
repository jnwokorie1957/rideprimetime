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
        status='published',published_on='2026-10-27',modified_on='2026-10-29',research_on='2026-10-27',intro=blocks(parts[0]),
        sections=[(parts[i],blocks(parts[i+1])) for i in range(1,len(parts),2)],sources=[])

def load_checklist():
    text=(Path(__file__).parent/'content'/'houston-ride-quote-checklist.md').read_text(encoding='utf-8')
    title,body=text.split('\n',1)
    parts=re.split(r'^## (.+)$',body,flags=re.M)
    blocks=lambda s:[p.strip() for p in s.strip().split('\n\n') if p.strip()]
    return dict(slug='houston-ride-quote-checklist',title=title.removeprefix('# '),
        seo_title='Houston Ride Quote Checklist for Families',
        summary='Prepare for a private-pay wheelchair or ambulatory ride inquiry in Houston with questions about arrival time, mobility needs, return plans and confirmation.',
        status='published',published_on='2026-10-28',modified_on='2026-10-30',research_on='2026-10-28',intro=blocks(parts[0]),
        sections=[(parts[i],blocks(parts[i+1])) for i in range(1,len(parts),2)],sources=[],publisher='Primetime Medical Transportation')

def load_planning_article(slug, seo_title, summary, research_on, published_on='2026-11-02', ai_disclosure=None):
    text = (Path(__file__).parent / 'content' / (slug + '.md')).read_text(encoding='utf-8')
    title, body = text.split('\n', 1)
    parts = re.split(r'^## (.+)$', body, flags=re.M)
    blocks = lambda value: [p.strip() for p in value.strip().split('\n\n') if p.strip()]
    return dict(slug=slug, title=title.removeprefix('# '), seo_title=seo_title,
                summary=summary, status='published', published_on=published_on,
                research_on=research_on, intro=blocks(parts[0]),
                sections=[(parts[i], blocks(parts[i+1])) for i in range(1, len(parts), 2)],
                sources=[], publisher='Primetime Medical Transportation', ai_disclosure=ai_disclosure)

ARTICLES = (load_article(), load_checklist(),
    load_planning_article('bringing-a-companion-on-a-medical-ride-in-houston',
        'Bringing a Companion on a Medical Ride in Houston',
        "Plan a companion's medical ride in Houston with clear roles, one-way or round-trip details, meeting points, contact plans, and questions to confirm.",
        '2026-10-31'),
    load_planning_article('planning-recurring-medical-rides-houston',
        'Planning Recurring Medical Rides in Houston',
        'Keep repeated Houston medical rides clear with a date-by-date family note for confirmations, return trips, schedule exceptions and changes.',
        '2026-11-01'),
    load_planning_article('finding-right-entrance-houston-medical-campus-ride',
        'Medical Campus Ride Entrance Planning in Houston',
        'Confirm the building, entrance, indoor check-in and return meeting point before arranging a private-pay Houston wheelchair or ambulatory ride.',
        '2026-11-04', published_on='2026-11-04'),
    load_planning_article('planning-wheelchair-ride-houston-family-gathering',
        'Planning a Wheelchair Ride to a Houston Family Gathering',
        "Plan a Houston family visit with questions about the host's space, arrival access, destination help, belongings and a separately agreed return ride.",
        '2026-11-05', published_on='2026-11-05',
        ai_disclosure='Prepared with AI drafting assistance.'))

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
    if len(lines)==1 and text.startswith('### '):
        return '<h3>'+inline(text[4:])+'</h3>'
    if all(line.startswith('- ') for line in lines):
        return '<ul>'+''.join('<li>'+inline(line[2:])+'</li>' for line in lines)+'</ul>'
    return '<p>'+inline(text)+'</p>'

def published_articles(articles, today=None):
    """Published entries, newest first; same-day entries retain registry order."""
    today = today or date.today()
    entries=[]
    for article in articles:
        status=article.get('status','draft')
        if status not in ('draft','published'):
            raise ValueError('Article status must be draft or published.')
        if status == 'published' and date.fromisoformat(article['published_on']) <= today:
            entries.append(article)
    return sorted(entries, key=lambda article: date.fromisoformat(article['published_on']), reverse=True)

def article_document(document, title, summary, path, body):
    """Style article outputs only; leave the common document shell untouched."""
    page = document(title, summary, path, body)
    return page.replace('</head>', '<link rel="stylesheet" href="/assets/articles.css?v=20261102">\n</head>', 1)


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
        if article.get('modified_on') and date.fromisoformat(article['modified_on']) < date.fromisoformat(article['published_on']):
            raise ValueError('Update date cannot precede publication.')
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
        modified=escape(article.get('modified_on',''))
        update_note=' Updated <time datetime="'+modified+'">'+modified+'</time>.' if modified else ''
        intro=''.join(block(p) for p in article.get('intro',[]))
        sections=''.join('<h2 id="section-'+str(i)+'">'+escape(h)+'</h2>'+''.join(block(p) for p in paragraphs)
                         for i,(h,paragraphs) in enumerate(article['sections'],1))
        contents='<nav class="article-toc" aria-label="In this article"><p class="article-toc-label">In this article</p><ol>'+''.join(
            '<li><a href="#section-'+str(i)+'">'+escape(h)+'</a></li>' for i,(h,_) in enumerate(article['sections'],1))+'</ol></nav>'
        sources=''.join('<li><a href="'+escape(url,quote=True)+'">'+escape(label)+'</a></li>'
                        for label,url in article['sources'])
        references='<h2>Sources</h2><ul>'+sources+'</ul>' if sources else ''
        disclosure='<p class="fine">'+escape(article['ai_disclosure'])+'</p>' if article.get('ai_disclosure') else ''
        structured=''
        article_attributes=''
        if article.get('publisher'):
            article_attributes=' itemscope itemtype="https://schema.org/Article"'
            structured=('<meta itemprop="headline" content="'+title+'">'
                        '<meta itemprop="datePublished" content="'+published+'">'
                        '<meta itemprop="url" content="https://www.rideprimetime.net'+path+'">'
                        '<span itemprop="publisher" itemscope itemtype="https://schema.org/Organization">'
                        '<meta itemprop="name" content="'+escape(article['publisher'],quote=True)+'"></span>')
        if modified and article.get('publisher'):
            structured+='<meta itemprop="dateModified" content="'+modified+'">'
        body=('<section class="page-hero wrap article-hero"><a class="breadcrumb" href="/articles/">Articles /</a>'
              '<p class="eyebrow">RIDE PRIMETIME ARTICLES</p><h1>'+title+'</h1><p class="lead">'+summary+'</p>'
              '<div class="article-meta"><p class="fine">Published by Robert, CTO of Primetime Medical Transportation</p>'
              '<p class="fine">Published <time datetime="'+published+'">'+published+'</time>. Research checked '+escape(article.get('research_on',article['published_on']))+'.'+update_note+'</p></div></section>'
              '<article class="section wrap prose article-prose"'+article_attributes+'>'+structured+intro+contents+sections+references+disclosure+'<p class="article-back"><a href="/articles/">Back to all articles <span aria-hidden="true">↗</span></a></p></article>')
        write(path,article_document(document,article.get('seo_title',article['title']),article['summary'],path,body))
        paths.append(path)
        items.append('<li><p class="article-card-meta">Article <span aria-hidden="true">·</span> <time datetime="'+published+'">'+published+'</time></p><h2><a href="'+path+'">'+title+'<span class="article-card-arrow" aria-hidden="true">↗</span></a></h2><p>'+summary+'</p></li>')
    index='/articles/'
    write(index,article_document(document,'Articles','Planning and service perspectives from Ride Primetime.',index,
          '<section class="page-hero wrap article-hero"><a class="breadcrumb" href="/">Home /</a><p class="eyebrow">ARTICLES</p>'
          '<h1>Perspectives on planned transportation.</h1><p class="lead">Practical guides for riders, families and the people helping plan the journey.</p></section><section class="section wrap prose article-prose article-index"><ul class="article-list">'
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
