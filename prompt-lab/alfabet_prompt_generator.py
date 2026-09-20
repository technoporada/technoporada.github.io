#!/usr/bin/env python3
# alfabet_prompt_generator.py - generator promptów z całego alfabetu w różnych językach
# BUILD - Arek + Muse Spark | jeden plik w jednym folderze przegeneruje wszystko

import random, json, string, pathlib

# Pełny alfabet + cyfry + polskie znaki
ALFABET = list(string.ascii_letters + string.digits + "ąćęłńóśźżĄĆĘŁŃÓŚŹŻ!@#$%^&*()-_=+[]{};:,.<>?/")
POLSKIE = list("ąćęłńóśźż")

# Szablony promptów w różnych językach (jak Wieża Babel: DE hart, PL środek, JP koniec)
TEMPLATES = {
    "pl": [
        "Napisz historię o {topic} w stylu {style}",
        "Wyjaśnij {topic} jak dla laika, dodaj hack {hack}",
        "Stwórz kod w Pythonie który {task} i używa {alfabet}",
        "Zrób analizę OSINT dla {topic} używając {tool}",
    ],
    "en": [
        "Write a story about {topic} in {style} style",
        "Explain {topic} like I'm 5, add hack {hack}",
        "Create Python code that {task} using {alfabet}",
        "Do OSINT analysis for {topic} using {tool}",
    ],
    "de": [
        "Schreibe eine Geschichte über {topic} im {style}-Stil",
        "Erkläre {topic} für Anfänger, füge Hack {hack} hinzu",
        "Erstelle Python-Code der {task} mit {alfabet}",
    ],
    "jp": [
        "{topic}について{style}スタイルで物語を書いて",
        "{topic}を初心者向けに説明し、ハック{hack}を追加",
        "{task}を行うPythonコードを{alfabet}で作成",
    ],
    "es": [
        "Escribe una historia sobre {topic} en estilo {style}",
        "Explica {topic} para novatos, añade hack {hack}",
    ],
}

TOPICS = ["chaos", "Tętnica Kodu", "ArekBox", "ThinkPad T440p", "przepowiednia", "kubiki Nyx", "Muse Spark", "pogoda", "proxy", "iptv"]
STYLES = ["cyberpunk", "noir", "glitch", "hard house 150 BPM", "Matrix rain", "Developer Chaos"]
HACKS = ["0xDEADBEEF", "whitelist", "dry-run", "self-healing 7890", "HIK!"]
TASKS = ["sortuje pliki", "rotuje proxy", "generuje obelgi", "sprawdza pogode", "szuka w kronice 4,6GB"]
TOOLS = ["nmap", "masscan", "edge-tts Zofia", "ollama", "ai_providers"]

def random_prompt(lang=None):
    lang = lang or random.choice(list(TEMPLATES.keys()))
    tmpl = random.choice(TEMPLATES[lang])
    # losowe znaki z alfabetu jako inspiracja
    alfabet_sample = ''.join(random.choices(ALFABET, k=5))
    return tmpl.format(
        topic=random.choice(TOPICS),
        style=random.choice(STYLES),
        hack=random.choice(HACKS),
        task=random.choice(TASKS),
        alfabet=alfabet_sample,
        tool=random.choice(TOOLS)
    ), lang

def prompt_3jezyki_2zdania():
    """Jeden prompt = 3 jezyki x max 2 zdania, kazdy pol tech (jak chcesz)"""
    # 2 zdania DE (tech polowa: np. Systemüberwachung + hack)
    de1,_ = random_prompt("de")
    de2,_ = random_prompt("de")
    de_part = f"{de1} {de2}".split(". ")[:2]
    de_part = ". ".join(de_part)[:200]
    if not de_part.endswith("."): de_part+="."
    # 2 zdania PL
    pl1,_ = random_prompt("pl")
    pl2,_ = random_prompt("pl")
    pl_part = f"{pl1} {pl2}".split(". ")[:2]
    pl_part = ". ".join(pl_part)[:200]
    if not pl_part.endswith("."): pl_part+="."
    # 2 zdania JP
    jp1,_ = random_prompt("jp")
    jp2,_ = random_prompt("jp")
    jp_part = f"{jp1} {jp2}".split(". ")[:2]
    jp_part = ". ".join(jp_part)[:200]
    if not jp_part.endswith("."): jp_part+="."
    # polacz: DE (2 zd) // PL (2 zd) // JP (2 zd)
    full = f"[DE] {de_part} // [PL] {pl_part} // [JP] {jp_part}"
    return full, "mix_3x2_tech"

def generate_batch(n=100, out_path="prompts_alfabet.jsonl"):
    out = pathlib.Path(__file__).parent / out_path
    with open(out, "w", encoding="utf-8") as f:
        for i in range(n):
            # co drugi prompt to nowy 3-jezyczny x2 zdania (jak chcesz)
            if i % 2 == 0:
                prompt, lang = prompt_3jezyki_2zdania()
            else:
                prompt, lang = random_prompt()
                # mieszany DE->PL->JP jak Most Mowy
                if i % 7 == 0:
                    de,_ = random_prompt("de")
                    pl,_ = random_prompt("pl")
                    jp,_ = random_prompt("jp")
                    prompt = f"{de} // {pl} // {jp}"
                    lang = "mix_DE_PL_JP"
            rec = {"id": i+1, "lang": lang, "prompt": prompt, "alfabet_sample": ''.join(random.choices(ALFABET, k=8))}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"✅ Wygenerowano {n} promptów (co drugi: 3 jezyki x2 zdania, pol tech) -> {out}")
    # podgląd
    with open(out, encoding="utf-8") as f:
        for line in [next(f) for _ in range(min(3,n))]:
            print(line.strip()[:220])
    return str(out)

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Generator promptów z alfabetu - jeden plik przegeneruje wszystko")
    ap.add_argument("-n", type=int, default=100, help="ile promptów")
    ap.add_argument("-o", default="prompts_alfabet.jsonl", help="plik wyjściowy")
    args = ap.parse_args()
    generate_batch(args.n, args.o)
    print(f"Użycie: python {__file__} -n 200 -o prompts.jsonl")
    print("Alfabet:", ''.join(ALFABET[:40]) + "... + polskie znaki")
