#!/usr/bin/env python3
"""
Derian's Cyber Class — CompTIA Certification Study Tool
Supports: Security+ SY0-701 · A+ Core 1 220-1201 · A+ Core 2 220-1202 · Network+ N10-009
Run with:  python3 derians_cyber_class.py
"""

import random, time, sys, os, re
from collections import defaultdict

# ══════════════════════════════════════════════════════════════════════════════
#  TERMINAL COLOUR PALETTE
# ══════════════════════════════════════════════════════════════════════════════

class C:
    RST  = "\033[0m"
    BOLD = "\033[1m"
    DIM  = "\033[2m"
    ITL  = "\033[3m"
    UL   = "\033[4m"

    BLK  = "\033[30m"
    RED  = "\033[91m"
    GRN  = "\033[92m"
    YLW  = "\033[93m"
    BLU  = "\033[94m"
    MAG  = "\033[95m"
    CYN  = "\033[96m"
    WHT  = "\033[97m"
    DGRY = "\033[90m"
    LRED = "\033[31m"
    LGRN = "\033[32m"
    LBLU = "\033[34m"
    LCYN = "\033[36m"
    LMAG = "\033[35m"
    ORG  = "\033[38;5;214m"
    PINK = "\033[38;5;213m"
    TEAL = "\033[38;5;51m"
    LIME = "\033[38;5;154m"
    PRP  = "\033[38;5;177m"
    SKY  = "\033[38;5;117m"
    GOLD = "\033[38;5;220m"
    SLTE = "\033[38;5;103m"

    BG_BLK  = "\033[40m"
    BG_RED  = "\033[41m"
    BG_GRN  = "\033[42m"
    BG_YLW  = "\033[43m"
    BG_BLU  = "\033[44m"
    BG_MAG  = "\033[45m"
    BG_CYN  = "\033[46m"
    BG_WHT  = "\033[47m"
    BG_DGRY = "\033[100m"
    BG_LRED = "\033[101m"
    BG_LGRN = "\033[102m"
    BG_ORG  = "\033[48;5;214m"
    BG_NVY  = "\033[48;5;17m"
    BG_CHAR = "\033[48;5;235m"
    BG_DARK = "\033[48;5;232m"

def clr(): os.system('cls' if os.name == 'nt' else 'clear')
def pause(msg="  Press ENTER to continue…"):
    input(f"\n{C.DGRY}{msg}{C.RST}")

# ══════════════════════════════════════════════════════════════════════════════
#  BOX-DRAWING HELPERS
# ══════════════════════════════════════════════════════════════════════════════

W = 80

