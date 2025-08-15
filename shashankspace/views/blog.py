import os
import markdown
import frontmatter
from flask import Blueprint, render_template, abort
from flask.views import MethodView

blog_bp = Blueprint("blog", __name__, url_prefix="/blog")

# Path to blog content folder
CONTENT_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "content", "blog"
)

def load_post(filename):
    """Load and parse a markdown blog post."""
    path = os.path.join(CONTENT_DIR, filename)
    if not os.path.exists(path):
        return None
    post_data = frontmatter.load(path)
    html_content = markdown.markdown(
        post_data.content,
        extensions=["fenced_code", "tables", "toc", "codehilite"]
    )
    return {
        "title": post_data.get("title", "Untitled"),
        "date": post_data.get("date", ""),
        "content": html_content
    }

class BlogList(MethodView):
    def get(self):
        posts = []
        if os.path.exists(CONTENT_DIR):
            for filename in sorted(os.listdir(CONTENT_DIR), reverse=True):
                if filename.endswith(".md"):
                    post_data = frontmatter.load(os.path.join(CONTENT_DIR, filename))
                    posts.append({
                        "slug": filename.replace(".md", ""),
                        "title": post_data.get("title", "Untitled"),
                        "date": post_data.get("date", ""),
                        "preview": post_data.content[:200] + "..."
                    })
        return render_template("blog_list.html", title="Blog", posts=posts)

class BlogDetail(MethodView):
    def get(self, slug):
        post = load_post(f"{slug}.md")
        if not post:
            abort(404)
        return render_template("blog_detail.html", title=post["title"], post=post)

# Routes
blog_bp.add_url_rule("/", view_func=BlogList.as_view("blog_list"))
blog_bp.add_url_rule("/<slug>/", view_func=BlogDetail.as_view("blog_detail"))
