import re

def clean_markdown(md: str) -> str:
    lines = md.split("\n")

    # 1. Remove duplicated headers/footers (heuristic)
    # Find lines that repeat many times → treat as header/footer noise
    freq = {}
    for ln in lines:
        freq[ln] = freq.get(ln, 0) + 1
    repeated = {ln for ln, c in freq.items() if c > 5 and len(ln.strip()) > 0}
    lines = [ln for ln in lines if ln not in repeated]

    # 2. Normalize bullets
    bullet_map = {
        "•": "-",
        "◦": "-",
        "–": "-",
        "—": "-",
        "*": "-"
    }
    bullet_re = re.compile(r"^[\s]*([" + "".join(re.escape(k) for k in bullet_map.keys()) + r"])\s+")
    def normalize_bullet(line):
        m = bullet_re.match(line)
        if m:
            return bullet_re.sub("- ", line)
        return line
    lines = [normalize_bullet(ln) for ln in lines]

    # 3. Join hyphenated words
    out = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.rstrip().endswith("-") and i + 1 < len(lines):
            nxt = lines[i + 1].lstrip()
            if nxt and nxt[0].islower():
                ln = ln.rstrip()[:-1] + nxt
                i += 2
                out.append(ln)
                continue
        out.append(ln)
        i += 1
    lines = out

    # 4. Join paragraph lines
    joined = []
    i = 0
    while i < len(lines):
        ln = lines[i].rstrip()

        if i + 1 < len(lines):
            nxt = lines[i + 1].lstrip()

            # heading check
            is_heading = (
                ln.isupper()
                or re.match(r"^CHAPTER\s+\d+", ln)
                or re.match(r"^\d+(\.\d+)*$", ln)
            )

            # section-like line
            is_section_start = bool(re.match(r"^(§?\d+(\.\d+)*)(\s+.+)?$", ln))

            if (not is_heading and not is_section_start and
                (ln.endswith((",", ";", ":")) or
                 (not re.search(r"[.!?]$", ln) and nxt and nxt[0].islower()))):
                ln = ln + " " + nxt
                i += 2
                joined.append(ln)
                continue

        joined.append(ln)
        i += 1
    lines = joined

    # 5. Ensure numbering/citations stay intact
    def protect_identifiers(text):
        text = re.sub(r"(\bTable\s+\d[\w\.-]*)\s*\n", r"\1 ", text)
        text = re.sub(r"(\bFigure\s+\d[\w\.-]*)\s*\n", r"\1 ", text)
        text = re.sub(r"(\bAPPENDIX\s+[A-Z]+)\s*\n", r"\1 ", text)
        text = re.sub(r"(\bAnnex\s+[A-Z]+)\s*\n", r"\1 ", text)
        return text

    cleaned = protect_identifiers("\n".join(lines))

    # 6. Normalize headings (#, ##, ###)
    def normalize_heading(line):
        m = re.match(r"^(§?\d+(\.\d+)*)(\s+.+)$", line)
        if m:
            depth = m.group(1).count(".") + 1
            hashes = "#" * min(depth, 6)
            return f"{hashes} {line}"
        if re.match(r"^CHAPTER\s+\d+", line):
            return f"# {line}"
        return line

    final_lines = [normalize_heading(ln) for ln in cleaned.split("\n")]

    return "\n".join(final_lines)