def _center(text, width=W):
    plain = re.sub(r'\033\[[0-9;]*m', '', text)
    pad   = max(0, (width - len(plain)) // 2)
    return " " * pad + text

def _rpad(text, total, fill=" "):
    plain = re.sub(r'\033\[[0-9;]*m', '', text)
    return text + fill * max(0, total - len(plain))

def wrap_lines(text, width=72):
    words = str(text).split()
    lines, cur = [], ""
    for word in words:
        if len(cur) + len(word) + 1 > width:
            if cur.strip():
                lines.append(cur.rstrip())
            cur = word + " "
        else:
            cur += word + " "
    if cur.strip():
        lines.append(cur.rstrip())
    return lines or [""]

def print_wrapped(text, color=C.DGRY, indent="  ", width=76):
    for line in wrap_lines(text, width=max(20, width - len(indent))):
        print(f"{indent}{color}{line}{C.RST}")

def box(lines, color=C.CYN, title="", width=W):
    inner = width - 4
    tl, tr, bl, br = "╭", "╮", "╰", "╯"
    hz, vt         = "─", "│"
    if title:
        bar = hz * 2 + " " + title + " " + hz * max(0, inner - len(title) - 4)
    else:
        bar = hz * inner
    print(f"  {color}{tl}{bar}{tr}{C.RST}")
    for ln in lines:
        print(f"  {color}{vt}{C.RST} {_rpad(ln, inner)} {color}{vt}{C.RST}")
    print(f"  {color}{bl}{hz * inner}{br}{C.RST}")

def panel(lines, color=C.CYN, title="", width=W):
    inner = width - 4
    tl, tr, bl, br = "╔", "╗", "╚", "╝"
    hz, vt         = "═", "║"
    if title:
        bar = hz*2 + " " + title + " " + hz * max(0, inner - len(title) - 4)
    else:
        bar = hz * inner
    print(f"  {color}{tl}{bar}{tr}{C.RST}")
    for ln in lines:
        print(f"  {color}{vt}{C.RST} {_rpad(ln, inner)} {color}{vt}{C.RST}")
    print(f"  {color}{bl}{hz * inner}{br}{C.RST}")

def divider(ch="─", color=C.DGRY, width=W):
    print(f"  {color}{ch * (width-4)}{C.RST}")

def badge(text, bg=C.BG_BLU, fg=C.WHT):
    return f"{bg}{C.BOLD}{fg} {text} {C.RST}"

def tag(text, color=C.CYN):
    return f"{color}{C.BOLD}[{text}]{C.RST}"

def gradient_bar(pct, width=30, filled_ch="█", empty_ch="░"):
    filled = int(pct / 100 * width)
    if pct >= 75:   col = C.LIME
    elif pct >= 55: col = C.GOLD
    elif pct >= 40: col = C.ORG
    else:           col = C.RED
    return f"{col}{filled_ch * filled}{C.DGRY}{empty_ch * (width - filled)}{C.RST}"

def stars(pct):
    if pct >= 90: return f"{C.GOLD}★★★★★{C.RST}"
    if pct >= 80: return f"{C.GOLD}★★★★{C.DGRY}☆{C.RST}"
    if pct >= 70: return f"{C.GOLD}★★★{C.DGRY}☆☆{C.RST}"
    if pct >= 55: return f"{C.GOLD}★★{C.DGRY}☆☆☆{C.RST}"
    return f"{C.DGRY}★{C.RST}{C.DGRY}☆☆☆☆{C.RST}"

def streak_badge(n):
    if n == 0:   return ""
    if n < 3:    return f" {C.YLW}🔥×{n}{C.RST}"
    if n < 6:    return f" {C.ORG}{C.BOLD}🔥×{n} HOT!{C.RST}"
    return          f" {C.RED}{C.BOLD}🔥×{n} ON FIRE!!{C.RST}"

def typing(text, delay=0.018, color=""):
    for ch in f"{color}{text}{C.RST if color else ''}":
        sys.stdout.write(ch); sys.stdout.flush(); time.sleep(delay)
    print()

def flash(msg, bg, fg=C.WHT, pause_after=0.7):
    clr()
    print("\n" * 6)
    print(_center(f"{bg}{C.BOLD}{fg}  {msg}  {C.RST}"))
    print("\n" * 6)
    time.sleep(pause_after)

def mini_spinner(msg="Loading", duration=0.8):
    frames = ["⣾","⣽","⣻","⢿","⡿","⣟","⣯","⣷"]
    t = time.time()
    i = 0
    while time.time() - t < duration:
        sys.stdout.write(f"\r  {C.CYN}{frames[i % len(frames)]}{C.RST}  {C.DGRY}{msg}…{C.RST}  ")
        sys.stdout.flush()
        time.sleep(0.07)
        i += 1
    sys.stdout.write("\r" + " " * 40 + "\r")
    sys.stdout.flush()

# ══════════════════════════════════════════════════════════════════════════════
#  GENERIC DOMAIN THEME HELPER
# ══════════════════════════════════════════════════════════════════════════════

DIFF_STYLE = {
    "easy":   (C.LGRN, "▸ Easy",   "●"),
    "medium": (C.GOLD, "▸▸ Medium", "●●"),
    "hard":   (C.LRED, "▸▸▸ Hard",  "●●●"),
}

def resolve_theme(domain_str, theme_dict):
    for k, v in theme_dict.items():
        if domain_str.startswith(k):
            return v
    return {"color": C.CYN, "icon": "❓", "short": "??", "bg": C.BG_BLU}

# ══════════════════════════════════════════════════════════════════════════════
#  SPLASH SCREEN — MAIN (cert-agnostic)
# ══════════════════════════════════════════════════════════════════════════════

MAIN_LOGO = r"""
   ██████╗  ██╗      ██╗   ██╗  ███████╗
  ██╔════╝  ██║      ██║   ██║  ██╔════╝
  ██║       ██║      ██║   ██║  ███████╗
  ██║       ██║      ██║   ██║       ██╝
  ╚██████╗  ███████╗ ╚██████╔╝  ███████╗
   ╚═════╝  ╚══════╝  ╚═════╝   ╚══════╝
"""

def splash_main():
    clr()
    logo_lines = MAIN_LOGO.strip("\n").split("\n")
    logo_colors = [C.TEAL, C.CYN, C.SKY, C.BLU, C.MAG, C.PRP]
    print()
    for i, line in enumerate(logo_lines):
        col = logo_colors[i % len(logo_colors)]
        print(_center(f"{col}{C.BOLD}{line}{C.RST}"))

    print()
    print(_center(f"{C.GOLD}{C.BOLD}✦  Derian's Cyber Class  ✦{C.RST}"))
    print(_center(f"{C.DGRY}CompTIA Certification Study Platform{C.RST}"))
    print()
    cert_line = (
        f"{C.TEAL}{C.BOLD}🔐 Security+{C.RST}  {C.DGRY}·{C.RST}  "
        f"{C.ORG}{C.BOLD}🖥️ A+ Core 1{C.RST}  {C.DGRY}·{C.RST}  "
        f"{C.RED}{C.BOLD}🛡️ A+ Core 2{C.RST}  {C.DGRY}·{C.RST}  "
        f"{C.SKY}{C.BOLD}🌐 Network+{C.RST}"
    )
    print(_center(cert_line))
    print()
    bar_width = 38
    print(_center(f"{C.DGRY}Initialising study engine…{C.RST}"))
    sys.stdout.write("  " + " " * ((W - bar_width) // 2 - 2))
    sys.stdout.flush()
    for i in range(bar_width + 1):
        pct = i / bar_width * 100
        col = C.TEAL if pct < 50 else (C.LIME if pct < 85 else C.GOLD)
        bar = f"{col}{'█' * i}{C.DGRY}{'░' * (bar_width - i)}{C.RST}"
        sys.stdout.write(f"\r  {' ' * ((W - bar_width) // 2 - 2)}{bar}  {C.DGRY}{pct:3.0f}%{C.RST}")
        sys.stdout.flush()
        time.sleep(0.02)
    print("\n")
    print(_center(f"{C.LGRN}{C.BOLD}✓  Ready — 4 certifications loaded{C.RST}"))
    print()
    input(_center(f"{C.DGRY}Press ENTER to choose your path…{C.RST}"))

def cert_splash(cfg):
    """Per-certification loading screen shown when a cert is selected."""
    clr()
    col   = cfg["color"]
    logo_lines = MAIN_LOGO.strip("\n").split("\n")
    logo_colors_cert = [col, C.CYN, col, C.SKY, col, C.WHT]
    print()
    for i, line in enumerate(logo_lines):
        c2 = logo_colors_cert[i % len(logo_colors_cert)]
        print(_center(f"{c2}{C.BOLD}{line}{C.RST}"))
    print()
    print(_center(f"{col}{C.BOLD}✦  {cfg['name']}  ✦{C.RST}"))
    print(_center(f"{C.DGRY}Derian's Cyber Class — {cfg['code']}{C.RST}"))
    print()
    theme = cfg["domain_theme"]
    tags_line = "  ".join([
        f"{v['color']}{C.BOLD}{v['icon']} D{i+1}{C.RST}"
        for i, v in enumerate(theme.values())
    ])
    print(_center(tags_line))
    print()
    bar_width = 38
    q_count   = len(cfg["questions"])
    d_count   = len(theme)
    print(_center(f"{C.DGRY}Loading {q_count} questions across {d_count} domains…{C.RST}"))
    sys.stdout.write("  " + " " * ((W - bar_width) // 2 - 2))
    sys.stdout.flush()
    for i in range(bar_width + 1):
        pct = i / bar_width * 100
        c2  = col if pct < 50 else (C.LIME if pct < 85 else C.GOLD)
        bar = f"{c2}{'█' * i}{C.DGRY}{'░' * (bar_width - i)}{C.RST}"
        sys.stdout.write(f"\r  {' ' * ((W - bar_width) // 2 - 2)}{bar}  {C.DGRY}{pct:3.0f}%{C.RST}")
        sys.stdout.flush()
        time.sleep(0.02)
    print("\n")
    print(_center(f"{C.LGRN}{C.BOLD}✓  {q_count} questions loaded — Let's get it!{C.RST}"))
    print()
    input(_center(f"{C.DGRY}Press ENTER to enter the arena…{C.RST}"))

# ══════════════════════════════════════════════════════════════════════════════
#  CERTIFICATION SELECTOR
# ══════════════════════════════════════════════════════════════════════════════

def cert_selector():
    """Second loading/selection screen — choose which cert to study."""
    while True:
        clr()
        print()
        panel([
            f"  {C.GOLD}{C.BOLD}✦  Choose Your Certification Path  ✦{C.RST}",
            f"  {C.DGRY}Pick a cert and get to work. You've got this.{C.RST}",
            "",
        ], color=C.GOLD, title="STUDY PATH")
        print()

        paths = [
            (C.TEAL,  "1", "🔐", "CompTIA Security+", "SY0-701",
             "5 domains · 750 scaled pass score · Up to 90 questions",
             f"{C.DGRY}Threats · Crypto · Architecture · Operations · Governance{C.RST}"),
            (C.ORG,   "2", "🖥️", "CompTIA A+  Core 1", "220-1201",
             "5 domains · 675 scaled pass score · 90 questions",
             f"{C.DGRY}Mobile Devices · Networking · Hardware · Cloud · Troubleshooting{C.RST}"),
            (C.RED,   "3", "🛡️", "CompTIA A+  Core 2", "220-1202",
             "4 domains · 700 scaled pass score · 90 questions",
             f"{C.DGRY}Operating Systems · Security · Software Troubleshooting · Procedures{C.RST}"),
            (C.SKY,   "4", "🌐", "CompTIA Network+",  "N10-009",
             "5 domains · 720 scaled pass score · Up to 90 questions",
             f"{C.DGRY}Concepts · Implementation · Operations · Security · Troubleshooting{C.RST}"),
        ]

        for col, key, ico, name, code, tagline, domains in paths:
            print(f"  {col}{C.BOLD}[{key}]{C.RST}  {ico}  {C.WHT}{C.BOLD}{name:<26}{C.RST}  "
                  f"{C.GOLD}{code}{C.RST}")
            print(f"        {C.DGRY}{tagline}{C.RST}")
            print(f"        {domains}")
            print()

        divider(ch="─", color=C.DGRY)
        print(f"  {C.DGRY}[Q] Quit  ·  [B] Back to intro{C.RST}")
        print()
        c = input(f"  {C.BOLD}{C.WHT}Select path › {C.RST}").strip().upper()

        key_map = {"1": "secplus", "2": "aplus1", "3": "aplus2", "4": "netplus"}
        if c == "Q":
            clr()
            print()
            print(_center(f"{C.CYN}{C.BOLD}Keep grinding — certs don't pass themselves!{C.RST}"))
            print()
            sys.exit(0)
        elif c == "B":
            splash_main()
            continue
        elif c in key_map:
            return key_map[c]
        else:
            mini_spinner("Invalid selection")

# ══════════════════════════════════════════════════════════════════════════════
#  QUESTION DISPLAY
# ══════════════════════════════════════════════════════════════════════════════

CHOICE_COLORS = {"A": C.CYN, "B": C.SKY, "C": C.TEAL, "D": C.LCYN}

def show_question(q, num, total_q, streak=0, theme_dict=None):
    if theme_dict is None:
        theme_dict = {}
    clr()
    th = resolve_theme(q["domain"], theme_dict)
    dcol = th["color"]
    icon = th["icon"]
    diff_col, diff_label, diff_dots = DIFF_STYLE.get(q["difficulty"], (C.WHT, "?", "?"))

    progress_pct = (num - 1) / total_q * 100
    prog_bar = gradient_bar(progress_pct, width=24)

    print()
    status = (
        f"{dcol}{C.BOLD}{icon} {q['domain'][:28]}{C.RST}"
        f"  {C.DGRY}│{C.RST}  "
        f"{diff_col}{diff_label}{C.RST}"
        f"  {C.DGRY}│{C.RST}  "
        f"{C.DGRY}Q {num}/{total_q}{C.RST}"
        f"{streak_badge(streak)}"
    )
    print(f"  {status}")
    print(f"  {C.DGRY}Progress:{C.RST} {prog_bar} {C.DGRY}{progress_pct:.0f}%{C.RST}  "
          f"{C.GOLD}{C.BOLD}{q['topic']}{C.RST}")

    print()
    inner_w = W - 8
    q_words = q["question"].split()
    q_lines = []
    cur = ""
    for word in q_words:
        if len(cur) + len(word) + 1 > inner_w:
            q_lines.append(cur.rstrip())
            cur = word + " "
        else:
            cur += word + " "
    if cur.strip():
        q_lines.append(cur.rstrip())

    inner = W - 4
    tl, tr, bl, br = "╭", "╮", "╰", "╯"
    hz, vt = "─", "│"
    q_bar = hz * 2 + f" {dcol}{C.BOLD}QUESTION{C.RST} " + f"{dcol}{hz * max(0, inner - 13)}{C.RST}"
    print(f"  {dcol}{tl}{q_bar}{tr}{C.RST}")
    print(f"  {dcol}{vt}{C.RST}{' ' * inner}{dcol}{vt}{C.RST}")
    for ql in q_lines:
        pad = inner - len(re.sub(r'\033\[[0-9;]*m', '', ql)) - 2
        print(f"  {dcol}{vt}{C.RST}  {C.WHT}{C.BOLD}{ql}{C.RST}{' ' * max(0, pad)}  {dcol}{vt}{C.RST}")
    print(f"  {dcol}{vt}{C.RST}{' ' * inner}{dcol}{vt}{C.RST}")
    print(f"  {dcol}{bl}{hz * inner}{br}{C.RST}")

    print()
    for letter, text in q["choices"].items():
        col   = CHOICE_COLORS.get(letter, C.WHT)
        words = text.split()
        lines_c = []
        cur_c = ""
        max_w = inner_w - 4
        for w in words:
            if len(cur_c) + len(w) + 1 > max_w:
                lines_c.append(cur_c.rstrip())
                cur_c = w + " "
            else:
                cur_c += w + " "
        if cur_c.strip():
            lines_c.append(cur_c.rstrip())

        bullet = f"{col}{C.BOLD}  ◆ [{letter}]{C.RST}"
        first_line = lines_c[0] if lines_c else ""
        print(f"  {bullet}  {C.WHT}{first_line}{C.RST}")
        for extra in lines_c[1:]:
            print(f"           {C.DGRY}{extra}{C.RST}")

    print()
    divider(ch="─", color=C.DGRY)
    prompt_opts = (
        f"{tag('A')} {tag('B')} {tag('C')} {tag('D')}"
        f"  {C.DGRY}│{C.RST}  {C.GOLD}{C.BOLD}[H]{C.RST}{C.DGRY} Hint{C.RST}"
        f"  {C.DGRY}│{C.RST}  {C.SLTE}[S]{C.RST}{C.DGRY} Skip{C.RST}"
        f"  {C.DGRY}│{C.RST}  {C.LRED}[Q]{C.RST}{C.DGRY} Quit{C.RST}"
    )
    print(f"\n  {prompt_opts}\n")

    while True:
        raw = input(f"  {C.BOLD}{C.WHT}Your answer ›{C.RST} ").strip().upper()
        if raw == "Q": return "QUIT"
        if raw == "S": return "SKIP"
        if raw == "H":
            wrong = [k for k in q["choices"] if k != q["answer"]]
            elim  = random.choice(wrong)
            print(f"\n  {C.GOLD}💡 Hint:{C.RST} {C.DGRY}Option{C.RST} {C.RED}{C.BOLD}[{elim}]{C.RST} {C.DGRY}is NOT the correct answer.{C.RST}\n")
            continue
        if raw in q["choices"]: return raw
        print(f"  {C.RED}⚠  Please enter A, B, C, or D.{C.RST}")

# ══════════════════════════════════════════════════════════════════════════════
#  RESULT SCREEN
# ══════════════════════════════════════════════════════════════════════════════

def show_result(q, user_ans, streak=0, theme_dict=None):
    if theme_dict is None:
        theme_dict = {}
    correct = (user_ans == q["answer"])
    th      = resolve_theme(q["domain"], theme_dict)
    dcol    = th["color"]

    print()
    if correct:
        result_lines = [
            f"{C.LGRN}{C.BOLD}  ✔  CORRECT!{streak_badge(streak)}{C.RST}",
            f"  {C.WHT}{q['choices'][q['answer']]}{C.RST}",
        ]
        box(result_lines, color=C.LGRN)
    else:
        result_lines = [
            f"{C.RED}{C.BOLD}  ✘  INCORRECT{C.RST}",
            f"  {C.DGRY}You chose:{C.RST}  {C.RED}[{user_ans}] {q['choices'].get(user_ans,'?')}{C.RST}",
            f"  {C.DGRY}Correct:  {C.RST}  {C.LGRN}{C.BOLD}[{q['answer']}] {q['choices'][q['answer']]}{C.RST}",
        ]
        box(result_lines, color=C.RED)

    print()
    inner_w = W - 8
    exp_words = q["explanation"].split()
    exp_lines = []
    cur = ""
    for word in exp_words:
        if len(cur) + len(word) + 1 > inner_w:
            exp_lines.append(cur.rstrip())
            cur = word + " "
        else:
            cur += word + " "
    if cur.strip():
        exp_lines.append(cur.rstrip())

    inner = W - 4
    tl, tr, bl, br = "╭", "╮", "╰", "╯"
    hz, vt = "─", "│"
    exp_bar = (hz * 2 + f" {C.MAG}{C.BOLD}💬 Derian's Cyber Class Explanation{C.RST} "
               + f"{C.MAG}{hz * max(0, inner - 38)}{C.RST}")
    print(f"  {C.MAG}{tl}{exp_bar}{tr}{C.RST}")
    print(f"  {C.MAG}{vt}{C.RST}{' ' * inner}{C.MAG}{vt}{C.RST}")
    for el in exp_lines:
        plain_len = len(re.sub(r'\033\[[0-9;]*m', '', el))
        pad       = inner - plain_len - 2
        print(f"  {C.MAG}{vt}{C.RST}  {C.WHT}{el}{C.RST}{' ' * max(0, pad)}  {C.MAG}{vt}{C.RST}")
    print(f"  {C.MAG}{vt}{C.RST}{' ' * inner}{C.MAG}{vt}{C.RST}")
    print(f"  {C.MAG}{bl}{hz * inner}{br}{C.RST}")

# ══════════════════════════════════════════════════════════════════════════════
#  SCORE TRACKER
# ══════════════════════════════════════════════════════════════════════════════

class ScoreTracker:
    def __init__(self):
        self.reset()

    def reset(self):
        self.total        = 0
        self.correct      = 0
        self.streak       = 0
        self.best_streak  = 0
        self.domain_stats = defaultdict(lambda: {"correct": 0, "total": 0})
        self.history      = []
        self.start_time   = time.time()

    def record(self, q, user_ans):
        hit = (user_ans == q["answer"])
        self.total  += 1
        if hit:
            self.correct += 1
            self.streak  += 1
            self.best_streak = max(self.best_streak, self.streak)
        else:
            self.streak = 0
        self.domain_stats[q["domain"]]["total"]   += 1
        if hit:
            self.domain_stats[q["domain"]]["correct"] += 1
        self.history.append({
            "question": q["question"][:60] + "…",
            "your":     f"[{user_ans}] {q['choices'].get(user_ans,'?')}",
            "correct":  f"[{q['answer']}] {q['choices'][q['answer']]}",
            "hit":      hit,
            "domain":   q["domain"],
            "topic":    q["topic"],
        })

    def pct(self):
        return self.correct / self.total * 100 if self.total else 0

    def render_final(self, dom_order=None, theme_dict=None, cert_name=""):
        if dom_order is None:
            dom_order = sorted(self.domain_stats.keys())
        if theme_dict is None:
            theme_dict = {}
        elapsed = int(time.time() - self.start_time)
        mins, secs = divmod(elapsed, 60)
        pct = self.pct()

        clr()
        print()
        score_color = C.LGRN if pct >= 80 else (C.GOLD if pct >= 65 else C.RED)
        print(_center(f"{score_color}{C.BOLD}{'━'*40}{C.RST}"))
        print(_center(f"{score_color}{C.BOLD}   SESSION COMPLETE   {C.RST}"))
        if cert_name:
            print(_center(f"{C.DGRY}  {cert_name}  {C.RST}"))
        print(_center(f"{score_color}{C.BOLD}{'━'*40}{C.RST}"))
        print()
        print(_center(f"{score_color}{C.BOLD}{pct:.1f}%{C.RST}  {stars(pct)}"))
        print(_center(f"{C.DGRY}{self.correct} correct / {self.total} answered  ·  {mins}m {secs}s{C.RST}"))
        print(_center(f"{C.GOLD}Best streak: 🔥×{self.best_streak}{C.RST}"))
        print()

        if pct >= 85:
            verdict = f"{C.LGRN}{C.BOLD}🏆  EXAM READY — Outstanding performance!{C.RST}"
            tip_txt  = "Keep reviewing weak domains to maintain your edge."
        elif pct >= 75:
            verdict = f"{C.GOLD}{C.BOLD}🎯  CLOSE TO PASSING — You're almost there!{C.RST}"
            tip_txt  = "Focus on reds below and review the weak domains."
        elif pct >= 60:
            verdict = f"{C.ORG}{C.BOLD}📚  KEEP STUDYING — Good foundation, needs work.{C.RST}"
            tip_txt  = "Spend extra time on weak domains and re-drill wrong answers."
        else:
            verdict = f"{C.RED}{C.BOLD}⚡  MORE PRACTICE NEEDED — Don't give up!{C.RST}"
            tip_txt  = "Review missed objectives and keep drilling the weak domains."

        print(_center(verdict))
        print(_center(f"{C.DGRY}{C.ITL}{tip_txt}{C.RST}"))
        print()

        print(f"  {C.WHT}{C.BOLD}Domain Performance{C.RST}")
        print(f"  {C.DGRY}{'─'*72}{C.RST}")

        for dom in dom_order:
            stats = self.domain_stats.get(dom, {"correct":0,"total":0})
            t = stats["total"]
            if t == 0:
                continue
            c   = stats["correct"]
            p   = c / t * 100
            th  = resolve_theme(dom, theme_dict)
            col = th["color"]
            ico = th["icon"]
            bar = gradient_bar(p, width=22)
            label = dom.replace("Domain ", "D").split("–")[0].strip()
            grade_col = C.LGRN if p >= 80 else (C.GOLD if p >= 65 else C.RED)
            print(f"  {col}{ico}{C.RST} {C.DGRY}{label:<5}{C.RST} "
                  f"{bar} {grade_col}{C.BOLD}{p:5.1f}%{C.RST} "
                  f"{C.DGRY}({c}/{t}){C.RST} {stars(p)}")
        print()

    def render_mini(self):
        pct = self.pct()
        bar = gradient_bar(pct, width=20)
        col = C.LGRN if pct >= 80 else (C.GOLD if pct >= 65 else C.RED)
        print(f"\n  {C.DGRY}Running score:{C.RST} {bar} "
              f"{col}{C.BOLD}{pct:.1f}%{C.RST}  "
              f"{C.DGRY}{self.correct}/{self.total}{C.RST}"
              f"{streak_badge(self.streak)}\n")

tracker = ScoreTracker()

# ══════════════════════════════════════════════════════════════════════════════
#  WEIGHTED EXAM POOL
# ══════════════════════════════════════════════════════════════════════════════

def weighted_exam_pool(pool, domain_weights, total=75):
    target = min(total, len(pool))
    if target <= 0:
        return []

    by_domain = defaultdict(list)
    for q in pool:
        by_domain[q["domain"]].append(q)

    raw_counts = {}
    counts = {}
    for dom, weight in domain_weights.items():
        exact = target * weight / 100
        raw_counts[dom] = exact
        counts[dom] = int(exact)

    assigned = sum(counts.values())
    leftovers = target - assigned
    fractions = sorted(
        domain_weights.keys(),
        key=lambda dom: raw_counts[dom] - counts[dom],
        reverse=True,
    )
    for dom in fractions[:leftovers]:
        counts[dom] += 1

    selected = []
    for dom in domain_weights:
        domain_pool = list(by_domain.get(dom, []))
        random.shuffle(domain_pool)
        selected.extend(domain_pool[:counts[dom]])

    selected_ids = {id(q) for q in selected}
    if len(selected) < target:
        remaining = [q for q in pool if id(q) not in selected_ids]
        random.shuffle(remaining)
        selected.extend(remaining[:target - len(selected)])

    random.shuffle(selected)
    return selected[:target]

# ══════════════════════════════════════════════════════════════════════════════
#  GAME MODES
# ══════════════════════════════════════════════════════════════════════════════

def run_quiz(pool, cfg, num=20, mode_name="Quick Quiz"):
    random.shuffle(pool)
    pool = pool[:num]
    tracker.reset()

    clr()
    print()
    box([
        f"  {C.CYN}{C.BOLD}⚡  {mode_name}{C.RST}",
        f"  {C.DGRY}{len(pool)} questions  ·  instant feedback  ·  streak tracking{C.RST}",
    ], color=C.CYN)
    print()
    input(f"  {C.DGRY}Press ENTER to begin…{C.RST}")

    td = cfg["domain_theme"]
    for i, q in enumerate(pool, 1):
        ans = show_question(q, i, len(pool), tracker.streak, td)
        if ans == "QUIT":
            break
        if ans == "SKIP":
            tracker.streak = 0
            print(f"\n  {C.DGRY}Skipped.{C.RST}")
            pause()
            continue
        tracker.record(q, ans)
        show_result(q, ans, tracker.streak, td)
        tracker.render_mini()
        pause()

    tracker.render_final(cfg["dom_order"], td, cfg["name"])
    pause()


def practice_exam(pool, cfg):
    clr()
    print()
    exam_q = cfg.get("exam_q", 75)
    panel([
        f"  {cfg['color']}{C.BOLD}🏆  PRACTICE EXAM  —  {exam_q} Questions  ·  Timed{C.RST}",
        f"",
        f"  {C.WHT}Simulates the real {cfg['code']} exam experience with domain weighting.{C.RST}",
        f"  {C.DGRY}Answer all questions, then review results at the end.{C.RST}",
        f"  {C.DGRY}Real exam: up to 90 questions  ·  90 minutes.{C.RST}",
        f"  {C.GOLD}Official passing score: {cfg['pass_score']} on a 100-900 scale{C.RST}",
    ], color=cfg["color"], title="EXAM MODE")
    print()
    input(f"  {C.BOLD}Press ENTER to start the clock…{C.RST} ")

    exam_pool = weighted_exam_pool(pool, cfg["domain_weights"], total=exam_q)
    tracker.reset()
    answers   = {}
    start     = time.time()
    td        = cfg["domain_theme"]

    for i, q in enumerate(exam_pool, 1):
        ans = show_question(q, i, len(exam_pool), tracker.streak, td)
        if ans == "QUIT":
            break
        if ans == "SKIP":
            answers[i] = {"q": q, "ans": None}
            tracker.streak = 0
            continue
        answers[i] = {"q": q, "ans": ans}
        tracker.record(q, ans)
        correct = (ans == q["answer"])
        if correct:
            print(f"\n  {C.LGRN}●{C.RST}  {C.DGRY}Marked.{C.RST}  {streak_badge(tracker.streak)}")
        else:
            print(f"\n  {C.RED}●{C.RST}  {C.DGRY}Marked.{C.RST}")
        time.sleep(0.35)

    elapsed = int(time.time() - start)
    mins, secs = divmod(elapsed, 60)
    clr()
    print()
    box([
        f"  {C.GOLD}{C.BOLD}⏱  Time: {mins}m {secs}s{C.RST}",
        f"  {C.DGRY}Questions answered: {len([v for v in answers.values() if v['ans']])}/{len(exam_pool)}{C.RST}",
    ], color=C.GOLD)
    time.sleep(1.2)

    tracker.render_final(cfg["dom_order"], td, cfg["name"])
    print()
    input(f"  {C.DGRY}Press ENTER to review wrong answers…{C.RST}")

    wrong = [v for v in answers.values() if v["ans"] and v["ans"] != v["q"]["answer"]]
    if wrong:
        clr()
        print()
        box([f"  {C.RED}{C.BOLD}📖  Reviewing {len(wrong)} wrong answer(s){C.RST}"], color=C.RED)
        print()
        for item in wrong:
            show_result(item["q"], item["ans"], theme_dict=td)
            pause()
    else:
        flash("  🎉  PERFECT SCORE — Zero mistakes!  ", C.BG_GRN)

    pause()


def domain_drill(pool, cfg):
    clr()
    print()
    domains = sorted(set(q["domain"] for q in pool))
    td      = cfg["domain_theme"]
    panel_lines = [f"  {C.WHT}{C.BOLD}Choose a Domain to Drill{C.RST}", ""]
    max_cnt = max((sum(1 for q in pool if q["domain"] == d) for d in domains), default=1)
    for i, d in enumerate(domains, 1):
        cnt = sum(1 for q in pool if q["domain"] == d)
        th  = resolve_theme(d, td)
        bar = gradient_bar(cnt / max_cnt * 100, width=10)
        panel_lines.append(
            f"  {th['color']}{C.BOLD}[{i}]{C.RST}  {th['icon']}  "
            f"{C.WHT}{d}{C.RST}  {bar}  {C.DGRY}{cnt}q{C.RST}"
        )
    panel_lines.append("")
    panel(panel_lines, color=C.BLU, title="DOMAIN DRILL")
    print()

    while True:
        try:
            c = int(input(f"  {C.BOLD}Select (1–{len(domains)}): {C.RST}"))
            if 1 <= c <= len(domains): break
        except ValueError: pass
        print(f"  {C.RED}Invalid.{C.RST}")

    chosen = domains[c - 1]
    run_quiz([q for q in pool if q["domain"] == chosen],
             cfg, num=999, mode_name=f"Domain Drill — {chosen.split('–')[0].strip()}")


def difficulty_drill(pool, cfg):
    clr()
    print()
    panel([
        f"  {C.WHT}{C.BOLD}Select Difficulty{C.RST}",
        "",
        f"  {C.LGRN}{C.BOLD}[1]  ●    Easy   {C.RST}{C.DGRY}— Fundamentals & definitions{C.RST}",
        f"  {C.GOLD}{C.BOLD}[2]  ●●   Medium {C.RST}{C.DGRY}— Applied concepts & scenarios{C.RST}",
        f"  {C.RED}{C.BOLD}[3]  ●●●  Hard   {C.RST}{C.DGRY}— Complex multi-step reasoning{C.RST}",
        "",
    ], color=C.YLW, title="DIFFICULTY DRILL")
    print()

    levels = {"1": "easy", "2": "medium", "3": "hard"}
    while True:
        c = input(f"  {C.BOLD}Select (1–3): {C.RST}").strip()
        if c in levels: break
        print(f"  {C.RED}Invalid.{C.RST}")

    lvl  = levels[c]
    sub  = [q for q in pool if q["difficulty"] == lvl]
    if not sub:
        print(f"  {C.RED}No questions at that level.{C.RST}")
        pause(); return

    run_quiz(sub, cfg, num=999, mode_name=f"{lvl.title()} Questions")


def flashcard_mode(pool, cfg):
    clr()
    print()
    td = cfg["domain_theme"]
    panel([
        f"  {C.CYN}{C.BOLD}📇  Flashcard Mode{C.RST}",
        f"",
        f"  {C.DGRY}Read the question, form your answer mentally,{C.RST}",
        f"  {C.DGRY}then press ENTER to reveal the answer and explanation.{C.RST}",
        f"  {C.DGRY}Self-mark with Y/N to track your confidence.{C.RST}",
        "",
    ], color=C.CYN, title="FLASHCARDS")
    print()
    input(f"  {C.DGRY}Press ENTER to start…{C.RST}")

    random.shuffle(pool)
    right = 0; total = 0

    for i, q in enumerate(pool, 1):
        clr()
        th   = resolve_theme(q["domain"], td)
        dcol = th["color"]
        print()
        print(f"  {dcol}{C.BOLD}{th['icon']}  Flashcard {i}/{len(pool)}  ·  {q['domain']}{C.RST}")
        print(f"  {C.GOLD}{q['topic']}{C.RST}")
        print()
        divider(ch="─")
        print()
        inner_w = W - 6
        words = q["question"].split()
        cur   = ""; lines = []
        for w in words:
            if len(cur) + len(w) + 1 > inner_w: lines.append(cur.rstrip()); cur = w + " "
            else: cur += w + " "
        if cur.strip(): lines.append(cur.rstrip())
        for ln in lines:
            print(f"  {C.WHT}{C.BOLD}{ln}{C.RST}")
        print()
        divider(ch="─")
        raw = input(f"\n  {C.DGRY}Think of your answer… press ENTER to reveal (or 'q' to stop): {C.RST}").strip().lower()
        if raw == "q": break

        print()
        box([
            f"  {C.LGRN}{C.BOLD}Answer: [{q['answer']}]{C.RST}",
            f"  {C.WHT}{q['choices'][q['answer']]}{C.RST}",
        ], color=C.LGRN)
        print()

        words2 = q["explanation"].split()
        cur2   = ""; lines2 = []
        for w in words2:
            if len(cur2) + len(w) + 1 > inner_w: lines2.append(cur2.rstrip()); cur2 = w + " "
            else: cur2 += w + " "
        if cur2.strip(): lines2.append(cur2.rstrip())
        print(f"  {C.MAG}{C.BOLD}💬 Explanation{C.RST}")
        for ln in lines2:
            print(f"  {C.DGRY}{ln}{C.RST}")

        print()
        got = input(f"  {C.BOLD}Got it right? {C.LGRN}[Y]{C.RST} / {C.RED}[N]{C.RST} : ").strip().lower()
        total += 1
        if got == "y":
            right += 1
            print(f"  {C.LGRN}✔  Marked correct!{C.RST}")
        else:
            print(f"  {C.RED}✘  Marked incorrect — it'll come back around.{C.RST}")
        time.sleep(0.5)

    if total:
        pct = right / total * 100
        clr(); print()
        panel([
            f"  {C.WHT}{C.BOLD}Flashcard Session Complete{C.RST}",
            f"",
            f"  {C.DGRY}Self-scored:{C.RST}  {gradient_bar(pct, width=24)}  "
            f"{C.BOLD}{pct:.1f}%{C.RST}  ({right}/{total})",
            f"  {stars(pct)}",
            "",
        ], color=C.CYN, title="RESULTS")
    pause()


def weak_spot_drill(pool, cfg):
    if not tracker.history:
        clr()
        print()
        box([f"  {C.YLW}No session history yet — complete a quiz first.{C.RST}"], color=C.YLW)
        pause(); return

    wrong_topics = set(h["topic"] for h in tracker.history if not h["hit"])
    if not wrong_topics:
        clr()
        print()
        box([f"  {C.LGRN}{C.BOLD}🏆  No wrong answers this session! Perfect!{C.RST}"], color=C.LGRN)
        pause(); return

    clr(); print()
    lines = [f"  {C.RED}{C.BOLD}🎯  Weak Spot Drill{C.RST}", ""]
    for t in sorted(wrong_topics):
        cnt = sum(1 for q in pool if q["topic"] == t)
        lines.append(f"  {C.RED}▸{C.RST}  {C.WHT}{t}{C.RST}  {C.DGRY}({cnt} questions){C.RST}")
    lines.append("")
    panel(lines, color=C.RED, title="YOUR WEAK SPOTS")
    print()
    input(f"  {C.DGRY}Press ENTER to drill these topics…{C.RST}")

    weak_pool = [q for q in pool if q["topic"] in wrong_topics]
    run_quiz(weak_pool, cfg, num=len(weak_pool), mode_name="Weak Spot Drill")


def exam_objectives_mode(cfg):
    QUESTIONS       = cfg["questions"]
    EXAM_OBJECTIVES = cfg["exam_objectives"]
    theme_dict      = cfg["domain_theme"]

    while True:
        clr(); print()
        lines = [
            f"  {cfg['color']}{C.BOLD}{cfg['code']} Objectives Roadmap{C.RST}",
            "",
            f"  {C.DGRY}Use this to decide what to drill next. Heavier domains deserve more reps.{C.RST}",
            "",
        ]
        for i, (dom, meta) in enumerate(EXAM_OBJECTIVES.items(), 1):
            cnt = sum(1 for q in QUESTIONS if q["domain"] == dom)
            th  = resolve_theme(dom, theme_dict)
            name = dom.split("–", 1)[1].strip() if "–" in dom else dom
            lines.append(
                f"  {th['color']}{C.BOLD}[{i}]{C.RST} {th['icon']} "
                f"{C.WHT}{name:<42}{C.RST} {C.GOLD}{meta['weight']:>2}%{C.RST} "
                f"{C.DGRY}{cnt}q{C.RST}"
            )
        lines.extend(["", f"  {C.RED}[Q]{C.RST}  Back to main menu", ""])
        panel(lines, color=cfg["color"], title="OBJECTIVES")

        c = input(f"  {C.BOLD}> {C.RST}").strip().upper()
        if c == "Q":
            break
        if not c.isdigit() or not (1 <= int(c) <= len(EXAM_OBJECTIVES)):
            mini_spinner("Invalid selection")
            continue

        dom  = list(EXAM_OBJECTIVES.keys())[int(c) - 1]
        meta = EXAM_OBJECTIVES[dom]
        th   = resolve_theme(dom, theme_dict)
        q_count = sum(1 for q in QUESTIONS if q["domain"] == dom)

        clr(); print()
        panel([
            f"  {th['color']}{C.BOLD}{th['icon']}  {dom}{C.RST}",
            f"  {C.GOLD}{meta['weight']}% of the exam{C.RST}  {C.DGRY}·  {q_count} practice questions{C.RST}",
            "",
        ], color=th["color"], title="DOMAIN FOCUS")

        print(f"\n  {C.WHT}{C.BOLD}What To Know{C.RST}")
        divider(ch="─", color=C.DGRY)
        for obj in meta["objectives"]:
            print_wrapped(f"- {obj}", color=C.DGRY, indent="  ", width=76)

        print(f"\n  {C.WHT}{C.BOLD}Study Moves{C.RST}")
        divider(ch="─", color=C.DGRY)
        for tip in meta["study"]:
            print_wrapped(f"- {tip}", color=C.DGRY, indent="  ", width=76)
        pause()


def glossary_quiz_mode(glossary, rounds=15):
    terms = list(glossary.items())
    if len(terms) < 4:
        box([f"  {C.YLW}Need at least four glossary terms for quiz mode.{C.RST}"], color=C.YLW)
        pause()
        return

    random.shuffle(terms)
    rounds = min(rounds, len(terms))
    score  = 0

    for i, (term, correct_def) in enumerate(terms[:rounds], 1):
        wrong_defs = [d for t, d in glossary.items() if t != term]
        choices = random.sample(wrong_defs, 3) + [correct_def]
        random.shuffle(choices)
        answer_key = {letter: choice for letter, choice in zip("ABCD", choices)}
        correct_letter = next(k for k, v in answer_key.items() if v == correct_def)

        clr(); print()
        panel([
            f"  {C.MAG}{C.BOLD}Glossary Quiz  {i}/{rounds}{C.RST}",
            "",
            f"  {C.WHT}What does {C.CYN}{C.BOLD}{term}{C.RST}{C.WHT} mean?{C.RST}",
            "",
        ], color=C.MAG, title="TERM DRILL")

        for letter, definition in answer_key.items():
            print_wrapped(f"[{letter}] {definition}", color=C.DGRY, indent="  ", width=76)
            print()

        while True:
            ans = input(f"  {C.BOLD}Answer A-D, or Q to quit: {C.RST}").strip().upper()
            if ans == "Q":
                i -= 1
                break
            if ans in answer_key:
                break
            print(f"  {C.RED}Invalid.{C.RST}")
        if ans == "Q":
            break

        if ans == correct_letter:
            score += 1
            print(f"\n  {C.LGRN}{C.BOLD}Correct.{C.RST}")
        else:
            print(f"\n  {C.RED}{C.BOLD}Not quite.{C.RST} {C.DGRY}Correct answer: [{correct_letter}]{C.RST}")
        print_wrapped(correct_def, color=C.DGRY, indent="  ", width=76)
        pause()

    answered = i if terms else 0
    if answered:
        pct = score / answered * 100
        clr(); print()
        panel([
            f"  {C.WHT}{C.BOLD}Glossary Quiz Complete{C.RST}",
            "",
            f"  {C.DGRY}Score:{C.RST}  {gradient_bar(pct, width=24)}  "
            f"{C.BOLD}{pct:.1f}%{C.RST}  ({score}/{answered})",
            f"  {stars(pct)}",
            "",
        ], color=C.MAG, title="RESULTS")
        pause()


def glossary_mode(cfg):
    glossary = cfg["glossary"]
    while True:
        clr(); print()
        panel([
            f"  {C.MAG}{C.BOLD}📖  {cfg['code']} Glossary  —  {len(glossary)} terms{C.RST}",
            "",
            f"  {C.CYN}[1]{C.RST}  Browse all terms alphabetically",
            f"  {C.CYN}[2]{C.RST}  Search for a term or keyword",
            f"  {C.CYN}[3]{C.RST}  Random glossary quiz",
            f"  {C.RED}[Q]{C.RST}  Back to main menu",
            "",
        ], color=C.MAG, title="GLOSSARY")
        print()
        c = input(f"  {C.BOLD}> {C.RST}").strip().upper()

        if c == "Q":
            break
        elif c == "1":
            clr(); print()
            panel([f"  {C.MAG}{C.BOLD}All Terms A–Z{C.RST}"], color=C.MAG)
            print()
            for term in sorted(glossary.keys()):
                print(f"  {C.CYN}{C.BOLD}{term:<22}{C.RST}  {C.DGRY}{glossary[term]}{C.RST}")
            pause()
        elif c == "2":
            srch = input(f"\n  {C.BOLD}Search: {C.RST}").strip().lower()
            results = [(t, d) for t, d in glossary.items()
                       if srch in t.lower() or srch in d.lower()]
            clr(); print()
            if results:
                panel([f"  {C.MAG}{C.BOLD}Results for \"{srch}\" — {len(results)} found{C.RST}"],
                      color=C.MAG)
                print()
                for term, defn in sorted(results):
                    print(f"  {C.CYN}{C.BOLD}{term}{C.RST}")
                    words = defn.split()
                    cur = "    "; out = []
                    for w in words:
                        if len(cur) + len(w) > 76: out.append(cur); cur = "    " + w + " "
                        else: cur += w + " "
                    if cur.strip(): out.append(cur)
                    for ln in out:
                        print(f"{C.DGRY}{ln}{C.RST}")
                    print()
            else:
                box([f"  {C.YLW}No terms found matching '{srch}'.{C.RST}"], color=C.YLW)
            pause()
        elif c == "3":
            glossary_quiz_mode(glossary)

# ══════════════════════════════════════════════════════════════════════════════
#  MAIN MENU (parameterized)
# ══════════════════════════════════════════════════════════════════════════════

def main_menu(cfg):
    pool_src = cfg["questions"]
    col      = cfg["color"]
    td       = cfg["domain_theme"]

    MENU_LOGO_MINI = (
        f"\n{col}{C.BOLD}   ┌─────────────────────────────────────────────────────────────────────┐\n"
        f"   │  ■  {cfg['name']:<55}■  │\n"
        f"   │       {C.GOLD}\"Know It. Master It. Pass It.\"{col}"
        f"                                       │\n"
        f"   └─────────────────────────────────────────────────────────────────────┘{C.RST}"
    )

    while True:
        clr()
        print(MENU_LOGO_MINI)
        print()

        dom_legend = "   ".join([
            f"{v['color']}{C.BOLD}{v['icon']} D{i+1}{C.RST}"
            for i, v in enumerate(td.values())
        ])
        print(f"  {dom_legend}")
        print()

        if tracker.total > 0:
            pct = tracker.pct()
            c2 = C.LGRN if pct >= 80 else (C.GOLD if pct >= 65 else C.RED)
            bar = gradient_bar(pct, width=20)
            print(f"  {C.DGRY}Session:{C.RST} {bar} {c2}{C.BOLD}{pct:.1f}%{C.RST}  "
                  f"{C.DGRY}{tracker.correct}/{tracker.total} correct{C.RST}"
                  f"{streak_badge(tracker.streak)}")
            print()

        q_total = len(pool_src)
        g_total = len(cfg["glossary"])
        menu_items = [
            (C.TEAL,  "1", "⚡",  "Quick Quiz",        "20 random questions · instant feedback · streaks"),
            (C.RED,   "2", "🏆",  "Practice Exam",      f"{cfg.get('exam_q',75)}-question timed simulation · full debrief"),
            (C.BLU,   "3", "🎯",  "Domain Drill",       "Focus deep on a single domain"),
            (C.GOLD,  "4", "⚙️",  "Difficulty Drill",   "Filter by Easy / Medium / Hard"),
            (C.CYN,   "5", "📇",  "Flashcard Mode",     "Self-scored confidence check"),
            (C.LRED,  "6", "🔁",  "Weak Spot Drill",    "Re-drill topics you got wrong this session"),
            (C.SLTE,  "7", "📚",  "All Questions",      f"Every question shuffled ({q_total} total)"),
            (C.MAG,   "8", "📖",  "Glossary",           f"Browse & search {g_total} key terms"),
            (C.PRP,   "9", "🧭",  "Objectives Map",     "Domain weights, objectives, and focus tips"),
            (C.SLTE, "10", "📊",  "Session Stats",      "View full domain breakdown"),
            (C.DGRY, "11", "↩️",  "Change Cert",        "Go back to certification selector"),
        ]

        left  = menu_items[:6]
        right = menu_items[6:]

        for i in range(max(len(left), len(right))):
            left_str  = ""
            right_str = ""
            if i < len(left):
                mc, key, ico, name, desc = left[i]
                left_str = (f"  {mc}{C.BOLD}[{key}]{C.RST} {ico}  "
                            f"{C.WHT}{C.BOLD}{name:<18}{C.RST}  "
                            f"{C.DGRY}{desc}{C.RST}")
            if i < len(right):
                mc, key, ico, name, desc = right[i]
                right_str = (f"  {mc}{C.BOLD}[{key}]{C.RST} {ico}  "
                             f"{C.WHT}{C.BOLD}{name:<18}{C.RST}  "
                             f"{C.DGRY}{desc}{C.RST}")
            plain_l = len(re.sub(r'\033\[[0-9;]*m', '', left_str))
            print(left_str + " " * max(0, 40 - plain_l) + right_str)

        print()
        divider(ch="─", color=C.DGRY)
        print(f"  {C.DGRY}[Q] Quit{C.RST}  ·  {C.DGRY}{q_total} questions · "
              f"Pass: {cfg['pass_score']} scaled{C.RST}")
        print()

        c = input(f"  {C.BOLD}{C.WHT}Select › {C.RST}").strip().upper()
        pool = list(pool_src)

        dispatch = {
            "1":  lambda: run_quiz(pool, cfg, 20, "Quick Quiz"),
            "2":  lambda: practice_exam(pool, cfg),
            "3":  lambda: domain_drill(pool, cfg),
            "4":  lambda: difficulty_drill(pool, cfg),
            "5":  lambda: flashcard_mode(pool, cfg),
            "6":  lambda: weak_spot_drill(pool, cfg),
            "7":  lambda: run_quiz(pool, cfg, len(pool), "All Questions"),
            "8":  lambda: glossary_mode(cfg),
            "9":  lambda: exam_objectives_mode(cfg),
            "10": lambda: (tracker.render_final(cfg["dom_order"], td, cfg["name"]), pause())
                          if tracker.total else
                          (box([f"  {C.YLW}No data yet — complete a quiz first.{C.RST}"], C.YLW), pause()),
            "11": None,
            "Q":  None,
        }

        if c in ("Q", "11"):
            if c == "Q":
                clr()
                print()
                print(_center(f"{col}{C.BOLD}Good luck on your {cfg['code']} exam!{C.RST}"))
                print(_center(f"{C.DGRY}CompTIA.org  ·  {cfg['code']} objectives{C.RST}"))
                print()
                sys.exit(0)
            return  # go back to cert selector
        elif c in dispatch and dispatch[c]:
            dispatch[c]()
        else:
            mini_spinner("Invalid selection")

# ══════════════════════════════════════════════════════════════════════════════
#  SECURITY+ SY0-701 — DOMAIN THEME, WEIGHTS & OBJECTIVES
# ══════════════════════════════════════════════════════════════════════════════

DOMAIN_THEME_SECPLUS = {
    "Domain 1": {"color": C.TEAL,  "icon": "🔐", "short": "D1", "bg": C.BG_CYN},
    "Domain 2": {"color": C.LRED,  "icon": "⚠️",  "short": "D2", "bg": C.BG_LRED},
    "Domain 3": {"color": C.SKY,   "icon": "🏗️",  "short": "D3", "bg": C.BG_BLU},
    "Domain 4": {"color": C.LIME,  "icon": "⚙️",  "short": "D4", "bg": C.BG_GRN},
    "Domain 5": {"color": C.GOLD,  "icon": "📋",  "short": "D5", "bg": C.BG_YLW},
}

DOMAIN_WEIGHTS_SECPLUS = {
    "Domain 1 – General Security Concepts": 12,
    "Domain 2 – Threats, Vulnerabilities & Mitigations": 22,
    "Domain 3 – Security Architecture": 18,
    "Domain 4 – Security Operations": 28,
    "Domain 5 – Security Program Management & Oversight": 20,
}

DOM_ORDER_SECPLUS = [
    "Domain 1 – General Security Concepts",
    "Domain 2 – Threats, Vulnerabilities & Mitigations",
    "Domain 3 – Security Architecture",
    "Domain 4 – Security Operations",
    "Domain 5 – Security Program Management & Oversight",
]

EXAM_OBJECTIVES_SECPLUS = {
    "Domain 1 – General Security Concepts": {
        "weight": 12,
        "objectives": [
            "Compare security control categories and control types: preventive, detective, corrective, deterrent, compensating, directive, technical, managerial, operational, physical.",
            "Explain fundamental concepts: CIA triad, AAA, non-repudiation, Zero Trust, least privilege, deception/disruption technology.",
            "Explain change management: approvals, documentation, impact analysis, rollback planning, version control.",
            "Choose appropriate cryptographic solutions: PKI, encryption, hashing, obfuscation, digital signatures, certificates, and key management.",
        ],
        "study": [
            "Memorize the difference between control categories and control types — the exam often asks for the BEST label.",
            "Practice crypto wording carefully: encrypt for confidentiality, hash for integrity, sign for authenticity and non-repudiation.",
            "When a question mentions a production change, look for approval, testing, rollback, and documentation.",
        ],
    },
    "Domain 2 – Threats, Vulnerabilities & Mitigations": {
        "weight": 22,
        "objectives": [
            "Compare threat actors and motivations: nation-state, hacktivism, insider threats, organized crime, shadow IT, espionage, disruption, financial gain.",
            "Explain threat vectors and attack surfaces: email, SMS, voice, removable media, supply chain, vulnerable software, unsecured networks.",
            "Explain application, cloud, mobile, hardware, virtualization, OS, web, and supply-chain vulnerabilities.",
            "Analyze indicators of malicious activity across malware, password attacks, application attacks, physical attacks, network attacks, and cryptographic attacks.",
            "Select mitigation techniques: segmentation, access control, patching, hardening, isolation, configuration enforcement, and monitoring.",
        ],
        "study": [
            "For scenario questions, identify the vector first, then the mitigation that reduces that specific path.",
            "Know the differences among phishing, smishing, vishing, whaling, pretexting, baiting, and tailgating.",
            "Tie each vulnerability to a practical control: input validation for injection, patching for known CVEs, MFA for credential attacks.",
        ],
    },
    "Domain 3 – Security Architecture": {
        "weight": 18,
        "objectives": [
            "Compare architecture models: on-premises, cloud, virtualization, containers, serverless, IoT, OT/ICS, and infrastructure as code.",
            "Apply security principles to enterprise infrastructure: segmentation, secure communications, control placement, high availability, secure access.",
            "Compare data protection concepts: data states, classification, tokenization, masking, encryption, DLP, and geographic/legal considerations.",
            "Explain resilience and recovery: redundancy, backups, site types, power, platform diversity, continuity of operations, RTO, and RPO.",
        ],
        "study": [
            "Draw the architecture mentally — where is the trust boundary, where is the data, what control belongs there?",
            "Cloud questions often test shared responsibility: provider secures the cloud; customer secures what they put in it.",
            "For resilience, separate data loss (RPO) from downtime (RTO).",
        ],
    },
    "Domain 4 – Security Operations": {
        "weight": 28,
        "objectives": [
            "Apply secure operations to computing resources: secure baselines, hardening, mobile security, wireless security, application security, sandboxing, monitoring.",
            "Explain asset management for hardware, software, and data assets across acquisition, assignment, monitoring, inventory, and disposal.",
            "Explain vulnerability management activities from discovery and prioritization through remediation, validation, exception handling, and reporting.",
            "Use alerting, monitoring, enterprise security tools, identity controls, automation, incident response, digital forensics, and investigation data sources.",
        ],
        "study": [
            "This is the biggest domain — drill logs, incidents, identity operations, vulnerability management, and tool selection heavily.",
            "For incident response, preserve evidence first, contain spread, eradicate root cause, then recover and document lessons learned.",
            "For monitoring questions, match the data source to the question: DNS logs for domain lookups, firewall logs for flow decisions, EDR for endpoint process behavior.",
        ],
    },
    "Domain 5 – Security Program Management & Oversight": {
        "weight": 20,
        "objectives": [
            "Summarize governance components: policies, standards, procedures, guidelines, roles, responsibilities, external considerations, and monitoring.",
            "Explain risk management: identification, assessment, analysis, treatment, risk registers, risk appetite, risk tolerance, reporting, and BIA.",
            "Explain third-party risk management, contracts, vendor assessments, questionnaires, rules of engagement, monitoring, and agreements.",
            "Summarize compliance, privacy, audits, assessments, attestation, penetration testing, and security awareness practices.",
        ],
        "study": [
            "Separate policy words: policy is high-level, standard is mandatory detail, procedure is step-by-step, guideline is optional advice.",
            "Know qualitative versus quantitative risk and the ALE = SLE × ARO formula.",
            "Vendor and compliance questions usually hinge on evidence, contracts, right to audit, data handling, and continuous monitoring.",
        ],
    },
}

QUESTIONS = [

    # DOMAIN 1 — GENERAL SECURITY CONCEPTS
    {
        "domain": "Domain 1 – General Security Concepts",
        "topic": "CIA Triad", "difficulty": "easy",
        "question": "Which element of the CIA triad ensures that information is accessible only to those authorized to access it?",
        "choices": {"A":"Integrity","B":"Availability","C":"Confidentiality","D":"Non-repudiation"},
        "answer": "C",
        "explanation": "Confidentiality is the 'C' in CIA. It ensures that data is accessible ONLY to authorized individuals. Think of it as keeping secrets secret. Techniques include encryption, access controls, and data classification. Integrity ('I') ensures data hasn't been tampered with; Availability ('A') ensures data is there when you need it. Non-repudiation is a bonus property — it means you can't deny doing something."
    },
    {
        "domain": "Domain 1 – General Security Concepts",
        "topic": "CIA Triad", "difficulty": "easy",
        "question": "A hospital database is corrupted by ransomware and patient records become unreadable. Which CIA component is PRIMARILY violated?",
        "choices": {"A":"Confidentiality","B":"Integrity","C":"Availability","D":"Authentication"},
        "answer": "C",
        "explanation": "When data is rendered unreadable or inaccessible, the Availability pillar is broken. The records still exist (integrity isn't destroyed in a read-only sense) and may not be exposed (confidentiality may be intact), but clinicians CANNOT USE THEM — that is an availability failure. Ransomware is the classic availability attack. Backups and disaster recovery plans are the countermeasures."
    },
    {
        "domain": "Domain 1 – General Security Concepts",
        "topic": "Authentication Factors", "difficulty": "easy",
        "question": "Which authentication factor category does a fingerprint scan belong to?",
        "choices": {"A":"Something you know","B":"Something you have","C":"Something you are","D":"Somewhere you are"},
        "answer": "C",
        "explanation": "Biometrics — fingerprints, retina scans, voice recognition, facial recognition — fall under 'Something you ARE.' The five factors are: (1) Something you KNOW (password, PIN), (2) Something you HAVE (smart card, token, phone), (3) Something you ARE (biometrics), (4) Somewhere you ARE (geolocation), (5) Something you DO (behavioral biometrics like typing cadence). MFA requires two or more DIFFERENT categories."
    },
    {
        "domain": "Domain 1 – General Security Concepts",
        "topic": "Authentication Factors", "difficulty": "medium",
        "question": "A user logs in with a password AND a one-time code sent to their smartphone. This is an example of:",
        "choices": {"A":"Single-factor authentication","B":"Multi-factor authentication","C":"Role-based access control","D":"Federated identity"},
        "answer": "B",
        "explanation": "This is MFA — the user combines something they KNOW (password) with something they HAVE (the smartphone receiving the OTP). Both factors come from DIFFERENT categories, which is the key requirement. Using two passwords would be two-step verification, NOT MFA. The Security+ exam loves to test this distinction. MFA dramatically reduces the risk of credential-based attacks like phishing."
    },
    {
        "domain": "Domain 1 – General Security Concepts",
        "topic": "Encryption", "difficulty": "medium",
        "question": "Which encryption type uses the SAME key to both encrypt and decrypt data?",
        "choices": {"A":"Asymmetric encryption","B":"Hashing","C":"Symmetric encryption","D":"Elliptic curve cryptography"},
        "answer": "C",
        "explanation": "Symmetric encryption uses ONE shared secret key for both encryption and decryption. Examples: AES (gold standard today), DES (obsolete), 3DES, RC4, Blowfish. It is FAST — great for bulk data. The weakness: key distribution. How do you securely share the key? That's where asymmetric encryption steps in. Asymmetric uses a KEY PAIR — a public key (share freely) and a private key (guard with your life). Examples: RSA, ECC, Diffie-Hellman."
    },
    {
        "domain": "Domain 1 – General Security Concepts",
        "topic": "Hashing", "difficulty": "medium",
        "question": "Which property of a cryptographic hash function ensures that two different inputs CANNOT produce the same hash output?",
        "choices": {"A":"Confusion","B":"Collision resistance","C":"Avalanche effect","D":"Key stretching"},
        "answer": "B",
        "explanation": "Collision resistance means it is computationally infeasible for two different inputs to produce the same hash value. MD5 and SHA-1 are BROKEN because collisions have been demonstrated. Use SHA-256 or SHA-3. The avalanche effect means a tiny input change creates a radically different hash — this is a FEATURE, not a property name. Key stretching (PBKDF2, bcrypt, Argon2) makes password hashing slower to resist brute-force. Remember: hashing is ONE-WAY — you cannot reverse a hash."
    },
    {
        "domain": "Domain 1 – General Security Concepts",
        "topic": "PKI / Certificates", "difficulty": "medium",
        "question": "What is the role of a Certificate Authority (CA) in a Public Key Infrastructure (PKI)?",
        "choices": {"A":"To encrypt all network traffic between endpoints","B":"To issue and digitally sign digital certificates, binding public keys to identities","C":"To store private keys for all users in the organization","D":"To generate symmetric session keys for TLS connections"},
        "answer": "B",
        "explanation": "A CA is a trusted third party that vouches for identities by signing certificates. When a CA signs a certificate, it is saying: 'I have verified that this public key belongs to this entity.' The chain of trust flows from Root CA → Intermediate CA → End-entity certificate. A Root CA is the ultimate trust anchor; its certificate is self-signed. CAs NEVER hold your private key. Key terms: CRL (Certificate Revocation List), OCSP (Online Certificate Status Protocol) — both are used to check if a cert is still valid."
    },
    {
        "domain": "Domain 1 – General Security Concepts",
        "topic": "Access Control", "difficulty": "medium",
        "question": "An administrator assigns permissions based on an employee's job title (Nurse, Doctor, Admin). This is BEST described as:",
        "choices": {"A":"Mandatory Access Control (MAC)","B":"Discretionary Access Control (DAC)","C":"Role-Based Access Control (RBAC)","D":"Rule-Based Access Control"},
        "answer": "C",
        "explanation": "RBAC grants permissions to ROLES, and users are assigned to roles. It is the most common model in enterprise environments. MAC = the operating system enforces access based on classification labels (Top Secret, Secret, etc.) — used in military/government. DAC = the DATA OWNER controls access — like file permissions where you can share your own files. Rule-Based = access based on RULES (e.g., firewall rules). Also know ABAC — Attribute-Based Access Control — which uses attributes like department, clearance level, AND time of day."
    },
    {
        "domain": "Domain 1 – General Security Concepts",
        "topic": "Security Controls", "difficulty": "easy",
        "question": "A security guard standing at the entrance to a data center is an example of which type of security control?",
        "choices": {"A":"Technical control","B":"Administrative control","C":"Physical control","D":"Compensating control"},
        "answer": "C",
        "explanation": "Physical controls are tangible, real-world mechanisms: security guards, fences, locks, mantraps, badge readers, CCTV cameras, bollards. Technical (Logical) controls are implemented in software/hardware: firewalls, IDS/IPS, encryption, antivirus, ACLs. Administrative (Managerial) controls are policies and procedures: security policies, background checks, security awareness training. Compensating controls are alternatives when a primary control can't be implemented (e.g., increased monitoring when a patch can't be applied to a legacy system)."
    },
    {
        "domain": "Domain 1 – General Security Concepts",
        "topic": "Zero Trust", "difficulty": "medium",
        "question": "Which principle is the FOUNDATION of a Zero Trust security model?",
        "choices": {"A":"Trust but verify all internal network traffic","B":"Never trust, always verify — regardless of network location","C":"Grant broad access first, then restrict as needed","D":"Perimeter firewalls are sufficient to protect internal resources"},
        "answer": "B",
        "explanation": "Zero Trust demolishes the old 'castle-and-moat' mindset where once you're inside the network, you're trusted. Zero Trust says: assume breach, verify everything, grant least privilege. Key Zero Trust pillars: (1) Verify explicitly — always authenticate and authorize based on all available data points, (2) Use least privilege access, (3) Assume breach — minimize blast radius. Technologies enabling Zero Trust: micro-segmentation, identity-aware proxies, continuous monitoring, Software-Defined Perimeter (SDP), SASE."
    },
    {
        "domain": "Domain 1 – General Security Concepts",
        "topic": "Non-repudiation", "difficulty": "medium",
        "question": "Which cryptographic mechanism provides NON-REPUDIATION by proving that a specific person sent a message?",
        "choices": {"A":"Symmetric encryption with AES-256","B":"A digital signature created with the sender's private key","C":"A VPN tunnel between two endpoints","D":"A hash value computed with SHA-256"},
        "answer": "B",
        "explanation": "Non-repudiation means the sender CANNOT deny sending the message. Digital signatures achieve this: the sender hashes the message, then encrypts that hash with their PRIVATE key — that encrypted hash is the digital signature. Anyone with the sender's PUBLIC key can verify it. Since only the sender has their private key, they cannot claim someone else signed it. Remember: you SIGN with your private key, you VERIFY with the sender's public key. You ENCRYPT with the recipient's public key, you DECRYPT with your private key."
    },
    {
        "domain": "Domain 1 – General Security Concepts",
        "topic": "Gap Analysis", "difficulty": "medium",
        "question": "A company compares its current security posture against the NIST Cybersecurity Framework to identify missing controls. This is called a:",
        "choices": {"A":"Penetration test","B":"Vulnerability assessment","C":"Gap analysis","D":"Risk assessment"},
        "answer": "C",
        "explanation": "A gap analysis compares WHERE YOU ARE (current state) against WHERE YOU WANT TO BE (desired state / framework / regulation). The 'gaps' are the missing or weak controls that need to be addressed. Common frameworks used as targets: NIST CSF, ISO 27001, CIS Controls, PCI DSS. It's different from a vulnerability assessment (which uses scanning tools to find technical weaknesses), and different from a risk assessment (which quantifies likelihood and impact of threats)."
    },
    {
        "domain": "Domain 1 – General Security Concepts",
        "topic": "Deception Technologies", "difficulty": "hard",
        "question": "A security team deploys fake server resources that appear legitimate but have no business purpose. When accessed, an alert is immediately triggered. These are called:",
        "choices": {"A":"Honeypots / Honeynets","B":"DMZ servers","C":"Canary tokens","D":"Sinkholes"},
        "answer": "A",
        "explanation": "Honeypots are decoy systems designed to attract and detect attackers. ANY interaction with a honeypot is suspicious — legitimate users have no reason to access it. Honeynet: a network of honeypots simulating an entire enterprise environment. Canary tokens: specific files, links, or credentials that generate an alert when accessed (e.g., a Word doc with a tracking URL). DNS sinkhole: redirects malicious domain lookups to a safe IP — when a bot tries to reach its C2 server, the sinkhole intercepts it. Honeypots are valuable for early detection and studying attacker behavior."
    },
    {
        "domain": "Domain 1 – General Security Concepts",
        "topic": "Secure Protocols", "difficulty": "medium",
        "question": "Which protocol provides BOTH confidentiality AND integrity for data in transit and is the foundation of HTTPS?",
        "choices": {"A":"SSL 3.0","B":"TLS 1.3","C":"IPSec AH","D":"SSH"},
        "answer": "B",
        "explanation": "TLS (Transport Layer Security) 1.3 is the current standard (RFC 8446, 2018). It provides: Confidentiality (encryption), Integrity (MAC), and Authentication (certificates). TLS 1.3 improvements: faster handshake (1-RTT), removed weak cipher suites (RC4, DES, 3DES), removed RSA key exchange (forward secrecy is now mandatory via ECDHE), removed compression. SSL: DEPRECATED and BROKEN. TLS 1.0 and 1.1 are also deprecated. Only TLS 1.2 and TLS 1.3 are acceptable. IPSec AH provides integrity and authentication but NO confidentiality (no encryption)."
    },

    # DOMAIN 2 — THREATS, VULNERABILITIES & MITIGATIONS
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Social Engineering", "difficulty": "easy",
        "question": "An attacker calls an employee pretending to be from IT support and tricks them into revealing their password. This is an example of:",
        "choices": {"A":"Phishing","B":"Vishing","C":"Smishing","D":"Whaling"},
        "answer": "B",
        "explanation": "Vishing = Voice phishing (phone call). Phishing = email-based social engineering (the broadest category). Smishing = SMS/text message phishing. Spear phishing = highly targeted phishing aimed at a specific individual. Whaling = spear phishing targeting high-value targets (C-suite executives). Pharming = redirecting users to a fake website via DNS poisoning. The BEST defense for all social engineering: security awareness training."
    },
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Social Engineering", "difficulty": "medium",
        "question": "An attacker leaves infected USB drives in a company parking lot hoping employees will plug them in. This is called:",
        "choices": {"A":"Tailgating","B":"Baiting","C":"Pretexting","D":"Piggybacking"},
        "answer": "B",
        "explanation": "Baiting exploits human curiosity by leaving malware-laden physical media (USB drives, CDs, QR codes) in places where victims will find and use them. Studies show that 45-98% of found USB drives get plugged in! Pretexting = creating a fabricated scenario to manipulate someone, like pretending to be a vendor. Tailgating/Piggybacking = following someone through a secured door without authenticating. Mitigation for baiting: disable AutoRun/AutoPlay, use endpoint security, train users."
    },
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Malware Types", "difficulty": "easy",
        "question": "Which type of malware self-replicates WITHOUT requiring a host file or user interaction to spread across a network?",
        "choices": {"A":"Virus","B":"Trojan","C":"Worm","D":"Rootkit"},
        "answer": "C",
        "explanation": "A WORM is self-replicating and self-propagating — it spreads across networks autonomously without needing to attach to a host file and without user interaction. Famous examples: WannaCry, Blaster, Code Red, Slammer. A VIRUS requires a host file AND user interaction to spread (opening an infected file). A TROJAN appears legitimate but contains malicious code — it does NOT self-replicate. A ROOTKIT hides itself and other malware deep in the OS (kernel level), making it very hard to detect. A BOTNET is a network of compromised computers controlled by a C2/C&C server."
    },
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Malware Types", "difficulty": "medium",
        "question": "Malware that records every keystroke a user makes and sends it to an attacker is called a:",
        "choices": {"A":"Ransomware","B":"Spyware","C":"Keylogger","D":"Adware"},
        "answer": "C",
        "explanation": "A keylogger captures and records every keystroke — passwords, credit card numbers, messages — and sends them to the attacker. Can be software-based (malware) or hardware-based (a physical device plugged between keyboard and computer). Spyware is broader — it monitors user activity (browsing, screenshots, webcam) without consent. Keyloggers are a type of spyware. Ransomware encrypts files and demands payment for the decryption key. Defense: anti-malware, MFA (so captured passwords alone aren't enough), virtual keyboards for sensitive input."
    },
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Attack Types", "difficulty": "medium",
        "question": "An attacker floods a web server with millions of HTTP requests from thousands of compromised computers, making it unavailable to legitimate users. This is a:",
        "choices": {"A":"Man-in-the-Middle attack","B":"Distributed Denial of Service (DDoS) attack","C":"SQL Injection attack","D":"Buffer overflow attack"},
        "answer": "B",
        "explanation": "A DDoS attack uses MULTIPLE sources (a botnet) to overwhelm a target, attacking AVAILABILITY. 'Distributed' means traffic comes from many locations simultaneously. Types of DDoS: Volumetric (flood — UDP flood, ICMP flood), Protocol (exploit weaknesses — SYN flood, Smurf attack), Application Layer (HTTP flood — traffic looks legitimate). Mitigations: rate limiting, traffic scrubbing, CDNs, cloud-based DDoS protection (Cloudflare, AWS Shield), blackholing."
    },
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Attack Types", "difficulty": "medium",
        "question": "An attacker intercepts a login request and resends it later to gain unauthorized access. This is known as a:",
        "choices": {"A":"Replay attack","B":"Pass-the-hash attack","C":"Birthday attack","D":"Rainbow table attack"},
        "answer": "A",
        "explanation": "In a replay attack, the attacker captures valid authentication data (e.g., a token, session cookie, or Kerberos ticket) and replays it to impersonate the legitimate user later. The data is valid — it's the RE-USE that's malicious. Countermeasures: timestamps with short validity windows, sequence numbers, nonces (number used once), session tokens that expire. Pass-the-hash: attacker steals a password HASH and uses it directly to authenticate (specific to NTLM authentication). Rainbow table: precomputed hash-to-password lookup tables. Counter: salting."
    },
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Web Application Attacks", "difficulty": "medium",
        "question": "An attacker enters ' OR '1'='1 into a website's login form to bypass authentication. This is a:",
        "choices": {"A":"Cross-Site Scripting (XSS) attack","B":"Cross-Site Request Forgery (CSRF)","C":"SQL Injection attack","D":"Command injection attack"},
        "answer": "C",
        "explanation": "SQL Injection (SQLi) occurs when attacker-controlled input is inserted into a SQL query without proper sanitization. ' OR '1'='1 makes the query always return true, bypassing a login check. SQLi can also dump entire databases, modify data, or execute OS commands (via xp_cmdshell in MSSQL). Prevention: parameterized queries / prepared statements (this is THE fix), stored procedures, input validation, least privilege database accounts. XSS: injects malicious JavaScript. CSRF: tricks authenticated users into submitting malicious requests. Command injection: injects OS commands via vulnerable input fields."
    },
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Web Application Attacks", "difficulty": "hard",
        "question": "Which type of XSS attack stores malicious script in the target web server's database, affecting all users who visit the compromised page?",
        "choices": {"A":"Reflected XSS","B":"DOM-based XSS","C":"Stored (Persistent) XSS","D":"Blind XSS"},
        "answer": "C",
        "explanation": "Stored (Persistent) XSS: malicious script is SAVED in the server's database (e.g., in a comment or forum post). Every user who loads that page runs the script — much more dangerous. Reflected XSS: the malicious script is in the URL; the server 'reflects' it back in the response. Victim must click a specially crafted link. DOM-based XSS: the attack occurs entirely in the browser — the server never sees the payload. Prevention for all XSS: output encoding/escaping, Content Security Policy (CSP) headers, input validation, HttpOnly and Secure cookie flags."
    },
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Cryptographic Attacks", "difficulty": "hard",
        "question": "An attacker has intercepted encrypted communications and is systematically trying every possible key until finding the correct one. This is called a:",
        "choices": {"A":"Dictionary attack","B":"Brute force attack","C":"Birthday attack","D":"Downgrade attack"},
        "answer": "B",
        "explanation": "A brute force attack tries EVERY possible combination until the correct one is found. It will always eventually succeed — the question is whether it takes years or centuries. Countermeasures: long/complex passwords, account lockout, key stretching (bcrypt, Argon2, PBKDF2), long encryption keys (AES-256). Dictionary attack: uses a wordlist of common passwords — faster than brute force. Birthday attack: exploits hash collision probability (the birthday paradox). Downgrade attack: tricks systems into using older, weaker protocols (SSL 2.0 instead of TLS 1.3) — also called a version rollback attack."
    },
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Threat Intelligence", "difficulty": "medium",
        "question": "Which threat intelligence source is automatically shared between organizations in a standardized, machine-readable format to enable real-time threat detection?",
        "choices": {"A":"OSINT","B":"Dark web monitoring","C":"STIX/TAXII","D":"Vulnerability databases (NVD)"},
        "answer": "C",
        "explanation": "STIX (Structured Threat Information Expression) and TAXII (Trusted Automated eXchange of Intelligence Information) are open standards for sharing cyber threat intelligence (CTI) in a machine-readable, automated way. STIX defines the FORMAT; TAXII defines the TRANSPORT protocol. OSINT (Open Source Intelligence): freely available public sources — social media, Shodan, government reports, security blogs. ISACs: sector-specific threat sharing communities (FS-ISAC for financial, H-ISAC for healthcare). IoC: artifacts indicating a breach — IP addresses, file hashes, domains."
    },
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Vulnerability Scanning", "difficulty": "medium",
        "question": "A vulnerability scan finds CVE-2021-44228 (Log4Shell) on a server. The CVSS base score is 10.0 (Critical). What should happen FIRST?",
        "choices": {"A":"Schedule the patch for the next quarterly maintenance window","B":"Ignore it if the server is behind a firewall","C":"Immediately prioritize patching and apply mitigations such as WAF rules","D":"Perform a penetration test to confirm exploitability"},
        "answer": "C",
        "explanation": "A CVSS score of 10.0 is the MAXIMUM — this is as critical as it gets. Log4Shell was actively exploited in the wild within hours of disclosure. Immediate action: apply patches (highest priority), implement interim mitigations (WAF rules, disabling JNDI lookups), isolate affected systems if patching takes time. CVSS (Common Vulnerability Scoring System) rates vulnerabilities 0-10: 0-3.9 Low, 4-6.9 Medium, 7-8.9 High, 9-10 Critical. CVE (Common Vulnerabilities and Exposures): the standardized naming system for publicly known security vulnerabilities. Managed by MITRE, hosted at NVD (NIST)."
    },
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Insider Threats", "difficulty": "medium",
        "question": "An employee with authorized access deliberately exfiltrates intellectual property before resigning. This is BEST classified as:",
        "choices": {"A":"An external threat actor","B":"A malicious insider threat","C":"A zero-day exploit","D":"An advanced persistent threat (APT)"},
        "answer": "B",
        "explanation": "A malicious insider is someone with LEGITIMATE ACCESS who intentionally causes harm. They are extremely dangerous because they already have credentials and knowledge of internal systems. Types: Malicious (intentional harm), Negligent (accidentally causes harm — clicking phishing links), Compromised (credentials stolen by outside attacker). Mitigations: least privilege, separation of duties, mandatory vacations, user activity monitoring (UBA/UEBA), DLP (Data Loss Prevention), proper off-boarding procedures (immediately revoke access upon resignation/termination). APT: a sophisticated, long-term attack campaign, often state-sponsored."
    },
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Supply Chain Security", "difficulty": "hard",
        "question": "The SolarWinds attack (2020) is a prime example of which type of attack?",
        "choices": {"A":"Zero-day exploit","B":"Supply chain attack","C":"Watering hole attack","D":"Credential stuffing"},
        "answer": "B",
        "explanation": "SolarWinds was a supply chain attack: attackers compromised the BUILD PROCESS of SolarWinds' Orion software, injecting malware (SUNBURST) into a legitimate software update distributed to ~18,000 customers — including US government agencies. The customers TRUSTED the update because it appeared legitimate and signed. Supply chain attacks are devastating because they exploit trust relationships. Mitigations: software bill of materials (SBOM), code signing verification, vendor risk assessments, integrity verification of updates. Watering hole attack: compromise a website frequently visited by the target audience."
    },
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Password Attacks", "difficulty": "medium",
        "question": "An attacker uses a list of username/password combinations stolen from one breached website to attempt logins on other websites. This is called:",
        "choices": {"A":"Password spraying","B":"Credential stuffing","C":"Brute force attack","D":"Kerberoasting"},
        "answer": "B",
        "explanation": "Credential stuffing exploits password REUSE. If you use the same password on LinkedIn and your bank, and LinkedIn gets breached, attackers automatically try those credentials everywhere. Automated tools (Sentry MBA, Snipr) make this trivial at scale. Prevention: unique passwords everywhere (use a password manager!), MFA. Password spraying: tries a FEW common passwords (Password1!, Welcome1) across MANY accounts — avoids lockout policies. Kerberoasting: requests Kerberos tickets for service accounts and cracks them offline — specific to Active Directory environments."
    },
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Physical Security", "difficulty": "medium",
        "question": "A person badges into a secure facility and holds the door open for the person behind them without checking their credentials. This is called:",
        "choices": {"A":"Shoulder surfing","B":"Tailgating / Piggybacking","C":"Dumpster diving","D":"Impersonation"},
        "answer": "B",
        "explanation": "Tailgating (piggybacking): following an authorized person through a secured door without presenting credentials — exploiting social courtesy ('hold the door!'). This bypasses physical access controls entirely. Prevention: security awareness training, mantraps (double-door systems that allow only one person through at a time), security guards, turnstiles, cameras. Shoulder surfing: observing someone's screen or keyboard to steal information (PINs, passwords). Defense: privacy screens. Dumpster diving: searching trash for sensitive information. Defense: shredding policies, clear desk policies."
    },
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Advanced Persistent Threats", "difficulty": "hard",
        "question": "An APT group maintains persistent access to a corporate network for 18 months, slowly exfiltrating R&D data while avoiding detection. Which tactic BEST describes their low-and-slow exfiltration method?",
        "choices": {"A":"A rapid DDoS attack against the perimeter","B":"DNS tunneling to slowly move data over legitimate DNS traffic","C":"A ransomware deployment for immediate financial gain","D":"A watering hole attack against employees"},
        "answer": "B",
        "explanation": "DNS tunneling encodes data inside DNS queries and responses — a protocol that's almost always allowed through firewalls. To a casual observer, it looks like normal DNS traffic. APTs use this for covert C2 communication AND data exfiltration. Other covert exfiltration techniques: HTTPS to a cloud storage service, steganography (hiding data in image files), ICMP tunneling, email to external accounts. The MITRE ATT&CK framework documents these under 'Exfiltration' and 'Command and Control' tactics. Detection: DNS analytics for unusual query patterns, volume anomalies, queries to newly registered domains."
    },
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Zero-Day Attacks", "difficulty": "hard",
        "question": "A zero-day vulnerability is BEST defined as:",
        "choices": {"A":"A vulnerability that was discovered exactly 0 days ago","B":"A vulnerability that is known to attackers but has NO vendor patch available yet","C":"A vulnerability with a CVSS score of 0.0","D":"A vulnerability in a system that has been running for 0 days"},
        "answer": "B",
        "explanation": "Zero-day: the vendor has had ZERO DAYS to fix it — a vulnerability is being exploited BEFORE the vendor is aware of it or has released a patch. Extremely dangerous because signature-based defenses cannot protect against them. Zero-day lifecycle: Vulnerability exists → Attacker discovers it → Attacker exploits it → Vendor discovers it → Vendor patches it (now it's an 'n-day' vulnerability) → Patch is deployed. Defenses: defense in depth, behavioral detection (EDR/anomaly), application sandboxing, memory protection (ASLR, DEP), network segmentation. Zero-day exploits sell for millions on the black market."
    },
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Indicators of Compromise", "difficulty": "medium",
        "question": "An analyst finds an executable with an unknown hash that beacons to an IP address in a foreign country every 60 seconds. These observations are BEST described as:",
        "choices": {"A":"False positives from the IDS","B":"Indicators of Compromise (IoCs)","C":"Normal baseline behavior","D":"Indicators of Exposure (IoEs)"},
        "answer": "B",
        "explanation": "Indicators of Compromise (IoCs) are forensic artifacts that suggest a system has been compromised. Types: Network-based (unusual outbound connections, connections to known malicious IPs, DNS queries to newly registered domains), Host-based (unknown processes, suspicious registry keys, new user accounts, unusual file hashes). The 60-second beaconing pattern is a classic C2 (command and control) behavior — the malware 'phones home' at regular intervals. IoCs are shared via STIX/TAXII and threat intelligence platforms. IoEs: conditions that make a system vulnerable to attack (e.g., unpatched software) — BEFORE compromise happens."
    },

    # DOMAIN 3 — SECURITY ARCHITECTURE
    {
        "domain": "Domain 3 – Security Architecture",
        "topic": "Network Security", "difficulty": "easy",
        "question": "Which network security device examines traffic at OSI Layer 7 (Application Layer) and can make filtering decisions based on application content?",
        "choices": {"A":"Packet-filtering firewall","B":"Stateful inspection firewall","C":"Next-Generation Firewall (NGFW)","D":"Network switch"},
        "answer": "C",
        "explanation": "A Next-Generation Firewall (NGFW) operates at LAYER 7 and can inspect application content. Features: deep packet inspection (DPI), intrusion prevention (IPS), SSL/TLS inspection, user identity awareness, malware sandboxing. Packet-filtering firewall: Layer 3-4 only — inspects source/destination IP, port, protocol. Simple and fast, but stateless. Stateful inspection firewall: Layer 3-4, tracks the STATE of connections (established, related) — smarter than packet filtering. Remember the OSI model for the exam — firewalls and their layers are frequently tested."
    },
    {
        "domain": "Domain 3 – Security Architecture",
        "topic": "Network Segmentation", "difficulty": "medium",
        "question": "A company places its web servers in a network zone that is accessible from the internet but isolated from the internal corporate network. This zone is called a:",
        "choices": {"A":"VLAN","B":"DMZ (Demilitarized Zone)","C":"Intranet","D":"Air gap"},
        "answer": "B",
        "explanation": "A DMZ (Demilitarized Zone) is a screened subnet between the internet and internal network. It hosts publicly accessible services (web servers, email servers, DNS) while keeping internal resources protected. If an attacker compromises a DMZ server, they still face another firewall to reach the internal network — containing the breach. Classic DMZ architecture uses TWO firewalls: one between internet and DMZ, one between DMZ and internal network. VLAN: logical network segmentation within a switch. Air gap: physical separation — no network connection whatsoever (used for critical systems like nuclear plant controls, classified networks)."
    },
    {
        "domain": "Domain 3 – Security Architecture",
        "topic": "Wireless Security", "difficulty": "medium",
        "question": "Which wireless security protocol should be used for a corporate Wi-Fi network to provide the strongest authentication?",
        "choices": {"A":"WEP","B":"WPA2-Personal (PSK)","C":"WPA3-Enterprise with 802.1X","D":"WPA2-Personal with TKIP"},
        "answer": "C",
        "explanation": "WPA3-Enterprise with 802.1X is the gold standard for corporate Wi-Fi. 802.1X provides port-based network access control with a RADIUS authentication server — each user authenticates with unique credentials (certificates or username/password) rather than a shared key. WPA3 adds Simultaneous Authentication of Equals (SAE) replacing the vulnerable 4-way handshake, forward secrecy, and stronger encryption. WEP: BROKEN — do not use. Crackable in minutes. WPA2-Personal (PSK): all users share the same pre-shared key — if one device is compromised or an employee leaves, you must change the password for EVERYONE. TKIP: deprecated — vulnerable. Use AES (CCMP) or GCMP instead."
    },
    {
        "domain": "Domain 3 – Security Architecture",
        "topic": "VPN", "difficulty": "medium",
        "question": "Which VPN protocol operates at OSI Layer 3 and provides strong security using IKEv2 for key exchange?",
        "choices": {"A":"L2TP/IPSec","B":"PPTP","C":"SSL VPN","D":"IPSec IKEv2"},
        "answer": "D",
        "explanation": "IPSec IKEv2 is a robust, standards-based VPN protocol at Layer 3 (Network layer). IKEv2 handles the key exchange (fast, supports MOBIKE for seamless network switching). IPSec uses two protocols: AH (Authentication Header) — provides integrity and authentication but NO encryption; ESP (Encapsulating Security Payload) — provides integrity, authentication, AND encryption (used in practice). IPSec modes: Transport (encrypts only payload), Tunnel (encrypts entire packet — used for site-to-site VPNs). PPTP: obsolete and broken — never use. SSL VPN: Layer 7, uses TLS, works through firewalls/NAT — great for remote access. L2TP: tunneling protocol, IPSec provides security."
    },
    {
        "domain": "Domain 3 – Security Architecture",
        "topic": "Cloud Security", "difficulty": "medium",
        "question": "In the cloud shared responsibility model, which security aspect is ALWAYS the customer's responsibility, regardless of cloud service model (IaaS, PaaS, SaaS)?",
        "choices": {"A":"Physical security of the data center","B":"Hypervisor security","C":"Data classification and protection of customer data","D":"Operating system patching"},
        "answer": "C",
        "explanation": "The shared responsibility model splits security obligations between cloud provider and customer. No matter what service model you use, the customer is ALWAYS responsible for their OWN DATA — its classification, who can access it, and ensuring it's protected. IaaS (like AWS EC2): Customer manages OS, applications, data. Provider manages hypervisor, hardware, facility. PaaS (like AWS RDS): Customer manages applications and data. Provider manages OS and runtime. SaaS (like Office 365): Customer manages data and user access. Provider manages everything else. Physical security is ALWAYS the provider's responsibility."
    },
    {
        "domain": "Domain 3 – Security Architecture",
        "topic": "Virtualization & Containers", "difficulty": "hard",
        "question": "Which security risk is UNIQUE to containerized environments and does NOT typically apply to traditional VMs?",
        "choices": {"A":"Privilege escalation","B":"Kernel sharing leading to container escape attacks","C":"Unpatched software vulnerabilities","D":"Denial of service attacks"},
        "answer": "B",
        "explanation": "Containers (Docker, Kubernetes) SHARE the HOST OS KERNEL, unlike VMs which each have their own kernel. This means a container escape exploit can compromise the host and all other containers. VMs have stronger isolation via a hypervisor. Container-specific risks: container escape, image vulnerabilities (use only trusted base images), insecure configurations, over-privileged containers. Best practices: run containers as non-root, use read-only file systems, implement resource limits, scan images for vulnerabilities (Trivy, Snyk), use namespaces and cgroups for isolation, sign container images."
    },
    {
        "domain": "Domain 3 – Security Architecture",
        "topic": "Identity & Access Management", "difficulty": "medium",
        "question": "Which IAM concept ensures a single employee cannot both approve and execute a financial transaction — requiring two different people?",
        "choices": {"A":"Least privilege","B":"Need to know","C":"Separation of duties","D":"Job rotation"},
        "answer": "C",
        "explanation": "Separation of Duties (SoD) divides critical tasks across multiple individuals to prevent fraud and errors. No single person should have end-to-end control of a sensitive process. Example: one person creates a vendor, a different person approves payments to that vendor. Least privilege: grant users the MINIMUM access needed for their job. Need to know: access to classified information only when needed for a specific task. Job rotation: employees periodically switch roles — detects fraud (difficult to hide when someone else takes over your duties) and cross-trains staff. Mandatory vacation: forces employees to take time off — irregularities may surface when someone else covers."
    },
    {
        "domain": "Domain 3 – Security Architecture",
        "topic": "Data Protection", "difficulty": "medium",
        "question": "A company needs to analyze customer credit card data for fraud patterns WITHOUT exposing actual card numbers to analysts. Which technique BEST addresses this?",
        "choices": {"A":"Encryption","B":"Tokenization","C":"Data masking","D":"Hashing"},
        "answer": "C",
        "explanation": "Data masking replaces sensitive data with realistic but fictitious values for use in non-production environments (dev, testing, analytics). The masked data preserves format and analytical properties without exposing real values. Tokenization: replaces sensitive data with a NON-SENSITIVE TOKEN that maps back to the real value in a secure token vault. Used in payment systems (PCI DSS). The token has no mathematical relationship to the original — unlike encrypted data. Encryption: transforms data into ciphertext — requires a key to decrypt. The original data still EXISTS in encrypted form. Hashing: one-way — useful for verifying integrity but cannot recover original data."
    },
    {
        "domain": "Domain 3 – Security Architecture",
        "topic": "Redundancy & Availability", "difficulty": "medium",
        "question": "A company has a Recovery Time Objective (RTO) of 4 hours and a Recovery Point Objective (RPO) of 1 hour. What do these values mean?",
        "choices": {"A":"The system must be restored within 4 hours; backups must be taken every hour","B":"Backups must complete in 4 hours; the system can lose 1 hour of transactions","C":"The system can be down for 1 hour; recovery takes 4 hours","D":"Data can be 4 hours old; the system restores in 1 hour"},
        "answer": "A",
        "explanation": "RTO (Recovery Time Objective): the maximum acceptable DOWNTIME — how quickly the system must be restored. '4-hour RTO' means the system MUST be back online within 4 hours of an outage. RPO (Recovery Point Objective): the maximum acceptable DATA LOSS — how old the restored data can be. '1-hour RPO' means you can only afford to lose 1 hour of data, so backups must occur at least hourly. Lower RTO/RPO = more expensive (requires hot standby, real-time replication). High RTO/RPO = cheaper (cold backups on tape). Also know: MTTR (Mean Time To Repair) and MTBF (Mean Time Between Failures)."
    },
    {
        "domain": "Domain 3 – Security Architecture",
        "topic": "Secure Protocols", "difficulty": "easy",
        "question": "Which protocol replaces Telnet for secure remote command-line access by encrypting all traffic?",
        "choices": {"A":"FTP","B":"SSH (Secure Shell)","C":"SNMP v1","D":"RDP"},
        "answer": "B",
        "explanation": "SSH (port 22) provides encrypted, authenticated remote terminal access. It replaces Telnet (port 23) which sends EVERYTHING in plaintext — including passwords. SSH also supports: SFTP (Secure File Transfer over SSH), SCP (Secure Copy), port forwarding/tunneling, public key authentication. Other insecure-to-secure replacements: HTTP (80) → HTTPS (443, uses TLS). FTP (20/21) → SFTP (22) or FTPS (990, FTP over SSL). Telnet (23) → SSH (22). SNMP v1/v2 (community strings in plaintext) → SNMP v3 (authentication + encryption). HTTPS uses TLS for encryption + server authentication via certificates."
    },
    {
        "domain": "Domain 3 – Security Architecture",
        "topic": "Endpoint Security", "difficulty": "medium",
        "question": "Which endpoint security solution uses behavioral analysis and machine learning to detect threats that have NO known signature?",
        "choices": {"A":"Traditional antivirus (signature-based)","B":"EDR (Endpoint Detection and Response)","C":"Host-based firewall","D":"Full disk encryption"},
        "answer": "B",
        "explanation": "EDR goes far beyond traditional AV. It uses behavioral analysis, ML, and threat intelligence to detect zero-days and fileless malware that have no signature. It provides: continuous monitoring, threat hunting capabilities, detailed telemetry, automated response (isolate host, kill process). Traditional AV: signature-based only — excellent against known malware, blind to novel threats and fileless attacks. XDR (Extended Detection and Response): extends EDR across network, cloud, and email — correlates telemetry from multiple sources. MDR (Managed Detection and Response): EDR/XDR as a managed service (SOC-as-a-service). Full disk encryption: protects data at rest (BitLocker, FileVault, VeraCrypt)."
    },
    {
        "domain": "Domain 3 – Security Architecture",
        "topic": "Email Security", "difficulty": "medium",
        "question": "Which email authentication mechanism allows a domain owner to specify WHICH mail servers are authorized to send email on their behalf?",
        "choices": {"A":"DKIM","B":"DMARC","C":"SPF","D":"S/MIME"},
        "answer": "C",
        "explanation": "SPF (Sender Policy Framework): a DNS TXT record listing all IP addresses/servers authorized to send email for your domain. Receiving servers check SPF to verify the sender is legitimate. Helps prevent spoofing and phishing. DKIM (DomainKeys Identified Mail): adds a CRYPTOGRAPHIC SIGNATURE to outgoing emails — receiving server verifies the signature using the sender's public key in DNS. DMARC (Domain-based Message Authentication, Reporting & Conformance): builds on SPF and DKIM, allowing domain owners to specify POLICY for failed authentication (reject, quarantine, or none) and receive reports. S/MIME: encrypts and signs email content end-to-end using certificates. Best practice: deploy all three (SPF + DKIM + DMARC)."
    },
    {
        "domain": "Domain 3 – Security Architecture",
        "topic": "Load Balancers & HA", "difficulty": "medium",
        "question": "A company runs its application across three servers behind a load balancer. If one server fails, the other two continue serving requests. This provides which security benefit?",
        "choices": {"A":"Confidentiality of data","B":"Non-repudiation","C":"High Availability, supporting the Availability component of CIA","D":"Defense in depth"},
        "answer": "C",
        "explanation": "Load balancers distribute traffic across multiple servers AND provide fault tolerance (high availability). If one server fails, the load balancer routes traffic to remaining servers — no single point of failure. This directly supports AVAILABILITY in the CIA triad. Load balancer types: Layer 4 (TCP/UDP based), Layer 7 (application-aware — can route based on URL, cookies, headers). Also provides some DDoS protection and SSL offloading. Related concepts: clustering (active-active vs active-passive), geographic redundancy, anycast routing, CDNs for content availability."
    },
    {
        "domain": "Domain 3 – Security Architecture",
        "topic": "Secure Architecture Design", "difficulty": "hard",
        "question": "An architect designs a system where the web tier, application tier, and database tier each run in separate network segments with strict firewall rules between them. This implements which security principle?",
        "choices": {"A":"Defense in depth with network segmentation","B":"Fail-open design","C":"Single point of failure elimination","D":"Security by obscurity"},
        "answer": "A",
        "explanation": "Defense in depth (layered security) means multiple independent security controls protect the same asset — if one fails, others remain. Separating web, app, and DB tiers into different network segments with firewall controls means: if an attacker compromises the web tier, they STILL face a firewall before reaching the app tier, and another before the database. This is also network segmentation / micro-segmentation. Fail-open: when a control fails, it allows traffic (dangerous). Fail-safe (fail-closed): when a control fails, it blocks everything — more secure. Security by obscurity: hiding implementation details to prevent attack — NOT a substitute for real security controls (Kerckhoffs's principle)."
    },
    {
        "domain": "Domain 3 – Security Architecture",
        "topic": "Network Security", "difficulty": "hard",
        "question": "Which attack exploits ARP's stateless, trust-based design to redirect network traffic through an attacker's machine on a local network segment?",
        "choices": {"A":"IP spoofing","B":"ARP poisoning (ARP cache poisoning)","C":"BGP hijacking","D":"DNS amplification"},
        "answer": "B",
        "explanation": "ARP (Address Resolution Protocol) maps IP addresses to MAC addresses on a LAN. ARP has no authentication — anyone can send fake ARP replies. An attacker sends gratuitous ARP replies saying 'I am the gateway' and devices update their ARP cache with the attacker's MAC address. All traffic meant for the gateway now goes through the attacker — a classic Man-in-the-Middle (MitM) attack. Tools: Arpspoof, Bettercap, Ettercap. Defenses: Dynamic ARP Inspection (DAI) — switch feature that validates ARP packets against a DHCP snooping table; static ARP entries for critical systems; encrypted protocols. BGP hijacking: rerouting internet traffic by announcing false BGP routes — affects routing BETWEEN autonomous systems (internet-scale)."
    },

    # DOMAIN 4 — SECURITY OPERATIONS
    {
        "domain": "Domain 4 – Security Operations",
        "topic": "Incident Response", "difficulty": "easy",
        "question": "What is the CORRECT order of the NIST incident response lifecycle phases?",
        "choices": {"A":"Detection → Preparation → Containment → Recovery → Post-Incident","B":"Preparation → Detection & Analysis → Containment/Eradication/Recovery → Post-Incident Activity","C":"Identification → Containment → Eradication → Recovery → Lessons Learned → Preparation","D":"Triage → Escalation → Remediation → Closure"},
        "answer": "B",
        "explanation": "The NIST SP 800-61 Incident Response lifecycle has 4 phases: 1. PREPARATION: develop policies, train the team, set up tools BEFORE an incident. 2. DETECTION & ANALYSIS: identify and analyze the incident (what happened? scope?). 3. CONTAINMENT, ERADICATION & RECOVERY: stop the spread, remove the threat, restore. 4. POST-INCIDENT ACTIVITY: lessons learned meeting, update procedures, documentation. The SANS model (also tested) has 6 steps: Preparation, Identification, Containment, Eradication, Recovery, Lessons Learned (PICERL). The exam may ask about BOTH models — know which steps belong to each."
    },
    {
        "domain": "Domain 4 – Security Operations",
        "topic": "Incident Response", "difficulty": "medium",
        "question": "During a ransomware incident, what is the FIRST priority action in the containment phase?",
        "choices": {"A":"Pay the ransom to quickly restore operations","B":"Isolate infected systems from the network to prevent further spread","C":"Immediately rebuild all affected servers from scratch","D":"Notify the media about the breach"},
        "answer": "B",
        "explanation": "Containment's first goal: STOP THE BLEEDING. Isolate infected systems immediately to prevent the ransomware from spreading to other hosts, backups, and network shares. Isolation options: disconnect from network (pull the cable or disable NIC), place in a quarantine VLAN, use EDR to isolate the host remotely. Paying the ransom is generally discouraged (FBI position) — you may not get the key, you mark yourself as a target, and you fund criminal organizations. Before eradicating: take forensic images to preserve evidence. Check if backups are clean and unaffected BEFORE restoring from them."
    },
    {
        "domain": "Domain 4 – Security Operations",
        "topic": "Digital Forensics", "difficulty": "medium",
        "question": "During a forensic investigation, evidence must be collected in order from most volatile to least volatile. Which item should be collected FIRST?",
        "choices": {"A":"Hard drive image","B":"Backup tapes","C":"Contents of RAM (memory dump)","D":"Archived log files"},
        "answer": "C",
        "explanation": "The Order of Volatility (RFC 3227): collect most volatile data FIRST because it disappears the fastest. 1. CPU registers, cache (most volatile). 2. RAM / memory (contains running processes, encryption keys, network connections). 3. Network connections (routing tables, ARP cache, active connections). 4. Running processes. 5. Disk storage (hard drives, SSDs). 6. Remote logs. 7. Backup tapes, CDs (least volatile). RAM is critical in malware investigations — fileless malware exists ONLY in memory. Tools: WinPmem, DumpIt, Magnet RAM Capture. Always create a hash to verify integrity."
    },
    {
        "domain": "Domain 4 – Security Operations",
        "topic": "Digital Forensics", "difficulty": "medium",
        "question": "Which forensic concept ensures that evidence has not been altered from the time of collection through the entire investigation?",
        "choices": {"A":"Chain of custody","B":"Legal hold","C":"Right-to-audit clause","D":"Non-repudiation"},
        "answer": "A",
        "explanation": "Chain of custody documents who had access to evidence, when, and what was done with it. This creates an auditable trail proving the evidence is authentic and unaltered. Required for evidence to be admissible in court. Broken chain of custody can cause evidence to be thrown out entirely. Steps: document evidence collection (photos, notes), create forensic hash (MD5/SHA) of original, work on COPIES not originals, log every person who accesses evidence, maintain secure storage with limited access. Legal hold: a directive to preserve all potentially relevant evidence once litigation is anticipated (stops routine data deletion). eDiscovery: finding, collecting, and producing electronic evidence."
    },
    {
        "domain": "Domain 4 – Security Operations",
        "topic": "SIEM & Log Management", "difficulty": "medium",
        "question": "Which security tool collects, aggregates, and correlates log data from multiple sources to detect threats and generate alerts?",
        "choices": {"A":"IDS (Intrusion Detection System)","B":"SIEM (Security Information and Event Management)","C":"DLP (Data Loss Prevention)","D":"WAF (Web Application Firewall)"},
        "answer": "B",
        "explanation": "SIEM is the central nervous system of a SOC. It: COLLECTS logs from firewalls, endpoints, servers, cloud services; NORMALIZES data into a common format; CORRELATES events across sources to identify patterns; ALERTS on suspicious activity; provides dashboards and enables threat hunting. Example: SIEM correlates a failed login from IP X on the firewall with a successful login from the same IP 5 minutes later — generates a brute-force alert. IDS: detects intrusions in network traffic (passive — alerts only). IPS: detects AND blocks intrusions (inline — active). Popular SIEMs: Splunk, IBM QRadar, Microsoft Sentinel, Elastic SIEM."
    },
    {
        "domain": "Domain 4 – Security Operations",
        "topic": "Vulnerability Management", "difficulty": "medium",
        "question": "A vulnerability scan is performed with administrative credentials on the target systems. This is called a:",
        "choices": {"A":"Unauthenticated scan","B":"Credentialed (authenticated) scan","C":"Passive scan","D":"Intrusive scan"},
        "answer": "B",
        "explanation": "A credentialed (authenticated) scan logs into target systems using admin credentials to perform a deep inspection — checking installed software, registry settings, patch levels, running services. This finds MANY more vulnerabilities than external scanning alone. Unauthenticated (external) scan: no credentials, sees only what an external attacker would see — open ports, service banners, externally visible vulnerabilities. Passive scan: monitors network traffic without actively probing — no noise, but less thorough. Great for discovering unknown assets. Vulnerability management lifecycle: Discover → Prioritize → Assess → Report → Remediate → Verify. Popular scanners: Nessus, Qualys, OpenVAS, Rapid7 Nexpose."
    },
    {
        "domain": "Domain 4 – Security Operations",
        "topic": "Penetration Testing", "difficulty": "medium",
        "question": "A penetration tester performs an assessment with NO prior knowledge of the target environment, simulating an external attacker. This is called a:",
        "choices": {"A":"White box test","B":"Gray box test","C":"Black box test","D":"Red team exercise"},
        "answer": "C",
        "explanation": "Black box test: tester has NO prior knowledge — simulates an outside attacker. Most realistic simulation, but can miss internal weaknesses and takes longer. White box test: tester has FULL knowledge (network diagrams, source code, credentials) — most thorough, but less realistic. Also called crystal box or clear box. Gray box test: tester has PARTIAL knowledge (network ranges, some credentials) — balances realism and thoroughness. Most common in practice. Red team: adversary simulation exercise, often multi-phase, using multiple TTPs to test the ENTIRE security program including people, process, and technology. Blue team: defenders. Purple team: red + blue working collaboratively."
    },
    {
        "domain": "Domain 4 – Security Operations",
        "topic": "Penetration Testing", "difficulty": "hard",
        "question": "During a pen test, the tester exploits a vulnerability to gain initial access, then uses that foothold to access additional systems. This phase is called:",
        "choices": {"A":"Reconnaissance","B":"Scanning","C":"Lateral movement / Pivoting","D":"Covering tracks"},
        "answer": "C",
        "explanation": "Lateral movement (pivoting) is when an attacker uses a compromised host as a stepping stone to reach OTHER systems on the internal network. They 'pivot' through the network to expand access and reach high-value targets. Pen test phases: (1) Reconnaissance (OSINT, passive info gathering), (2) Scanning/Enumeration (Nmap, Nessus), (3) Exploitation (gain initial access), (4) Post-exploitation / Lateral Movement (pivot, escalate privileges), (5) Reporting. The MITRE ATT&CK framework categorizes attacker TTPs including Lateral Movement as a tactic. Key tools: Metasploit, Cobalt Strike, BloodHound (AD enumeration). Covering tracks: deleting logs to avoid detection."
    },
    {
        "domain": "Domain 4 – Security Operations",
        "topic": "Network Security Monitoring", "difficulty": "medium",
        "question": "Which type of IDS analyzes traffic patterns and alerts when behavior deviates significantly from an established baseline?",
        "choices": {"A":"Signature-based IDS","B":"Anomaly-based (behavior-based) IDS","C":"Heuristic-based IDS","D":"Protocol-based IDS"},
        "answer": "B",
        "explanation": "Anomaly-based IDS establishes a BASELINE of normal behavior, then alerts when traffic deviates significantly. Advantage: can detect ZERO-DAY attacks (no signature needed). Disadvantage: HIGH FALSE POSITIVE RATE — legitimate unusual activity (e.g., a large file transfer during backup) may trigger alerts. Signature-based IDS: compares traffic against a database of known attack signatures. Advantage: LOW false positive rate. Disadvantage: CANNOT detect zero-days. Requires constant signature updates. NIDS: monitors network traffic. HIDS: monitors a single host. IPS = IDS that can actively BLOCK threats (inline device). UTM: combines firewall + IPS + AV + content filtering."
    },
    {
        "domain": "Domain 4 – Security Operations",
        "topic": "Identity Management", "difficulty": "medium",
        "question": "An organization uses a RADIUS server so that employees authenticate to the Wi-Fi network using their Active Directory credentials. What is this an example of?",
        "choices": {"A":"Single Sign-On (SSO)","B":"Federation","C":"802.1X with centralized authentication","D":"Multifactor authentication"},
        "answer": "C",
        "explanation": "802.1X is a port-based network access control standard that integrates with a RADIUS server for centralized authentication. The user authenticates with their domain credentials before getting network access. Components: Supplicant (client device), Authenticator (wireless AP or switch), Authentication Server (RADIUS). SSO: one login grants access to multiple systems without re-entering credentials (Kerberos, SAML, OAuth, OIDC). Federation: SSO across DIFFERENT organizations or domains (SAML). Example: logging into a partner company's portal using your own company's credentials. LDAP: directory protocol used to query Active Directory."
    },
    {
        "domain": "Domain 4 – Security Operations",
        "topic": "Identity Management", "difficulty": "hard",
        "question": "An attacker dumps the NTLM hash of an administrator account and uses it to authenticate to other servers WITHOUT cracking the password. This is called:",
        "choices": {"A":"Golden ticket attack","B":"Pass-the-hash attack","C":"Kerberoasting","D":"Silver ticket attack"},
        "answer": "B",
        "explanation": "Pass-the-Hash (PtH): in NTLM authentication, the hash IS the credential. The attacker doesn't need the plaintext password — they just use the hash directly with tools like Mimikatz. Very common in Windows lateral movement. Mitigation: Protected Users security group, Credential Guard, LAPS (Local Admin Password Solution) to give each machine a unique local admin password. Golden ticket: forges a Kerberos TGT using the KRBTGT account's hash — grants access to ANY resource in the domain for up to 10 years. Requires domain controller compromise. Silver ticket: forges a Kerberos service ticket (TGS) for a specific service. Kerberoasting: requests service tickets and cracks them offline to get service account passwords."
    },
    {
        "domain": "Domain 4 – Security Operations",
        "topic": "Secure Coding", "difficulty": "medium",
        "question": "A developer fails to check the length of user input before copying it into a fixed-size memory buffer. This is MOST likely to result in a:",
        "choices": {"A":"SQL injection vulnerability","B":"Cross-site scripting vulnerability","C":"Buffer overflow vulnerability","D":"Race condition"},
        "answer": "C",
        "explanation": "A buffer overflow occurs when a program writes more data to a buffer than it can hold, overflowing into adjacent memory. Attackers can overwrite the return address on the stack to redirect execution to malicious shellcode. Historically devastating — used in Code Red, Slammer, Blaster worms. Mitigations: Input validation (check length!), safe functions (strncpy vs strcpy), ASLR (Address Space Layout Randomization — randomizes memory addresses), DEP/NX bit (marks stack as non-executable), Stack Canaries (sentinel value between buffer and return address — detects overflow), modern memory-safe languages (Rust). Race condition: two processes try to access shared resources concurrently without proper synchronization — can lead to TOCTOU (Time-of-Check to Time-of-Use) attacks."
    },
    {
        "domain": "Domain 4 – Security Operations",
        "topic": "Automation & Orchestration", "difficulty": "medium",
        "question": "A SOC implements a playbook that automatically blocks a suspicious IP address across all firewalls when the SIEM generates a specific alert. This is an example of:",
        "choices": {"A":"SIEM correlation","B":"SOAR (Security Orchestration, Automation, and Response)","C":"Threat intelligence platform","D":"Vulnerability management"},
        "answer": "B",
        "explanation": "SOAR automates repetitive security tasks and orchestrates responses across multiple tools. Key capabilities: automated playbooks (respond to alerts automatically), case management, threat intelligence integration, and human-in-the-loop workflows. SOAR dramatically reduces MTTR (Mean Time To Respond) and frees analysts from repetitive tasks. Example playbook: Phishing email → SOAR automatically: extracts IoCs, checks reputation, disables user's account, blocks sender domain, notifies security team — all in seconds, not hours. SIEM: data collection and correlation. SOAR: automated response. They complement each other (many vendors now combine them into SIEM+SOAR platforms)."
    },
    {
        "domain": "Domain 4 – Security Operations",
        "topic": "Memory Forensics", "difficulty": "hard",
        "question": "During malware analysis, a file appears benign on disk but exhibits malicious behavior when executed. The malware likely uses which technique?",
        "choices": {"A":"Rootkit installation","B":"Process injection / process hollowing","C":"Polymorphic encryption","D":"Bluebugging"},
        "answer": "B",
        "explanation": "Process injection: malware injects malicious code into a LEGITIMATE, TRUSTED process (svchost.exe, explorer.exe) — the malicious code runs under the trusted process's identity, bypassing security tools that whitelist by process name. Process hollowing: creates a legitimate process in a suspended state, empties its memory, and fills it with malicious code — the process LOOKS legitimate but runs malicious code. Polymorphic malware: changes its code signature on each infection to evade signature detection, but the BEHAVIOR remains the same. Metamorphic malware: completely rewrites its own code. Detection: memory forensics (Volatility framework), behavioral EDR analysis, monitoring for unusual process parent-child relationships."
    },
    {
        "domain": "Domain 4 – Security Operations",
        "topic": "Log Analysis", "difficulty": "medium",
        "question": "A security analyst notices thousands of failed login attempts to a web app from a single IP, followed by one successful login. This MOST likely indicates:",
        "choices": {"A":"A DDoS attack","B":"A successful brute force or credential stuffing attack","C":"A cross-site scripting attack","D":"Normal user behavior"},
        "answer": "B",
        "explanation": "The pattern — many failures then one success — is the classic signature of a brute force or credential stuffing attack that ultimately succeeded. This is a serious incident: the attacker has gained access. Immediate response: (1) Block the source IP, (2) Disable the compromised account, (3) Investigate what the attacker accessed after logging in, (4) Force password reset, (5) Enable MFA if not already in place. Detection controls: account lockout policies, CAPTCHA, rate limiting, impossible travel detection (login from New York then London 10 minutes later), MFA (a correct password isn't enough). SIEM should have a correlation rule for this exact pattern."
    },
    {
        "domain": "Domain 4 – Security Operations",
        "topic": "Threat Hunting", "difficulty": "hard",
        "question": "A threat hunter proactively searches for signs of compromise that automated tools have NOT detected. They are operating on which assumption?",
        "choices": {"A":"The network is completely secure and threat hunting is only for compliance","B":"Attackers are NOT present and the goal is to verify a clean environment","C":"Adversaries MAY already be present and evading automated detection","D":"Threat hunting replaces the need for IDS/IPS and SIEM"},
        "answer": "C",
        "explanation": "Threat hunting operates on the assumption of compromise — 'assume breach.' Automated tools (IDS, SIEM) react to KNOWN indicators. Threat hunters proactively look for TTPs (tactics, techniques, procedures) that haven't triggered alerts. The hunt hypothesis: 'I believe an attacker using this TTP would leave THESE artifacts — let me go look for them.' Process: (1) Hypothesis, (2) Investigate using SIEM, EDR, logs, (3) Uncover TTPs, (4) Inform detections (update SIEM rules, EDR signatures). Tools: SIEM for log analysis, EDR for endpoint telemetry, YARA rules for file pattern matching, Sigma rules for log pattern matching, threat intel feeds. Requires skilled analysts — not a beginner task."
    },

    # DOMAIN 5 — SECURITY PROGRAM MANAGEMENT & OVERSIGHT
    {
        "domain": "Domain 5 – Security Program Management & Oversight",
        "topic": "Risk Management", "difficulty": "easy",
        "question": "A company calculates that a threat has a 25% chance of occurring per year and would cause $400,000 in damages. What is the Annualized Loss Expectancy (ALE)?",
        "choices": {"A":"$100,000","B":"$400,000","C":"$1,600,000","D":"$25,000"},
        "answer": "A",
        "explanation": "ALE = ARO × SLE. ARO (Annualized Rate of Occurrence) = 0.25 (25% = once every 4 years). SLE (Single Loss Expectancy) = $400,000. ALE = 0.25 × $400,000 = $100,000 per year. This means on average, you lose $100,000 per year to this threat. You'd only spend UP TO $100,000/year on controls to address this risk. If a control costs $150,000/year, it's not cost-effective! This is QUANTITATIVE risk assessment. Qualitative risk: uses descriptive ratings (High/Medium/Low) instead of dollar values — simpler but less precise."
    },
    {
        "domain": "Domain 5 – Security Program Management & Oversight",
        "topic": "Risk Management", "difficulty": "medium",
        "question": "An organization decides to purchase cyber insurance to offset the financial impact of a data breach. This risk response strategy is called:",
        "choices": {"A":"Risk avoidance","B":"Risk mitigation","C":"Risk transference","D":"Risk acceptance"},
        "answer": "C",
        "explanation": "Risk transference (sharing): transfer the financial risk to a THIRD PARTY. Cyber insurance is the classic example — you pay a premium, the insurer covers breach costs (notification, legal, recovery). Outsourcing is another form — if your cloud provider has a breach, the liability may transfer to them (per SLA). Risk avoidance: STOP the risky activity. Risk mitigation: implement controls to REDUCE the risk. Risk acceptance: acknowledge the risk and do NOTHING — appropriate for low-likelihood, low-impact risks. Risk appetite: how much risk an organization is WILLING to accept. Residual risk: the risk that REMAINS after controls are applied."
    },
    {
        "domain": "Domain 5 – Security Program Management & Oversight",
        "topic": "Compliance & Regulations", "difficulty": "medium",
        "question": "A company processes, stores, or transmits credit card data. Which compliance framework MUST they adhere to?",
        "choices": {"A":"HIPAA","B":"SOX","C":"PCI DSS","D":"GDPR"},
        "answer": "C",
        "explanation": "PCI DSS (Payment Card Industry Data Security Standard): mandatory for any entity that handles cardholder data (Visa, Mastercard, etc.). 12 requirements covering network security, encryption, access control, monitoring, and more. HIPAA (Health Insurance Portability and Accountability Act): protects Protected Health Information (PHI) in the US healthcare sector. SOX (Sarbanes-Oxley): financial reporting controls for publicly traded US companies. GDPR (General Data Protection Regulation): EU regulation protecting personal data of EU citizens — applies to ANY company that handles EU residents' data. Heavy fines: up to 4% of global annual revenue. GLBA: US financial institutions. FERPA: educational records."
    },
    {
        "domain": "Domain 5 – Security Program Management & Oversight",
        "topic": "Privacy Regulations", "difficulty": "medium",
        "question": "Under GDPR, the 'right to erasure' (also called the 'right to be forgotten') means:",
        "choices": {"A":"Organizations must encrypt all personal data","B":"Individuals can request that their personal data be deleted","C":"Backup data must be erased after 30 days","D":"Organizations must report breaches within 72 hours"},
        "answer": "B",
        "explanation": "GDPR grants EU data subjects multiple rights: Right to erasure ('right to be forgotten'): request deletion of their personal data. Right of access: know what data is held about them. Right to rectification: correct inaccurate data. Right to data portability: receive data in a machine-readable format. Right to restrict processing: limit how their data is used. GDPR also requires: breach notification within 72 hours of discovery, appointment of a DPO (Data Protection Officer) in some cases, data protection by design and by default (privacy by design), lawful basis for processing personal data (consent, legitimate interest, etc.)."
    },
    {
        "domain": "Domain 5 – Security Program Management & Oversight",
        "topic": "Security Policies", "difficulty": "easy",
        "question": "Which type of organizational document defines the HIGH-LEVEL goals and requirements for information security, but does NOT specify HOW to implement them?",
        "choices": {"A":"Security procedure","B":"Security standard","C":"Security policy","D":"Security baseline"},
        "answer": "C",
        "explanation": "The hierarchy of policy documents: POLICY: high-level, management-driven statements of goals and intentions. WHY. Example: 'All sensitive data must be encrypted in transit.' STANDARD: specific mandatory requirements supporting the policy. WHAT. Example: 'TLS 1.2 or higher must be used.' PROCEDURE: step-by-step instructions for implementing a standard. HOW. Example: 'How to configure TLS on Apache.' GUIDELINE: recommendations, not mandatory. SUGGESTIONS. BASELINE: the minimum security configuration for a specific system type. Remember: Policies are signed by senior management (CISO, CEO) and are the highest authority in the document hierarchy."
    },
    {
        "domain": "Domain 5 – Security Program Management & Oversight",
        "topic": "Vendor Management", "difficulty": "medium",
        "question": "Before signing a contract with a cloud service provider, a security team reviews the provider's SOC 2 Type II report. What does this report PRIMARILY evaluate?",
        "choices": {"A":"The provider's financial stability and profitability","B":"The effectiveness of security controls over a period of time","C":"The provider's compliance with PCI DSS requirements","D":"The technical specifications of the cloud infrastructure"},
        "answer": "B",
        "explanation": "SOC 2 (Service Organization Control 2): evaluates controls related to the Trust Services Criteria: Security, Availability, Processing Integrity, Confidentiality, and Privacy. Type I: evaluates whether controls are SUITABLY DESIGNED at a POINT IN TIME. Type II: evaluates whether controls were OPERATING EFFECTIVELY over a PERIOD OF TIME (usually 6-12 months) — far more valuable. Requesting a SOC 2 Type II from vendors is a key third-party risk management practice. Also know: ISO 27001 (international ISMS certification), SOC 1 (financial reporting controls), FedRAMP (US federal cloud authorization)."
    },
    {
        "domain": "Domain 5 – Security Program Management & Oversight",
        "topic": "Business Continuity", "difficulty": "medium",
        "question": "Which document outlines the procedures for maintaining CRITICAL BUSINESS FUNCTIONS during a disruption, even if IT systems are unavailable?",
        "choices": {"A":"Disaster Recovery Plan (DRP)","B":"Incident Response Plan (IRP)","C":"Business Continuity Plan (BCP)","D":"Communications Plan"},
        "answer": "C",
        "explanation": "BCP (Business Continuity Plan): focuses on keeping BUSINESS OPERATIONS running during a disruption — manual workarounds, alternate locations, communication procedures. It's broader than IT. Example: if the ERP system is down, how does accounting still process payroll? DRP (Disaster Recovery Plan): IT-focused — how do you RESTORE TECHNOLOGY SYSTEMS after a disaster? Covers backup restoration, failover to DR site, system rebuild. IRP: specifically for security incidents (breaches, malware). The BCP umbrella contains the DRP. Tests: tabletop exercises (talk through scenarios), simulation exercises, full interruption test (actually fail over — most disruptive but most realistic)."
    },
    {
        "domain": "Domain 5 – Security Program Management & Oversight",
        "topic": "Security Awareness", "difficulty": "easy",
        "question": "What is the PRIMARY goal of a phishing simulation program within a security awareness initiative?",
        "choices": {"A":"To punish employees who fall for phishing emails","B":"To identify and train employees who are susceptible to phishing attacks","C":"To test the spam filter's effectiveness","D":"To replace the need for technical email security controls"},
        "answer": "B",
        "explanation": "Phishing simulations send realistic (but safe) fake phishing emails to employees. Those who click or provide credentials are identified and immediately directed to targeted training. Goals: measure susceptibility, track improvement over time, reinforce training with real-world-like scenarios, build a security-aware culture. Key principle: phishing simulations should be EDUCATIONAL, not punitive. Effective security awareness programs include: annual policy sign-offs, quarterly training, phishing simulations, role-specific training (privileged users, executives), newsletters/posters, gamification. Humans are the #1 attack vector — technical controls help but trained employees are the last and most important line of defense."
    },
    {
        "domain": "Domain 5 – Security Program Management & Oversight",
        "topic": "Data Classification", "difficulty": "medium",
        "question": "A government document labeled 'TOP SECRET' can only be accessed by individuals with TOP SECRET clearance and a need to know. This is an example of which access control model?",
        "choices": {"A":"Discretionary Access Control (DAC)","B":"Mandatory Access Control (MAC)","C":"Role-Based Access Control (RBAC)","D":"Attribute-Based Access Control (ABAC)"},
        "answer": "B",
        "explanation": "MAC (Mandatory Access Control) is the most RESTRICTIVE access control model. The OPERATING SYSTEM (or security policy) enforces access based on classification labels and security clearances — the DATA OWNER cannot override it. Used in military and government environments. Labels: Top Secret, Secret, Confidential, Unclassified. The Bell-LaPadula model enforces MAC for confidentiality: No read up (can't read above your clearance), No write down (can't write to lower classification — prevents data leakage). Common classification: Government: Top Secret > Secret > Confidential > Unclassified. Commercial: Confidential > Private > Sensitive > Public."
    },
    {
        "domain": "Domain 5 – Security Program Management & Oversight",
        "topic": "Auditing & Assessments", "difficulty": "medium",
        "question": "Which type of audit is performed by an organization's OWN internal security or audit team?",
        "choices": {"A":"First-party audit","B":"Second-party audit","C":"Third-party audit","D":"Regulatory audit"},
        "answer": "A",
        "explanation": "Audit types by party: First-party (internal audit): performed BY the organization ON itself. Less expensive, less objective — auditors are employees. Good for ongoing compliance monitoring and readiness assessments before external audits. Second-party audit: performed by a CUSTOMER or PARTNER on a vendor. Example: a bank auditing its cloud provider's controls. Third-party audit: performed by an INDEPENDENT auditor. Most credible. Required for PCI DSS QSA assessments, ISO 27001 certification, SOC 2 reporting. Bug bounty programs: companies invite external researchers to find vulnerabilities in exchange for rewards — complementary to formal audits."
    },
    {
        "domain": "Domain 5 – Security Program Management & Oversight",
        "topic": "Frameworks", "difficulty": "medium",
        "question": "The NIST Cybersecurity Framework (CSF) core functions in the correct order are:",
        "choices": {"A":"Protect, Identify, Detect, Respond, Recover","B":"Identify, Protect, Detect, Respond, Recover","C":"Detect, Identify, Protect, Recover, Respond","D":"Identify, Detect, Protect, Respond, Recover"},
        "answer": "B",
        "explanation": "NIST CSF core functions (memorize with 'I PDRR'): 1. IDENTIFY: understand your assets, risks, and governance (asset inventory, risk assessment, supply chain risk). 2. PROTECT: implement safeguards (access control, awareness training, data security, patching). 3. DETECT: implement monitoring to identify events (SIEM, IDS, anomaly detection). 4. RESPOND: respond to detected incidents (IRP, communications, analysis). 5. RECOVER: restore capabilities (BCP/DRP, improvements, communications). NIST CSF 2.0 (released 2024) adds a 6th function: GOVERN — cybersecurity risk strategy, expectations, and policy at the organizational level. The CSF is voluntary for most, but NIST SP 800-53 controls are mandatory for US federal agencies."
    },
    {
        "domain": "Domain 5 – Security Program Management & Oversight",
        "topic": "Data Privacy", "difficulty": "hard",
        "question": "A healthcare company wants to share patient data with researchers but must protect patient identities. Which technique removes all direct identifiers but may still allow re-identification through data combinations?",
        "choices": {"A":"Encryption","B":"De-identification / Anonymization","C":"Full data masking","D":"Tokenization"},
        "answer": "B",
        "explanation": "De-identification removes direct identifiers (name, SSN, DOB, zip code, etc.) but quasi-identifiers (age range, gender, medical condition) can sometimes be combined to RE-IDENTIFY individuals — this is called the re-identification risk. Famous example: a 1997 study re-identified 87% of Americans using only zip code, DOB, and gender from 'anonymized' data. HIPAA Safe Harbor: removes 18 specific identifiers to de-identify PHI. Pseudonymization: replaces identifiers with a pseudonym (can be reversed with a key) — GDPR counts this as a risk reduction measure but not full anonymization. True anonymization: irreversible. Differential privacy: adds mathematical noise to datasets to prevent re-identification."
    },
]

