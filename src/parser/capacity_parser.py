import re
from pathlib import Path


def read_text(path: Path) -> str:
    for enc in ("utf-8", "cp950", "big5", "latin-1"):
        try:
            return path.read_text(encoding=enc, errors="strict")
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="ignore")


def to_float(value):
    if not value:
        return None
    return float(str(value).replace(",", ""))


def gib_to_tib(value):
    return None if value is None else round(value / 1024, 2)


class CapacityParser:
    def parse(self, path: Path):
        text = read_text(path)

        if "SERVER USAGE" not in text or "/data:" not in text:
            return None

        hostname = self._find_value(text, "HOSTNAME")
        model = self._find_value(text, "MODEL_NO")
        serial = self._find_value(text, "SYSTEM_SERIALNO")
        ddos = self._find_value(text, "VERSION")

        generated = self._find_generated(text)

        pre_match = re.search(
            r"^/data:\s+pre-comp\s+-\s+([\d,\.]+)\s+-\s+-",
            text,
            re.MULTILINE,
        )

        post_match = re.search(
            r"^/data:\s+post-comp\s+([\d,\.]+)\s+([\d,\.]+)\s+([\d,\.]+)\s+(\d+)%",
            text,
            re.MULTILINE,
        )

        if not post_match:
            return None

        pre_gib = to_float(pre_match.group(1)) if pre_match else None
        size_gib, used_gib, avail_gib, use_pct = post_match.groups()

        return {
            "generated_time": generated,
            "hostname": hostname,
            "model": model,
            "serial": serial,
            "ddos": ddos,
            "pre_comp_used_tib": gib_to_tib(pre_gib),
            "post_comp_used_tib": gib_to_tib(to_float(used_gib)),
            "post_comp_size_tib": gib_to_tib(to_float(size_gib)),
            "post_comp_avail_tib": gib_to_tib(to_float(avail_gib)),
            "use_pct": to_float(use_pct),
            "source_file": str(path),
        }

    def _find_value(self, text: str, key: str) -> str:
        m = re.search(rf"^{re.escape(key)}=(.*)$", text, re.MULTILINE)
        return m.group(1).strip() if m else ""

    def _find_generated(self, text: str) -> str:
        m = re.search(
            r"==========\s+SERVER USAGE\s+==========.*?^GENERATED:\s*(.+)$",
            text,
            re.S | re.M,
        )
        return m.group(1).strip() if m else ""