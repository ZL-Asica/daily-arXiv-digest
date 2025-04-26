import argparse
import json
import os
from itertools import count
from pathlib import Path


def get_ranker(preference: list[str]):
    def rank(cate: str) -> int:
        return preference.index(cate) if cate in preference else len(preference)

    return rank


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert AI-enhanced JSONL to Markdown."
    )
    parser.add_argument(
        "--data", type=str, help="Path to the input JSONL file", required=True
    )
    args = parser.parse_args()

    data_path = Path(args.data)
    data = []

    # Get preferred category order from env
    preference_str = os.environ.get("CATEGORIES", "cs.HC,cs.LG,cs.CL")
    preference = [c.strip() for c in preference_str.split(",")]

    # Load data
    with data_path.open("r", encoding="utf-8") as f:
        data = [json.loads(line) for line in f]

    # Rank categories by preference
    rank = get_ranker(preference)
    all_categories = sorted({item["categories"][0] for item in data}, key=rank)
    count_by_category = {cate: 0 for cate in all_categories}

    for item in data:
        first_cate = item["categories"][0]
        if first_cate in count_by_category:
            count_by_category[first_cate] += 1

    # Load markdown template
    template = Path("paper_template.md").read_text(encoding="utf-8")

    # Start writing markdown
    output_lines = []

    output_lines.append(f"# {data_path.stem.split('_')[0]}")
    output_lines.append("<div id=toc></div>\n\n## Table of Contents")

    for cate in all_categories:
        output_lines.append(f"- [{cate}](#{cate}) [Total: {count_by_category[cate]}]")

    idx = count(1)

    for cate in all_categories:
        output_lines.append(f"<div id='{cate}'></div>")
        output_lines.append(f"## {cate} [[Back]](#toc)")

        for item in data:
            if item["categories"][0] == cate:
                output_lines.append(
                    template.format(
                        title=item["title"],
                        authors=", ".join(item["authors"]),
                        summary=item["summary"].replace("\n", " "),
                        url=item["abs"],
                        tldr=item["AI"]["tldr"],
                        cate=cate,
                        keywords=", ".join(item["AI"]["keywords"]),
                        relevance_score=item["AI"]["importance_score"],
                        read_time=item["AI"]["read_time_minutes"],
                        motivation=item["AI"]["motivation"],
                        method=item["AI"]["method"],
                        result=item["AI"]["result"],
                        conclusion=item["AI"]["conclusion"],
                        key_contributions=", ".join(item["AI"]["key_contributions"]),
                        limitations=item["AI"]["limitations"],
                        future_work=item["AI"]["future_work"],
                        idx=next(idx),
                    )
                )

    output_md = data_path.with_name(data_path.stem.split("_")[0] + ".md")
    output_md = Path(str(output_md).replace("/data/", "/contents/"))
    output_md.write_text("\n\n".join(output_lines), encoding="utf-8")

    print(f"Total papers: {len(data)}")
    print(f"✅ Markdown saved to {output_md}")