# ══════════════════════════════════════════════════════════════════════════════
#  ADDITIONAL SY0-701 PRACTICE QUESTIONS
# ══════════════════════════════════════════════════════════════════════════════

QUESTIONS.extend([

    # DOMAIN 1 — GENERAL SECURITY CONCEPTS
    {
        "domain": "Domain 1 – General Security Concepts",
        "topic": "Security Controls", "difficulty": "medium",
        "question": "A badge reader unlocks a data center door only after a valid card swipe. Which control type BEST describes this control?",
        "choices": {"A":"Detective physical control","B":"Preventive physical control","C":"Corrective technical control","D":"Compensating managerial control"},
        "answer": "B",
        "explanation": "The badge reader is physical because it controls access to a real space, and preventive because it blocks unauthorized entry before it happens. Detective controls identify events after or during occurrence, corrective controls restore normal operations, and compensating controls substitute for a preferred control that cannot be used."
    },
    {
        "domain": "Domain 1 – General Security Concepts",
        "topic": "Security Controls", "difficulty": "medium",
        "question": "A policy requires managers to review user access every quarter and remove privileges that are no longer needed. What category of control is this?",
        "choices": {"A":"Managerial control","B":"Physical control","C":"Cryptographic control","D":"Corrective technical control"},
        "answer": "A",
        "explanation": "Policies, standards, risk decisions, and access review requirements are managerial controls. The actual IAM system is technical, but the formal requirement and governance process are managerial."
    },
    {
        "domain": "Domain 1 – General Security Concepts",
        "topic": "AAA", "difficulty": "easy",
        "question": "A VPN records the username, login time, source IP address, and commands executed during an administrative session. Which part of AAA is this?",
        "choices": {"A":"Authentication","B":"Authorization","C":"Accounting","D":"Attestation"},
        "answer": "C",
        "explanation": "Accounting tracks what a subject did: logins, commands, timestamps, access attempts, and session details. Authentication proves identity, and authorization decides what the identity is allowed to access."
    },
    {
        "domain": "Domain 1 – General Security Concepts",
        "topic": "Change Management", "difficulty": "medium",
        "question": "A firewall rule change breaks a production payment application, and the team cannot quickly restore the previous configuration. Which change-management element was MOST likely missing?",
        "choices": {"A":"Rollback plan","B":"Data classification","C":"Key escrow","D":"Non-repudiation"},
        "answer": "A",
        "explanation": "A rollback plan defines how to return to the last known good state if a change causes problems. Production changes should also include testing, approvals, documentation, scheduling, impact analysis, and communication."
    },
    {
        "domain": "Domain 1 – General Security Concepts",
        "topic": "Hashing", "difficulty": "medium",
        "question": "Why should password hashes be stored with a unique salt for each user?",
        "choices": {"A":"To make the hash reversible for account recovery","B":"To make identical passwords produce different hash values","C":"To encrypt the password using the user's private key","D":"To prove who originally created the password"},
        "answer": "B",
        "explanation": "A salt is a unique random value added before hashing. It makes identical passwords hash differently and reduces the usefulness of rainbow tables. Salts do not make hashes reversible and do not provide digital signatures."
    },
    {
        "domain": "Domain 1 – General Security Concepts",
        "topic": "Key Stretching", "difficulty": "medium",
        "question": "A security engineer configures bcrypt so each password guess requires significant CPU time. What is this technique called?",
        "choices": {"A":"Key stretching","B":"Tokenization","C":"Steganography","D":"Certificate pinning"},
        "answer": "A",
        "explanation": "Key stretching deliberately slows password verification so brute-force and offline cracking attacks become much more expensive. Common examples include bcrypt, PBKDF2, scrypt, and Argon2."
    },
    {
        "domain": "Domain 1 – General Security Concepts",
        "topic": "Digital Signatures", "difficulty": "medium",
        "question": "A developer wants recipients to verify that a file came from the developer and was not modified. Which cryptographic control should be used?",
        "choices": {"A":"Encrypt the file with AES","B":"Digitally sign the file with the developer's private key","C":"Encode the file with Base64","D":"Compress the file and publish the archive"},
        "answer": "B",
        "explanation": "A digital signature provides integrity, authentication, and non-repudiation. The sender signs with a private key, and recipients verify with the sender's public key. Encryption alone protects confidentiality but does not prove who created the file."
    },
    {
        "domain": "Domain 1 – General Security Concepts",
        "topic": "PKI / Certificates", "difficulty": "medium",
        "question": "A browser needs to check whether a website certificate has been revoked without downloading a full certificate revocation list. Which protocol is designed for this?",
        "choices": {"A":"OCSP","B":"SAML","C":"SNMP","D":"SRTP"},
        "answer": "A",
        "explanation": "OCSP, the Online Certificate Status Protocol, lets a client query certificate status. CRLs are downloadable revocation lists. SAML is used for federated identity, SNMP is used for device management, and SRTP secures real-time media."
    },
    {
        "domain": "Domain 1 – General Security Concepts",
        "topic": "Data Protection", "difficulty": "medium",
        "question": "A customer support portal displays only the last four digits of a Social Security number. Which technique is being used?",
        "choices": {"A":"Hashing","B":"Masking","C":"Key exchange","D":"Blockchain"},
        "answer": "B",
        "explanation": "Masking hides part of a value while allowing limited use, such as showing only the last four digits. Hashing creates a one-way digest, encryption is reversible with a key, and tokenization replaces sensitive data with a substitute token."
    },
    {
        "domain": "Domain 1 – General Security Concepts",
        "topic": "Zero Trust", "difficulty": "hard",
        "question": "A company allows access to an internal app only after checking user identity, MFA status, device health, location risk, and requested resource sensitivity. Which concept does this BEST represent?",
        "choices": {"A":"Implicit trust","B":"Zero Trust continuous evaluation","C":"Security through obscurity","D":"Open authentication"},
        "answer": "B",
        "explanation": "Zero Trust continuously verifies identity, device posture, context, and authorization instead of trusting a user simply because they are on an internal network. It combines least privilege, explicit verification, segmentation, and assume-breach thinking."
    },

    # DOMAIN 2 — THREATS, VULNERABILITIES & MITIGATIONS
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Threat Actors", "difficulty": "easy",
        "question": "A foreign intelligence service spends months stealing diplomatic emails from a government agency. Which attacker type and motivation BEST fit this activity?",
        "choices": {"A":"Unskilled attacker seeking fame","B":"Nation-state actor conducting espionage","C":"Insider threat seeking convenience","D":"Hacktivist pursuing public embarrassment"},
        "answer": "B",
        "explanation": "Nation-state actors are commonly associated with long-term, well-funded campaigns involving espionage, influence, disruption, or strategic advantage. The scenario describes patient intelligence collection rather than a quick opportunistic attack."
    },
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Insider Threats", "difficulty": "medium",
        "question": "An employee who recently resigned downloads thousands of customer records outside normal work hours. What is the BEST immediate interpretation?",
        "choices": {"A":"Normal business activity","B":"Possible insider data exfiltration","C":"A cryptographic collision","D":"A false positive caused by DNS caching"},
        "answer": "B",
        "explanation": "Unusual volume, sensitive data, off-hours activity, and employment change are insider-risk indicators. This does not prove guilt by itself, but it should trigger investigation, access review, and possible containment."
    },
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Shadow IT", "difficulty": "medium",
        "question": "A sales team stores contracts in an unsanctioned file-sharing app because it is easier than the approved platform. What risk is MOST directly introduced?",
        "choices": {"A":"The data may bypass approved security controls and monitoring","B":"The data is automatically protected by corporate DLP","C":"The app becomes a hardware root of trust","D":"All contracts become public domain"},
        "answer": "A",
        "explanation": "Shadow IT creates risk because security teams may not be able to enforce access controls, retention, encryption, DLP, logging, or vendor review. The issue is loss of governance and visibility."
    },
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Supply Chain Security", "difficulty": "hard",
        "question": "A build system downloads a malicious package from a public repository because it has the same name as an internal package but a higher version number. What attack is this?",
        "choices": {"A":"Credential stuffing","B":"Dependency confusion","C":"Bluejacking","D":"Session fixation"},
        "answer": "B",
        "explanation": "Dependency confusion tricks package managers into pulling attacker-controlled packages from public sources instead of private internal repositories. Mitigations include scoped packages, repository pinning, internal registries, lock files, package signing, and allow lists."
    },
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Malware Types", "difficulty": "medium",
        "question": "Malicious PowerShell commands run directly in memory and avoid writing a traditional malware file to disk. What type of attack is this?",
        "choices": {"A":"Fileless malware","B":"Logic bomb","C":"Firmware rootkit","D":"Birthday attack"},
        "answer": "A",
        "explanation": "Fileless malware uses trusted tools, scripts, memory, registry keys, or living-off-the-land binaries to reduce file-based detection. EDR, script logging, PowerShell controls, and behavior analytics help detect it."
    },
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Web Application Attacks", "difficulty": "hard",
        "question": "A vulnerable web app fetches a URL supplied by a user. An attacker supplies a cloud metadata service URL and retrieves temporary credentials. What vulnerability is this?",
        "choices": {"A":"Cross-site scripting","B":"Server-side request forgery","C":"Directory traversal","D":"Clickjacking"},
        "answer": "B",
        "explanation": "Server-side request forgery, or SSRF, tricks a server into making requests to internal or privileged resources. Cloud metadata endpoints are a common target. Mitigations include allow-listed destinations, metadata protections, egress filtering, and input validation."
    },
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Web Application Attacks", "difficulty": "medium",
        "question": "A user changes /invoice?id=1044 to /invoice?id=1045 and sees another customer's invoice. What vulnerability is present?",
        "choices": {"A":"Insecure direct object reference","B":"SQL deadlock","C":"DNS poisoning","D":"Password spraying"},
        "answer": "A",
        "explanation": "IDOR occurs when an application exposes object identifiers and fails to enforce authorization for each object. The fix is server-side access checks, not just hiding or randomizing IDs."
    },
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Wireless Attacks", "difficulty": "medium",
        "question": "An attacker sets up a fake Wi-Fi access point named like the company's guest network to capture user traffic. What attack is this?",
        "choices": {"A":"Evil twin","B":"Bluebugging","C":"RFID cloning","D":"ARP poisoning"},
        "answer": "A",
        "explanation": "An evil twin is a rogue wireless access point made to look legitimate. It can capture credentials, intercept traffic, or deliver captive portal attacks. Strong WPA3-Enterprise, certificate validation, and user training help reduce this risk."
    },
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Cryptographic Attacks", "difficulty": "hard",
        "question": "An attacker forces a client and server to negotiate an older, weaker encryption protocol even though both support a stronger one. What attack is this?",
        "choices": {"A":"Downgrade attack","B":"Replay attack","C":"Collision attack","D":"Pass-the-ticket attack"},
        "answer": "A",
        "explanation": "A downgrade attack forces systems to use weaker security than they otherwise would. Defenses include disabling legacy protocols, using secure defaults, enforcing minimum TLS versions, and using mechanisms that detect protocol tampering."
    },
    {
        "domain": "Domain 2 – Threats, Vulnerabilities & Mitigations",
        "topic": "Social Engineering", "difficulty": "medium",
        "question": "Attackers compromise a popular industry website used by employees of a target company and wait for those employees to visit it. What attack is this?",
        "choices": {"A":"Watering hole attack","B":"Shoulder surfing","C":"Smishing","D":"Dumpster diving"},
        "answer": "A",
        "explanation": "A watering hole attack compromises a site the intended victims already trust or frequently visit. It is targeted but indirect, and it often relies on browser, plugin, or drive-by-download exploitation."
    },

    # DOMAIN 3 — SECURITY ARCHITECTURE
    {
        "domain": "Domain 3 – Security Architecture",
        "topic": "Cloud Security", "difficulty": "medium",
        "question": "In an IaaS cloud model, who is typically responsible for patching the guest operating system running on a customer-managed virtual machine?",
        "choices": {"A":"The cloud provider only","B":"The customer","C":"The internet service provider","D":"The certificate authority"},
        "answer": "B",
        "explanation": "In IaaS, the provider secures the underlying cloud infrastructure, while the customer manages what they deploy, including guest OS patching, applications, identities, data, and many network security settings."
    },
    {
        "domain": "Domain 3 – Security Architecture",
        "topic": "Infrastructure as Code", "difficulty": "medium",
        "question": "A cloud security team wants every firewall and storage change to be peer reviewed, versioned, and repeatable. Which approach BEST supports this?",
        "choices": {"A":"Infrastructure as Code","B":"Manual console changes","C":"Screen recording","D":"Network address translation"},
        "answer": "A",
        "explanation": "Infrastructure as Code defines infrastructure in version-controlled templates. It supports peer review, repeatability, testing, change tracking, and rollback. Manual console changes often cause drift and weak documentation."
    },
    {
        "domain": "Domain 3 – Security Architecture",
        "topic": "Cloud Security", "difficulty": "medium",
        "question": "Which technology commonly provides visibility, policy enforcement, and access control between users and cloud/SaaS applications?",
        "choices": {"A":"CASB","B":"TPM","C":"SCADA","D":"HSM"},
        "answer": "A",
        "explanation": "A Cloud Access Security Broker helps enforce policy for cloud and SaaS use. It can support discovery, DLP, access control, malware protection, and activity monitoring. TPM and HSM protect keys; SCADA relates to industrial control."
    },
    {
        "domain": "Domain 3 – Security Architecture",
        "topic": "Data Protection", "difficulty": "easy",
        "question": "Which data state describes data currently being processed in memory by an application?",
        "choices": {"A":"Data at rest","B":"Data in transit","C":"Data in use","D":"Data archived"},
        "answer": "C",
        "explanation": "Data in use is actively being processed, often in memory. Data at rest is stored, and data in transit is moving across a network. Each state needs different protection strategies."
    },
    {
        "domain": "Domain 3 – Security Architecture",
        "topic": "Data Protection", "difficulty": "medium",
        "question": "A payment processor replaces credit card numbers with random values that map back to the original data in a secure vault. What technique is this?",
        "choices": {"A":"Tokenization","B":"Steganography","C":"Compression","D":"Hash collision"},
        "answer": "A",
        "explanation": "Tokenization replaces sensitive data with a non-sensitive token. The real value is stored separately in a secure token vault. This reduces exposure of cardholder data in applications and databases."
    },
    {
        "domain": "Domain 3 – Security Architecture",
        "topic": "Resilience & Recovery", "difficulty": "medium",
        "question": "Which recovery site is fully equipped and ready to take over operations with the shortest downtime?",
        "choices": {"A":"Cold site","B":"Warm site","C":"Hot site","D":"Reciprocal agreement only"},
        "answer": "C",
        "explanation": "A hot site has systems, data, connectivity, and infrastructure ready for rapid failover. It is the fastest and most expensive. A warm site is partially ready, and a cold site is mostly empty space and basic facilities."
    },
    {
        "domain": "Domain 3 – Security Architecture",
        "topic": "Resilience & Recovery", "difficulty": "medium",
        "question": "A database can lose no more than 15 minutes of transactions during an outage. Which metric is being described?",
        "choices": {"A":"RTO","B":"RPO","C":"MTBF","D":"MTTR"},
        "answer": "B",
        "explanation": "Recovery Point Objective is the maximum acceptable amount of data loss, measured as time. Recovery Time Objective is how long recovery may take. MTBF and MTTR are reliability and repair metrics."
    },
    {
        "domain": "Domain 3 – Security Architecture",
        "topic": "ICS / OT Security", "difficulty": "hard",
        "question": "A manufacturing plant must protect legacy industrial controllers that cannot be patched frequently. Which mitigation is usually MOST appropriate?",
        "choices": {"A":"Expose the controllers directly to the internet for vendor access","B":"Place the controllers in a segmented OT network with tightly controlled access","C":"Disable monitoring because availability is important","D":"Install consumer antivirus on every controller immediately"},
        "answer": "B",
        "explanation": "Legacy OT and ICS environments often prioritize availability and safety. Segmentation, jump hosts, allow-listed access, monitoring, strict change windows, and compensating controls are common when direct patching is difficult."
    },
    {
        "domain": "Domain 3 – Security Architecture",
        "topic": "Network Segmentation", "difficulty": "hard",
        "question": "A company wants to limit east-west movement between workloads inside the same data center after one server is compromised. Which design is MOST helpful?",
        "choices": {"A":"Microsegmentation","B":"A larger subnet mask","C":"Disabling logging","D":"A public DNS record"},
        "answer": "A",
        "explanation": "Microsegmentation applies granular controls between workloads, not just at the network perimeter. It reduces lateral movement and blast radius when an attacker compromises one internal system."
    },
    {
        "domain": "Domain 3 – Security Architecture",
        "topic": "Containers", "difficulty": "medium",
        "question": "Which practice BEST reduces the risk of deploying a malicious or vulnerable container image?",
        "choices": {"A":"Pull images only by the latest tag","B":"Use signed images from trusted registries and scan them before deployment","C":"Run all containers as root for compatibility","D":"Disable image provenance checks"},
        "answer": "B",
        "explanation": "Container security includes using trusted registries, signed images, vulnerability scanning, minimal base images, least privilege, secrets management, and avoiding privileged/root containers unless truly required."
    },

    # DOMAIN 4 — SECURITY OPERATIONS
    {
        "domain": "Domain 4 – Security Operations",
        "topic": "Secure Baselines", "difficulty": "easy",
        "question": "A server build disables unnecessary services, configures logging, enforces password policy, and applies approved settings before deployment. What is this called?",
        "choices": {"A":"Secure baseline","B":"Open relay","C":"Data remanence","D":"Business impact analysis"},
        "answer": "A",
        "explanation": "A secure baseline is a known-good configuration standard for a system type. Hardening applies those settings by reducing attack surface, enabling security controls, and removing unnecessary functions."
    },
    {
        "domain": "Domain 4 – Security Operations",
        "topic": "Asset Management", "difficulty": "medium",
        "question": "A company retires encrypted laptops and destroys the encryption keys instead of wiping every storage block. Which disposal method is this?",
        "choices": {"A":"Cryptographic erase","B":"Degaussing only","C":"Tokenization","D":"Chain of custody"},
        "answer": "A",
        "explanation": "Cryptographic erase destroys the keys needed to decrypt data, making encrypted data unrecoverable. It is fast and useful when strong full-disk encryption was used correctly."
    },
    {
        "domain": "Domain 4 – Security Operations",
        "topic": "Vulnerability Management", "difficulty": "medium",
        "question": "A scanner reports a critical vulnerability on a server, but the service is not installed. What should the analyst do NEXT?",
        "choices": {"A":"Immediately rebuild every server","B":"Validate the finding as a likely false positive","C":"Accept the risk forever","D":"Disable all vulnerability scanning"},
        "answer": "B",
        "explanation": "Vulnerability management includes validation. Scanners can create false positives, so analysts verify findings before remediation. Then they prioritize real findings based on severity, exposure, exploitability, and asset criticality."
    },
    {
        "domain": "Domain 4 – Security Operations",
        "topic": "Vulnerability Management", "difficulty": "hard",
        "question": "Two vulnerabilities have the same CVSS score, but one is on an internet-facing payment server and the other is on a lab machine. Which should usually be fixed first?",
        "choices": {"A":"The lab machine because it is easier","B":"The internet-facing payment server because asset criticality and exposure increase risk","C":"Neither because CVSS scores are equal","D":"Whichever was discovered last"},
        "answer": "B",
        "explanation": "Risk-based prioritization considers more than CVSS. Exposure, business criticality, exploit availability, data sensitivity, compensating controls, and threat intelligence all affect remediation priority."
    },
    {
        "domain": "Domain 4 – Security Operations",
        "topic": "Endpoint Security", "difficulty": "medium",
        "question": "Which tool is BEST for investigating suspicious process execution, parent-child process relationships, and endpoint behavior over time?",
        "choices": {"A":"EDR","B":"UPS","C":"NAT gateway","D":"Load balancer"},
        "answer": "A",
        "explanation": "Endpoint Detection and Response collects endpoint telemetry and supports investigation, detection, containment, and response. It is stronger for endpoint behavior analysis than traditional signature-only antivirus."
    },
    {
        "domain": "Domain 4 – Security Operations",
        "topic": "Alerting & Monitoring", "difficulty": "medium",
        "question": "A security platform correlates endpoint, network, identity, cloud, and email telemetry into one detection and response workflow. What is this commonly called?",
        "choices": {"A":"XDR","B":"WEP","C":"RAID","D":"NAT"},
        "answer": "A",
        "explanation": "Extended Detection and Response combines telemetry across multiple security layers to improve detection, correlation, investigation, and response. It expands beyond endpoint-only EDR."
    },
    {
        "domain": "Domain 4 – Security Operations",
        "topic": "Identity Management", "difficulty": "hard",
        "question": "Administrators receive elevated privileges only for an approved maintenance window, and the privileges are automatically removed afterward. Which control is this?",
        "choices": {"A":"Just-in-time privileged access","B":"Shared local administrator account","C":"Permanent standing privilege","D":"Anonymous authorization"},
        "answer": "A",
        "explanation": "Just-in-time privileged access grants elevated rights only when needed and for a limited time. It reduces standing privilege, limits attacker opportunity, and is often part of privileged access management."
    },
    {
        "domain": "Domain 4 – Security Operations",
        "topic": "Identity Management", "difficulty": "medium",
        "question": "An HR termination event automatically disables the user's account, revokes SaaS sessions, and removes group memberships. Which IAM process is this?",
        "choices": {"A":"Deprovisioning","B":"Federation","C":"Password spraying","D":"Transitive trust"},
        "answer": "A",
        "explanation": "Deprovisioning removes access when a user no longer needs it, especially during termination or role change. Fast deprovisioning prevents orphaned accounts and reduces insider and credential misuse risk."
    },
    {
        "domain": "Domain 4 – Security Operations",
        "topic": "Automation & Orchestration", "difficulty": "medium",
        "question": "A phishing alert automatically extracts URLs, checks threat intelligence, blocks malicious domains, opens a ticket, and notifies the user. What capability is being used?",
        "choices": {"A":"SOAR playbook","B":"Manual packet capture only","C":"Cold site recovery","D":"Static code compilation"},
        "answer": "A",
        "explanation": "SOAR platforms use playbooks to automate and orchestrate repeatable response steps across tools. Automation improves speed and consistency, but playbooks still need testing, approvals, and exception handling."
    },
    {
        "domain": "Domain 4 – Security Operations",
        "topic": "Digital Forensics", "difficulty": "medium",
        "question": "An analyst documents who collected a hard drive, when it was collected, where it was stored, and each transfer of possession. What is being maintained?",
        "choices": {"A":"Chain of custody","B":"Risk appetite","C":"Data masking","D":"Secure boot"},
        "answer": "A",
        "explanation": "Chain of custody documents evidence handling from collection through storage, transfer, analysis, and disposal. It supports integrity, admissibility, and repeatability in forensic investigations."
    },

    # DOMAIN 5 — SECURITY PROGRAM MANAGEMENT & OVERSIGHT
    {
        "domain": "Domain 5 – Security Program Management & Oversight",
        "topic": "Risk Management", "difficulty": "medium",
        "question": "A board states that the organization will not accept more than four hours of customer portal downtime per quarter. What does this define?",
        "choices": {"A":"Risk tolerance","B":"Hash value","C":"Key escrow","D":"Attack surface"},
        "answer": "A",
        "explanation": "Risk tolerance is the acceptable variation around risk objectives, often expressed as a threshold. Risk appetite is the broader amount and type of risk leadership is willing to pursue or accept."
    },
    {
        "domain": "Domain 5 – Security Program Management & Oversight",
        "topic": "Risk Management", "difficulty": "medium",
        "question": "A security team tracks identified risks, owners, likelihood, impact, treatment plans, and current status in one living document. What is this called?",
        "choices": {"A":"Risk register","B":"Certificate signing request","C":"Packet capture","D":"Configuration baseline"},
        "answer": "A",
        "explanation": "A risk register is the central record for known risks and their treatment status. It commonly includes risk owners, likelihood, impact, inherent risk, residual risk, response strategy, due dates, and status."
    },
    {
        "domain": "Domain 5 – Security Program Management & Oversight",
        "topic": "Business Impact Analysis", "difficulty": "medium",
        "question": "Which activity identifies critical business processes, dependencies, maximum tolerable downtime, RTO, and RPO?",
        "choices": {"A":"Business impact analysis","B":"Rainbow table generation","C":"Port mirroring","D":"Certificate stapling"},
        "answer": "A",
        "explanation": "A BIA determines which business processes are critical, what they depend on, and how outages would affect the organization. BIA results drive BCP and DRP requirements."
    },
    {
        "domain": "Domain 5 – Security Program Management & Oversight",
        "topic": "Vendor Management", "difficulty": "easy",
        "question": "A contract requires a cloud provider to maintain 99.9% monthly uptime and defines credits if the target is missed. What agreement is this?",
        "choices": {"A":"SLA","B":"NDA","C":"MOU","D":"EULA only"},
        "answer": "A",
        "explanation": "A Service Level Agreement defines measurable service expectations such as uptime, response time, support availability, and remedies. An NDA protects confidential information; an MOU documents mutual understanding."
    },
    {
        "domain": "Domain 5 – Security Program Management & Oversight",
        "topic": "Third-Party Risk", "difficulty": "medium",
        "question": "A company wants the contractual ability to review a vendor's security controls and evidence. Which clause is MOST important?",
        "choices": {"A":"Right to audit","B":"Force all passwords to expire daily","C":"Disable incident reporting","D":"Public domain waiver"},
        "answer": "A",
        "explanation": "Right-to-audit language gives the customer permission to review vendor controls, reports, and evidence. It is a key third-party risk mechanism, especially when vendors process sensitive data or support critical services."
    },
    {
        "domain": "Domain 5 – Security Program Management & Oversight",
        "topic": "Privacy Regulations", "difficulty": "hard",
        "question": "Under GDPR-style privacy terminology, which party determines the purposes and means of processing personal data?",
        "choices": {"A":"Data controller","B":"Data processor","C":"Certificate authority","D":"Threat actor"},
        "answer": "A",
        "explanation": "The data controller decides why and how personal data is processed. A processor acts on behalf of the controller. This distinction affects contracts, accountability, data subject rights, and breach obligations."
    },
    {
        "domain": "Domain 5 – Security Program Management & Oversight",
        "topic": "Auditing & Assessments", "difficulty": "medium",
        "question": "An independent auditor issues a formal opinion that management's description of controls is fairly presented. What is this generally called?",
        "choices": {"A":"Attestation","B":"Phishing simulation","C":"Key rotation","D":"Packet replay"},
        "answer": "A",
        "explanation": "Attestation is a formal statement or opinion by an independent party about controls, compliance, or assertions. SOC reports are common examples of attestation reporting for service organizations."
    },
    {
        "domain": "Domain 5 – Security Program Management & Oversight",
        "topic": "Third-Party Risk", "difficulty": "medium",
        "question": "Before onboarding a SaaS vendor, a company asks about encryption, access controls, incident response, data retention, and subcontractors. What process is this?",
        "choices": {"A":"Vendor security questionnaire due diligence","B":"ARP poisoning","C":"Blue team containment","D":"Hash salting"},
        "answer": "A",
        "explanation": "Vendor questionnaires are used during due diligence to understand a third party's security posture. They help determine risk, required contract terms, compensating controls, and whether deeper evidence such as SOC 2 is needed."
    },
    {
        "domain": "Domain 5 – Security Program Management & Oversight",
        "topic": "Governance", "difficulty": "hard",
        "question": "A legacy medical system cannot be patched for 60 days. Security approves temporary network isolation, extra monitoring, and a documented expiration date. What governance process is this?",
        "choices": {"A":"Security exception with compensating controls","B":"Permanent risk elimination","C":"Uncontrolled change","D":"Data anonymization"},
        "answer": "A",
        "explanation": "A security exception documents a temporary deviation from policy or standard. Good exceptions include business justification, owner, compensating controls, risk acceptance, review date, and expiration."
    },
    {
        "domain": "Domain 5 – Security Program Management & Oversight",
        "topic": "Security Awareness", "difficulty": "medium",
        "question": "System administrators receive additional training on privileged access, secure remote administration, and change control. What awareness principle is being applied?",
        "choices": {"A":"Role-based training","B":"Universal default passwords","C":"Implicit trust","D":"Data remanence"},
        "answer": "A",
        "explanation": "Security awareness should include general training for all users plus role-based training for higher-risk duties. Privileged users, executives, developers, and help desk staff often need targeted content."
    },
])

