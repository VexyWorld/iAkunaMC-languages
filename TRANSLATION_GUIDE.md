# iAkunaMC Translation Guide

Guide for LLMs and human translators contributing to iAkunaMC language files.

## Overview

- Base language: `pt_br.json` (Portuguese BR) — source of truth
- Reference translation: `en_us.json` (English US) — second most complete
- Available languages: `ar_sa`, `en_us`, `es_es`, `fr_fr`, `ja_jp`, `ru_ru`, `tr_tr`, `zh_cn`
- ~1542 translatable keys per file

---

## File Structure

Each file is a nested JSON object. Keys use dot-notation when referenced in this guide but are nested in the actual file.

```json
{
    "_displayname": "English (US)",
    "_authors": ["YourName"],
    "bedwars": {
        "game": {
            "waiting": "§cWaiting for more players..."
        }
    }
}
```

### Special keys (do NOT translate)
- `_displayname` — keep as the language's own name in its own script (e.g., `"日本語"`, `"Русский"`, `"العربية"`)
- `_authors` — add your name/handle to the array
- `_prefix` keys — copy exactly from `en_us.json`, do not translate (contain color codes only)

---

## Minecraft Color Codes (`§`)

Color codes are prefixed with `§` and a single character. They **must be preserved exactly** — position, order, and character all matter.

### Color reference
| Code | Color       | Common use in this project          |
|------|-------------|-------------------------------------|
| `§r` | Reset       | After game names, before normal text |
| `§7` | Grey        | Normal/body text                    |
| `§8` | Dark grey   | Brackets `§8(§8)`, separators `§8:` |
| `§f` | White       | Part of game names (`§fWars`)       |
| `§c` | Red         | Errors, BedWars name, alerts        |
| `§b` | Aqua        | SkyWars name, BlockSumo name        |
| `§e` | Yellow      | MlgBlock name                       |
| `§9` | Blue        | TheBridge name, Plot prefix         |
| `§2` | Dark green  | Duels name, emerald timer           |
| `§a` | Green       | Success messages, Skills            |
| `§5` | Purple      | Cosmetics                           |
| `§3` | Dark aqua   | Profile values                      |
| `§d` | Pink        | Party prefix                        |
| `§6` | Gold        | Missions prefix                     |

### Rules for color codes

**1. Game names are always colored the same way — never change them:**
```
§bSky§fWars        §cBed§fWars        §cThe§9Bridge
§eMlg§fBlock       §bBlock§fSumo      §2Duels
§fi§cAkuna§9MC
```

**2. After a colored game name inside a grey (§7) sentence, add `§7` before the next word:**
```
✗ §7Your §bSky§fWars wins
✓ §7Your §bSky§fWars §7wins

✗ §7Win {target} §cBed§fWars matches
✓ §7Win {target} §cBed§fWars §7matches
```

**3. Do NOT add §7 inside `§8(...)` parenthetical blocks:**
```
✓ §8(§cFinal Kill§8)     ← "Final Kill" stays red inside brackets
✓ §8(§f{count}§8)        ← value stays colored inside brackets
```

**4. Sentences starting with `§c` (error/warning) stay entirely red — do not inject `§7`:**
```
✓ §cVocê não pode fazer isso...
✓ §cInvalid mode...
```

---

## Placeholders

Placeholders like `{player}`, `{time}`, `{count}` are replaced at runtime. **Never translate them.**

```
✗ §7Começando em §c{tempo}s        ← "tempo" breaks the substitution
✓ §7Starting in §c{time}s          ← {time} unchanged
```

Placeholders are always inside `{}`. Common ones:
- `{player}`, `{killer}`, `{victim}`, `{target}` — player names
- `{time}`, `{seconds}`, `{start}` — countdowns
- `{count}`, `{max}`, `{total}` — numbers
- `{team}` — team name (already colored, e.g. `§aGreen`)
- `{n}` — **newline character**, not a placeholder to translate

---

## Newlines

`{n}` inside strings is a newline. Do not translate it. Scoreboard and profile strings are multi-line and use `{n}` extensively.

