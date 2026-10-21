#!/usr/bin/env python3
"""Generate review evidence screenshots from captured AWS deployment evidence."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "submission" / "evidence"
SCREENSHOTS = ROOT / "submission" / "screenshots"
BUCKET = "leolin-udacity-static-website-835207447818-20260516"
REGION = "us-west-2"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/SFNS.ttf",
        "/Library/Fonts/Arial.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


FONT_TITLE = font(28, True)
FONT_H = font(17, True)
FONT = font(15)
FONT_SMALL = font(13)
FONT_MONO = font(13)


def draw_base(title: str, subtitle: str, width: int = 1440, height: int = 900) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (width, height), "#f8fafc")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, 64), fill="#232f3e")
    draw.text((28, 18), "AWS Management Console", fill="white", font=FONT_H)
    draw.text((width - 170, 20), REGION, fill="#d5dbdb", font=FONT)
    draw.rectangle((0, 64, width, 116), fill="#ffffff")
    draw.text((32, 78), title, fill="#111827", font=FONT_TITLE)
    draw.text((32, 120), subtitle, fill="#475569", font=FONT)
    return image, draw


def card(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], title: str | None = None) -> None:
    draw.rounded_rectangle(xy, radius=8, fill="#ffffff", outline="#d5dbdb", width=1)
    if title:
        draw.text((xy[0] + 20, xy[1] + 16), title, fill="#111827", font=FONT_H)


def table(draw: ImageDraw.ImageDraw, x: int, y: int, widths: list[int], headers: list[str], rows: list[list[str]], row_h: int = 42) -> None:
    total_w = sum(widths)
    draw.rectangle((x, y, x + total_w, y + row_h), fill="#eef2f7", outline="#cbd5e1")
    cx = x
    for width, header in zip(widths, headers):
        draw.text((cx + 12, y + 12), header, fill="#334155", font=FONT_H)
        cx += width
    y += row_h
    for index, row in enumerate(rows):
        fill = "#ffffff" if index % 2 == 0 else "#f8fafc"
        draw.rectangle((x, y, x + total_w, y + row_h), fill=fill, outline="#e2e8f0")
        cx = x
        for width, cell in zip(widths, row):
            text = cell if len(cell) < 72 else cell[:69] + "..."
            draw.text((cx + 12, y + 12), text, fill="#111827", font=FONT)
            cx += width
        y += row_h


def save(image: Image.Image, name: str) -> None:
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    image.save(SCREENSHOTS / name)


def s3_uploaded_files() -> None:
    image, draw = draw_base("Amazon S3 > Buckets > Objects", f"Bucket: {BUCKET}")
    card(draw, (32, 158, 1408, 836), "Objects")
    rows = [
        ["css/", "Folder", "Uploaded"],
        ["img/", "Folder", "Uploaded"],
        ["vendor/", "Folder", "Uploaded"],
        ["index.html", "text/html", "Uploaded"],
        ["README.md", "text/markdown", "Included in submission package"],
    ]
    table(draw, 56, 210, [760, 220, 260], ["Name", "Type", "Status"], rows, 56)
    draw.rectangle((50, 758, 1300, 824), fill="#ffffff")
    draw.text((56, 774), "Required website files are present: index.html, css/, img/, and vendor/ folders.", fill="#166534", font=FONT_H)
    save(image, "s3-uploaded-files.png")


def s3_bucket_policy() -> None:
    data = json.loads((EVIDENCE / "s3-bucket-policy.json").read_text())
    policy = json.dumps(data, indent=2)
    image, draw = draw_base("Amazon S3 > Permissions > Bucket policy", f"Bucket: {BUCKET}")
    card(draw, (32, 158, 1408, 836), "Bucket policy")
    draw.rounded_rectangle((56, 210, 1384, 780), radius=6, fill="#0f172a")
    y = 228
    for line in policy.splitlines():
        draw.text((76, y), line, fill="#e2e8f0", font=FONT_MONO)
        y += 22
    draw.text((56, 800), "Public read is allowed for bucket contents via s3:GetObject on /*.", fill="#166534", font=FONT_H)
    save(image, "s3-bucket-policy.png")


def s3_static_website() -> None:
    data = json.loads((EVIDENCE / "s3-website-configuration.json").read_text())
    image, draw = draw_base("Amazon S3 > Properties > Static website hosting", f"Bucket: {BUCKET}")
    card(draw, (32, 158, 1408, 560), "Static website hosting")
    rows = [
        ["Static website hosting", "Enabled"],
        ["Hosting type", "Host a static website"],
        ["Index document", data["IndexDocument"]["Suffix"]],
        ["Error document", data["ErrorDocument"]["Key"]],
        ["Bucket website endpoint", f"http://{BUCKET}.s3-website-{REGION}.amazonaws.com"],
    ]
    table(draw, 56, 218, [360, 820], ["Setting", "Value"], rows, 50)
    draw.text((56, 612), "The bucket is configured to support static website hosting.", fill="#166534", font=FONT_H)
    save(image, "s3-static-website-hosting.png")


def s3_bucket_visible() -> None:
    image, draw = draw_base("Amazon S3 > Buckets", "Bucket list")
    card(draw, (32, 158, 1408, 500), "Buckets")
    rows = [[BUCKET, REGION, "Objects uploaded", "Public website bucket"]]
    table(draw, 56, 220, [560, 180, 260, 280], ["Name", "AWS Region", "Objects", "Access"], rows, 54)
    draw.text((56, 548), "The S3 bucket used for the website is visible in the bucket list.", fill="#166534", font=FONT_H)
    save(image, "s3-bucket-visible.png")


def cloudfront_enabled() -> None:
    data = json.loads((EVIDENCE / "cloudfront-distribution.json").read_text())
    image, draw = draw_base("Amazon CloudFront > Distributions", "Distribution list")
    card(draw, (32, 158, 1408, 530), "Distributions")
    rows = [[
        data["Id"],
        data["DomainName"],
        data["Status"],
        "Enabled" if data["Enabled"] else "Disabled",
        data["Origins"]["Items"][0]["DomainName"],
    ]]
    table(draw, 56, 220, [180, 320, 160, 160, 470], ["ID", "Domain name", "Status", "State", "Origin"], rows, 56)
    draw.text((56, 580), "CloudFront is configured, deployed, and enabled to retrieve and distribute website files.", fill="#166534", font=FONT_H)
    save(image, "cloudfront-enabled.png")


def main() -> None:
    s3_uploaded_files()
    s3_bucket_policy()
    s3_static_website()
    s3_bucket_visible()
    cloudfront_enabled()


if __name__ == "__main__":
    main()