GLOSSARY = {
    "AAA": "Authentication, Authorization, Accounting — foundational security framework.",
    "ALE": "Annualized Loss Expectancy = ARO × SLE — expected annual financial loss from a threat.",
    "APT": "Advanced Persistent Threat — sophisticated, long-term attacker (often state-sponsored).",
    "ASLR": "Address Space Layout Randomization — randomizes memory addresses to hinder exploitation.",
    "BCP": "Business Continuity Plan — keeps business operations running during disruptions.",
    "CA": "Certificate Authority — trusted entity that issues and signs digital certificates.",
    "CIA Triad": "Confidentiality, Integrity, Availability — the three core security properties.",
    "CVSS": "Common Vulnerability Scoring System — 0-10 scale for severity. 9-10 = Critical.",
    "CVE": "Common Vulnerabilities and Exposures — standardized vulnerability naming (CVE-YEAR-NUMBER).",
    "DAC": "Discretionary Access Control — data owner controls access permissions.",
    "DDoS": "Distributed Denial of Service — floods a target with traffic from many sources.",
    "DKIM": "DomainKeys Identified Mail — cryptographic email signing to verify sender authenticity.",
    "DLP": "Data Loss Prevention — monitors and prevents unauthorized data exfiltration.",
    "DMZ": "Demilitarized Zone — network segment between internet and internal network.",
    "DMARC": "Domain-based Message Authentication, Reporting & Conformance — email policy enforcement.",
    "DRP": "Disaster Recovery Plan — IT-focused plan for restoring systems after a disaster.",
    "EDR": "Endpoint Detection and Response — advanced endpoint security with behavioral detection.",
    "GDPR": "General Data Protection Regulation — EU privacy law; 72-hour breach notification.",
    "HIPAA": "Health Insurance Portability and Accountability Act — US healthcare privacy law.",
    "IDS/IPS": "Intrusion Detection/Prevention System — monitors for and optionally blocks intrusions.",
    "IoC": "Indicator of Compromise — artifact suggesting a system has been breached.",
    "MAC": "Mandatory Access Control — OS enforces access based on classification labels.",
    "MFA": "Multi-Factor Authentication — requires 2+ factors from different categories.",
    "MTTR": "Mean Time To Repair — average time to restore a system after failure.",
    "MTBF": "Mean Time Between Failures — average time between system failures.",
    "NIST CSF": "NIST Cybersecurity Framework — Identify, Protect, Detect, Respond, Recover.",
    "PCI DSS": "Payment Card Industry Data Security Standard — required for handling card data.",
    "PKI": "Public Key Infrastructure — framework for managing digital certificates and encryption keys.",
    "RBAC": "Role-Based Access Control — permissions assigned to roles, users assigned to roles.",
    "RPO": "Recovery Point Objective — max acceptable data loss (how old can restored data be?).",
    "RTO": "Recovery Time Objective — max acceptable downtime (how quickly must systems recover?).",
    "SIEM": "Security Information and Event Management — centralizes log collection and correlation.",
    "SOAR": "Security Orchestration, Automation, and Response — automates incident response.",
    "SOC 2": "Service Organization Control 2 — audit of security controls at a service provider.",
    "SPF": "Sender Policy Framework — DNS record authorizing mail servers for a domain.",
    "SSO": "Single Sign-On — one login grants access to multiple systems.",
    "STIX/TAXII": "Standards for sharing cyber threat intelligence in machine-readable format.",
    "TLS": "Transport Layer Security — cryptographic protocol securing data in transit (HTTPS).",
    "VPN": "Virtual Private Network — encrypted tunnel over public networks.",
    "XSS": "Cross-Site Scripting — injects malicious JavaScript into web pages.",
    "Zero Trust": "Security model: never trust, always verify — regardless of network location.",
}

