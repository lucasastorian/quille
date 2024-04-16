import re
from typing import Optional


def convert_markdown_content_to_html(content: Optional[str]) -> str:
    """Converts the Markdown content to HTML"""
    if not content:
        return content

    # Replace bold sections
    content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
    # Replace italic sections
    content = re.sub(r'\*(.*?)\*', r'<i>\1</i>', content)

    content = convert_unordered_markdown_to_html_list(content=content)

    content = content.strip("\n")
    sections = content.split("\n")

    new_sections = []
    for section in sections:
        if section.startswith("### "):
            section = f"<h3>{section.lstrip('### ')}</h3>"
            new_sections.append(section)
        elif section.startswith("## "):
            section = f"<h2>{section.lstrip('## ')}</h2>"
            new_sections.append(section)
        elif section.startswith("# "):
            section = f"<h1>{section.lstrip('# ')}</h1>"
            new_sections.append(section)
        elif section == "":
            new_sections.append("<p></p>")
        else:
            new_sections.append(f"<p>{section}</p>")

    html_content = "".join(new_sections)

    return html_content


def convert_html_to_markdown(content: str) -> str:
    """Converts the HTML content back to Markdown"""
    content = re.sub(r'<strong>(.*?)</strong>', r'**\1**', content)
    content = re.sub(r"<i>(.*?)</i>", r"*\1*", content)
    content = convert_unordered_html_to_markdown_list(content=content)

    pattern = re.compile(r'<(h1|h2|h3|p)>(.*?)</\1>', re.DOTALL)
    matches = pattern.findall(content)

    markdown_sections = []
    for tag, content in matches:
        if tag == 'h1':
            markdown_sections.append(f"# {content.strip()}")
        elif tag == 'h2':
            markdown_sections.append(f"## {content.strip()}")
        elif tag == 'h3':
            markdown_sections.append(f"### {content.strip()}")
        elif tag == 'p':
            if content.strip():
                markdown_sections.append(content.strip())
            else:
                markdown_sections.append("")

    markdown_content = "\n".join(markdown_sections)

    return markdown_content


def convert_unordered_markdown_to_html_list(content: str):
    # Pattern to find Markdown lists blocks
    pattern = r"(?:^- .*\n)+"

    # Function to convert a Markdown list block to an HTML list
    def markdown_to_html_list(match):
        items = match.group(0).strip().split("\n")
        html_items = [f"<li>{item[2:].strip()}</li>" for item in items if item.strip()]
        return "<ul>" + "".join(html_items) + "</ul>"

    # Replace all Markdown list blocks with HTML lists
    content = re.sub(pattern, markdown_to_html_list, content, flags=re.MULTILINE)

    return content


def convert_unordered_html_to_markdown_list(content: str):
    def html_list_to_markdown(match):
        list_block = match.group(0)
        # Find all list items and convert them
        items = re.findall(r"<li>(.*?)</li>", list_block, flags=re.DOTALL)
        markdown_items = [f"- {item.strip()}" for item in items]
        return "\n".join(markdown_items) + "\n"

    # Pattern to find HTML <ul> blocks
    ul_pattern = r"<ul>.*?</ul>"

    # Replace all HTML list blocks with Markdown lists
    content = re.sub(ul_pattern, html_list_to_markdown, content, flags=re.DOTALL)

    return content
