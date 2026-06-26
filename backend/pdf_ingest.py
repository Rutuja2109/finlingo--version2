"""Generic PDF ingestion pipeline for FinLingo.

Uses `pdftotext` (poppler-utils) which is 15-20x faster than pdfplumber/pypdf
for large PDFs (12s vs 200s+ for a 300-page textbook).

Strategy:
1. Convert PDF to plain text with pdftotext (preserves layout).
2. Group lines by chapter using the running header regex.
3. Strip noise (copyright, repeated headers, page-section markers).
4. Cap body text per chapter so LLM cost stays predictable.
"""
from __future__ import annotations
import re
import shutil
import subprocess
import tempfile
import os
from dataclasses import dataclass, asdict
from typing import List, Optional, Pattern

# Running-header chapter pattern. Works for LOMA + most textbooks with running heads.
DEFAULT_CHAPTER_RE = re.compile(r"Ch\s+(\d+)\s*[:\.]\s*([A-Z][^|\n]+?)\s*\|", re.IGNORECASE)

NOISE_PATTERNS = [
    re.compile(r"Copyright\s+©.+?(?:loma\.org|reserved\.?)", re.IGNORECASE),
    re.compile(r"All\s+rights\s+reserved\.?", re.IGNORECASE),
    re.compile(r"www\.loma\.org", re.IGNORECASE),
    re.compile(r"Institutional Investing: Principles[^\n]*", re.IGNORECASE),
]


@dataclass
class ChapterExtract:
    chapter_no: int
    title: str
    body_text: str
    start_page: int
    end_page: int


def _clean_text(text: str) -> str:
    out = text
    for pat in NOISE_PATTERNS:
        out = pat.sub(" ", out)
    out = re.sub(r"\s+", " ", out).strip()
    return out


def _run_pdftotext(pdf_path: str) -> str:
    """Convert PDF to text using poppler-utils. Returns the full text."""
    if not shutil.which("pdftotext"):
        raise RuntimeError("pdftotext (poppler-utils) not installed")
    out = subprocess.run(
        ["pdftotext", "-raw", pdf_path, "-"],
        capture_output=True, text=True, timeout=120, check=False,
    )
    if out.returncode != 0:
        raise RuntimeError(f"pdftotext failed: {out.stderr[:300]}")
    return out.stdout


def extract_chapters(pdf_path: str, chapter_re: Optional[Pattern] = None,
                     max_chars_per_chapter: int = 12000,
                     max_chapters: int = 0) -> List[ChapterExtract]:
    """Parse PDF and return one entry per detected chapter."""
    pat = chapter_re or DEFAULT_CHAPTER_RE
    full = _run_pdftotext(pdf_path)
    lines = full.splitlines()

    chapters: dict[int, dict] = {}
    current_ch: Optional[int] = None
    page_no = 1  # form-feed delimits pages in pdftotext output

    for line in lines:
        if "\f" in line:
            page_no += line.count("\f")
            line = line.replace("\f", "")
        m = pat.search(line)
        if m:
            ch_no = int(m.group(1))
            title = m.group(2).strip().rstrip(":.- ")
            entry = chapters.setdefault(ch_no, {
                "title": title, "start": page_no, "end": page_no,
                "chunks": [], "total_chars": 0,
            })
            entry["end"] = page_no
            current_ch = ch_no
            continue
        if current_ch is None:
            continue
        entry = chapters[current_ch]
        if entry["total_chars"] >= max_chars_per_chapter:
            # Possible early exit
            if max_chapters > 0:
                filled = sum(1 for c in chapters.values()
                             if c["total_chars"] >= max_chars_per_chapter)
                if filled >= max_chapters:
                    break
            continue
        cleaned = _clean_text(line)
        if not cleaned or len(cleaned) < 3:
            continue
        room = max_chars_per_chapter - entry["total_chars"]
        entry["chunks"].append(cleaned[:room])
        entry["total_chars"] += len(cleaned[:room])

    out: List[ChapterExtract] = []
    for ch_no in sorted(chapters.keys()):
        c = chapters[ch_no]
        text = " ".join(c["chunks"]).strip()
        if not text:
            continue
        out.append(ChapterExtract(
            chapter_no=ch_no, title=c["title"], body_text=text,
            start_page=c["start"], end_page=c["end"],
        ))
    return out


def chapter_to_dict(c: ChapterExtract) -> dict:
    return asdict(c)