GLOSSARY.update({
    "ABAC": "Attribute-Based Access Control — access decisions based on attributes like user, device, location, time, and data sensitivity.",
    "ACL": "Access Control List — rule list that permits or denies access to a resource.",
    "AES": "Advanced Encryption Standard — modern symmetric encryption used for bulk data protection.",
    "Allow List": "Only approved applications, users, domains, or actions are permitted; everything else is denied.",
    "Anomaly Detection": "Detection method that identifies activity that differs from an established baseline.",
    "ARO": "Annualized Rate of Occurrence — how often a threat is expected to happen per year.",
    "Asset Inventory": "Authoritative list of hardware, software, cloud, and data assets that must be managed and protected.",
    "Attack Surface": "All exposed paths an attacker could use to enter or affect a system.",
    "Authentication": "Process of proving identity, such as with passwords, MFA, certificates, or biometrics.",
    "Authorization": "Process of deciding what an authenticated subject is allowed to access.",
    "Baiting": "Social engineering attack that tempts victims with something enticing, such as infected USB media.",
    "Bcrypt": "Password hashing and key-stretching algorithm designed to slow offline cracking.",
    "BIA": "Business Impact Analysis — identifies critical processes, dependencies, outage impact, RTO, and RPO.",
    "Block List": "Known-bad items are denied while everything else is allowed unless another control blocks it.",
    "Blue Team": "Defensive security team responsible for monitoring, hardening, detection, and response.",
    "Botnet": "Network of compromised systems controlled by an attacker through command-and-control.",
    "BYOD": "Bring Your Own Device — personal device use for work, requiring mobile and data controls.",
    "Canary Token": "Decoy file, URL, credential, or value that generates an alert when touched.",
    "CASB": "Cloud Access Security Broker — enforces visibility and security policy between users and cloud/SaaS services.",
    "Certificate Pinning": "Technique that limits trust to expected certificates or public keys to reduce impersonation risk.",
    "Change Advisory Board": "Group that reviews, approves, and coordinates significant production changes.",
    "CIRT": "Computer Incident Response Team — team responsible for coordinating incident response.",
    "Cold Site": "Recovery location with basic facilities but little or no ready-to-run IT equipment.",
    "Compensating Control": "Alternative control used when the preferred control is not feasible.",
    "Container": "Lightweight isolated runtime package for an application and its dependencies.",
    "COOP": "Continuity of Operations Plan — keeps essential functions operating during disruptions.",
    "CRL": "Certificate Revocation List — published list of certificates that should no longer be trusted.",
    "CSRF": "Cross-Site Request Forgery — tricks a user's browser into submitting unwanted authenticated actions.",
    "DAST": "Dynamic Application Security Testing — tests a running application for vulnerabilities.",
    "Data at Rest": "Data stored on media such as disks, databases, object storage, or backups.",
    "Data Controller": "Privacy role that determines why and how personal data is processed.",
    "Data in Transit": "Data moving across a network, commonly protected with TLS, VPNs, or IPsec.",
    "Data in Use": "Data actively being processed in memory or by an application.",
    "Data Minimization": "Privacy principle: collect and retain only the data needed for a defined purpose.",
    "Data Owner": "Person or role accountable for classifying data and approving its use and access.",
    "Data Processor": "Privacy role that processes personal data on behalf of a controller.",
    "Data Sovereignty": "Concept that data may be subject to laws based on where it is stored or processed.",
    "De-identification": "Removal of direct identifiers to reduce privacy risk, though re-identification may still be possible.",
    "Dependency Confusion": "Supply-chain attack where a package manager pulls a malicious public package instead of a private one.",
    "DevSecOps": "Practice of integrating security into development, testing, deployment, and operations workflows.",
    "Differential Privacy": "Privacy technique that adds mathematical noise to reduce re-identification risk in datasets.",
    "Digital Signature": "Private-key signature that provides integrity, authenticity, and non-repudiation.",
    "Directory Traversal": "Web attack that uses path manipulation such as ../ to access unauthorized files.",
    "DNS Sinkhole": "DNS control that redirects malicious domain lookups to a safe destination for blocking and detection.",
    "Downgrade Attack": "Attack that forces systems to use an older or weaker protocol or cipher.",
    "EAP": "Extensible Authentication Protocol — framework used by 802.1X and enterprise wireless authentication.",
    "Evil Twin": "Rogue wireless access point that impersonates a legitimate network.",
    "False Negative": "A security tool misses malicious or noncompliant activity.",
    "False Positive": "A security tool flags benign activity as malicious or noncompliant.",
    "Federation": "Trust relationship that lets identities from one organization or provider access another service.",
    "Fileless Malware": "Malware technique that runs from memory or trusted tools instead of a normal file on disk.",
    "FIM": "File Integrity Monitoring — detects unauthorized changes to important files.",
    "Firewall": "Network or host control that allows or blocks traffic based on rules.",
    "Firmware": "Low-level software embedded in hardware devices.",
    "Fuzzing": "Testing technique that sends unexpected or random input to find crashes and vulnerabilities.",
    "HIDS": "Host-based Intrusion Detection System — detects suspicious activity on an endpoint or server.",
    "HIPS": "Host-based Intrusion Prevention System — blocks suspicious activity on an endpoint or server.",
    "Honeynet": "Network of honeypots that simulates a larger environment for detection and research.",
    "Honeypot": "Decoy system designed to attract and detect attackers.",
    "Hot Site": "Fully equipped recovery site designed for rapid failover with minimal downtime.",
    "HSM": "Hardware Security Module — tamper-resistant device for generating, storing, and using cryptographic keys.",
    "IaC": "Infrastructure as Code — defines infrastructure in version-controlled templates or code.",
    "IdP": "Identity Provider — service that authenticates users and issues identity assertions or tokens.",
    "IDOR": "Insecure Direct Object Reference — missing authorization check on a directly referenced object.",
    "Incident Response": "Structured process for preparing, detecting, containing, eradicating, recovering, and learning from incidents.",
    "Indicator of Attack": "Behavior or pattern suggesting an attack is currently underway.",
    "Input Validation": "Checking input for type, length, format, range, and safety before processing.",
    "JIT Access": "Just-in-time access — grants privileges only when needed and for a limited period.",
    "Jump Server": "Hardened intermediary host used to administer sensitive network segments.",
    "Key Escrow": "Process where encryption keys are held by a trusted third party or recovery system.",
    "Key Rotation": "Replacing cryptographic keys on a planned schedule or after suspected exposure.",
    "Least Privilege": "Grant only the permissions needed to perform required tasks.",
    "Logic Bomb": "Malicious code triggered by a condition such as a date, event, or account change.",
    "MOU": "Memorandum of Understanding — document describing mutual expectations, usually less formal than a contract.",
    "NAC": "Network Access Control — checks and controls devices before or during network access.",
    "NDA": "Non-Disclosure Agreement — contract requiring protection of confidential information.",
    "Non-repudiation": "Assurance that someone cannot credibly deny an action, often provided by digital signatures and logging.",
    "OCSP": "Online Certificate Status Protocol — checks certificate revocation status in near real time.",
    "OIDC": "OpenID Connect — identity layer built on OAuth 2.0 for authentication.",
    "Password Spraying": "Trying a few common passwords across many accounts to avoid lockouts.",
    "PBKDF2": "Password-Based Key Derivation Function 2 — key-stretching method for slowing password guessing.",
    "Pharming": "Redirecting users to a fake site, often through DNS or host-file manipulation.",
    "Pretexting": "Social engineering that uses a fabricated scenario or identity to manipulate a target.",
    "Privileged Access Management": "Controls for managing, monitoring, approving, and limiting elevated access.",
    "Pseudonymization": "Replacing identifiers with pseudonyms; reversible if the mapping key exists.",
    "Rainbow Table": "Precomputed password hash table used to speed up cracking unsalted hashes.",
    "Red Team": "Offensive security team that emulates attackers to test defenses.",
    "Residual Risk": "Risk remaining after controls are applied.",
    "Right to Audit": "Contract clause allowing a customer to review a vendor's controls or evidence.",
    "Risk Acceptance": "Decision to acknowledge a risk and take no additional action at this time.",
    "Risk Appetite": "Broad amount and type of risk an organization is willing to accept.",
    "Risk Avoidance": "Risk response that stops the risky activity entirely.",
    "Risk Mitigation": "Risk response that reduces likelihood, impact, or both by applying controls.",
    "Risk Register": "Central record of identified risks, owners, ratings, treatment plans, and status.",
    "Risk Tolerance": "Specific acceptable variation or threshold around risk objectives.",
    "Risk Transference": "Risk response that shifts financial impact to another party, such as insurance.",
    "SAML": "Security Assertion Markup Language — XML-based federation protocol often used for SSO.",
    "SASE": "Secure Access Service Edge — cloud-delivered networking and security architecture.",
    "SAST": "Static Application Security Testing — analyzes source code or binaries without running the app.",
    "SCADA": "Supervisory Control and Data Acquisition — industrial control systems for monitoring and controlling processes.",
    "Secure Baseline": "Approved minimum secure configuration for a system, application, device, or service.",
    "Security Exception": "Documented temporary approval to deviate from a policy or standard with risk acceptance.",
    "Separation of Duties": "Dividing critical tasks so no single person has unchecked control.",
    "Serverless": "Cloud execution model where the provider manages runtime infrastructure and the customer deploys functions.",
    "SLA": "Service Level Agreement — measurable service commitment such as uptime or response time.",
    "SLE": "Single Loss Expectancy — expected financial loss from one occurrence of a risk event.",
    "Smishing": "SMS/text-message phishing.",
    "SOC": "Security Operations Center — team and function responsible for monitoring, detection, and response.",
    "Spear Phishing": "Targeted phishing aimed at a specific person, role, or organization.",
    "SRTP": "Secure Real-time Transport Protocol — protects voice and video media streams.",
    "SSRF": "Server-Side Request Forgery — tricks a server into making unauthorized requests.",
    "Tailgating": "Following an authorized person into a secure area without authenticating.",
    "Tabletop Exercise": "Discussion-based test of a plan using a realistic scenario.",
    "Tokenization": "Replacing sensitive data with a substitute token mapped to the real value in a secure vault.",
    "TPM": "Trusted Platform Module — hardware chip used for key storage, measured boot, and device trust.",
    "UEFI Secure Boot": "Boot protection that verifies trusted bootloaders and helps prevent bootkits.",
    "Vishing": "Voice phishing using phone calls or voice messages.",
    "Warm Site": "Partially equipped recovery site that can be made operational faster than a cold site.",
    "Watering Hole": "Attack that compromises a site commonly visited by the intended victims.",
    "WPA3": "Modern Wi-Fi security standard with stronger authentication and encryption than WPA2.",
    "XDR": "Extended Detection and Response — correlates telemetry across endpoints, network, cloud, identity, and email.",
})

# ══════════════════════════════════════════════════════════════════════════════
#  A+ CORE 1 (220-1201) — DOMAIN THEME, WEIGHTS & OBJECTIVES
# ══════════════════════════════════════════════════════════════════════════════

DOMAIN_THEME_APLUS1 = {
    "Domain 1": {"color": C.ORG,  "icon": "📱", "short": "D1", "bg": C.BG_ORG},
    "Domain 2": {"color": C.GOLD, "icon": "🌐", "short": "D2", "bg": C.BG_YLW},
    "Domain 3": {"color": C.LIME, "icon": "🔧", "short": "D3", "bg": C.BG_GRN},
    "Domain 4": {"color": C.SKY,  "icon": "☁️",  "short": "D4", "bg": C.BG_BLU},
    "Domain 5": {"color": C.PRP,  "icon": "🛠️",  "short": "D5", "bg": C.BG_MAG},
}

DOMAIN_WEIGHTS_APLUS1 = {
    "Domain 1 – Mobile Devices": 15,
    "Domain 2 – Networking": 20,
    "Domain 3 – Hardware": 25,
    "Domain 4 – Virtualization and Cloud Computing": 11,
    "Domain 5 – Hardware and Network Troubleshooting": 29,
}

DOM_ORDER_APLUS1 = [
    "Domain 1 – Mobile Devices",
    "Domain 2 – Networking",
    "Domain 3 – Hardware",
    "Domain 4 – Virtualization and Cloud Computing",
    "Domain 5 – Hardware and Network Troubleshooting",
]

EXAM_OBJECTIVES_APLUS1 = {
    "Domain 1 – Mobile Devices": {
        "weight": 15,
        "objectives": [
            "Install and configure laptop hardware: display types (IPS/OLED/TN/VA), keyboard, touchpad, battery, RAM (SO-DIMM/LPDDR5X), and storage (M.2/NVMe).",
            "Compare mobile device types: smartphones, tablets, wearables, e-readers, and their OS ecosystems (iOS, Android, iPadOS).",
            "Configure mobile connectivity: Bluetooth pairing, Wi-Fi profiles, 4G LTE/5G bands, GPS, NFC, hotspot/tethering.",
            "Summarize mobile synchronization: cloud sync (iCloud, Google), USB sync, and corporate MDM enrollment.",
            "Explain mobile security: screen locks, biometrics, remote wipe, MDM policies, and app permissions.",
            "Identify connector types: USB-C, Lightning, Micro-USB and their data/power capabilities.",
        ],
        "study": [
            "Display tech: IPS (accurate color, wide 178° angles), TN (fast 1ms response, poor angles), OLED (true blacks, no backlight), VA (best contrast of LCD types).",
            "Digitizer = touch layer; LCD/OLED panel = image layer — they fail independently and can be replaced separately.",
            "5G bands: low-band (coverage, 4G-like speed), mid-band/C-band (best balance), mmWave (multi-Gbps, short range, dense urban only).",
            "MDM lets IT enforce policies, push/remove apps, locate devices, and remote wipe corporate devices.",
            "NFC: under 4 cm range. Bluetooth 5.x: up to 400 m. GPS requires clear sky view.",
        ],
    },
    "Domain 2 – Networking": {
        "weight": 20,
        "objectives": [
            "Identify networking hardware: switches, routers, access points, firewalls, PoE injectors, cable modems, ONTs.",
            "Configure TCP/IP: addressing, subnet masks, CIDR, default gateway, DNS, DHCP.",
            "Compare wireless standards: 802.11a/b/g/n/ac/ax (Wi-Fi 6/6E) and 802.11be (Wi-Fi 7) — frequencies, speeds.",
            "Identify cable types: Cat5e/6/6a/8, fiber (single/multi-mode), coaxial — max speed and distance.",
            "Identify TCP/UDP ports: DNS (53), DHCP (67/68), HTTP (80), HTTPS (443), SSH (22), RDP (3389), etc.",
            "Summarize network services: DNS, DHCP, VPN, proxy, firewall, load balancer roles.",
        ],
        "study": [
            "Wi-Fi 7 (802.11be): MLO uses 2.4/5/6 GHz simultaneously; 46 Gbps theoretical — new to 1201 series.",
            "Cat8: 40 Gbps at 30 m (data centers only). Cat6a: 10 Gbps at 100 m. Cat6: 10 Gbps at 55 m only.",
            "PoE 802.3af=15.4W, PoE+ 802.3at=30W, PoE++ 802.3bt=60-100W. Match standard to device requirements.",
            "ONT converts fiber signal to Ethernet at customer premises for fiber-to-the-home installations.",
            "Hub (Layer 1, shared bandwidth) vs Switch (Layer 2, MAC-based, dedicated bandwidth) vs Router (Layer 3, IP-based).",
        ],
    },
    "Domain 3 – Hardware": {
        "weight": 25,
        "objectives": [
            "Install storage: HDD (SATA), SSD (SATA/NVMe/M.2 Gen3/4/5), optical drives, external storage.",
            "Install memory: DDR4, DDR5, SO-DIMM, ECC, single/dual/quad-channel configurations.",
            "Select and install CPUs: socket types (LGA, PGA, BGA), thermal paste, coolers (air/liquid), TDP.",
            "Identify motherboard components: PCIe slots, headers, UEFI/BIOS, CMOS battery, chipsets.",
            "Summarize printer types: laser, inkjet, thermal, impact (dot matrix), 3D — components and consumables.",
            "Identify cables: SATA, ATX power (24-pin main, 8-pin EPS, PCIe 6/8-pin), display (HDMI, DP, VGA, DVI).",
            "Explain display tech: IPS/TN/VA/OLED, resolution, refresh rate, HDR, aspect ratio, adaptive sync.",
        ],
        "study": [
            "DDR5 vs DDR4: higher bandwidth, 1.1V (vs 1.2V), on-die ECC, dual independent 32-bit channels per DIMM.",
            "NVMe speeds — Gen 3: 3,500 MB/s  Gen 4: 7,000 MB/s  Gen 5: 14,000 MB/s  SATA III: 600 MB/s max.",
            "Laser print order: Processing → Charging → Exposing → Developing → Transferring → Fusing → Cleaning.",
            "3D printing: FDM (filament/cheapest), SLA (resin/high detail), SLS (powder sintering/industrial).",
            "Resolution: 1080p=FHD, 1440p=QHD/2K, 2160p=UHD/4K. Adaptive sync (FreeSync/G-Sync) eliminates tearing.",
        ],
    },
    "Domain 4 – Virtualization and Cloud Computing": {
        "weight": 11,
        "objectives": [
            "Summarize cloud: public/private/hybrid/community; IaaS/PaaS/SaaS/DaaS; NIST 5 characteristics.",
            "Explain client virtualization: Type 1/2 hypervisors, VM components, snapshots, templates, resource pools.",
            "Compare containers vs VMs: Docker, Kubernetes, shared kernel, image scanning.",
            "Summarize VDI and application virtualization use cases.",
        ],
        "study": [
            "Type 1 (bare metal): ESXi, Hyper-V, KVM — runs on hardware directly, enterprise use.",
            "Type 2 (hosted): VirtualBox, VMware Workstation — runs on top of OS, desktop/lab use.",
            "Containers share host OS kernel — much lighter than VMs, less isolated. Kubernetes orchestrates at scale.",
            "NIST 5 cloud characteristics: on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service.",
            "Snapshot = point-in-time VM state for rollback. NOT a replacement for backups.",
        ],
    },
    "Domain 5 – Hardware and Network Troubleshooting": {
        "weight": 29,
        "objectives": [
            "Apply CompTIA troubleshooting methodology to all hardware and network problems.",
            "Troubleshoot storage: HDDs (clicking, slow), SSDs (wear, not recognized), RAID failures.",
            "Troubleshoot display/video: no signal, artifacts, flickering, dead pixels, resolution issues.",
            "Troubleshoot power: no POST, random shutdowns, capacitor bulge, PSU failure.",
            "Troubleshoot CPU/RAM/motherboard: POST beep codes, BSODs, memory errors.",
            "Troubleshoot printers: jams, ghosting, smearing, streaks, connectivity.",
            "Troubleshoot wired/wireless networks: IP conflicts, APIPA, packet loss, slow speeds, interference.",
        ],
        "study": [
            "Steps: 1-Identify 2-Theory 3-Test 4-Plan/Implement 5-Verify 6-Document.",
            "Capacitor bulge on motherboard = replace the board immediately.",
            "Inkjet nozzle streaks: run head cleaning utility first, then nozzle check. Replace cartridge last.",
            "Wireless SNR: at least +25 dB is good. Low SNR = retransmissions and slow throughput.",
            "RAID 5: survives 1 failure. RAID 6: survives 2. After failure, replace drive and let array rebuild before anything else.",
        ],
    },
}