```
"§7Line one{n}§7Line two"
```

---

## Sections

### Game mode sections
`bedwars`, `skywars`, `mlgblock`, `blocksumo`, `thebridge`

Each has sub-sections:
- `game` — in-game messages (join, leave, countdown, win)
- `combat` — kill/death messages
- `command` — command responses
- `scoreboard` — in-game HUD (contains `{n}`, layout-sensitive)

### Lobby / profile
- `profile.profile` and `profile.profile_other` — long multi-line strings with `{n}`, contain statistics
- `lobby.*` — lobby scoreboards

### Economy
- `pay`, `balance`, `addbalance`, `economy` — Akunas currency messages
- Keep "Akunas" as-is (it's the server's currency name, a proper noun)

### Social
- `chat`, `tell`, `reply`, `party`, `clan`, `marriage`

### Punishments
- `ban`, `tempban`, `kick`, `mute`, `tempmute`, `warn`

### Missions (`mission`)
All mission description keys follow the pattern:
```
mission.<type>.<minigame>: "§7<Verb> {target} <object> in §bSky§fWars §7<trailing>"
```
Types: `kill`, `win`, `play`, `break`, `mine`, `score`, `first.kill`, `buy.items`, `buy.upgrades`, `complete`, `craft`, `get`, `place`

---

## Tone & style

- **Error messages** (`§c`): concise, second person, end with `...` for soft errors
  - `§cYou are not in an arena...`
  - `§cInvalid team...`
- **Success messages** (`§7`): friendly, confirm what happened
  - `§7You joined the §aGreen §7team!`
- **Prefixes** (`_prefix`): not translated, copy from `en_us.json`
- **Headers** (`§8-=-=-=-=== ... §8===-=-=-=-`): translate the label in the middle only
  - `§8-=-=-=-=== §fi§cAkuna§9MC §8| §7Available Settings §8===-=-=-=-`
  - Translate `Available Settings` only

---

## Commands in strings

Some strings contain command syntax hints. Translate the readable parts, keep command names as-is:

```
pt_br: §7Para entrar utilize §8/§7bw entrar §8<§7modo§8>
en_us: §7To join use §8/§7bw join §8<§7mode§8>
```

- `/bw`, `/sw`, `/p`, `/bwcustom`, etc. — do NOT translate
- Argument names inside `§8<§7...§8>` or `§8[§7...§8]` — translate to target language
- `§8/§7command` pattern — the `§8/` and `§7` color codes must stay

---

## What NOT to translate

| Item | Example | Reason |
|------|---------|--------|
| Game names | `§bSky§fWars`, `§cBed§fWars` | Proper nouns |
| Server name | `§fi§cAkuna§9MC` | Brand name |
| Currency | `Akunas` | Server-specific currency |
| Commands | `/bw`, `/sw`, `/p claim` | Command names |
| Placeholders | `{player}`, `{time}` | Runtime substitutions |
| URLs | `https://loja.iakunamc.com` | Links |
| Color codes | `§c`, `§7`, `§r` | Formatting |
| `_prefix` keys | `§cBed§fWars §8§l» §r` | UI decorators |

---

## Validation checklist

Before submitting a translation:

- [ ] All `{placeholder}` names match exactly (case-sensitive)
- [ ] All `§` color codes are preserved in the same positions relative to game names
- [ ] Game names (`§bSky§fWars` etc.) not modified
- [ ] `§7` added after game names when followed by plain text in grey sentences
- [ ] `_prefix`, `_displayname` keys handled correctly
- [ ] No Portuguese words left in non-pt_br file (compare suspicious strings with `en_us.json`)
- [ ] JSON is valid (no trailing commas, proper escaping)
- [ ] `{n}` preserved as-is in multi-line strings

---

## Adding a new language

1. Copy `en_us.json` as starting point (closer to neutral than pt_br)
2. Update `_displayname` to the language's own name
3. Add your name to `_authors`
4. Translate all string values, following rules above
5. Do not add or remove keys — key structure must match `pt_br.json`
6. File name format: `<lang>_<country>.json` (e.g., `de_de.json`, `ko_kr.json`)
