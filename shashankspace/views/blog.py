import os
import re
import markdown
import frontmatter
from datetime import datetime
from flask import Blueprint, render_template, abort
from flask.views import MethodView

blog_bp = Blueprint("blog", __name__, url_prefix="/blog")

CONTENT_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content", "blog")
)

def _slug_from_filename(filename: str) -> str:
    return filename.rsplit(".", 1)[0]

def _parse_date(meta_date):
    """
    Accepts 'YYYY-MM-DD' or datetime/date; returns datetime for sorting.
    Falls back to file date if not present/parsable.
    """
    if isinstance(meta_date, datetime):
        return meta_date
    if isinstance(meta_date, str):
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y"):
            try:
                return datetime.strptime(meta_date, fmt)
            except ValueError:
                pass
    return None

def _render_markdown(md_text: str) -> str:
    # GitHub-like rendering with fenced code, tables, toc, codehilite
    return markdown.markdown(
        md_text,
        extensions=["fenced_code", "tables", "toc", "codehilite"]
    )

def _excerpt(md_text: str, length: int = 220) -> str:
    # crude excerpt: strip code fences and headings, take first N chars
    text = re.sub(r"```.*?```", "", md_text, flags=re.S)      # remove fenced code
    text = re.sub(r"^#+\s*", "", text, flags=re.M)            # remove heading markers
    text = re.sub(r"\*|_|`|\[|\]|\(|\)|>", "", text)          # strip common md
    text = " ".join(text.split())
    return (text[:length] + "…") if len(text) > length else text

def _load_post(slug: str):
    path = os.path.join(CONTENT_DIR, f"{slug}.md")
    if not os.path.exists(path):
        return None
    post_data = frontmatter.load(path)
    html = _render_markdown(post_data.content)
    return {
        "slug": slug,
        "title": post_data.get("title", "Untitled"),
        "date": post_data.get("date", ""),
        "tags": post_data.get("tags", []),
        "content": html,
    }

class BlogList(MethodView):
    def get(self):
        posts = []
        if os.path.isdir(CONTENT_DIR):
            for filename in os.listdir(CONTENT_DIR):
                if filename.endswith(".md"):
                    path = os.path.join(CONTENT_DIR, filename)
                    fm = frontmatter.load(path)
                    slug = _slug_from_filename(filename)
                    date_meta = _parse_date(fm.get("date"))
                    # Fall back to file modified time if no date
                    sort_date = date_meta or datetime.fromtimestamp(os.path.getmtime(path))
                    posts.append({
                        "slug": slug,
                        "title": fm.get("title", "Untitled"),
                        "date": fm.get("date", ""),
                        "tags": fm.get("tags", []),
                        "excerpt": _excerpt(fm.content),
                        "sort_date": sort_date,
                    })

        posts.sort(key=lambda p: p["sort_date"], reverse=True)
        return render_template("blog_list.html", title="Blog", posts=posts)

class BlogDetail(MethodView):
    def get(self, slug):
        post = _load_post(slug)
        if not post:
            abort(404)
        return render_template("blog_detail.html", title=post["title"], post=post)

# Routes
blog_bp.add_url_rule("/", view_func=BlogList.as_view("list"))
blog_bp.add_url_rule("/<slug>/", view_func=BlogDetail.as_view("detail"))