QUESTIONS_APLUS1 = [

    # DOMAIN 1 — MOBILE DEVICES
    {
        "domain": "Domain 1 – Mobile Devices",
        "topic": "Mobile Connectors", "difficulty": "easy",
        "question": "Which connector is now the universal standard on modern Android phones, laptops, and tablets for both data and charging, and is reversible so it works in either orientation?",
        "choices": {"A":"Lightning","B":"Micro-USB","C":"USB-C","D":"Mini-USB"},
        "answer": "C",
        "explanation": "USB-C (Type-C) is reversible, supports USB 3.x speeds, Thunderbolt 4, DisplayPort Alt Mode, and USB Power Delivery up to 240W. It is universal across modern Android phones, iPads, MacBooks, and most laptops. Lightning was Apple's proprietary connector for older iPhones — replaced by USB-C starting with iPhone 15. Micro-USB was the previous Android standard — slower and directional (only one way). Mini-USB is an older standard seen on cameras and older external drives. For 220-1201: know all connector types and which devices use them."
    },
    {
        "domain": "Domain 1 – Mobile Devices",
        "topic": "Display Technologies", "difficulty": "medium",
        "question": "A laptop advertises 178-degree viewing angles and accurate color reproduction suitable for photo editing. Which panel technology does it MOST likely use?",
        "choices": {"A":"TN (Twisted Nematic)","B":"IPS (In-Plane Switching)","C":"CRT","D":"Plasma"},
        "answer": "B",
        "explanation": "IPS (In-Plane Switching) panels offer consistent, accurate color from virtually any angle (178° horizontal and vertical) and are the standard for professional photo/video work and quality laptops. Trade-off: slightly slower pixel response than TN panels. TN panels: fastest response (1ms), best for competitive gaming — terrible viewing angles and color accuracy. OLED: self-emitting pixels, perfect blacks, infinite contrast — premium phones and high-end laptops. VA: better contrast than IPS, better angles than TN — common in budget monitors. For 220-1201: know all four panel types and their trade-offs."
    },
    {
        "domain": "Domain 1 – Mobile Devices",
        "topic": "Digitizer vs Display", "difficulty": "medium",
        "question": "A tablet screen displays a perfect image but does not respond to any touch input at all. Which component has MOST likely failed?",
        "choices": {"A":"LCD backlight","B":"GPU","C":"Digitizer","D":"Battery"},
        "answer": "C",
        "explanation": "The digitizer is the transparent capacitive touch-sensing layer on top of the display panel. It detects touch and converts it to digital coordinates — completely separate from the display itself. When the digitizer fails, the screen still shows images normally (the LCD or OLED panel is fine) but touch input stops entirely. A failed backlight causes a dim or black screen. On modern devices the digitizer is often fused to the glass — a cracked digitizer usually means replacing the full display assembly. The key diagnostic: image is fine but touch is dead = digitizer. Image is dark or absent = backlight, GPU, or cable."
    },
    {
        "domain": "Domain 1 – Mobile Devices",
        "topic": "NFC and Short-Range Wireless", "difficulty": "easy",
        "question": "Which short-range wireless technology enables contactless payments like Apple Pay and Google Pay by bringing a device within about 4 centimeters of a terminal?",
        "choices": {"A":"Bluetooth 5.0","B":"NFC","C":"Wi-Fi Direct","D":"RFID (125 kHz)"},
        "answer": "B",
        "explanation": "NFC (Near Field Communication) operates at 13.56 MHz with a range under 4 cm, making accidental eavesdropping extremely difficult. Uses: contactless payments (Apple Pay, Google Pay), transit card taps, Bluetooth quick-pair, and small data transfers. The very short range is a security feature. Bluetooth 5.0: up to 400 m (Class 1) — used for peripherals, headphones, speakers. Wi-Fi Direct: peer-to-peer Wi-Fi without an access point — used for screen mirroring and file transfer. RFID at 125 kHz: one-way, read-only, used in older access badges and inventory tags. NFC is bidirectional — both devices can send and receive."
    },
    {
        "domain": "Domain 1 – Mobile Devices",
        "topic": "5G Bands", "difficulty": "medium",
        "question": "A user achieves multi-gigabit download speeds on 5G in a downtown area but loses signal when entering buildings. Which 5G frequency band is providing these speeds?",
        "choices": {"A":"Low-band 5G (sub-1 GHz)","B":"Mid-band 5G (C-band, 2.5–6 GHz)","C":"mmWave 5G (24–100 GHz)","D":"4G LTE-A"},
        "answer": "C",
        "explanation": "mmWave (millimeter wave) 5G operates at 24–100 GHz and delivers multi-gigabit speeds (2–10 Gbps) with extremely low latency. Drawbacks: very poor building penetration and limited range (hundreds of meters) — requires dense small cell deployment in urban cores. Low-band 5G: excellent nationwide coverage and building penetration, speeds similar to fast 4G LTE (100–300 Mbps). Mid-band 5G (C-band): the best balance — good speed (500 Mbps–2 Gbps) with reasonable coverage and some building penetration. Most carrier deployments focus on C-band for the best user experience. The 220-1201 exam tests all three 5G band characteristics."
    },
    {
        "domain": "Domain 1 – Mobile Devices",
        "topic": "Laptop RAM", "difficulty": "easy",
        "question": "A technician is upgrading RAM in a laptop. Which RAM form factor is standard for laptops?",
        "choices": {"A":"SO-DIMM","B":"UDIMM","C":"RDIMM","D":"LRDIMM"},
        "answer": "A",
        "explanation": "SO-DIMM (Small Outline DIMM) is the laptop form factor — physically smaller than desktop DIMMs. DDR4 SO-DIMM: 260 pins. DDR5 SO-DIMM: 262 pins. Desktop DDR4 DIMM: 288 pins. Many modern ultrabooks and MacBooks use soldered LPDDR5/5X — permanently attached to the motherboard and not user-upgradeable. Always check before purchasing: is the laptop's RAM socketed (SO-DIMM) or soldered? UDIMM: standard unbuffered desktop memory. RDIMM: registered server memory for large-capacity configurations. LRDIMM: load-reduced server memory. For 220-1201: laptop = SO-DIMM or soldered; desktop = DIMM."
    },
    {
        "domain": "Domain 1 – Mobile Devices",
        "topic": "MDM", "difficulty": "medium",
        "question": "A company issues smartphones to employees and needs to enforce PIN requirements, restrict camera use, and remotely wipe devices if stolen. Which technology enables this?",
        "choices": {"A":"NFC device management","B":"MDM — Mobile Device Management","C":"Bluetooth tethering policy","D":"GPS tracking only"},
        "answer": "B",
        "explanation": "MDM (Mobile Device Management) platforms (Microsoft Intune, Jamf, VMware Workspace ONE) allow IT to: enforce passcode complexity, disable hardware features (camera, microphone, USB), push and remove apps remotely, enforce encryption, locate devices via GPS, remotely lock, and perform remote wipe. Devices must be MDM enrolled — either by the user (BYOD/self-enrollment) or pre-enrolled by IT (corporate). MDM can containerize work apps separately from personal apps on BYOD devices, allowing corporate data wipe without touching personal data. Without MDM, there is no centralized way to enforce policies or remotely wipe a lost device."
    },
    {
        "domain": "Domain 1 – Mobile Devices",
        "topic": "Mobile OS Features", "difficulty": "easy",
        "question": "Which mobile feature allows a smartphone to share its cellular data connection with a laptop or other device wirelessly?",
        "choices": {"A":"NFC pairing","B":"Bluetooth audio","C":"Personal hotspot / tethering","D":"AirDrop"},
        "answer": "C",
        "explanation": "Personal hotspot (iOS) or Mobile Hotspot (Android) allows a smartphone to act as a portable Wi-Fi router, sharing its cellular data connection with up to several other devices wirelessly. USB tethering shares the connection via USB cable — faster and charges the phone simultaneously. Bluetooth tethering: shares data via Bluetooth — slower than Wi-Fi hotspot. Carrier plans may restrict or charge extra for hotspot use. AirDrop: Apple-proprietary file sharing between Apple devices via Bluetooth + Wi-Fi Direct — NOT for sharing internet. NFC pairing: establishes Bluetooth or Wi-Fi connections quickly — not an internet sharing technology."
    },

    # DOMAIN 2 — NETWORKING
    {
        "domain": "Domain 2 – Networking",
        "topic": "Cable Categories", "difficulty": "easy",
        "question": "Which cable category supports 10 Gbps Ethernet at the full 100-meter distance and is the current standard for new commercial installations?",
        "choices": {"A":"Cat5e","B":"Cat6","C":"Cat6a","D":"Cat3"},
        "answer": "C",
        "explanation": "Cat6a (Augmented Cat6) supports 10GBASE-T at the full 100-meter segment length. The 'augmented' spec reduces alien crosstalk compared to standard Cat6. Cat5e: 1 Gbps at 100 m (common in older buildings). Cat6: 10 Gbps only up to 55 m; drops to 1 Gbps at 100 m. Cat6a: 10 Gbps at full 100 m — recommended for new installations. Cat8: 25/40 Gbps but only 30 m — data center use only (server-to-switch connections). Fiber optic: multi-mode up to ~550 m (OM4), single-mode up to tens of kilometers — immune to EMI. All copper Ethernet uses the 100 m segment rule except Cat8 (30 m)."
    },
    {
        "domain": "Domain 2 – Networking",
        "topic": "DHCP", "difficulty": "easy",
        "question": "Which protocol automatically provides IP addresses, subnet masks, default gateways, and DNS server addresses to client devices on a network?",
        "choices": {"A":"DNS","B":"DHCP","C":"ARP","D":"SNMP"},
        "answer": "B",
        "explanation": "DHCP (Dynamic Host Configuration Protocol) uses ports 67 (server) and 68 (client) over UDP. The DORA process: Discover (client broadcasts), Offer (server proposes IP), Request (client accepts), Acknowledge (server confirms). If DHCP fails, Windows self-assigns an APIPA address (169.254.x.x). DNS (port 53): resolves hostnames to IP addresses. ARP: resolves IP addresses to MAC addresses on the local segment. SNMP (161/162): monitors and manages network devices. DHCP leases are temporary — clients renew at 50% of lease time. Static IPs bypass DHCP and are used for servers, printers, and network devices needing consistent addresses."
    },
    {
        "domain": "Domain 2 – Networking",
        "topic": "Common Ports", "difficulty": "easy",
        "question": "A user cannot access any websites by name but can access them by IP address. Which service has MOST likely failed?",
        "choices": {"A":"DHCP","B":"DNS","C":"HTTP","D":"FTP"},
        "answer": "B",
        "explanation": "DNS (Domain Name System, port 53) resolves hostnames (like google.com) to IP addresses. If DNS fails, hostnames cannot be resolved — but direct IP access still works because no name resolution is needed. Confirming DNS failure: ping google.com fails but ping 8.8.8.8 succeeds. Fix: check DNS server setting in ipconfig /all, try setting DNS manually to 8.8.8.8 (Google) or 1.1.1.1 (Cloudflare), run ipconfig /flushdns to clear stale cache entries. DHCP failure causes APIPA (169.254.x.x) — no IP at all, not just DNS. HTTP failure means web server is down — the issue would be specific to that site, not all sites."
    },
    {
        "domain": "Domain 2 – Networking",
        "topic": "Wi-Fi Standards", "difficulty": "medium",
        "question": "Which Wi-Fi standard introduced Multi-Link Operation (MLO), allowing devices to transmit across multiple frequency bands simultaneously, and carries the Wi-Fi 7 designation?",
        "choices": {"A":"802.11ac (Wi-Fi 5)","B":"802.11ax (Wi-Fi 6)","C":"802.11be (Wi-Fi 7)","D":"802.11n (Wi-Fi 4)"},
        "answer": "C",
        "explanation": "802.11be (Wi-Fi 7): introduced Multi-Link Operation (MLO) — a device can simultaneously use multiple bands (2.4/5/6 GHz) for aggregated throughput and reduced latency. Theoretical max: 46 Gbps. Wi-Fi generation quick reference: 802.11b = Wi-Fi 1 (11 Mbps), 802.11a/g = Wi-Fi 2/3 (54 Mbps), 802.11n = Wi-Fi 4 (600 Mbps, dual-band), 802.11ac = Wi-Fi 5 (3.5 Gbps, 5 GHz), 802.11ax = Wi-Fi 6 (9.6 Gbps, OFDMA), 802.11ax + 6 GHz = Wi-Fi 6E, 802.11be = Wi-Fi 7 (46 Gbps, MLO). The 220-1201 adds Wi-Fi 7 as a tested standard."
    },
    {
        "domain": "Domain 2 – Networking",
        "topic": "PoE Standards", "difficulty": "medium",
        "question": "A network administrator needs to power IP cameras requiring 25W each over Cat6a cable with no separate power outlet available. Which PoE standard is the MINIMUM that meets this requirement?",
        "choices": {"A":"802.3af (PoE) — 15.4W","B":"802.3at (PoE+) — 30W","C":"802.3bt Type 3 (PoE++) — 60W","D":"Standard Ethernet — no power"},
        "answer": "B",
        "explanation": "PoE standards and power budgets: 802.3af (PoE): 15.4W per port max — VoIP phones, basic APs, low-power cameras. 802.3at (PoE+): 30W per port max — most IP cameras, mid-range APs, PTZ cameras. 802.3bt Type 3 (PoE++): 60W — high-end APs, video conferencing systems. 802.3bt Type 4: 100W — thin clients, LED panels. At 25W the camera exceeds PoE's 15.4W but fits within PoE+'s 30W budget. Both switch port and device must support the same PoE standard. PoE injectors add PoE to individual ports on non-PoE switches — useful for adding a single camera without replacing the entire switch."
    },
    {
        "domain": "Domain 2 – Networking",
        "topic": "Network Devices", "difficulty": "easy",
        "question": "Which network device forwards frames based on MAC addresses, creates a separate collision domain for each port, and operates at OSI Layer 2?",
        "choices": {"A":"Hub","B":"Router","C":"Switch","D":"Modem"},
        "answer": "C",
        "explanation": "A managed or unmanaged switch operates at Layer 2 (Data Link) and learns MAC addresses dynamically to build a forwarding table. It sends frames only to the correct destination port — unlike a hub which broadcasts to all ports. Each switch port is its own collision domain, eliminating collisions entirely. All switch ports share one broadcast domain (unless VLANs are configured). Hub: Layer 1 — shares bandwidth among all ports, all in one collision domain, obsolete. Router: Layer 3 — routes between different IP networks using IP addresses. Modem: converts analog signals (coax, phone line, fiber) to digital Ethernet — connects the home/office to the ISP."
    },
    {
        "domain": "Domain 2 – Networking",
        "topic": "IP Addressing", "difficulty": "medium",
        "question": "A workstation with IP 192.168.10.50/24, gateway 192.168.10.1, can ping the gateway but cannot browse any websites. Pinging 8.8.8.8 by IP succeeds. What is the problem?",
        "choices": {"A":"The subnet mask is incorrect","B":"The default gateway is misconfigured","C":"DNS is not configured or not reachable","D":"The workstation's NIC is failing"},
        "answer": "C",
        "explanation": "The test results tell the full story: pinging the gateway (192.168.10.1) confirms the physical connection and local routing work correctly. Pinging 8.8.8.8 (an internet IP) confirms the path to the internet works — packets are reaching external servers. Failing to browse websites by name means hostname-to-IP resolution (DNS) is broken. Without a functioning DNS server, the browser cannot translate 'google.com' into an IP address. Fix: set DNS to 8.8.8.8 or 1.1.1.1 in the network adapter settings, or run ipconfig /flushdns to clear stale cache. The subnet mask /24 (255.255.255.0) is correct for this range, and the gateway 192.168.10.1 is in the same /24 subnet."
    },
    {
        "domain": "Domain 2 – Networking",
        "topic": "Fiber Optic Cabling", "difficulty": "medium",
        "question": "A network engineer needs to run a cable between two buildings 400 meters apart. Copper Ethernet will not work. Which cable type should be used?",
        "choices": {"A":"Cat6a UTP","B":"Cat8 STP","C":"Fiber optic","D":"Coaxial RG-6"},
        "answer": "C",
        "explanation": "All copper Ethernet is limited to 100 meters (Cat8 is 30 m). At 400 meters, only fiber optic cable can carry Ethernet signals. Fiber transmits light, not electrical signals, so it is also immune to electromagnetic interference (EMI) — ideal for running between buildings (where lightning strikes on copper can damage equipment) and through electrically noisy environments. Multi-mode fiber (MMF): up to ~550 m (OM4) using LED light, lower cost transceivers — good for 400 m. Single-mode fiber (SMF): up to tens of kilometers using laser light — overkill for 400 m but future-proof. Common fiber connectors: LC (small, data center standard), SC (square, push-pull), ST (bayonet, older installations)."
    },

    # DOMAIN 3 — HARDWARE
    {
        "domain": "Domain 3 – Hardware",
        "topic": "CPU Sockets", "difficulty": "medium",
        "question": "Intel Core Ultra (LGA 1851) and AMD Ryzen 9000 (AM5) both use which socket type where the contact pins are located on the motherboard?",
        "choices": {"A":"PGA — pins on the CPU","B":"BGA — soldered to board","C":"LGA — pins on the motherboard socket","D":"ZIF — zero insertion force with pins on both"},
        "answer": "C",
        "explanation": "Both modern Intel (LGA 1851 for Core Ultra) and AMD AM5 (Ryzen 7000/9000) now use LGA (Land Grid Array) sockets where the pins are on the MOTHERBOARD and the CPU has flat contact pads (lands). A bent socket pin means an expensive motherboard repair. Historical context: AMD used PGA (pins on CPU) for AM4 (Ryzen 1000–5000) — bent CPU pins were more forgivable to fix. Intel has used LGA since LGA 775. BGA (Ball Grid Array): soldered permanently — laptops and mobile devices. For 220-1201: both current Intel and AMD desktop platforms now use LGA-style sockets, though they are not compatible with each other."
    },
    {
        "domain": "Domain 3 – Hardware",
        "topic": "NVMe Storage", "difficulty": "medium",
        "question": "A technician installs an M.2 NVMe Gen 4 SSD. What approximate sequential read speed should this drive achieve?",
        "choices": {"A":"600 MB/s (SATA III max)","B":"3,500 MB/s (NVMe Gen 3)","C":"7,000 MB/s (NVMe Gen 4)","D":"14,000 MB/s (NVMe Gen 5)"},
        "answer": "C",
        "explanation": "NVMe generational speeds (sequential read): Gen 3 (PCIe 3.0 x4): ~3,500 MB/s. Gen 4 (PCIe 4.0 x4): ~7,000 MB/s. Gen 5 (PCIe 5.0 x4): ~14,000 MB/s. SATA III: 600 MB/s hard ceiling. The M.2 form factor (2242, 2260, 2280) is just the physical size — it supports BOTH SATA and NVMe protocols. Check the drive label or spec sheet to determine which protocol is used. The motherboard slot must also support the correct PCIe generation for full speed (a Gen 4 NVMe in a Gen 3 slot runs at Gen 3 speed). For 220-1201, know all three NVMe generations and the SATA ceiling."
    },
    {
        "domain": "Domain 3 – Hardware",
        "topic": "DDR5 Memory", "difficulty": "medium",
        "question": "Which benefit does DDR5 have over DDR4 that improves memory reliability even in systems without a dedicated ECC controller?",
        "choices": {"A":"DDR5 runs at higher voltage for stability","B":"DDR5 includes on-die ECC built into each memory chip","C":"DDR5 uses a narrower bus for less noise","D":"DDR5 is backward compatible with DDR4 slots"},
        "answer": "B",
        "explanation": "DDR5 includes on-die ECC (Error-Correcting Code) within each individual memory chip — this is separate from system-level ECC (which requires a server motherboard and ECC DIMMs). On-die ECC detects and corrects single-bit errors within the memory chip itself before the data even leaves the module, improving stability for all DDR5 systems. Other DDR5 improvements: higher bandwidth (6400+ MT/s vs DDR4's 3200 MT/s), lower voltage (1.1V vs 1.2V), higher density (up to 128GB per DIMM), two independent 32-bit sub-channels per DIMM. DDR5 uses a different 288-pin slot with a notch in a different position — NOT backward compatible with DDR4."
    },
    {
        "domain": "Domain 3 – Hardware",
        "topic": "Laser Printer Process", "difficulty": "medium",
        "question": "A laser printer produces pages where toner smears when rubbed with a finger immediately after printing. Which stage of the laser printing process has failed?",
        "choices": {"A":"Charging — drum not getting negative charge","B":"Exposing — laser not drawing the image","C":"Fusing — heat and pressure not bonding toner to paper","D":"Developing — toner not adhering to drum"},
        "answer": "C",
        "explanation": "Fusing is Stage 6: heat rollers (~180°C) and pressure rollers permanently melt toner into the paper fibers. A failing fuser (broken heating element, worn rollers) means toner sits loose on the paper surface — it smears when touched. Test: rub your finger on a freshly printed page — if it smears, replace the fuser. Full 7-stage laser printing process: 1-Processing (RIP), 2-Charging (drum gets -600V uniform charge), 3-Exposing (laser neutralizes charged areas to form latent image), 4-Developing (toner attaches to exposed areas), 5-Transferring (paper gets positive charge, attracts toner), 6-Fusing (heat bonds toner permanently), 7-Cleaning (residual toner removed from drum). Know every stage and what failure looks like."
    },
    {
        "domain": "Domain 3 – Hardware",
        "topic": "3D Printing", "difficulty": "medium",
        "question": "A dental lab needs to produce highly detailed models with smooth surfaces and tight tolerances using 3D printing. Which 3D printing method is BEST suited for this?",
        "choices": {"A":"FDM (Fused Deposition Modeling)","B":"SLA (Stereolithography)","C":"SLS (Selective Laser Sintering)","D":"Inkjet 3D printing"},
        "answer": "B",
        "explanation": "SLA (Stereolithography) uses a UV laser to cure liquid photopolymer resin layer by layer, producing very high detail, smooth surfaces, and tight tolerances — ideal for dental models, jewelry, miniatures, and prototyping. Post-processing required: wash and UV cure. FDM: most affordable, visible layer lines, limited detail — best for functional parts, not fine detail. SLS: industrial method fusing nylon or metal powder with a laser — strong parts, no support structures needed, expensive — used for functional mechanical components. DLP (Digital Light Processing): similar to SLA but uses a projector — faster than SLA, also high detail. For 220-1201, know FDM, SLA, and SLS as the three primary 3D printing types."
    },
    {
        "domain": "Domain 3 – Hardware",
        "topic": "PSU and Power", "difficulty": "easy",
        "question": "A PC has absolutely no signs of life — no fans, no LEDs, no beeps. The wall outlet is confirmed working. What is the FIRST component to test?",
        "choices": {"A":"RAM","B":"CPU","C":"PSU (Power Supply Unit)","D":"GPU"},
        "answer": "C",
        "explanation": "When a PC shows zero signs of life (no fans, no LEDs, no display, no beeps), the PSU is the first suspect because it powers every other component. A completely failed PSU means nothing else can receive power to operate. PSU test: use a PSU tester, or the paperclip test (short the PS_ON green wire to a ground/black wire on the 24-pin connector — if the PSU fan spins, the PSU has basic functionality). If PSU passes: check the wall outlet again, check the power cable, check the front panel power switch connector on the motherboard. RAM or CPU failures typically cause POST failures — system powers on (fans spin, LEDs light) but fails to boot, often with beep codes."
    },
    {
        "domain": "Domain 3 – Hardware",
        "topic": "Display Connectors", "difficulty": "easy",
        "question": "Which display connector standard carries both digital video AND audio in a single cable and is the most common connector on consumer televisions and monitors?",
        "choices": {"A":"VGA (DB-15)","B":"DVI-D","C":"HDMI","D":"S-Video"},
        "answer": "C",
        "explanation": "HDMI (High-Definition Multimedia Interface) carries both digital video and audio in one cable — no separate audio cable needed. HDMI 2.1 supports 4K@120Hz, 8K, HDR10+, VRR (Variable Refresh Rate), and eARC. DisplayPort: digital video (and audio), higher max bandwidth than HDMI, used on PC monitors and laptops — DP 2.1 supports up to 16K. USB-C/Thunderbolt: can carry DisplayPort Alt Mode signal plus power and data. VGA (DB-15): analog video only, no audio, 15-pin D-Sub connector — obsolete, limited resolution. DVI-D: digital video only, no audio — mostly replaced. DVI-I: carries both analog and digital but still no audio. For the exam: HDMI = video + audio on one cable."
    },

    # DOMAIN 4 — VIRTUALIZATION AND CLOUD
    {
        "domain": "Domain 4 – Virtualization and Cloud Computing",
        "topic": "Cloud Service Models", "difficulty": "easy",
        "question": "A company uses Microsoft 365 for email and Office apps hosted entirely by Microsoft with no on-premises servers to manage. Which cloud service model is this?",
        "choices": {"A":"IaaS","B":"PaaS","C":"SaaS","D":"DaaS"},
        "answer": "C",
        "explanation": "SaaS (Software as a Service): the provider manages everything — hardware, OS, middleware, and the application. The customer only manages their data and user access. Examples: Microsoft 365, Google Workspace, Salesforce, Dropbox, Zoom, Adobe Creative Cloud. IaaS: provider delivers virtualized infrastructure (compute, storage, networking); customer manages OS and above. Examples: AWS EC2, Azure VMs. PaaS: provider manages infrastructure and runtime; customer manages application code and data. Examples: Azure App Service, AWS Lambda, Google App Engine. DaaS (Desktop as a Service): virtual desktops from the cloud. Examples: Amazon WorkSpaces, Azure Virtual Desktop — useful for remote workers, thin clients, kiosk deployments."
    },
    {
        "domain": "Domain 4 – Virtualization and Cloud Computing",
        "topic": "Hypervisor Types", "difficulty": "medium",
        "question": "VMware ESXi runs directly on server hardware with no host OS installed beneath it. This is a Type ___ hypervisor, and it is preferred in production because:",
        "choices": {"A":"Type 2; it is easier to configure","B":"Type 1; it has direct hardware access for better performance and security","C":"Type 1; it supports more guest OS types","D":"Type 2; it requires less specialized hardware"},
        "answer": "B",
        "explanation": "Type 1 (bare-metal) hypervisors run DIRECTLY on physical hardware with no host OS layer — direct hardware access delivers better performance, efficiency, and a smaller attack surface. Examples: VMware ESXi, Microsoft Hyper-V (server), Proxmox VE, Xen, KVM. Standard in data centers and enterprise. Type 2 (hosted) hypervisors run as applications on top of a host OS. The host OS mediates hardware access — adding overhead and attack surface. Examples: Oracle VirtualBox, VMware Workstation/Fusion, Parallels Desktop. Used for developer workstations, testing labs, and desktop virtualization. For 220-1201: Type 1 = enterprise/server; Type 2 = desktop/personal use."
    },
    {
        "domain": "Domain 4 – Virtualization and Cloud Computing",
        "topic": "NIST Cloud Characteristics", "difficulty": "medium",
        "question": "A web app automatically provisions additional cloud servers during a product launch traffic spike, then releases them when demand drops — paying only for actual usage. Which two NIST cloud characteristics does this describe?",
        "choices": {"A":"Multi-tenancy and SLA","B":"Broad network access and private cloud","C":"Rapid elasticity and measured service","D":"On-demand self-service and resource pooling"},
        "answer": "C",
        "explanation": "NIST defines five essential cloud characteristics: 1. On-demand self-service: provision resources without provider interaction. 2. Broad network access: accessible over any network. 3. Resource pooling: provider resources shared across customers. 4. Rapid elasticity: scale resources up or down quickly and automatically. 5. Measured service: usage is metered, billed per consumption (pay-per-use). Auto-scaling during traffic spikes = rapid elasticity. Pay-only-for-what-you-use = measured service. Together they enable cost-efficient handling of variable workloads — a major cloud advantage over fixed on-premises infrastructure. Containers (Docker/Kubernetes) enable rapid elasticity at the application layer by spinning up/down containers in seconds."
    },
    {
        "domain": "Domain 4 – Virtualization and Cloud Computing",
        "topic": "Containers vs VMs", "difficulty": "hard",
        "question": "A DevOps team deploys 50 microservices using Docker containers on a single Linux host. How do containers differ from running 50 virtual machines on the same host?",
        "choices": {"A":"Containers each run a full OS; VMs share the host kernel","B":"Containers share the host OS kernel and are far lighter; VMs each include a full OS via a hypervisor","C":"Both are identical in resource usage and isolation","D":"Containers use Type 1 hypervisors; VMs use Type 2"},
        "answer": "B",
        "explanation": "Containers share the host OS kernel — they package only the application and its dependencies. This makes them much lighter (MBs vs GBs), start in seconds (vs minutes for VMs), and pack many more instances on the same hardware. Trade-off: less isolation than VMs — a kernel vulnerability could affect all containers on that host. Virtual Machines each include a complete guest OS running on a hypervisor — stronger isolation, larger footprint, slower to start. Use containers for: microservices, CI/CD pipelines, rapid deployment, cloud-native apps. Use VMs for: strong isolation requirements, running different OS families on same hardware, legacy app compatibility. Docker: container runtime. Kubernetes: orchestrates containers across clusters at scale."
    },

    # DOMAIN 5 — HARDWARE AND NETWORK TROUBLESHOOTING
    {
        "domain": "Domain 5 – Hardware and Network Troubleshooting",
        "topic": "Troubleshooting Methodology", "difficulty": "easy",
        "question": "According to CompTIA's A+ troubleshooting methodology, what is the SECOND step after identifying a problem?",
        "choices": {"A":"Implement the solution immediately","B":"Establish a theory of probable cause","C":"Document findings and outcomes","D":"Escalate to a senior technician"},
        "answer": "B",
        "explanation": "CompTIA A+ six-step troubleshooting process: 1. Identify the problem — question the user, observe symptoms, review recent changes, duplicate the issue. 2. Establish a theory of probable cause — consider the most likely explanations first (Occam's Razor). 3. Test the theory — if confirmed, proceed; if not, re-establish a new theory or escalate. 4. Establish a plan of action and implement the solution. 5. Verify full system functionality and implement preventive measures. 6. Document findings, actions, and outcomes. This prevents the common mistake of randomly swapping parts. 'What changed recently?' is your most powerful question — most problems follow a recent change to hardware, software, configuration, or environment."
    },
    {
        "domain": "Domain 5 – Hardware and Network Troubleshooting",
        "topic": "HDD Failure", "difficulty": "easy",
        "question": "A desktop PC is making a repetitive clicking noise from inside. The user is in the middle of a project. What should the technician do FIRST?",
        "choices": {"A":"Run a defragmentation utility to fix the issue","B":"Immediately back up all critical data — the hard drive is failing","C":"Reformat and reinstall Windows","D":"Replace the CPU cooling fan"},
        "answer": "B",
        "explanation": "The 'click of death' — a rhythmic clicking from a mechanical HDD — means the read/write heads are failing to find their home position and resetting. This indicates imminent and total physical failure that can happen within minutes. DATA PRESERVATION is the only priority. Copy all critical files to another drive or cloud storage immediately. Every additional read/write operation on a failing drive risks accelerating the failure and making data permanently unrecoverable. After securing data: replace the drive (ideally with an SSD), reinstall Windows, restore data from backup. A defrag writes heavily to the drive — extremely dangerous on a clicking drive. SSDs fail differently — SMART warnings usually precede failure. Always monitor SMART health data proactively."
    },
    {
        "domain": "Domain 5 – Hardware and Network Troubleshooting",
        "topic": "POST Beep Codes", "difficulty": "medium",
        "question": "A newly assembled PC powers on but emits a repeating single long beep and shows no video output. What does this beep pattern MOST likely indicate?",
        "choices": {"A":"Successful POST — the system is ready","B":"RAM not seated correctly or incompatible memory","C":"Hard drive not detected","D":"GPU driver needs updating"},
        "answer": "B",
        "explanation": "A continuous or repeating long beep at POST almost universally indicates a memory (RAM) error on AMI and Award BIOS systems. With no video and this beep pattern: 1. Power off completely. 2. Reseat RAM modules firmly — press until both retention clips snap. 3. Try one stick at a time in different slots. 4. Clear CMOS (jumper or remove battery for 30 seconds) to reset BIOS settings. 5. Test with known-good RAM. Beep code meanings vary by BIOS manufacturer — always check the motherboard manual. No beeps + no power = PSU or motherboard. No beeps + has power but no video = possible GPU issue. Multiple short beeps (3–5) = often GPU issues on certain BIOS implementations."
    },
    {
        "domain": "Domain 5 – Hardware and Network Troubleshooting",
        "topic": "Printer Troubleshooting", "difficulty": "medium",
        "question": "A laser printer produces pages with a faint repeated image appearing at regular intervals across the entire page — like a ghost of the previous print. Which component is MOST likely causing this?",
        "choices": {"A":"Fuser assembly","B":"Imaging drum","C":"Toner cartridge level","D":"Transfer corona wire"},
        "answer": "B",
        "explanation": "Ghosting — a faint repeated 'shadow' of previous content appearing at regular intervals matching the drum's circumference — is caused by a worn or damaged imaging drum that is not cleaning properly between rotations. Residual toner or charge from the previous cycle creates a faint impression on subsequent pages. The drum is the photosensitive cylinder that holds the electrostatic image before toner transfer. In many modern printers, the drum is integrated into the toner cartridge assembly — replacing the cartridge resolves both. Fuser issues: toner smears when touched (not bonded). Transfer corona issues: blank or very faint pages (toner not transferred). Toner cartridge depletion: gradually fading output, not repetitive ghost marks."
    },
    {
        "domain": "Domain 5 – Hardware and Network Troubleshooting",
        "topic": "APIPA / IP Troubleshooting", "difficulty": "medium",
        "question": "A laptop is connected to the network via Ethernet but shows IP address 169.254.88.15. Other devices on the same switch work fine. What does this IP indicate and what should be checked first?",
        "choices": {"A":"The laptop has a static IP correctly set in this range","B":"DHCP failed — the OS self-assigned an APIPA address. Check the DHCP lease and network connection","C":"The laptop is connected to a secondary VLAN","D":"The IP indicates the laptop is using IPv6"},
        "answer": "B",
        "explanation": "169.254.0.0/16 is the APIPA (Automatic Private IP Addressing) range — Windows self-assigns an address here when it cannot reach a DHCP server within 60 seconds. APIPA hosts can only communicate with other APIPA devices on the same segment — no gateway, no internet, no domain resources. Since other devices work, the network itself is fine. The problem is specific to this laptop. Troubleshooting steps: 1. Check physical connection — is the link light on? 2. ipconfig /release then ipconfig /renew. 3. Check if the laptop's NIC has a manual/static configuration overriding DHCP. 4. Check if the DHCP scope has available addresses. 5. Try a different cable or switch port. 6. Check if a firewall on the laptop is blocking DHCP."
    },
    {
        "domain": "Domain 5 – Hardware and Network Troubleshooting",
        "topic": "Wireless Troubleshooting", "difficulty": "medium",
        "question": "Users report slow Wi-Fi speeds during business hours but excellent speeds on evenings and weekends. AP signal strength is strong. What is the MOST likely cause?",
        "choices": {"A":"The AP firmware is outdated","B":"Channel congestion from too many simultaneous users or neighboring APs on the same channel","C":"The Ethernet uplink cable to the AP is faulty","D":"DHCP scope exhaustion"},
        "answer": "B",
        "explanation": "The time-of-day pattern (slow during business hours when all users are present, fast when the office is empty) is the classic signature of channel congestion — too many devices competing for airtime on the same Wi-Fi channel. Solutions: Use a Wi-Fi analyzer (NetSpot, inSSIDer) to find the least congested channel. On 2.4 GHz use only channels 1, 6, or 11 (non-overlapping). Migrate heavy users to 5 GHz (more channels, less interference, shorter range). Enable band steering to automatically push 5 GHz-capable devices to 5 GHz. Deploy additional APs to reduce clients per AP. Wi-Fi 6 (802.11ax) with OFDMA dramatically improves performance in dense environments. Strong signal + slow speed = congestion problem, NOT a coverage problem."
    },
    {
        "domain": "Domain 5 – Hardware and Network Troubleshooting",
        "topic": "Inkjet Troubleshooting", "difficulty": "medium",
        "question": "An inkjet printer outputs pages with horizontal white lines and streaks through text and images. What is the MOST likely cause and first corrective action?",
        "choices": {"A":"Replace the fuser assembly","B":"Run the printhead nozzle cleaning utility to clear clogged ink nozzles","C":"Replace all ink cartridges immediately","D":"Adjust the paper thickness setting"},
        "answer": "B",
        "explanation": "Horizontal streaks (missing bands of color or white lines through output) in inkjet printing are the classic symptom of clogged print nozzles. Ink dries in the tiny nozzle openings when the printer sits unused. First action: run the built-in printhead cleaning utility (found in printer software under Maintenance, or on the printer control panel). Then print a nozzle check pattern to verify improvement. Multiple cleaning cycles may be needed for severe clogs. Only replace cartridges if ink levels are confirmed low — a nozzle check pattern helps identify which color is clogged. Prevention: print at least one page per week to keep nozzles from drying. Persistent clogs after multiple cleaning cycles may require manual head cleaning or printhead replacement."
    },
    {
        "domain": "Domain 5 – Hardware and Network Troubleshooting",
        "topic": "RAID Troubleshooting", "difficulty": "hard",
        "question": "A server running RAID 5 across four drives reports one drive failure. The array is still accessible. What is the CORRECT immediate action?",
        "choices": {"A":"Shut the server down immediately to prevent data loss","B":"The data is already lost — restore from backup","C":"Replace the failed drive as soon as possible to restore parity and redundancy before a second drive fails","D":"Convert the remaining three drives to RAID 0 for better performance"},
        "answer": "C",
        "explanation": "RAID 5 can survive exactly ONE drive failure — it continues operating in a degraded state, reconstructing data on the fly using parity. However in this state there is ZERO remaining redundancy — a second drive failure means complete data loss. The critical window between the first and second failure is dangerous: degraded array I/O stresses remaining drives, and rebuild reads stress them further (URE risk). Immediate actions: replace the failed drive immediately (use a hot spare if available for auto-rebuild). Monitor rebuild progress — it can take hours on large drives. Avoid heavy I/O workloads during rebuild. After rebuild completes: verify data integrity and consider upgrading to RAID 6 (survives 2 failures) for improved resilience. RAID is NOT a backup — always maintain separate backups."
    },
]

# ══════════════════════════════════════════════════════════════════════════════
#  A+ CORE 1 (220-1201) GLOSSARY
# ══════════════════════════════════════════════════════════════════════════════

GLOSSARY_APLUS1 = {
    "802.11be": "Wi-Fi 7 — Multi-Link Operation (MLO); 2.4/5/6 GHz simultaneous; 46 Gbps theoretical.",
    "802.11ax": "Wi-Fi 6 — OFDMA, MU-MIMO; 2.4/5 GHz; 9.6 Gbps. Wi-Fi 6E adds 6 GHz band.",
    "802.3af (PoE)": "PoE standard — 15.4W per port. Powers VoIP phones and basic APs.",
    "802.3at (PoE+)": "PoE+ — 30W per port. Powers most IP cameras and mid-range access points.",
    "802.3bt (PoE++)": "PoE++ — Type 3=60W, Type 4=100W. Powers video conferencing and LED panels.",
    "APIPA": "Automatic Private IP Addressing — 169.254.x.x self-assigned when DHCP fails.",
    "ATX": "Standard desktop motherboard/PSU form factor. 24-pin main, 8-pin EPS CPU power.",
    "BGA": "Ball Grid Array — CPU soldered to motherboard. Not upgradeable. Common in mobile.",
    "Bluetooth 5.x": "Wireless PAN at 2.4 GHz. Up to 400 m (Class 1). Used for peripherals, audio, IoT.",
    "Cat6a": "Ethernet cable — 10 Gbps at full 100 m. Current standard for new commercial installations.",
    "Cat8": "Ethernet cable — 25/40 Gbps at up to 30 m. Data center use only.",
    "CMOS": "Stores BIOS/UEFI settings. Powered by CR2032 coin battery. Remove battery to clear/reset.",
    "DDR5": "Current desktop/laptop RAM standard. 1.1V, on-die ECC, higher bandwidth than DDR4.",
    "DHCP": "Dynamic Host Configuration Protocol — auto-assigns IP, mask, gateway, DNS. Ports 67/68.",
    "Digitizer": "Transparent capacitive touch-sensing layer — separate from the display panel itself.",
    "DisplayPort 2.1": "Digital video/audio connector — up to 16K resolution; used on high-end PC monitors.",
    "Docker": "Leading container runtime platform; packages apps with dependencies, shares host OS kernel.",
    "DNS": "Domain Name System — resolves hostnames to IP addresses. Port 53 (TCP/UDP).",
    "FDM": "Fused Deposition Modeling — most common consumer 3D printing; melts plastic filament.",
    "GPU": "Graphics Processing Unit — handles rendering; needs PCIe x16 slot; discrete or integrated.",
    "HDMI 2.1": "Video+audio connector — 4K@120Hz, 8K, VRR, eARC. Standard for TVs and monitors.",
    "Hypervisor Type 1": "Bare-metal — runs on hardware (ESXi, Hyper-V, KVM). Enterprise/production use.",
    "Hypervisor Type 2": "Hosted — runs on OS (VirtualBox, VMware Workstation). Development/lab use.",
    "IaaS": "Infrastructure as a Service — cloud provides virtualized compute, storage, networking.",
    "IPS panel": "In-Plane Switching LCD — 178° viewing angles, accurate color. Standard for productivity.",
    "Kubernetes": "Container orchestration — manages Docker containers at scale across server clusters.",
    "LC connector": "Small-form-factor fiber optic connector — standard in data centers and SFP modules.",
    "LGA": "Land Grid Array — pins on motherboard socket. Used by Intel and AMD AM5.",
    "Lightning": "Apple proprietary connector — older iPhones/iPads. Replaced by USB-C (iPhone 15+).",
    "LPDDR5X": "Low-Power DDR5X — soldered mobile RAM in ultrabooks and phones. Not upgradeable.",
    "M.2": "Small expansion slot supporting NVMe SSDs and Wi-Fi cards. Supports SATA or NVMe.",
    "MDM": "Mobile Device Management — centrally manages devices; enforces policies; enables remote wipe.",
    "mmWave 5G": "5G at 24–100 GHz — multi-Gbps speeds, very short range, poor building penetration.",
    "NFC": "Near Field Communication — 13.56 MHz, under 4 cm range. Tap payments and device pairing.",
    "NVMe Gen 3": "PCIe 3.0 x4 — ~3,500 MB/s sequential read. Common in current mid-range SSDs.",
    "NVMe Gen 4": "PCIe 4.0 x4 — ~7,000 MB/s sequential read. Current high-performance standard.",
    "NVMe Gen 5": "PCIe 5.0 x4 — ~14,000 MB/s sequential read. Latest, highest-performance SSDs.",
    "OLED": "Organic LED — self-emitting pixels, true blacks, infinite contrast. Premium phones/monitors.",
    "ONT": "Optical Network Terminal — converts fiber to Ethernet at customer premises.",
    "PaaS": "Platform as a Service — cloud manages OS/runtime; customer manages app and data.",
    "PCIe 5.0": "Latest PCI Express generation. Doubles PCIe 4.0 bandwidth. Supports NVMe Gen 5 and GPUs.",
    "PGA": "Pin Grid Array — pins on the CPU. AMD AM4 (Ryzen 1000–5000). Bent pins more repairable.",
    "PoE injector": "Adds PoE power to a single non-PoE switch port for one powered device.",
    "POST": "Power-On Self Test — BIOS/UEFI hardware diagnostic at startup. Beep codes signal failures.",
    "PSU": "Power Supply Unit — converts AC to DC (+12V, +5V, +3.3V) for PC components.",
    "RAID 5": "Striping with parity — 3+ drives, survives 1 failure. Balanced speed and redundancy.",
    "RAID 6": "Double parity — 4+ drives, survives 2 simultaneous failures.",
    "RAID 10": "Mirrored stripes — 4+ drives, highest performance with redundancy.",
    "SaaS": "Software as a Service — fully managed cloud application. User manages data only.",
    "SATA III": "Serial ATA storage interface — 600 MB/s max. Used by HDDs and SATA SSDs.",
    "SC connector": "Square push-pull fiber optic connector — older installations and single-mode fiber.",
    "SLA (printing)": "Stereolithography — UV laser cures resin; high detail, smooth surfaces. Dental/jewelry.",
    "SLS": "Selective Laser Sintering — industrial 3D printing fusing powder; strong functional parts.",
    "SMART": "Self-Monitoring Analysis and Reporting Technology — drive health monitoring. Check proactively.",
    "SO-DIMM": "Small Outline DIMM — laptop RAM. DDR4=260-pin, DDR5=262-pin.",
    "ST connector": "Bayonet twist-lock fiber connector — older campus and industrial installations.",
    "TN panel": "Twisted Nematic LCD — fastest response (1ms), gaming use, poor viewing angles.",
    "Thunderbolt 4": "Intel interface on USB-C connector — 40 Gbps, 2x4K displays, PCIe, USB3.",
    "USB-C": "Reversible universal connector — USB 3.2, Thunderbolt, DisplayPort Alt Mode, PD charging.",
    "VA panel": "Vertical Alignment LCD — best contrast of LCD types; sits between IPS and TN.",
    "VDI": "Virtual Desktop Infrastructure — cloud-hosted desktops accessed from thin clients.",
    "Wi-Fi 6E": "802.11ax with added 6 GHz band — less congestion, faster in dense environments.",
    "Wi-Fi 7": "802.11be — MLO uses multiple bands simultaneously; up to 46 Gbps theoretical.",
}


# ══════════════════════════════════════════════════════════════════════════════
#  A+ CORE 2 (220-1202) — DOMAIN THEME, WEIGHTS & OBJECTIVES
# ══════════════════════════════════════════════════════════════════════════════

DOMAIN_THEME_APLUS2 = {
    "Domain 1": {"color": C.RED,   "icon": "🖥️",  "short": "D1", "bg": C.BG_RED},
    "Domain 2": {"color": C.ORG,   "icon": "🔒",  "short": "D2", "bg": C.BG_ORG},
    "Domain 3": {"color": C.LIME,  "icon": "🛠️",  "short": "D3", "bg": C.BG_GRN},
    "Domain 4": {"color": C.PRP,   "icon": "📋",  "short": "D4", "bg": C.BG_MAG},
}

DOMAIN_WEIGHTS_APLUS2 = {
    "Domain 1 – Operating Systems": 27,
    "Domain 2 – Security": 24,
    "Domain 3 – Software Troubleshooting": 26,
    "Domain 4 – Operational Procedures": 23,
}

DOM_ORDER_APLUS2 = [
    "Domain 1 – Operating Systems",
    "Domain 2 – Security",
    "Domain 3 – Software Troubleshooting",
    "Domain 4 – Operational Procedures",
]

EXAM_OBJECTIVES_APLUS2 = {
    "Domain 1 – Operating Systems": {
        "weight": 27,
        "objectives": [
            "Identify Windows editions (Home, Pro, Enterprise, Education) and choose the correct edition per scenario.",
            "Use Windows admin tools: Task Manager, Event Viewer, Device Manager, regedit, msconfig, secpol.msc.",
            "Use CLI tools: ipconfig, ping, tracert, netstat, nslookup, net use, gpupdate, gpresult, sfc, DISM.",
            "Configure Windows networking: workgroup vs domain, network discovery, VPN client, Remote Desktop.",
            "Identify macOS features: Spotlight, Mission Control, Keychain, FileVault, Time Machine, Homebrew.",
            "Use Linux basics: ls, cd, pwd, cp, mv, rm, chmod, chown, apt/yum/dnf, grep, ps, sudo, systemctl.",
            "Perform OS installs: clean install, upgrade, image deployment, PXE boot, unattended setup.",
        ],
        "study": [
            "Windows Home missing: domain join, BitLocker, Group Policy editor, Hyper-V, RDP host, AppLocker.",
            "Event Viewer logs: Application (app errors), System (OS/driver errors), Security (logon/audit events).",
            "Run DISM /Cleanup-Image /RestoreHealth BEFORE sfc /scannow when system files are severely corrupted.",
            "gpupdate /force = apply Group Policy now. gpresult /r = show what policies are applied.",
            "Linux chmod 755 = rwxr-xr-x. chmod 644 = rw-r--r--. chmod 777 = rwxrwxrwx (avoid on sensitive files).",
        ],
    },
    "Domain 2 – Security": {
        "weight": 24,
        "objectives": [
            "Summarize security measures: physical security, data destruction, account policies, password managers.",
            "Configure Windows security: UAC, BitLocker, EFS, Windows Defender, software firewall, user accounts.",
            "Detect and remove malware using CompTIA's 7-step removal process.",
            "Explain social engineering: phishing, vishing, smishing, whaling, tailgating, shoulder surfing, dumpster diving.",
            "Implement workstation security: least privilege, account lockout, MFA, screen lock, encryption.",
            "Explain data destruction: shredding, degaussing, incineration, overwriting, cryptographic erase.",
        ],
        "study": [
            "7-step malware removal: Investigate → Quarantine (disconnect network) → Disable System Restore → Remediate → Schedule/Update → Re-enable System Restore → Educate user.",
            "Degaussing works on HDDs (magnetic) only — has ZERO effect on SSDs or flash storage.",
            "MFA factors: know (password/PIN), have (token/phone/smartcard), are (biometric), where (location/geofence).",
            "Shoulder surfing = watching screen/keyboard. Defense = privacy filter, screen positioning.",
            "BitLocker = Windows Pro+, full disk. EFS = per-file, tied to user certificate — losing cert loses data.",
        ],
    },
    "Domain 3 – Software Troubleshooting": {
        "weight": 26,
        "objectives": [
            "Troubleshoot Windows: BSOD stop codes, slow performance, boot failures, app crashes, profile corruption.",
            "Troubleshoot security issues: malware symptoms, browser hijacking, pop-ups, ransom messages.",
            "Apply CompTIA's 7-step malware removal process.",
            "Troubleshoot mobile OS: app crashes, battery drain, overheating, slow performance, connectivity.",
            "Troubleshoot mobile security: fake apps, unauthorized access, leaked data, failed OS updates.",
        ],
        "study": [
            "BSOD codes: 0x7B=Inaccessible Boot Device, 0x50=Page Fault (RAM), 0xA=IRQL (driver), 0xEF=Critical Process Died.",
            "100% disk usage: Windows Update, failing HDD (check SMART), Search Indexing, Superfetch, malware.",
            "Browser hijacking: changed homepage, new extensions, redirects. Fix: remove extensions, reset browser, scan.",
            "Mobile battery drain: background apps, always-on location, weak signal, aging battery (swollen = replace now).",
            "Performance tools: Task Manager (real-time) → Resource Monitor (detailed) → Performance Monitor (historical).",
        ],
    },
    "Domain 4 – Operational Procedures": {
        "weight": 23,
        "objectives": [
            "Implement documentation: network diagrams, knowledge base, ticketing, asset inventory, SOPs.",
            "Apply change management: request, impact analysis, approval, rollback plan, implementation, documentation.",
            "Implement backup strategies: 3-2-1 rule, full/incremental/differential, cloud backup, restore testing.",
            "Apply safety: ESD prevention, lifting techniques, fire suppression, electrical safety, MSDS/SDS.",
            "Explain environmental controls: temperature, humidity, UPS, surge protectors, cable management.",
            "Apply scripting: batch (.bat), PowerShell (.ps1), shell scripts (.sh), Python basics, automation use cases.",
            "Configure remote access: RDP (3389), VNC (5900), SSH (22), Remote Assistance, VPN.",
        ],
        "study": [
            "3-2-1 rule: 3 copies, 2 media types, 1 offsite. Full=fastest restore. Incremental=smallest backup. Differential=balance.",
            "PowerShell cmdlets: Get-Process, New-ADUser, Set-Item, Invoke-Command — manages Windows, AD, Azure.",
            "UPS types: Online (always on battery, best) vs Line-interactive (switches on power drop) vs Standby (slowest).",
            "Class C extinguisher for electrical fires. Clean agent (FM-200, Novec 1230) for server rooms — no residue.",
            "Change management: request → risk/impact analysis → CAB approval → rollback plan → implement → verify → document.",
        ],
    },
}

