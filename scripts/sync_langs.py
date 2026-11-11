import argparse
import json
import os
import re
import sys

LANG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "languages")
PRIMARY = "pt_br"
SECONDARY = "en_us"
BASES = (PRIMARY, SECONDARY)

def load(name):
    with open(os.path.join(LANG_DIR, name + ".json"), encoding="utf-8") as f:
        return json.load(f)


def save(name, data):
    with open(os.path.join(LANG_DIR, name + ".json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.write("\n")


def flatten(d, prefix=""):
    out = {}
    for k, v in d.items():
        p = prefix + k
        if isinstance(v, dict):
            out.update(flatten(v, p + "."))
        else:
            out[p] = v
    return out


def merge(base, target):
    result = {}
    for k, v in base.items():
        if isinstance(v, dict):
            sub = target.get(k) if isinstance(target.get(k), dict) else {}
            result[k] = merge(v, sub)
        else:
            result[k] = target[k] if k in target and not isinstance(target[k], dict) else v
    for k, v in target.items():
        if k not in result:
            result[k] = v
    return result


def union(primary, secondary):
    result = {}
    for k, v in primary.items():
        if isinstance(v, dict):
            sv = secondary.get(k) if isinstance(secondary.get(k), dict) else {}
            result[k] = union(v, sv)
        else:
            result[k] = v
    for k, v in secondary.items():
        if k not in result:
            result[k] = v
    return result


def is_translatable(key, value):
    if key.split(".")[-1].startswith("_"):
        return False
    if not isinstance(value, str):
        return False
    stripped = re.sub(r"§.|\{[^}]*\}", "", value)
    return re.search(r"[^\W\d_]", stripped) is not None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", default="report.md")
    args = ap.parse_args()

    names = sorted(f[:-5] for f in os.listdir(LANG_DIR) if f.endswith(".json"))
    pt = load(PRIMARY)
    en = load(SECONDARY)

    full_base = union(pt, en)
    pt_flat = flatten(pt)
    en_flat = flatten(en)

    added = {}
    for name in names:
        data = load(name)
        before = set(flatten(data))
        merged = merge(full_base, data)
        added[name] = sorted(set(flatten(merged)) - before)
        save(name, merged)

    lines = []
    total = 0
    for name in names:
        if name in BASES:
            continue
        same = [
            k
            for k, v in flatten(load(name)).items()
            if is_translatable(k, v) and (v == pt_flat.get(k) or v == en_flat.get(k))
        ]
        if not same and not added[name]:
            continue
        total += len(same)
        lines.append(f"<details><summary><b>{name}</b> - {len(same)} untranslated</summary>\n")
        if added[name]:
            lines.append(f"Keys added by the last sync: {len(added[name])}\n")
        lines.extend(f"- `{k}`" for k in same)
        lines.append("\n</details>\n")

    header = [
        "Keys whose value is identical to the base langs (`pt_br` / `en_us`) and are probably not translated yet.",
        f"\n**Total:** {total}\n",
    ]
    with open(args.report, "w", encoding="utf-8") as f:
        f.write("\n".join(header + lines) + "\n")
    print(f"Report: {total} untranslated keys")
    return 0


if __name__ == "__main__":
    sys.exit(main())
