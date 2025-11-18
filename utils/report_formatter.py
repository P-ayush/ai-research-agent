def json_to_markdown(data: dict) -> str:
    md = f"# {data.get('title','Research Report')}\n\n"

    md += "## Summary\n"
    md += f"{data.get('summary','No summary available.')}\n\n"

    for section in data.get("sections", []):
        md += f"## {section.get('heading', '')}\n"
        md += f"{section.get('content','')}\n\n"

    if "sources" in data and len(data["sources"]) > 0:
        md += "## Sources\n"
        for src in data["sources"]:
            md += f"- {src}\n"

    return md