QUESTIONS_APLUS2 = [

    # DOMAIN 1 — OPERATING SYSTEMS
    {
        "domain": "Domain 1 – Operating Systems",
        "topic": "Windows Editions", "difficulty": "easy",
        "question": "A small business needs Windows 11 workstations that can join an Active Directory domain and use BitLocker encryption. What is the MINIMUM required edition?",
        "choices": {"A":"Windows 11 Home","B":"Windows 11 Pro","C":"Windows 11 S Mode","D":"Windows 11 IoT"},
        "answer": "B",
        "explanation": "Windows 11 Pro includes: Active Directory domain join, BitLocker full-disk encryption, Group Policy editor (gpedit.msc), Hyper-V, Remote Desktop host, Windows Sandbox. Windows 11 Home lacks ALL enterprise features — no domain join, no BitLocker, no Group Policy. Windows 11 Enterprise adds AppLocker, advanced Defender features, BranchCache — requires volume licensing. Windows 11 Education: similar to Enterprise for academic institutions. S Mode: restricted to Microsoft Store apps only. For any exam question involving domain join OR BitLocker, the answer is Pro or higher. Pro for Workstations adds NVMe/RAID optimizations and higher RAM limits."
    },
    {
        "domain": "Domain 1 – Operating Systems",
        "topic": "Windows Commands", "difficulty": "easy",
        "question": "Which ipconfig flag displays the full IP configuration including MAC address, DHCP server address, and lease expiration time?",
        "choices": {"A":"ipconfig /release","B":"ipconfig /all","C":"ipconfig /flushdns","D":"ipconfig /renew"},
        "answer": "B",
        "explanation": "ipconfig /all: full network details — IP address, subnet mask, default gateway, DNS servers, Physical Address (MAC), DHCP enabled status, DHCP server IP, lease obtained/expires. ipconfig (no flag): shows IP, mask, gateway only — no MAC, no DHCP details. ipconfig /release: releases current DHCP lease (IP goes away). ipconfig /renew: requests a new DHCP lease. ipconfig /flushdns: clears the local DNS resolver cache — fixes stale DNS entries causing wrong-site redirects. ipconfig /registerdns: re-registers the computer's hostname with DNS. For troubleshooting, /all gives the most diagnostic information in a single command."
    },
    {
        "domain": "Domain 1 – Operating Systems",
        "topic": "NTFS Permissions", "difficulty": "medium",
        "question": "User Alice is in Group A (Read) and Group B (Modify) for a folder. Group C has Deny Write for the same folder, and Alice is also in Group C. What are Alice's effective permissions?",
        "choices": {"A":"Modify — most permissive wins","B":"Read only — Deny Write blocks the Write part of Modify","C":"Full Control — multiple groups grant everything","D":"No Access — any Deny overrides all permissions"},
        "answer": "B",
        "explanation": "NTFS effective permissions = UNION of all Allow permissions MINUS any explicit Deny. Alice gets: Read (from Group A) + Modify (from Group B) — combined = Modify. But Deny Write (from Group C) removes the Write component of Modify. Result: Alice can read and execute but cannot write or delete. Deny removes a specific right, not all access. Only an explicit Deny Full Control or Deny Read would block all access. Key rules: 1. Allow permissions from multiple groups are combined (most permissive). 2. Explicit Deny overrides Allow for that specific permission. 3. Deny Full Control = no access regardless of other groups."
    },
    {
        "domain": "Domain 1 – Operating Systems",
        "topic": "Windows Registry", "difficulty": "medium",
        "question": "A technician needs to edit a setting that affects only the currently logged-in user's environment, not other users on the same machine. Which registry hive should be modified?",
        "choices": {"A":"HKEY_LOCAL_MACHINE (HKLM)","B":"HKEY_CURRENT_USER (HKCU)","C":"HKEY_CLASSES_ROOT (HKCR)","D":"HKEY_CURRENT_CONFIG (HKCC)"},
        "answer": "B",
        "explanation": "HKEY_CURRENT_USER (HKCU): stores settings for the currently logged-in user — desktop wallpaper, user-specific app settings, printer preferences, personal environment variables. Changes here only affect the current user's profile. HKEY_LOCAL_MACHINE (HKLM): machine-wide settings affecting ALL users — hardware, installed software, system-wide policies. HKEY_CLASSES_ROOT (HKCR): file extension associations and COM registration — a merged view of HKLM\\Software\\Classes and HKCU\\Software\\Classes. HKEY_CURRENT_CONFIG (HKCC): current hardware profile info. Registry editor: regedit.exe. ALWAYS export (back up) a key before editing — File → Export — a bad registry edit can prevent Windows from booting."
    },
    {
        "domain": "Domain 1 – Operating Systems",
        "topic": "System File Repair", "difficulty": "medium",
        "question": "A Windows 11 PC has widespread system instability. sfc /scannow reports it cannot repair some files. What should be run FIRST before trying sfc again?",
        "choices": {"A":"chkdsk /r","B":"DISM /Online /Cleanup-Image /RestoreHealth","C":"format C: /fs:ntfs","D":"diskpart"},
        "answer": "B",
        "explanation": "When sfc /scannow fails to repair files, it means the Windows Component Store (the source files sfc uses for replacement) is itself corrupted. DISM (Deployment Image Servicing and Management) repairs the component store by downloading fresh files from Windows Update or a mounted image. Command: DISM /Online /Cleanup-Image /RestoreHealth. After DISM completes successfully, run sfc /scannow again — it can now use the repaired component store. Sequence: DISM first → sfc second. chkdsk /r: scans and repairs disk errors and bad sectors — separate from OS file corruption and unrelated to sfc failures. diskpart: partition management tool — not used for OS file repair."
    },
    {
        "domain": "Domain 1 – Operating Systems",
        "topic": "GPT vs MBR", "difficulty": "medium",
        "question": "A technician installs a new 6TB hard drive. After initializing in Disk Management with MBR style, only 2TB appears as usable space. How should this be fixed?",
        "choices": {"A":"Format with FAT32 to access the full 6TB","B":"Convert the disk to GPT partition style to support drives over 2TB","C":"Split the drive into three 2TB volumes","D":"Update the BIOS — MBR will then support 6TB"},
        "answer": "B",
        "explanation": "MBR (Master Boot Record) uses 32-bit LBA addressing and has a hard ceiling of 2TB. Any space beyond 2TB on an MBR disk is completely inaccessible and cannot be partitioned. Solution: convert to GPT (GUID Partition Table), which supports disks up to 9.4 ZB and up to 128 partitions on Windows. If the disk is empty: right-click in Disk Management → Convert to GPT Disk. If the disk has data: use MBR2GPT.exe (converts without data loss, requires Windows 10 1703+). GPT also requires UEFI firmware for bootable system drives. For any drive over 2TB — the answer is always GPT. FAT32 has a 2TB volume limit and a 4GB per-file limit — not a solution."
    },
    {
        "domain": "Domain 1 – Operating Systems",
        "topic": "Windows Admin Tools", "difficulty": "easy",
        "question": "A technician suspects a recently installed device driver is causing system instability. Which Windows tool lets them view installed drivers, check device status, and roll back a driver?",
        "choices": {"A":"Event Viewer","B":"Device Manager","C":"Disk Management","D":"Services.msc"},
        "answer": "B",
        "explanation": "Device Manager (devmgmt.msc) is the go-to tool for hardware and driver management: view all detected hardware, see yellow exclamation marks for problematic devices, update drivers, roll back to a previous driver version, disable/enable devices, and uninstall devices. Driver rollback (Device Properties → Driver tab → Roll Back Driver) restores the previous driver — extremely useful when a new driver causes instability. Event Viewer: shows Windows system, application, and security logs — great for identifying WHAT went wrong (error messages, stop codes) but not for managing drivers. Disk Management: manages partitions and volumes. Services.msc: manages Windows services (start, stop, disable)."
    },
    {
        "domain": "Domain 1 – Operating Systems",
        "topic": "macOS Features", "difficulty": "easy",
        "question": "A macOS user needs to search for a file, launch an app, or perform a quick calculation without opening any application. Which macOS feature provides this?",
        "choices": {"A":"Mission Control","B":"Spotlight","C":"FileVault","D":"Keychain Access"},
        "answer": "B",
        "explanation": "macOS features tested on 220-1202: Spotlight (Cmd+Space): universal instant search — apps, files, emails, calendar, web results, unit conversions, math. Mission Control (Ctrl+Up arrow or 3-finger swipe up): shows all open windows, Spaces (virtual desktops), and full-screen apps — for window management. FileVault: macOS full-disk encryption using AES-128 — equivalent to Windows BitLocker. Requires recovery key backup. Time Machine: automated backup to external drive or network location — keeps hourly/daily/weekly snapshots. Keychain: macOS password/credential manager — stores Wi-Fi passwords, website logins, app credentials. Homebrew: community package manager for macOS — installs Unix/developer tools via command line."
    },
    {
        "domain": "Domain 1 – Operating Systems",
        "topic": "Linux Commands", "difficulty": "medium",
        "question": "A Linux administrator runs 'chmod 644 report.txt'. What permissions does this set on the file?",
        "choices": {"A":"rwxrwxrwx — everyone has full access","B":"rw-r--r-- — owner can read/write; group and others can read only","C":"rwxr-xr-x — owner full; group/others read and execute","D":"rw-rw-rw- — everyone can read and write"},
        "answer": "B",
        "explanation": "Linux permissions use octal notation: 4=read(r), 2=write(w), 1=execute(x). Three groups: owner, group, others. 644: 6(rw-)=owner read+write, 4(r--)=group read only, 4(r--)=others read only. Common permission values: 755 = rwxr-xr-x: standard for directories and executable scripts (owner full, others read+execute). 644 = rw-r--r--: standard for text/config files (owner read+write, others read only). 700 = rwx------: private to owner only. 777 = rwxrwxrwx: everyone full access — avoid on sensitive files/dirs. chmod command: chmod [octal] [file]. chown changes file ownership: chown user:group file. View permissions: ls -la shows the permission string in front of each file."
    },

    # DOMAIN 2 — SECURITY
    {
        "domain": "Domain 2 – Security",
        "topic": "Malware Removal Steps", "difficulty": "medium",
        "question": "According to CompTIA's malware removal process, what is the SECOND step after identifying a malware infection?",
        "choices": {"A":"Run a full antivirus scan with updated definitions","B":"Quarantine the infected system by disconnecting it from the network","C":"Format and reinstall the operating system","D":"Change all user passwords from the infected machine"},
        "answer": "B",
        "explanation": "CompTIA 7-step malware removal process: 1. Investigate and verify malware symptoms. 2. QUARANTINE — isolate the system (disconnect network cable, disable Wi-Fi) to prevent lateral spread to other devices and cut the malware's connection to command-and-control servers. 3. Disable System Restore — malware can hide copies in restore points. 4. Remediate — boot to Safe Mode, update anti-malware definitions, run full scan, remove infections. 5. Schedule scans and run OS/software updates. 6. Re-enable System Restore and create a clean restore point. 7. Educate the user about how the infection occurred. Never change passwords from the infected machine — a keylogger may capture the new credentials."
    },
    {
        "domain": "Domain 2 – Security",
        "topic": "Data Destruction", "difficulty": "medium",
        "question": "A company is disposing of old SSDs containing sensitive customer data. A technician suggests degaussing the drives. Why is this approach INCORRECT for SSDs?",
        "choices": {"A":"Degaussing is too expensive for SSDs","B":"SSDs use NAND flash memory, not magnetic platters — degaussing has no effect on flash storage","C":"Degaussing only works on USB drives, not M.2 SSDs","D":"Degaussing requires the drive to be powered on"},
        "answer": "B",
        "explanation": "Degaussing works by applying an intense magnetic field to erase magnetically stored data — it is effective ONLY on magnetic media (HDDs, magnetic tape, floppy disks). SSDs store data in NAND flash memory chips using electrical charge — magnetic fields have absolutely no effect on them. For SSDs: Cryptographic erase — if the SSD uses self-encryption (SED/TCG Opal), destroying the encryption key makes all data mathematically unrecoverable. ATA Secure Erase — manufacturer-level command that resets all NAND cells. Physical destruction — shredding, disintegration, incineration — most absolute method. For HDDs: degaussing, overwriting (DoD 5220.22-M), or physical destruction. For compliance (HIPAA, PCI DSS, GDPR): obtain a certificate of destruction."
    },
    {
        "domain": "Domain 2 – Security",
        "topic": "Social Engineering", "difficulty": "easy",
        "question": "An attacker calls an employee pretending to be from the corporate help desk, claims the employee's account was compromised, and urgently requests their current password to 'fix it.' This is BEST described as:",
        "choices": {"A":"Phishing","B":"Vishing","C":"Smishing","D":"Dumpster diving"},
        "answer": "B",
        "explanation": "Vishing (Voice phishing): social engineering attacks conducted via telephone or voice calls. The attacker impersonates a trusted authority (IT help desk, bank, IRS, tech support) to create urgency and manipulate the victim. Defense: IT departments have a policy of NEVER asking for passwords over the phone — train users to know this. Call-back verification: hang up and call the help desk's official number. Phishing: email-based. Smishing: SMS/text-based. Spear phishing: targeted phishing at a specific individual. Whaling: phishing targeting executives. Dumpster diving: physically searching trash for sensitive information. Pretexting: creating a fabricated scenario/identity to gain trust — vishing is a form of pretexting."
    },
    {
        "domain": "Domain 2 – Security",
        "topic": "BitLocker vs EFS", "difficulty": "medium",
        "question": "A manager's laptop is stolen. The hard drive contains sensitive files encrypted with EFS. What risk does EFS encryption NOT fully protect against?",
        "choices": {"A":"Someone reading files by booting a different OS from USB and accessing the drive","B":"Unauthorized access to the files while the user is logged in and their EFS certificate is loaded","C":"A thief removing the hard drive and reading it in another computer","D":"Remote wiping the device via MDM"},
        "answer": "A",
        "explanation": "EFS (Encrypting File System) encrypts individual files and ties decryption to the user's Windows certificate/private key. If a thief removes the drive and mounts it in another Windows PC, the EFS-encrypted files appear as locked — they cannot be read without the certificate. However: if a thief boots the original laptop from a Linux USB drive, they can mount the Windows partition — EFS-encrypted files will appear as encrypted gibberish (still protected). BUT: EFS does NOT protect the entire OS or unencrypted files. BitLocker encrypts the ENTIRE drive — even booting from USB shows only encrypted data. Best practice: BitLocker protects the entire drive; EFS is for specific sensitive files within an already-running OS. For a stolen laptop, BitLocker is the correct full protection."
    },
    {
        "domain": "Domain 2 – Security",
        "topic": "Account Lockout Policy", "difficulty": "easy",
        "question": "A security policy locks user accounts after 5 failed login attempts and requires an administrator to manually unlock them. What attack does this PRIMARILY prevent?",
        "choices": {"A":"Phishing attacks","B":"Brute force and password spray attacks","C":"Physical tailgating","D":"SQL injection"},
        "answer": "B",
        "explanation": "Account lockout policy prevents brute force attacks (trying many password combinations rapidly against one account) and password spray attacks (trying a few common passwords against many accounts). By locking after 5 failures, automated tools cannot systematically try thousands of passwords. Account lockout settings (Local Security Policy / Group Policy): Lockout threshold: number of bad attempts before lockout (5 is a common setting). Lockout duration: how long the account stays locked (0 = admin must unlock manually). Observation window: time window for counting failures. Trade-off: too aggressive lockout settings can cause denial-of-service (an attacker intentionally locks everyone out). Balance with reasonable thresholds. Complement with MFA for best protection."
    },
    {
        "domain": "Domain 2 – Security",
        "topic": "Wireless Security", "difficulty": "medium",
        "question": "Which Wi-Fi security protocol should a technician configure for BEST security on a small office wireless network in 2024?",
        "choices": {"A":"WEP — strongest legacy encryption","B":"WPA2-Personal with AES","C":"WPA3-Personal with SAE","D":"Open network — rely on VPN for security"},
        "answer": "C",
        "explanation": "WPA3-Personal uses SAE (Simultaneous Authentication of Equals), which replaces WPA2's vulnerable PSK handshake. SAE provides: resistance to offline dictionary attacks (captured handshakes cannot be cracked offline), forward secrecy (past sessions cannot be decrypted even if the password is later discovered), protection against PMKID attacks. WEP: broken in minutes using free tools — never use. WPA (WPA1): deprecated, TKIP has known vulnerabilities. WPA2-Personal: still acceptable if WPA3 hardware is not available — use AES/CCMP mode, strong password (20+ random characters). WPA3 Transition Mode: supports both WPA2 and WPA3 clients simultaneously during hardware transition. For the 220-1202: WPA3 > WPA2 > WPA1 > WEP."
    },
    {
        "domain": "Domain 2 – Security",
        "topic": "MFA", "difficulty": "easy",
        "question": "A user logs in with a password, then approves a push notification sent to their smartphone. Which MFA factor categories are being used?",
        "choices": {"A":"Two knowledge factors — password and PIN","B":"Something you know (password) and something you have (smartphone)","C":"Something you are and something you know","D":"Three factors — knowledge, possession, and location"},
        "answer": "B",
        "explanation": "Authentication factor categories: Something you KNOW: passwords, PINs, security questions, passphrases. Something you HAVE (possession): smartphone (authenticator app, push notification), hardware security key (YubiKey), smart card, OTP token, backup codes. Something you ARE (biometric/inherence): fingerprint, face scan, iris scan, voice recognition, behavioral biometrics. Somewhere you ARE: GPS location, IP geofencing — supplementary factor. True MFA requires two or more DIFFERENT categories. Password (know) + phone push (have) = two different categories = MFA. Password + PIN = two knowledge factors = NOT true MFA. Password + fingerprint = know + are = MFA. Hardware token (have) + PIN to unlock token (know) = MFA. The 220-1202 exam tests factor category identification."
    },
    {
        "domain": "Domain 2 – Security",
        "topic": "UAC", "difficulty": "easy",
        "question": "When a standard user attempts to install software requiring admin rights on Windows, UAC prompts for administrator credentials. Which security principle does UAC implement?",
        "choices": {"A":"Defense in depth","B":"Least privilege","C":"Separation of duties","D":"Non-repudiation"},
        "answer": "B",
        "explanation": "UAC (User Account Control) enforces least privilege — users and processes run with the minimum privileges needed for everyday tasks. Even administrator accounts run as standard users by default; elevation is only granted when explicitly requested and approved. UAC levels: Always Notify (strictest — prompts for all changes). Notify for app changes (default — prompts when apps make changes, not for Windows settings). Notify without desktop dimming (less secure). Never notify (off — dangerous, malware can escalate without prompts). Disabling UAC removes this protection layer entirely. Least privilege principle: grant users/processes only the access they specifically need — nothing more. This limits blast radius if an account is compromised or malware runs under it."
    },

    # DOMAIN 3 — SOFTWARE TROUBLESHOOTING
    {
        "domain": "Domain 3 – Software Troubleshooting",
        "topic": "BSOD Stop Codes", "difficulty": "medium",
        "question": "A Windows workstation BSODs with stop code 0x0000000A (IRQL_NOT_LESS_OR_EQUAL) after installing a new USB hub driver. What is the MOST likely cause?",
        "choices": {"A":"The hard drive has bad sectors","B":"The new USB driver has a bug causing improper memory access at an incorrect interrupt level","C":"The user profile is corrupted","D":"Windows Update failed to download"},
        "answer": "B",
        "explanation": "IRQL_NOT_LESS_OR_EQUAL (0x0000000A): a process or driver attempted to access a memory address at an IRQL (Interrupt Request Level) that was too high — almost always caused by a buggy, incompatible, or corrupted device driver. The timing (after installing a new USB hub driver) makes the culprit obvious. Fix: roll back the driver (Device Manager → USB Hub → Driver → Roll Back Driver) or uninstall the driver and download the updated version from the manufacturer. Other BSODs to know: 0x7B (INACCESSIBLE_BOOT_DEVICE) = storage controller/BIOS change. 0x50 (PAGE_FAULT_IN_NONPAGED_AREA) = RAM failure. 0xEF (CRITICAL_PROCESS_DIED) = core Windows process crash. BAD_POOL_HEADER = memory corruption."
    },
    {
        "domain": "Domain 3 – Software Troubleshooting",
        "topic": "Windows Performance", "difficulty": "medium",
        "question": "Task Manager shows Windows disk usage at 100% constantly. The machine is a 3-year-old laptop with the original HDD. What should the technician check FIRST?",
        "choices": {"A":"Increase the monitor refresh rate","B":"Check SMART data for HDD health — a failing drive causes constant high disk activity","C":"Update the graphics driver","D":"Reinstall Windows immediately"},
        "answer": "B",
        "explanation": "Persistent 100% disk usage on an older mechanical HDD often indicates drive degradation — bad sectors cause repeated read retries, which show as constant disk activity. Check SMART (Self-Monitoring Analysis and Reporting Technology) data using tools like CrystalDiskInfo (Windows) or smartctl (Linux) — look for Reallocated Sectors, Pending Sectors, or Uncorrectable Errors. Other 100% disk causes: Windows Update running (temporary — wait for completion), Search Indexing (initial setup — temporary), Superfetch/SysMain on low-RAM systems (disable if under 8GB), malware. Resource Monitor (resmon.exe) shows EXACTLY which process is causing disk activity — more detailed than Task Manager. An SSD upgrade dramatically improves performance on old laptops."
    },
    {
        "domain": "Domain 3 – Software Troubleshooting",
        "topic": "Browser Hijacking", "difficulty": "easy",
        "question": "A user reports their browser homepage changed to an unknown site, new toolbars appeared, and searches redirect to unfamiliar engines. What malware type and remediation steps are indicated?",
        "choices": {"A":"Ransomware — restore files from backup","B":"Browser hijacker — remove extensions, reset browser, run anti-malware scan","C":"Rootkit — boot from live CD and reinstall OS","D":"Keylogger — change all passwords immediately"},
        "answer": "B",
        "explanation": "Browser hijackers modify browser settings — homepage, default search engine, new tab page — and install unwanted extensions or toolbars. Often bundled with free software (PUPs — Potentially Unwanted Programs). Remediation: 1. Remove suspicious extensions in browser settings. 2. Reset browser to defaults (Settings → Reset/Restore). 3. Check installed programs for unknown recent installations and uninstall them. 4. Run Malwarebytes or similar anti-malware (effective against PUPs and adware). 5. Check browser shortcut target for appended URLs. 6. Consider a full browser uninstall/reinstall for persistent cases. Ransomware: files locked, ransom demand note. Rootkit: deeply hidden, hard to detect, no obvious browser symptoms. Keylogger: silently records input, no visible browser changes."
    },
    {
        "domain": "Domain 3 – Software Troubleshooting",
        "topic": "Boot Repair", "difficulty": "medium",
        "question": "A Windows 11 PC displays 'Winload.efi is missing or corrupt' and will not boot. What is the correct repair approach?",
        "choices": {"A":"Run sfc /scannow from a command prompt in Windows","B":"Boot from Windows installation media → Repair → Advanced Options → Startup Repair or bootrec commands","C":"Use Disk Management to reformat the boot partition","D":"Run chkdsk /f from within Windows"},
        "answer": "B",
        "explanation": "Winload.efi is the UEFI Windows boot loader — if missing or corrupt, Windows cannot start at all. Repair requires booting from external media (USB/DVD): Insert Windows installation media → Repair your computer → Troubleshoot → Advanced Options → Startup Repair (automatic) or Command Prompt (manual). Manual bootrec commands: bootrec /fixmbr (repairs MBR — legacy BIOS only). bootrec /fixboot (writes new boot sector). bootrec /rebuildbcd (rebuilds Boot Configuration Data — often fixes winload.efi). bcdboot C:\\Windows /s C: (copies boot files, creates BCD). sfc /scannow cannot run before Windows boots — it requires a working OS environment. Startup Repair successfully handles the most common boot failures automatically."
    },
    {
        "domain": "Domain 3 – Software Troubleshooting",
        "topic": "Mobile Battery Issues", "difficulty": "medium",
        "question": "A 2-year-old iPhone battery is swollen — the screen is slightly raised from the case. What action should the technician take?",
        "choices": {"A":"Drain the battery completely and recharge to recalibrate","B":"Stop using the device immediately — a swollen lithium battery is a fire/explosion hazard; replace professionally","C":"Puncture the battery to release the buildup safely","D":"Put the phone in the freezer to reduce swelling"},
        "answer": "B",
        "explanation": "A swollen (puffed) lithium battery is a critical safety hazard — the internal cells are producing gas from a chemical reaction (often from overcharging, heat damage, or age). A swollen battery is at risk of thermal runaway — it can rupture, release toxic gas, catch fire, or explode with significant force. Correct actions: Stop using the device immediately. Do not charge it further. Do not puncture, crush, or put in the microwave or freezer — these actions are dangerous. Take it to an authorized repair center for safe battery replacement and disposal. The repair tech must handle removal carefully — swollen batteries are fragile and must not be pierced or bent. Lithium battery fires burn intensely and require Class D or dry sand to extinguish — not water."
    },
    {
        "domain": "Domain 3 – Software Troubleshooting",
        "topic": "Application Not Responding", "difficulty": "easy",
        "question": "A user's spreadsheet application stops responding mid-task. The rest of the system is working fine. What is the QUICKEST way to terminate only the frozen application?",
        "choices": {"A":"Hold the power button for 10 seconds","B":"Ctrl+Shift+Esc → Task Manager → right-click frozen app → End Task","C":"Run sfc /scannow to fix the application","D":"Reinstall the application before trying again"},
        "answer": "B",
        "explanation": "Task Manager (Ctrl+Shift+Esc is the direct shortcut — faster than Ctrl+Alt+Del → Task Manager) lets you selectively End Task only the frozen application without affecting anything else. Under the Processes tab, right-click the frozen app → End Task. Note: any unsaved work in the crashed application will be lost. Alternative if Task Manager won't open: Win+R → taskmgr. For deeper process analysis: Process Explorer (Sysinternals/Microsoft) shows process trees, DLL usage, and handles. Holding the power button reboots the entire system — loses all unsaved work in every open application. sfc repairs Windows system files — has no effect on third-party application crashes."
    },
    {
        "domain": "Domain 3 – Software Troubleshooting",
        "topic": "Slow Windows Performance", "difficulty": "medium",
        "question": "A user's Windows PC takes 5 minutes to boot and runs slowly afterward. Task Manager shows CPU at 15% but the startup tab shows 40 programs set to auto-start. What should the technician do?",
        "choices": {"A":"Reinstall Windows to fix the performance issue","B":"Disable unnecessary startup programs via Task Manager Startup tab or msconfig","C":"Add more RAM before any other action","D":"Defragment the hard drive as the first step"},
        "answer": "B",
        "explanation": "Excessive startup programs are a leading cause of slow boot times — each program initializes at startup, competing for disk I/O and CPU. Fix: Task Manager → Startup tab → right-click unneeded programs → Disable. Or: Win+R → msconfig → Startup tab (older Windows versions). Keep only essential programs (antivirus, cloud sync client, critical utilities) — disable everything else. Other performance tools: Disk Cleanup (cleanmgr.exe): removes temp files, old Windows updates. Storage Sense: automatic cleanup. Defrag: only for HDDs — SSDs should never be defragmented (it wears NAND flash). Prefetch/Superfetch: can cause disk thrashing on low-RAM systems. Check for malware — it often causes persistent slowness and may appear in startup entries."
    },

    # DOMAIN 4 — OPERATIONAL PROCEDURES
    {
        "domain": "Domain 4 – Operational Procedures",
        "topic": "Backup Types", "difficulty": "medium",
        "question": "A company runs a full backup every Sunday night. The rest of the week it runs incremental backups Monday through Saturday. If Friday's data needs to be restored, which backup sets are required?",
        "choices": {"A":"Sunday full backup only","B":"Sunday full + Monday + Tuesday + Wednesday + Thursday incremental backups","C":"Only Thursday's incremental backup","D":"Sunday full + Friday incremental only"},
        "answer": "B",
        "explanation": "Incremental backups store only the changes since the LAST backup of any type. To restore Friday: you need the last full (Sunday) as the base, then EVERY incremental in sequence — Monday, Tuesday, Wednesday, Thursday — each building on the previous. This is the main disadvantage of incremental: many backup sets needed for restore (but each individual backup is small and fast). Differential backup: stores all changes since the LAST FULL only. To restore Friday with differential: just Sunday full + Thursday differential (only 2 sets). Differential grows larger each day but restores faster. Full backup: only 1 set to restore but takes the most time/space to create. The 220-1202 exam heavily tests backup type characteristics and restore procedures."
    },
    {
        "domain": "Domain 4 – Operational Procedures",
        "topic": "ESD Prevention", "difficulty": "easy",
        "question": "A technician is about to install a RAM module into a desktop PC on a carpeted floor. What is the MOST important precaution to take?",
        "choices": {"A":"Work quickly to minimize exposure time","B":"Wear an anti-static wrist strap bonded to the PC chassis before handling components","C":"Wear thick rubber gloves to insulate hands","D":"Keep the RAM in the anti-static bag during installation"},
        "answer": "B",
        "explanation": "An anti-static wrist strap equalizes the electrical potential between the technician and the equipment — preventing electrostatic discharge (ESD) that can damage components invisibly. Bond the wrist strap to bare metal on the chassis (not a painted surface). Carpet is a major ESD generator — walking on carpet can build thousands of volts of static charge. Anti-static wrist strap: equalizes potential (most effective). Anti-static mat: dissipates charge from work surface (use together with strap). Anti-static bags: protect components in transit — remove component from bag AT the moment of installation, not before. Rubber gloves: INSULATE, do NOT prevent ESD — can actually build up charge. Speed does not reduce ESD risk. ESD damage can be latent — component works initially then fails prematurely."
    },
    {
        "domain": "Domain 4 – Operational Procedures",
        "topic": "PowerShell", "difficulty": "medium",
        "question": "A sysadmin needs to automatically create 200 user accounts in Active Directory from a CSV file. Which scripting tool is BEST suited for this on Windows?",
        "choices": {"A":"Batch file (.bat) using net user commands","B":"PowerShell (.ps1) using New-ADUser with Import-Csv","C":"VBScript (.vbs) using WMI","D":"Python script using subprocess module"},
        "answer": "B",
        "explanation": "PowerShell is purpose-built for Windows automation and Active Directory management. New-ADUser cmdlet creates AD accounts; Import-Csv reads the CSV file; a simple ForEach loop processes all 200 rows. Example: Import-Csv users.csv | ForEach-Object { New-ADUser -Name $_.Name -UserPrincipalName $_.UPN ... }. PowerShell advantages for AD: native Active Directory module, structured objects (not just text), runs remotely, manages Azure AD, integrates with Microsoft 365, extensive cmdlet library. Batch files: basic Windows scripting — cannot natively manage Active Directory. VBScript: older Microsoft scripting, being deprecated. Python: powerful but requires additional modules for AD management and is not natively integrated with Windows AD management tooling."
    },
    {
        "domain": "Domain 4 – Operational Procedures",
        "topic": "Remote Access Tools", "difficulty": "easy",
        "question": "A help desk technician needs to remotely view and control a user's Windows desktop to troubleshoot an issue. The user is on the corporate network. Which port must be open for Windows Remote Desktop?",
        "choices": {"A":"Port 22 (SSH)","B":"Port 5900 (VNC)","C":"Port 3389 (RDP)","D":"Port 443 (HTTPS)"},
        "answer": "C",
        "explanation": "RDP (Remote Desktop Protocol) uses TCP port 3389. Requirements: Windows Pro or higher on the target PC, RDP enabled (System Properties → Remote → Allow connections), connecting user has permission, firewall rule allows port 3389. Security best practices: expose RDP only through VPN, not directly to the internet (RDP on internet = major attack surface). Enable Network Level Authentication (NLA). Consider changing default port from 3389 (security through obscurity, minor benefit). Restrict who can RDP via Group Policy. Port comparison: SSH = 22 (text-based terminal, Linux/network devices). VNC = 5900 (graphical, cross-platform, less secure by default). HTTPS = 443 (web, also used by some remote tools like TeamViewer through NAT)."
    },
    {
        "domain": "Domain 4 – Operational Procedures",
        "topic": "Change Management", "difficulty": "medium",
        "question": "Before deploying a major Windows update across 500 corporate workstations, an IT team creates step-by-step instructions for reverting to the previous state if the update causes widespread issues. What document is this?",
        "choices": {"A":"SLA (Service Level Agreement)","B":"Rollback plan","C":"Network diagram","D":"Acceptable Use Policy"},
        "answer": "B",
        "explanation": "A rollback plan (backout plan) documents exactly how to undo a change if it fails — step-by-step, specific commands, who is responsible. It is a required component of proper change management. CompTIA change management flow: 1. Documented business reason. 2. Risk and impact analysis. 3. Change Advisory Board (CAB) approval. 4. Create rollback plan BEFORE implementing. 5. Schedule maintenance window. 6. Implement (test in non-production first). 7. Verify success. 8. Document results. Without a rollback plan: a failed deployment affecting 500 machines could take days to remediate. With a rollback plan: reverting is structured and fast. SLA: service availability guarantee between provider and customer. AUP: Acceptable Use Policy — defines appropriate computer use for employees."
    },
    {
        "domain": "Domain 4 – Operational Procedures",
        "topic": "Safety and Environment", "difficulty": "easy",
        "question": "A server room contains expensive equipment and uses a Novec 1230 clean agent fire suppression system. What is the primary advantage of a clean agent system over water sprinklers in this environment?",
        "choices": {"A":"Clean agents are cheaper to install","B":"Clean agents are required by the NEC for all IT rooms","C":"Clean agents suppress fires without damaging electronics or leaving conductive residue","D":"Water sprinklers cannot extinguish electrical fires"},
        "answer": "C",
        "explanation": "Clean agent fire suppression systems (Novec 1230, FM-200/HFC-227ea, Inergen, CO2) extinguish fires by removing heat or displacing oxygen without water. Benefits for data centers: zero water damage, no conductive residue, electronics can potentially survive a suppression event, minimal cleanup. Water sprinklers: would destroy servers, storage arrays, and networking equipment even if the fire itself was minor. CO2 systems: very effective but dangerous to people (displaces oxygen) — areas must be evacuated BEFORE discharge; not suitable for occupied spaces. Halon: the original clean agent — very effective but ozone-depleting, globally phased out under the Montreal Protocol. For electrical fires with a portable extinguisher: use Class C (dry chemical) but expect residue damage to electronics."
    },
    {
        "domain": "Domain 4 – Operational Procedures",
        "topic": "Documentation", "difficulty": "easy",
        "question": "After resolving a rare but complex issue where a specific model of laptop loses Wi-Fi after sleep due to a power management setting, what should the technician create to help the entire support team?",
        "choices": {"A":"A purchase order for newer laptops","B":"A knowledge base article documenting the symptoms, root cause, and exact fix steps","C":"A change request to disable sleep on all laptops","D":"An email to the user explaining the fix"},
        "answer": "B",
        "explanation": "Knowledge base articles (KBAs) convert individual troubleshooting experience into reusable team knowledge. A complex 2-hour diagnosis becomes a 2-minute fix for any subsequent technician who searches the KB. Good KBA structure: Symptoms (exactly what the user reports), Affected hardware/software versions, Root cause, Step-by-step resolution, Any preventive measures, Author and date. Documentation the 220-1202 tests: Physical network diagram (cable runs, room locations), Logical diagram (IP addressing, VLANs, routing), Asset inventory (hardware/software), Knowledge base, Ticketing system records, Change log, SOP (Standard Operating Procedure), AUP (Acceptable Use Policy). Always document — it's faster the second time and enables team knowledge sharing."
    },
]

# ══════════════════════════════════════════════════════════════════════════════
#  A+ CORE 2 (220-1202) GLOSSARY
# ══════════════════════════════════════════════════════════════════════════════

GLOSSARY_APLUS2 = {
    "3-2-1 backup rule": "3 copies, 2 media types, 1 offsite. ALWAYS test restores — untested backups aren't backups.",
    "Anti-static wrist strap": "Grounding device worn during PC work; equalizes potential to prevent ESD damage.",
    "apt / dnf / yum": "Linux package managers: apt (Debian/Ubuntu), dnf/yum (RHEL/Fedora/CentOS).",
    "BAD_POOL_HEADER": "BSOD — memory pool corruption; often bad RAM, corrupted driver, or anti-malware conflict.",
    "BitLocker": "Windows full-disk encryption; requires Pro or higher + TPM chip; protects data if drive is stolen.",
    "bootrec": "Windows boot repair CLI — /fixmbr, /fixboot, /rebuildbcd, /scanos.",
    "BSOD": "Blue Screen of Death — kernel stop error showing hex stop code. Always note the stop code.",
    "CAB": "Change Advisory Board — reviews, approves, and coordinates production changes.",
    "Certificate of destruction": "Legal document from a data destruction vendor confirming secure media disposal.",
    "chmod": "Linux permission command: chmod 755 = rwxr-xr-x; 644 = rw-r--r--; 777 = rwxrwxrwx.",
    "chkdsk /r": "Checks disk for FS errors AND locates bad sectors, recovering readable data. Must schedule on C:.",
    "Cryptographic erase": "Destroys encryption key on self-encrypting drives — renders all data permanently unrecoverable.",
    "Degaussing": "Magnetic wipe — effective ONLY on HDDs and magnetic tape. Has NO effect on SSDs/flash.",
    "Device Manager": "Windows tool (devmgmt.msc) — manage hardware, update/roll back/uninstall drivers.",
    "Differential backup": "Backs up ALL changes since last full. Restore needs: full + 1 differential. Grows daily.",
    "DISM": "Deployment Image Servicing and Management — repairs Windows component store. Run before sfc.",
    "EFS": "Encrypting File System — per-file Windows encryption tied to user certificate. Lost cert = lost files.",
    "ESD": "Electrostatic Discharge — static electricity that invisibly damages components; use wrist strap.",
    "Event Viewer": "eventvwr.msc — Application (app errors), System (OS/driver), Security (audit/logon) logs.",
    "FileVault": "macOS full-disk encryption (AES-128) — equivalent to Windows BitLocker.",
    "FM-200": "Clean agent fire suppressant for data centers — extinguishes without water or residue.",
    "Full backup": "Complete data copy every time. Largest/slowest to back up; fastest/simplest to restore.",
    "gpresult /r": "Shows which Group Policy Objects are applied to the current user and computer.",
    "gpupdate /force": "Immediately reapplies all Group Policy settings without waiting for refresh cycle.",
    "Homebrew": "Community package manager for macOS — installs Unix/developer tools via Terminal.",
    "Incremental backup": "Backs up changes since LAST backup (any type). Smallest/fastest; most sets to restore.",
    "INACCESSIBLE_BOOT_DEVICE": "BSOD 0x7B — storage controller driver problem or BIOS SATA mode change.",
    "IRQL_NOT_LESS_OR_EQUAL": "BSOD 0x0000000A — buggy or incompatible device driver accessing wrong memory level.",
    "Keychain": "macOS built-in credential manager — stores Wi-Fi, web, and app passwords securely.",
    "Knowledge base": "Searchable repository of documented IT issues, root causes, and resolution steps.",
    "Least privilege": "Grant users/processes only the minimum access needed — nothing more.",
    "Mantrap": "Security double-door airlock — allows one person through at a time; prevents tailgating.",
    "MFA": "Multi-Factor Authentication — requires 2+ different factor categories (know + have + are + where).",
    "Mission Control": "macOS overview of all windows, Spaces (virtual desktops), and full-screen apps.",
    "msconfig": "System Configuration — manages startup programs, boot options, and services on Windows.",
    "New-ADUser": "PowerShell cmdlet for creating Active Directory user accounts. Works with Import-Csv.",
    "Novec 1230": "Clean agent fire suppressant — safer than FM-200, zero global warming potential.",
    "NTFS permissions": "Full Control > Modify > Read & Execute > List Folder > Read > Write. Deny overrides Allow.",
    "PAGE_FAULT_IN_NONPAGED_AREA": "BSOD 0x50 — RAM failure or driver attempting to access nonexistent memory.",
    "PowerShell": "Windows scripting/automation language (.ps1). Cmdlets manage OS, AD, Azure at scale.",
    "ps aux": "Linux — lists ALL running processes with owner, PID, CPU%, memory%, and command.",
    "PUP": "Potentially Unwanted Program — adware, toolbars, hijackers bundled with free software.",
    "RDP": "Remote Desktop Protocol — TCP port 3389. Graphical remote control for Windows Pro and above.",
    "regedit": "Windows Registry Editor — modifies HKLM (all users), HKCU (current user), HKCR, HKU, HKCC.",
    "Rollback plan": "Step-by-step instructions for reverting a change if it causes problems. Required before changes.",
    "SAE": "Simultaneous Authentication of Equals — WPA3 handshake replacing PSK; resists offline cracking.",
    "Safe Mode": "Minimal Windows boot (F8) — essential for malware removal and driver troubleshooting.",
    "secpol.msc": "Local Security Policy — configures password policies, account lockout, audit policies.",
    "sfc /scannow": "System File Checker — scans and repairs corrupted Windows system files. Run as admin.",
    "Smishing": "SMS/text message phishing attack.",
    "Shoulder surfing": "Watching victim's screen or keyboard to steal credentials. Prevention: privacy screen filter.",
    "SMART": "Self-Monitoring Analysis and Reporting Technology — monitors drive health; check before failure.",
    "SOP": "Standard Operating Procedure — documented step-by-step process for routine tasks.",
    "Spotlight": "macOS universal search (Cmd+Space) — apps, files, web, calculator, conversions.",
    "Swollen battery": "Lithium battery producing gas — CRITICAL safety hazard, do not use; replace professionally.",
    "Tailgating": "Following an authorized person through a secured entry without authenticating.",
    "Time Machine": "macOS automated backup — hourly/daily/weekly snapshots to external or network drive.",
    "TPM": "Trusted Platform Module — hardware chip securing cryptographic keys; required for BitLocker.",
    "UAC": "User Account Control — prompts for elevation before system changes; enforces least privilege.",
    "Vishing": "Voice phishing — phone-based social engineering impersonating IT, banks, or government.",
    "Winload.efi": "UEFI Windows boot loader. If corrupt, repair with bootrec /rebuildbcd or bcdboot.",
    "WPA3-Personal": "Wi-Fi security using SAE — forward secrecy, resists offline dictionary attacks.",
}

#  NETWORK+ N10-009 — DOMAIN THEME, WEIGHTS & OBJECTIVES
# ══════════════════════════════════════════════════════════════════════════════

DOMAIN_THEME_NETPLUS = {
    "Domain 1": {"color": C.SKY,   "icon": "🌐", "short": "D1", "bg": C.BG_BLU},
    "Domain 2": {"color": C.LIME,  "icon": "🔌", "short": "D2", "bg": C.BG_GRN},
    "Domain 3": {"color": C.GOLD,  "icon": "📡", "short": "D3", "bg": C.BG_YLW},
    "Domain 4": {"color": C.TEAL,  "icon": "🔐", "short": "D4", "bg": C.BG_CYN},
    "Domain 5": {"color": C.PRP,   "icon": "🛠️",  "short": "D5", "bg": C.BG_MAG},
}

