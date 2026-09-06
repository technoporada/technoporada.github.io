#!/usr/bin/env python3
# most_mowy.py - Wieża Babel: DE (hart, niskopoziomowo) -> PL (środek) -> JP (delikatnie)
# BUILD - Arek + Muse Spark

import random

# Proste słowniki mostu (dla demo, bez API)
DE_START = ["Systemüberwachung", "HARDLOCK", "Achtung", "Sicherheit", "Kontrolle"]
PL_MID = ["chaos to feature", "nie pytaj czemu działa", "kod ma działać", "pytaj czemu nie wybuchło"]
JP_END = ["光", "調和", "平和", "未来", "希望"]

# Mieszane warianty
MIX_TEMPLATES = [
    "{de} -> {pl} -> {jp}",
    "{de} {pl} {jp}",
    "{de}: {pl} // {jp}",
]

def most_mowy(prompt_pl="Test mostu"):
    """Zwraca prompt w 3 językach DE->PL->JP + wariant mieszany"""
    de = random.choice(DE_START)
    pl = random.choice(PL_MID) if prompt_pl=="Test mostu" else prompt_pl
    jp = random.choice(JP_END)
    # 3-jezyczny most
    bridge = f"{de} -> {pl} -> {jp}"
    # mieszany wariant
    mix = random.choice(MIX_TEMPLATES).format(de=de, pl=pl, jp=jp)
    return {"bridge": bridge, "mix": mix, "parts": {"de":de,"pl":pl,"jp":jp}}

def generate_batch(n=10):
    out=[]
    for i in range(n):
        out.append(most_mowy(f"prompt_{i+1} chaos"))
    return out

if __name__ == "__main__":
    print("=== MOST MOWY - Wieża Babel (DE->PL->JP) ===")
    for i in range(5):
        m = most_mowy()
        print(f"{i+1}. {m['bridge']} | mix: {m['mix']}")
    print("\nBatch 3:")
    for b in generate_batch(3):
        print(b)
    print("\nZapisano most_mowy.py - gotowe do stealth rotatora na #knajpa")
