from flask import Flask, render_template_string, request
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>HTML Link Cleaner</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        textarea { font-family: monospace; }
        .preview-container { display: flex; gap: 20px; }
        .preview-box { width: 48%; }
        .copy-msg { color: green; font-weight: bold; display: none; margin-top: 0.5rem; }
    </style>
</head>
<body class="bg-light p-4">
<div class="container">
    <h1 class="mb-4">HTML Link Cleaner</h1>
    <form method="post" id="htmlCleanerForm">
        <div class="mb-3">
            <label class="form-label">HTML Input</label>
            <textarea name="html_input" id="htmlInput" class="form-control" rows="10" required>{{ html_input or '' }}</textarea>
        </div>
        <div class="mb-3">
            <label class="form-label">Href Patterns (comma-separated)</label>
            <input type="text" name="pattern" class="form-control" value="{{ pattern or '' }}" required>
        </div>
        <div class="mb-3">
            <label class="form-label">Action</label>
            <select name="action" class="form-select">
                <option value="unwrap" {% if action == 'unwrap' %}selected{% endif %}>Unwrap &lt;a&gt; (keep text)</option>
                <option value="strip" {% if action == 'strip' %}selected{% endif %}>Remove href only, keep &lt;a&gt;</option>
                <option value="remove" {% if action == 'remove' %}selected{% endif %}>Remove &lt;a&gt; and text</option>
            </select>
        </div>
        <button type="button" class="btn btn-secondary ms-2" onclick="clearForm()">Clear</button>
        <button type="submit" class="btn btn-danger">Clean HTML</button>
    </form>

    {% if cleaned_html %}
    <hr>
    <h2>Preview</h2>
    <div class="preview-container">
        <div class="preview-box">
            <h5>Original HTML</h5>
            <textarea id="originalHtml" class="form-control" rows="10" readonly>{{ html_input }}</textarea>
        </div>
        <div class="preview-box">
            <h5>Cleaned HTML</h5>
            <textarea id="cleanedHtml" class="form-control" rows="10" readonly>{{ cleaned_html }}</textarea>
            <button type="button" class="btn btn-primary mt-2" onclick="copyCleanedHtml()">Copy</button>
            <div id="copyMessage" class="copy-msg">Copied!</div>
        </div>
    </div>

    {% if removed_links %}
    <hr>
    <h3>Matched Links</h3>
    <ol id="matchedLinks">
        {% for link in removed_links %}
            <li>{{ link }}</li>
        {% endfor %}
    </ol>
    {% endif %}
    {% endif %}
</div>

<script>
function copyCleanedHtml() {
    var copyText = document.getElementById("cleanedHtml");
    copyText.select();
    document.execCommand("copy");

    var msg = document.getElementById("copyMessage");
    msg.style.display = "inline";
    setTimeout(() => { msg.style.display = "none"; }, 2000);
}

function clearForm() {
    document.getElementById("htmlInput").value = "";
    var cleaned = document.getElementById("cleanedHtml");
    if (cleaned) cleaned.value = "";
    var original = document.getElementById("originalHtml");
    if (original) original.value = "";
    var matched = document.getElementById("matchedLinks");
    if (matched) matched.innerHTML = "";
}
</script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        html_input = request.form.get("html_input")
        pattern = request.form.get("pattern")
        action = request.form.get("action")

        patterns = [p.strip() for p in pattern.split(",")]

        soup = BeautifulSoup(html_input, "html.parser")
        removed_links = []

        for a_tag in soup.find_all("a", href=True):
            href = a_tag.get("href", "")
            if any(p in href for p in patterns):
                removed_links.append(href)
                if action == "remove":
                    a_tag.decompose()
                elif action == "strip":
                    a_tag.attrs.pop("href", None)
                    a_tag.attrs.pop("title", None)
                elif action == "unwrap":
                    a_tag.unwrap()
        cleaned_html = str(soup)
    else:
        html_input = ""
        cleaned_html = ""
        pattern = ""
        removed_links = []
        action = "unwrap"

    return render_template_string(
        HTML_TEMPLATE,
        cleaned_html=cleaned_html,
        html_input=html_input,
        pattern=pattern,
        removed_links=removed_links,
        action=action
    )

import webbrowser
import threading

if __name__ == "__main__":
    app.run(debug=True)