DOMAIN_WEIGHTS_NETPLUS = {
    "Domain 1 – Networking Concepts": 23,
    "Domain 2 – Network Implementation": 19,
    "Domain 3 – Network Operations": 17,
    "Domain 4 – Network Security": 20,
    "Domain 5 – Network Troubleshooting": 21,
}

DOM_ORDER_NETPLUS = [
    "Domain 1 – Networking Concepts",
    "Domain 2 – Network Implementation",
    "Domain 3 – Network Operations",
    "Domain 4 – Network Security",
    "Domain 5 – Network Troubleshooting",
]

EXAM_OBJECTIVES_NETPLUS = {
    "Domain 1 – Networking Concepts": {
        "weight": 23,
        "objectives": [
            "Explain the OSI model layers and how data encapsulation/decapsulation works.",
            "Compare and contrast network topologies, architecture types, and networking devices.",
            "Explain common network ports, protocols, and their use cases.",
            "Explain the concepts of IP addressing including IPv4, IPv6, subnetting, and CIDR notation.",
            "Compare cloud concepts and connectivity options.",
        ],
        "study": [
            "OSI model top to bottom: All People Seem To Need Data Processing (Application, Presentation, Session, Transport, Network, Data Link, Physical).",
            "Know which protocols live at which layer: HTTP/DNS/SMTP = Layer 7; TCP/UDP = Layer 4; IP = Layer 3; Ethernet/MAC = Layer 2; cables = Layer 1.",
            "Subnetting is heavily tested — practice calculating network address, broadcast, and host range from CIDR notation.",
            "IPv6 addresses are 128-bit, written as eight groups of four hex digits; :: represents consecutive zero groups.",
        ],
    },
    "Domain 2 – Network Implementation": {
        "weight": 19,
        "objectives": [
            "Install and configure switching technologies including VLANs, spanning tree, and link aggregation.",
            "Install and configure routing technologies including static routes, dynamic routing protocols, and NAT.",
            "Install and configure wireless networks including standards, channels, and security.",
            "Summarize cloud and datacenter infrastructure.",
        ],
        "study": [
            "VLANs logically segment a network at Layer 2 — devices in different VLANs cannot communicate without a Layer 3 router.",
            "Spanning Tree Protocol (STP) prevents Layer 2 loops by blocking redundant paths — knows root bridge, designated port, root port.",
            "Dynamic routing: RIP (hop count metric, max 15 hops), OSPF (link state, cost metric, fast convergence), BGP (internet routing, policy-based).",
            "NAT translates private IPs to public IPs — PAT (Port Address Translation) allows many-to-one mapping using port numbers.",
        ],
    },
    "Domain 3 – Network Operations": {
        "weight": 17,
        "objectives": [
            "Use appropriate statistics and sensors to ensure network availability.",
            "Explain the purpose of organizational documents and policies.",
            "Explain high availability and disaster recovery concepts.",
            "Use network monitoring tools and explain their purpose.",
        ],
        "study": [
            "SNMP monitors network devices — MIB stores device data; traps send alerts; polling queries devices.",
            "Syslog centralizes log collection — severity levels 0 (Emergency) to 7 (Debug).",
            "MTTR and MTBF measure reliability — lower MTTR and higher MTBF are better.",
            "Know the difference between active (generates traffic to test) and passive (observes existing traffic) monitoring.",
        ],
    },
    "Domain 4 – Network Security": {
        "weight": 20,
        "objectives": [
            "Explain common security concepts including CIA triad, zero trust, and defense in depth.",
            "Compare and contrast common attack types targeting networks.",
            "Apply network hardening techniques.",
            "Compare and contrast remote access methods and security implications.",
            "Explain the importance of physical security.",
        ],
        "study": [
            "Network attacks: ARP spoofing (poisons ARP cache, enables MITM), DNS poisoning (redirects traffic), DoS/DDoS (floods resources).",
            "Firewall types: packet filter (Layer 3/4), stateful (tracks connections), NGFW (Layer 7, app awareness, IPS).",
            "802.1X is port-based NAC — authenticates devices before they can use the network (uses RADIUS server).",
            "IPsec modes: transport (encrypts payload only) vs tunnel (encrypts entire packet, used for site-to-site VPN).",
        ],
    },
    "Domain 5 – Network Troubleshooting": {
        "weight": 21,
        "objectives": [
            "Explain the network troubleshooting methodology.",
            "Troubleshoot common cable connectivity issues and select the appropriate tools.",
            "Use the appropriate network software tools and commands.",
            "Troubleshoot common wireless connectivity issues.",
            "Troubleshoot general networking issues.",
        ],
        "study": [
            "Troubleshooting tools: cable tester (finds breaks/miswires), toner probe (traces cables), OTDR (fiber distance/faults), multimeter (voltage/continuity).",
            "Commands: ping (connectivity), tracert/traceroute (path), ipconfig/ifconfig (IP config), nslookup/dig (DNS), netstat (connections/ports), arp -a (ARP cache).",
            "Half-duplex vs full-duplex mismatch causes collisions and poor performance — look for late collisions and runts.",
            "Wireless issues: channel overlap (use non-overlapping channels 1, 6, 11 on 2.4GHz), interference (microwaves, Bluetooth), signal strength (SNR).",
        ],
    },
}

QUESTIONS_NETPLUS = [

    # DOMAIN 1 — NETWORKING CONCEPTS
    {
        "domain": "Domain 1 – Networking Concepts",
        "topic": "OSI Model", "difficulty": "easy",
        "question": "At which OSI model layer does a router primarily operate, making forwarding decisions based on IP addresses?",
        "choices": {"A":"Layer 1 — Physical","B":"Layer 2 — Data Link","C":"Layer 3 — Network","D":"Layer 4 — Transport"},
        "answer": "C",
        "explanation": "Routers operate at Layer 3 (Network layer) and make forwarding decisions based on IP addresses in the packet header. Key OSI layer device mapping: Layer 1 (Physical): hubs, repeaters, cables — just signals, no intelligence. Layer 2 (Data Link): switches, bridges — use MAC addresses to forward frames within a LAN. Layer 3 (Network): routers, Layer 3 switches — use IP addresses to route packets between networks. Layer 4 (Transport): firewalls (often), load balancers — TCP/UDP ports. Layer 7 (Application): application-layer firewalls, proxies. Mnemonic for OSI layers bottom-up: Please Do Not Throw Sausage Pizza Away (Physical, Data Link, Network, Transport, Session, Presentation, Application)."
    },
    {
        "domain": "Domain 1 – Networking Concepts",
        "topic": "OSI Model", "difficulty": "medium",
        "question": "Which OSI layer is responsible for end-to-end communication, error recovery, and flow control using protocols like TCP and UDP?",
        "choices": {"A":"Layer 2 — Data Link","B":"Layer 3 — Network","C":"Layer 4 — Transport","D":"Layer 5 — Session"},
        "answer": "C",
        "explanation": "Layer 4 (Transport) provides end-to-end communication between applications on different hosts. TCP (Transmission Control Protocol): connection-oriented, reliable, ordered delivery with acknowledgments, flow control (windowing), and error recovery. Uses 3-way handshake (SYN, SYN-ACK, ACK). UDP (User Datagram Protocol): connectionless, unreliable (no ACK), low overhead, faster. Used for streaming, VoIP, DNS, DHCP. Layer 4 also introduces port numbers that identify specific applications. Port numbers 0-1023: well-known ports. 1024-49151: registered ports. 49152-65535: dynamic/ephemeral ports. Flow control at Layer 4 prevents fast senders from overwhelming slow receivers."
    },
    {
        "domain": "Domain 1 – Networking Concepts",
        "topic": "IPv4 Addressing", "difficulty": "medium",
        "question": "What is the valid host range for the network 192.168.10.0/25?",
        "choices": {"A":"192.168.10.1 to 192.168.10.255","B":"192.168.10.1 to 192.168.10.126","C":"192.168.10.1 to 192.168.10.128","D":"192.168.10.0 to 192.168.10.127"},
        "answer": "B",
        "explanation": "/25 means 25 bits are the network portion, leaving 7 host bits. 2^7 = 128 total addresses; 128 - 2 = 126 usable hosts. Network address: 192.168.10.0 (all host bits = 0). First host: 192.168.10.1. Last host: 192.168.10.126. Broadcast: 192.168.10.127 (all host bits = 1). Subnet mask for /25: 255.255.255.128. Subnetting quick reference: /24 = 254 hosts; /25 = 126 hosts; /26 = 62 hosts; /27 = 30 hosts; /28 = 14 hosts; /29 = 6 hosts; /30 = 2 hosts (point-to-point links). Network and broadcast addresses cannot be assigned to hosts."
    },
    {
        "domain": "Domain 1 – Networking Concepts",
        "topic": "IPv6", "difficulty": "medium",
        "question": "Which type of IPv6 address is equivalent to a private RFC 1918 address in IPv4 and is only routable within a local site?",
        "choices": {"A":"Global unicast (2000::/3)","B":"Link-local (FE80::/10)","C":"Unique local (FC00::/7)","D":"Multicast (FF00::/8)"},
        "answer": "C",
        "explanation": "Unique local addresses (FC00::/7, commonly FC00:: to FDFF::) are the IPv6 equivalent of IPv4 private addresses (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) — not routable on the public internet. IPv6 address types: Global unicast (2000::/3): publicly routable, assigned by ISPs — equivalent to public IPv4. Link-local (FE80::/10): auto-configured on every IPv6 interface, only valid on the local link (cannot be routed). Required for IPv6 neighbor discovery. Loopback: ::1 (equivalent to 127.0.0.1 in IPv4). Multicast (FF00::/8): one-to-many delivery. Anycast: same address assigned to multiple interfaces; packet goes to nearest one."
    },
    {
        "domain": "Domain 1 – Networking Concepts",
        "topic": "Common Ports", "difficulty": "easy",
        "question": "Which protocol and port number is used to securely transfer files over an encrypted SSH connection?",
        "choices": {"A":"FTP on port 21","B":"TFTP on port 69","C":"SFTP on port 22","D":"FTPS on port 990"},
        "answer": "C",
        "explanation": "SFTP (SSH File Transfer Protocol) runs over SSH on port 22 — it encrypts both authentication AND data transfer. Not to be confused with FTPS. FTP (ports 20/21): completely unencrypted file transfer — credentials and data sent in cleartext. Never use on untrusted networks. SFTP (port 22): FTP over SSH — encrypted, secure. FTPS (port 990 implicit / 21 explicit): FTP over TLS/SSL — encrypted but uses certificates. TFTP (port 69/UDP): Trivial FTP — unauthenticated, used for PXE boot and network device firmware updates on trusted LANs. SCP (port 22): Secure Copy Protocol — also runs over SSH, for simple file copying."
    },
    {
        "domain": "Domain 1 – Networking Concepts",
        "topic": "Network Topologies", "difficulty": "easy",
        "question": "In which network topology does every device connect to a central device (switch or hub), making it the most common LAN design today?",
        "choices": {"A":"Bus","B":"Ring","C":"Mesh","D":"Star"},
        "answer": "D",
        "explanation": "Star topology: all devices connect to a central switch or hub. The dominant LAN topology today because: easy to add/remove devices, fault isolation (one cable failing doesn't affect others), easy troubleshooting. Single point of failure is the central switch (mitigated with redundant switches). Bus topology: all devices share a single cable (coaxial) — a break anywhere kills the whole network. Legacy, rarely seen today. Ring topology: devices connected in a circle; data travels in one or both directions — Token Ring (legacy). Mesh topology: every device connects to every other device — fully redundant but expensive. Used in WAN designs and critical infrastructure. Hybrid: combinations of the above."
    },
    {
        "domain": "Domain 1 – Networking Concepts",
        "topic": "DNS", "difficulty": "easy",
        "question": "Which DNS record type maps a hostname to an IPv4 address?",
        "choices": {"A":"MX record","B":"AAAA record","C":"CNAME record","D":"A record"},
        "answer": "D",
        "explanation": "DNS record types: A record: maps hostname to IPv4 address (e.g., www.example.com → 93.184.216.34). AAAA record: maps hostname to IPv6 address (quad-A, because IPv6 is 4x larger than IPv4). CNAME (Canonical Name): alias pointing to another hostname (e.g., mail.example.com → mailserver.example.com). MX (Mail Exchanger): specifies mail servers for a domain with priority values. NS (Name Server): specifies authoritative DNS servers for a domain. PTR (Pointer): reverse DNS — maps IP address back to hostname. TXT record: text data, used for SPF, DKIM, and domain verification. SOA (Start of Authority): zone information including primary NS, admin email, serial number, TTL values."
    },

    # DOMAIN 2 — NETWORK IMPLEMENTATION
    {
        "domain": "Domain 2 – Network Implementation",
        "topic": "VLANs", "difficulty": "medium",
        "question": "A network administrator wants to logically separate the HR department's traffic from the Engineering department on the same physical switch. Which technology should be used?",
        "choices": {"A":"Spanning Tree Protocol","B":"VLAN (Virtual Local Area Network)","C":"NAT","D":"DHCP relay"},
        "answer": "B",
        "explanation": "VLANs (Virtual LANs) create logical network segments on a single physical switch by tagging frames with VLAN IDs (802.1Q). Devices in different VLANs cannot communicate directly — they must go through a router (or Layer 3 switch) for inter-VLAN routing. Benefits: security (HR can't see Engineering traffic), broadcast domain reduction (broadcasts stay within a VLAN), flexibility (users in same VLAN regardless of physical location). Access port: carries traffic for one VLAN only (connects end devices). Trunk port: carries traffic for multiple VLANs simultaneously (switch-to-switch and switch-to-router links) using 802.1Q tagging. Native VLAN: untagged traffic on a trunk port."
    },
    {
        "domain": "Domain 2 – Network Implementation",
        "topic": "Spanning Tree", "difficulty": "hard",
        "question": "Spanning Tree Protocol (STP) prevents which specific Layer 2 problem on networks with redundant switch paths?",
        "choices": {"A":"IP address conflicts","B":"Layer 2 broadcast storms and switching loops","C":"DNS resolution failures","D":"MTU fragmentation"},
        "answer": "B",
        "explanation": "Without STP, redundant switch paths cause broadcast storms: a broadcast frame is forwarded out all ports, creating copies on both paths, which loop back and generate more broadcasts — exponentially filling the network until it collapses. STP prevents this by electing a root bridge (lowest Bridge ID = priority + MAC address) and blocking redundant ports. Port states: Blocking (no data, receives BPDUs), Listening, Learning (builds MAC table), Forwarding (active). RSTP (Rapid STP, 802.1w): faster convergence than original STP. MSTP (802.1s): multiple spanning tree instances for different VLANs. Modern networks use RSTP. PortFast: immediately transitions access ports to forwarding (skips STP calculation for end devices)."
    },
    {
        "domain": "Domain 2 – Network Implementation",
        "topic": "Routing Protocols", "difficulty": "medium",
        "question": "Which interior gateway routing protocol uses a cost metric based on bandwidth and builds a complete map of the network topology using link-state advertisements?",
        "choices": {"A":"RIP (Routing Information Protocol)","B":"BGP (Border Gateway Protocol)","C":"OSPF (Open Shortest Path First)","D":"EIGRP — using hop count"},
        "answer": "C",
        "explanation": "OSPF (Open Shortest Path First) is a link-state routing protocol: each router shares Link State Advertisements (LSAs) with all other routers to build an identical topology database (LSDB). Uses Dijkstra's algorithm to calculate shortest path. Metric: cost (based on bandwidth — lower bandwidth = higher cost). Fast convergence. Scales well. RIP (Routing Information Protocol): distance-vector, hop count metric (max 15 hops — severely limits network size), slow convergence. Version 1 uses broadcast; Version 2 uses multicast. Legacy. EIGRP: Cisco proprietary, hybrid (distance-vector + some link-state), uses composite metric (bandwidth + delay). BGP: exterior gateway protocol used between autonomous systems on the internet — policy-based routing, not just shortest path."
    },
    {
        "domain": "Domain 2 – Network Implementation",
        "topic": "NAT", "difficulty": "medium",
        "question": "A small office uses one public IP address for all 50 workstations. Multiple workstations browse the internet simultaneously. Which NAT type makes this possible?",
        "choices": {"A":"Static NAT (one-to-one mapping)","B":"Dynamic NAT (pool of public IPs)","C":"PAT — Port Address Translation (many-to-one)","D":"Twice NAT (bidirectional)"},
        "answer": "C",
        "explanation": "PAT (Port Address Translation), also called NAT overload or NAPT, maps many private IP addresses to a single public IP address using unique port numbers to track each session. When a workstation makes a connection, the router assigns a unique source port number — when the response arrives, the router matches the port number to translate the response back to the correct internal host. Static NAT: one private IP permanently maps to one public IP — used for servers needing a fixed public address. Dynamic NAT: pool of public IPs assigned from a pool as needed — still one-to-one but addresses are assigned dynamically. PAT is by far the most common — allows hundreds of devices to share a single public IP."
    },
    {
        "domain": "Domain 2 – Network Implementation",
        "topic": "Wireless Security", "difficulty": "medium",
        "question": "A corporate wireless network uses WPA3-Enterprise with 802.1X authentication. Which back-end server validates user credentials before allowing Wi-Fi access?",
        "choices": {"A":"DNS server","B":"DHCP server","C":"RADIUS server","D":"Proxy server"},
        "answer": "C",
        "explanation": "RADIUS (Remote Authentication Dial-In User Service) is the authentication server used by 802.1X/WPA-Enterprise. When a device connects: 1. Device sends credentials to the wireless access point (authenticator). 2. AP forwards credentials to the RADIUS server (authentication server). 3. RADIUS verifies credentials against a user database (Active Directory, LDAP). 4. RADIUS sends Accept or Reject back to AP. 5. AP grants or denies access. RADIUS uses ports 1812 (authentication) and 1813 (accounting). TACACS+ is a similar protocol from Cisco used for device administration. The advantage of 802.1X/RADIUS: each user has individual credentials — no shared PSK, so removing a user's access doesn't require changing the network password."
    },

    # DOMAIN 3 — NETWORK OPERATIONS
    {
        "domain": "Domain 3 – Network Operations",
        "topic": "Network Monitoring", "difficulty": "medium",
        "question": "Which protocol allows network devices to send unsolicited alert messages to a management station when a significant event occurs, such as an interface going down?",
        "choices": {"A":"SNMP Trap","B":"Syslog","C":"NetFlow","D":"ICMP ping"},
        "answer": "A",
        "explanation": "SNMP (Simple Network Management Protocol) uses port 161/UDP for queries and port 162/UDP for traps. SNMP Traps: unsolicited notifications sent by a managed device to the NMS (Network Management System) when a significant event occurs — interface down, CPU threshold exceeded, etc. The MIB (Management Information Base) defines what data each device exposes. SNMP versions: v1/v2c use community strings (cleartext — weak security). SNMPv3 adds authentication and encryption. Syslog: text-based logging protocol using port 514 (UDP or TCP). Severity 0 (Emergency) to 7 (Debug). NetFlow: captures metadata about IP traffic flows — source/destination IP, ports, bytes. Used for traffic analysis, not real-time alerts."
    },
    {
        "domain": "Domain 3 – Network Operations",
        "topic": "High Availability", "difficulty": "medium",
        "question": "Two routers share a virtual IP address and are configured so that if the primary router fails, the secondary automatically takes over. This is an example of:",
        "choices": {"A":"Load balancing with round-robin DNS","B":"First Hop Redundancy Protocol (HSRP or VRRP)","C":"Link aggregation (LACP)","D":"Spanning Tree failover"},
        "answer": "B",
        "explanation": "First Hop Redundancy Protocols (FHRPs) provide gateway redundancy: HSRP (Hot Standby Router Protocol): Cisco proprietary. One active router, one standby. Virtual IP and MAC address. If active fails, standby takes over in seconds. VRRP (Virtual Router Redundancy Protocol): open standard equivalent to HSRP. One master, one or more backups. GLBP (Gateway Load Balancing Protocol): Cisco proprietary, adds load balancing across multiple routers. All FHRPs share a virtual IP — hosts point to this VIP as their default gateway. They never know which physical router is handling traffic. Link aggregation (LACP/802.3ad): bundles multiple physical links into one logical link for bandwidth and redundancy between switches."
    },
    {
        "domain": "Domain 3 – Network Operations",
        "topic": "Network Documentation", "difficulty": "easy",
        "question": "Which type of network diagram shows the physical layout of devices, cable runs, rack locations, and room placements?",
        "choices": {"A":"Logical diagram","B":"Physical diagram","C":"Flowchart","D":"VLAN map"},
        "answer": "B",
        "explanation": "Network diagram types: Physical diagram: shows actual physical layout — where equipment is located, cable runs, rack positions, floor plans, distances. Used for installation, cabling work, and facilities management. Logical diagram: shows how data flows — IP addressing, subnets, VLANs, routing domains, protocol details. Device icons are connected by logical relationships, not physical paths. Both are needed for complete network documentation. Other important documentation: IP address management (IPAM) tables, VLAN assignments, port assignments, baseline performance data, change logs, and network policies. Good documentation reduces mean time to repair (MTTR) during outages."
    },

    # DOMAIN 4 — NETWORK SECURITY
    {
        "domain": "Domain 4 – Network Security",
        "topic": "ARP Attacks", "difficulty": "medium",
        "question": "An attacker sends unsolicited ARP reply messages to associate their MAC address with the gateway's IP address, causing all traffic to flow through the attacker first. This attack is called:",
        "choices": {"A":"DNS poisoning","B":"ARP spoofing / ARP poisoning","C":"IP spoofing","D":"Session hijacking"},
        "answer": "B",
        "explanation": "ARP spoofing (ARP poisoning) exploits the fact that ARP has no authentication — any device can send ARP replies claiming to own any IP address. By associating the attacker's MAC with the gateway's IP, all hosts on the segment send traffic to the attacker (man-in-the-middle). Defenses: Dynamic ARP Inspection (DAI) on managed switches validates ARP messages against a DHCP binding table. DHCP snooping must be enabled first (DAI depends on it). VLANs limit ARP broadcast domains. Static ARP entries (not practical at scale). ARP attacks are Layer 2 and only affect the local subnet — traffic between subnets goes through a router and is not vulnerable to local ARP attacks."
    },
    {
        "domain": "Domain 4 – Network Security",
        "topic": "Firewall Types", "difficulty": "medium",
        "question": "Which firewall type can identify and block specific applications (like BitTorrent or Facebook) regardless of the port being used, using deep packet inspection?",
        "choices": {"A":"Packet-filtering firewall","B":"Stateful inspection firewall","C":"Next-Generation Firewall (NGFW)","D":"Circuit-level gateway"},
        "answer": "C",
        "explanation": "Next-Generation Firewalls (NGFWs) operate at Layer 7 and include: Deep packet inspection (DPI): inspects actual packet content, not just headers. Application awareness: identifies applications by behavior, not port (blocks BitTorrent even if it uses port 80). Intrusion Prevention System (IPS): actively blocks detected threats. SSL/TLS inspection: decrypts and inspects encrypted traffic. User identity awareness: applies policies per user, not just IP. Packet-filtering firewall: Layer 3/4 only — ACLs based on IP and port. Simple and fast but blind to application content. Stateful inspection: tracks connection state (established, related) — smarter than packet filtering. Circuit-level gateway: validates TCP handshakes at Session layer without inspecting content."
    },
    {
        "domain": "Domain 4 – Network Security",
        "topic": "VPN Technologies", "difficulty": "medium",
        "question": "Which VPN type is typically used to securely connect an entire remote office network to headquarters over the internet as a persistent connection?",
        "choices": {"A":"Remote access VPN (client-to-site)","B":"SSL VPN","C":"Site-to-site VPN","D":"Split tunnel VPN only"},
        "answer": "C",
        "explanation": "Site-to-site VPN: connects two entire networks (LAN-to-LAN) using routers or VPN concentrators at each end. Always-on persistent connection. Users at the remote site don't need VPN client software — the router handles it. Uses IPsec in tunnel mode typically. Ideal for: permanent branch office connections, mergers, multi-location companies. Remote access VPN (client-to-site): individual users connect to the corporate network from their device using VPN client software. IPsec or SSL-based. SSL VPN: uses TLS/HTTPS (port 443) — works through most firewalls without special configuration. Split tunneling: only VPN-destined traffic goes through the tunnel; other internet traffic goes direct — trades security for performance. Full tunnel: all traffic routed through VPN."
    },
    {
        "domain": "Domain 4 – Network Security",
        "topic": "Network Hardening", "difficulty": "medium",
        "question": "A network administrator disables Telnet and enables SSH on all network devices. What security improvement does this achieve?",
        "choices": {"A":"Faster device management","B":"Replaces plaintext management with encrypted authentication and command sessions","C":"Enables remote desktop access","D":"Allows SNMP monitoring to begin"},
        "answer": "B",
        "explanation": "Telnet (port 23) sends all data — including usernames and passwords — in plain cleartext. Anyone on the network capturing traffic with a packet analyzer (Wireshark) can read Telnet credentials and commands. SSH (port 22) encrypts the entire session using symmetric encryption after an asymmetric key exchange — credentials and all commands are protected. SSH also supports public key authentication (more secure than passwords). Other network device hardening: change default credentials, disable unused ports and services, use SNMPv3 (not v1/v2c), restrict management access via ACLs, use out-of-band management (dedicated management network), enable logging to syslog, configure banners."
    },
    {
        "domain": "Domain 4 – Network Security",
        "topic": "DDoS Defense", "difficulty": "hard",
        "question": "A company's web server is being overwhelmed by millions of requests from thousands of different IP addresses. Which mitigation approach BEST addresses a Distributed Denial of Service (DDoS) attack?",
        "choices": {"A":"Block the single source IP address","B":"Use rate limiting, traffic scrubbing services, and CDN-based DDoS protection","C":"Reboot the web server every hour","D":"Increase the web server's RAM"},
        "answer": "B",
        "explanation": "DDoS attacks are distributed — blocking one IP is ineffective when thousands are attacking. Effective DDoS mitigation: Upstream scrubbing: traffic is rerouted to a scrubbing center that filters malicious traffic before it reaches your network (Cloudflare, Akamai, AWS Shield). CDN (Content Delivery Network): distributes traffic across global edge nodes, absorbing volumetric attacks. Rate limiting: limits requests per IP per second at the edge. Anycast routing: spreads traffic across distributed network infrastructure. Black hole routing: null-routes all traffic to the attacked IP — stops the attack but also stops legitimate traffic (last resort). ISP-level filtering: block attack traffic at the ISP before it enters your network."
    },

    # DOMAIN 5 — NETWORK TROUBLESHOOTING
    {
        "domain": "Domain 5 – Network Troubleshooting",
        "topic": "Troubleshooting Tools", "difficulty": "easy",
        "question": "Which command-line tool shows the complete path that packets take from a source to a destination, listing each router hop and the latency to each hop?",
        "choices": {"A":"ping","B":"netstat","C":"tracert / traceroute","D":"nslookup"},
        "answer": "C",
        "explanation": "tracert (Windows) / traceroute (Linux/Mac) sends packets with incrementally increasing TTL values to map each hop. Each router decrements TTL by 1 and returns an ICMP Time Exceeded message when TTL=0, revealing its IP address and response time. Uses: locate where a connection is failing (first hop with timeouts shows the problem). Identify routing loops. Measure latency to each hop. Three latency values per hop — asterisks (*) mean no response (router blocking ICMP). ping: tests basic connectivity (ICMP Echo) to a host. netstat: shows current TCP/UDP connections and listening ports. nslookup/dig: queries DNS for name resolution. arp -a: displays the ARP cache (IP-to-MAC mappings)."
    },
    {
        "domain": "Domain 5 – Network Troubleshooting",
        "topic": "Cable Troubleshooting", "difficulty": "medium",
        "question": "A network cable tests as 'open' on a cable tester. What does this result indicate?",
        "choices": {"A":"The cable is working correctly","B":"The cable has a break or disconnected wire","C":"The cable has too many splices","D":"The cable is too long"},
        "answer": "B",
        "explanation": "A cable tester sends a signal through each wire pair and checks for: Open: a wire is broken, disconnected, or not punched down — no continuity. Short: two wires are touching where they shouldn't be. Crossed pairs: wires connected to wrong pins on one end. Split pairs: correct pins on both ends but twisted with the wrong pair (causes crosstalk). Cable testing tools: Basic cable tester: pass/fail for opens, shorts, crossed pairs. Advanced cable tester/certifier: measures length, attenuation, crosstalk, and certifies the cable meets a specific standard (Cat6a, etc.). Tone generator and toner probe (fox and hound): traces cable runs through walls. OTDR (Optical Time-Domain Reflectometer): tests fiber optic cables, finds break distance."
    },
    {
        "domain": "Domain 5 – Network Troubleshooting",
        "topic": "Wireless Troubleshooting", "difficulty": "medium",
        "question": "Users in an office report slow Wi-Fi speeds during business hours but fast speeds early morning and on weekends. The AP signal strength is strong. What is the MOST likely cause?",
        "choices": {"A":"The AP needs a firmware update","B":"Channel congestion from too many users or overlapping SSIDs in the area","C":"The cable connecting the AP to the switch is faulty","D":"DHCP lease exhaustion"},
        "answer": "B",
        "explanation": "The time-of-day pattern (slow during business hours when many people/devices are active) strongly indicates channel congestion or co-channel interference — too many devices competing for the same wireless channel. Solutions: Use a Wi-Fi analyzer to find the least congested channel. On 2.4 GHz, use only channels 1, 6, or 11 (non-overlapping). Switch heavy users to 5 GHz (more channels, less congestion, shorter range). Deploy additional APs to reduce clients per AP (use different channels). Enable band steering to push capable devices to 5 GHz. Wi-Fi 6 (802.11ax) with OFDMA dramatically improves performance in dense environments. Strong signal but slow speeds = congestion, not coverage problem."
    },
    {
        "domain": "Domain 5 – Network Troubleshooting",
        "topic": "IP Troubleshooting", "difficulty": "medium",
        "question": "A user cannot communicate with anyone on the network and their IP address shows as 169.254.45.23. What does this address indicate?",
        "choices": {"A":"The user has a static IP correctly configured","B":"The user received a valid DHCP lease","C":"DHCP failed and the device self-assigned an APIPA address","D":"The user is connected to a different VLAN"},
        "answer": "C",
        "explanation": "169.254.0.0/16 is the APIPA (Automatic Private IP Addressing) range — also called link-local in Microsoft terminology (IPv4LL). When a Windows device cannot reach a DHCP server, it self-assigns an address in this range after a timeout (about 30-60 seconds). APIPA devices can communicate with OTHER APIPA devices on the same segment, but cannot reach routers, the internet, or most network resources. Troubleshooting APIPA: check physical connection (cable, link light). Check if DHCP server is reachable. Try ipconfig /renew. Check if DHCP scope is exhausted (no more addresses available). Verify DHCP helper/relay agent if on different subnet. Check DHCP server service status."
    },
    {
        "domain": "Domain 5 – Network Troubleshooting",
        "topic": "Network Performance", "difficulty": "hard",
        "question": "A network analyst notices a high number of late collisions on a switched Ethernet segment. What is the MOST likely cause?",
        "choices": {"A":"A failing DNS server","B":"Duplex mismatch between the switch port and connected device","C":"Too many VLANs configured","D":"An incorrect subnet mask"},
        "answer": "B",
        "explanation": "Late collisions (collisions occurring after the first 64 bytes of a frame) are a classic sign of a duplex mismatch. Full-duplex devices don't use CSMA/CD — they can transmit and receive simultaneously. If one side is full-duplex and the other is half-duplex, the half-duplex side detects collisions that the full-duplex side doesn't expect. Symptoms: late collisions, runts (undersized frames), poor throughput. Solution: configure matching duplex settings (both auto-negotiate, or both set to the same speed/duplex manually). Best practice: let both sides auto-negotiate. Forcing one side causes the auto-negotiating side to assume half-duplex, causing mismatches. Regular collisions (not late) in a switched network suggest a hub or shared segment somewhere."
    },
]

# ══════════════════════════════════════════════════════════════════════════════
#  NETWORK+ GLOSSARY
# ══════════════════════════════════════════════════════════════════════════════

GLOSSARY_NETPLUS = {
    "802.1Q": "IEEE standard for VLAN tagging on trunk ports; adds 4-byte tag to Ethernet frames.",
    "802.1X": "Port-based Network Access Control; requires authentication before network access is granted.",
    "ARP": "Address Resolution Protocol — maps IP addresses to MAC addresses on a local network segment.",
    "APIPA": "Automatic Private IP Addressing — 169.254.0.0/16; self-assigned when DHCP is unavailable.",
    "BGP": "Border Gateway Protocol — exterior routing protocol used between autonomous systems on the internet.",
    "CIDR": "Classless Inter-Domain Routing — flexible IP prefix notation (e.g., 192.168.1.0/24).",
    "DAI": "Dynamic ARP Inspection — switch feature validating ARP messages against DHCP snooping table.",
    "DHCP snooping": "Switch security feature filtering DHCP traffic; builds binding table for DAI.",
    "DNS": "Domain Name System — resolves hostnames to IPs. Port 53. A/AAAA/MX/CNAME/PTR records.",
    "EIGRP": "Enhanced Interior Gateway Routing Protocol — Cisco proprietary, composite metric routing.",
    "FHRP": "First Hop Redundancy Protocol — HSRP/VRRP; provides gateway redundancy with virtual IP.",
    "Full duplex": "Simultaneous send and receive on a network link; no collisions possible.",
    "Half duplex": "Send or receive at one time (not both); CSMA/CD prevents collisions.",
    "HSRP": "Hot Standby Router Protocol — Cisco FHRP; active/standby with virtual IP for redundancy.",
    "IPsec": "IP Security — Layer 3 encryption protocol suite; AH (integrity) + ESP (encryption). Transport and Tunnel modes.",
    "LACP": "Link Aggregation Control Protocol (802.3ad) — bundles multiple links into one for bandwidth and redundancy.",
    "LDAP": "Lightweight Directory Access Protocol — port 389 (636 for LDAPS); directory query protocol.",
    "Link-local": "IPv6 FE80::/10 addresses auto-configured on every interface; not routable beyond local segment.",
    "MIB": "Management Information Base — database defining what SNMP-managed devices expose.",
    "NAT": "Network Address Translation — maps private IPs to public IPs for internet access.",
    "NetFlow": "Cisco protocol capturing IP flow metadata for traffic analysis and capacity planning.",
    "OSPF": "Open Shortest Path First — link-state routing protocol; cost metric; Dijkstra algorithm.",
    "OTDR": "Optical Time-Domain Reflectometer — tests fiber optic cable for breaks and measures distance.",
    "PAT": "Port Address Translation (NAT overload) — many private IPs share one public IP via port mapping.",
    "PortFast": "STP feature bypassing listening/learning states for access ports connected to end devices.",
    "QoS": "Quality of Service — prioritizes network traffic types (voice, video, data) to ensure performance.",
    "RADIUS": "Remote Authentication Dial-In User Service — ports 1812/1813; 802.1X authentication server.",
    "RIP": "Routing Information Protocol — distance-vector; hop count metric; max 15 hops; legacy protocol.",
    "RSTP": "Rapid Spanning Tree Protocol (802.1w) — faster convergence than original STP.",
    "SDN": "Software-Defined Networking — separates control plane from data plane for centralized management.",
    "SFTP": "SSH File Transfer Protocol — secure file transfer over SSH (port 22); encrypted.",
    "SNMP": "Simple Network Management Protocol — ports 161/162; v3 adds encryption and authentication.",
    "Spanning Tree": "STP (802.1D) — prevents Layer 2 loops by blocking redundant switch paths.",
    "Split horizon": "Routing loop prevention: don't advertise a route back on the interface it was learned from.",
    "Syslog": "Standard for system log messages; port 514; severity 0 (Emergency) to 7 (Debug).",
    "TACACS+": "Terminal Access Controller Access-Control System Plus — Cisco; separates AAA functions; TCP 49.",
    "TFTP": "Trivial FTP — port 69/UDP; unauthenticated; used for PXE boot and device firmware updates.",
    "Traceroute": "Maps each hop to a destination using incrementally increasing TTL values.",
    "Trunk port": "Switch port carrying tagged traffic for multiple VLANs (802.1Q); switch-to-switch links.",
    "VLAN": "Virtual LAN — logical Layer 2 network segment; traffic separation without physical separation.",
    "VRRP": "Virtual Router Redundancy Protocol — open FHRP standard; master/backup gateway redundancy.",
    "WPA3-Enterprise": "WPA3 with 802.1X/RADIUS authentication; individual credentials per user; no shared PSK.",
}
# ══════════════════════════════════════════════════════════════════════════════
#  CERT CONFIGURATION TABLE — ties everything together
# ══════════════════════════════════════════════════════════════════════════════

CERT_CONFIGS = {
    "secplus": {
        "name":           "CompTIA Security+  SY0-701",
        "code":           "SY0-701",
        "color":          C.TEAL,
        "pass_score":     750,
        "exam_q":         75,
        "questions":      QUESTIONS,
        "glossary":       GLOSSARY,
        "domain_theme":   DOMAIN_THEME_SECPLUS,
        "domain_weights": DOMAIN_WEIGHTS_SECPLUS,
        "dom_order":      DOM_ORDER_SECPLUS,
        "exam_objectives":EXAM_OBJECTIVES_SECPLUS,
    },
    "aplus1": {
        "name":           "CompTIA A+  Core 1  220-1201",
        "code":           "220-1201",
        "color":          C.ORG,
        "pass_score":     675,
        "exam_q":         90,
        "questions":      QUESTIONS_APLUS1,
        "glossary":       GLOSSARY_APLUS1,
        "domain_theme":   DOMAIN_THEME_APLUS1,
        "domain_weights": DOMAIN_WEIGHTS_APLUS1,
        "dom_order":      DOM_ORDER_APLUS1,
        "exam_objectives":EXAM_OBJECTIVES_APLUS1,
    },
    "aplus2": {
        "name":           "CompTIA A+  Core 2  220-1202",
        "code":           "220-1202",
        "color":          C.RED,
        "pass_score":     700,
        "exam_q":         90,
        "questions":      QUESTIONS_APLUS2,
        "glossary":       GLOSSARY_APLUS2,
        "domain_theme":   DOMAIN_THEME_APLUS2,
        "domain_weights": DOMAIN_WEIGHTS_APLUS2,
        "dom_order":      DOM_ORDER_APLUS2,
        "exam_objectives":EXAM_OBJECTIVES_APLUS2,
    },
    "netplus": {
        "name":           "CompTIA Network+  N10-009",
        "code":           "N10-009",
        "color":          C.SKY,
        "pass_score":     720,
        "exam_q":         90,
        "questions":      QUESTIONS_NETPLUS,
        "glossary":       GLOSSARY_NETPLUS,
        "domain_theme":   DOMAIN_THEME_NETPLUS,
        "domain_weights": DOMAIN_WEIGHTS_NETPLUS,
        "dom_order":      DOM_ORDER_NETPLUS,
        "exam_objectives":EXAM_OBJECTIVES_NETPLUS,
    },
}

# ══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        splash_main()
        while True:
            cert_key = cert_selector()
            cfg      = CERT_CONFIGS[cert_key]
            cert_splash(cfg)
            main_menu(cfg)
            # main_menu returns when user selects "Change Cert" (option 11)
    except KeyboardInterrupt:
        print(f"\n\n  {C.CYN}Session ended. Keep grinding — you've got this! 💪{C.RST}\n")
        sys.exit(0)
