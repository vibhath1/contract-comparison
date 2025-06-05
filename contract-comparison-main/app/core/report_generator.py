#report_generator.py

from jinja2 import Template
from datetime import datetime

def generate_html_report(comparison_result: dict, filename: str = "comparison_report.html") -> str:
    template_str = """
    <html>
    <head>
        <title>Contract Comparison Report</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            h1, h2 { color: #2c3e50; }
            pre { background: #f4f4f4; padding: 10px; border-left: 4px solid #ccc; }
            .section { margin-bottom: 30px; }
        </style>
    </head>
    <body>
        <h1>Contract Comparison Report</h1>
        <p><strong>Generated:</strong> {{ timestamp }}</p>

        <div class="section">
            <h2>Text Differences (Semantic)</h2>
            {% if diff_as_list %}
                {% for item in diff %}
                    <div style="margin-bottom: 1em;">
                        <b>Doc 1:</b> {{ item.original_sentence }}<br>
                        <b>Doc 2:</b> {{ item.matched_sentence }}<br>
                        <b>Similarity Score:</b> {{ item.similarity_score }}<br>
                        <b>Note:</b> {{ item.note }}<br>
                    </div>
                {% endfor %}
            {% else %}
                <pre>{{ diff }}</pre>
            {% endif %}
        </div>

        <div class="section">
            <h2>Grammar Issues - Document 1</h2>
            <ul>
                {% for issue in grammar1 %}
                <li><strong>{{ issue.message }}</strong> — Suggestions: {{ issue.suggestions }}</li>
                {% endfor %}
            </ul>
        </div>

        <div class="section">
            <h2>Grammar Issues - Document 2</h2>
            <ul>
                {% for issue in grammar2 %}
                <li><strong>{{ issue.message }}</strong> — Suggestions: {{ issue.suggestions }}</li>
                {% endfor %}
            </ul>
        </div>

        <div class="section">
            <h2>Formatting Differences</h2>
            <pre>{{ formatting_diff | tojson(indent=2) }}</pre>
        </div>

        <div class="section">
            <h2>Visual Similarity</h2>
            <p>Similarity Score: <strong>{{ visual_score }}</strong></p>
        </div>
    </body>
    </html>
    """

    text_diff = comparison_result.get("text_diff", "")
    is_list = isinstance(text_diff, list)

    template = Template(template_str)
    html = template.render(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        diff=text_diff,
        diff_as_list=is_list,
        grammar1=comparison_result.get("grammar_issues_doc1", []),
        grammar2=comparison_result.get("grammar_issues_doc2", []),
        formatting_diff=comparison_result.get("formatting_diff", {}),
        visual_score=comparison_result.get("visual_comparison", {}).get("visual_similarity_score", "N/A")
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    return filename
