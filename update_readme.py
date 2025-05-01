import os
from collections import defaultdict
from datetime import datetime
from os.path import join


def build_toc(data_dir: str):
    # year → month → list of (date_str, filepath)
    grouped: dict[int, dict[str, list]] = defaultdict(lambda: defaultdict(list))

    for fname in sorted(os.listdir(data_dir), reverse=True):
        if not fname.endswith(".md"):
            continue
        date_str = fname[:-3]  # strip ".md"
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            # skip files that don’t match the date pattern
            continue

        y, m = dt.year, dt.strftime("%B")
        grouped[y][m].append((date_str, join(data_dir, fname)))

    return grouped


def render_readme(template_path: str, toc: dict):
    tpl = open(template_path, "r").read()

    now = datetime.now()
    current_year = now.year
    current_month = now.strftime("%B")

    update_str = now.strftime("Last update: %B %d, %Y at %I:%M %p")
    sections = [f"_**{update_str}**_\n"]

    # Sort years descending
    for year in sorted(toc.keys(), reverse=True):
        sections.append(f"### {year}\n")
        # Within each year, sort months by calendar order
        # Create a list of month names Jan–Dec
        month_order = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        # Reverse the order to get Dec–Jan
        month_order.reverse()

        for month in month_order:
            if month not in toc[year]:
                continue
            is_current = year == current_year and month == current_month
            if is_current:
                sections.append(f"#### 📅 {month} 🌟\n")
                for date_str, path in sorted(toc[year][month], reverse=True):
                    sections.append(f"- [{date_str}]({path})")
                sections.append("")  # blank line
            else:
                sections.append(f"<details><summary>📅 {month}</summary>\n\n")
                for date_str, path in sorted(toc[year][month], reverse=True):
                    sections.append(f"- [{date_str}]({path})")
                sections.append("\n</details>\n")
                sections.append("")  # blank line

    content = "\n".join(sections)
    return tpl.format(readme_content=content)


if __name__ == "__main__":
    DATA_DIR = "contents"
    TEMPLATE = "template.md"

    toc = build_toc(DATA_DIR)
    markdown = render_readme(TEMPLATE, toc)

    with open("README.md", "w") as f:
        f.write(markdown)
