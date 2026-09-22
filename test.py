import pygame
import random
import string

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SYSTEM BREACH")
clock = pygame.time.Clock()

FONT_MONO = pygame.font.SysFont("consolas", 16)
FONT_BIG = pygame.font.SysFont("consolas", 46, bold=True)
FONT_SMALL = pygame.font.SysFont("consolas", 13)

GREEN = (30, 255, 90)
DARK_GREEN = (0, 90, 30)
RED = (255, 30, 40)
WHITE = (220, 255, 220)
BLACK = (0, 0, 0)

CHARS = string.ascii_uppercase + string.digits + "$#@%&*!?/\\"

# ---------- Matrix rain setup ----------
COL_W = 16
n_cols = WIDTH // COL_W
drops = [random.randint(-30, 0) for _ in range(n_cols)]
speeds = [random.uniform(0.3, 1.0) for _ in range(n_cols)]
col_chars = [[random.choice(CHARS) for _ in range(HEIGHT // COL_W + 30)] for _ in range(n_cols)]

# ---------- fake log lines (terminal ala hacker) ----------
LOG_POOL = [
    "bypassing firewall node 7A...",
    "injecting payload sequence...",
    "decrypting handshake token...",
    "scanning open ports 0-65535...",
    "spoofing MAC address...",
    "brute forcing auth layer 3...",
    "rerouting through proxy chain...",
    "extracting credential cache...",
    "disabling intrusion logger...",
    "cracking hash 4C9F...E12A...",
    "root access requested...",
    "overwriting audit trail...",
]
log_lines = []
log_timer = 0

# ---------- glitch title state ----------
title_text = "SYSTEM BREACH"
glitch_timer = 0

# ---------- alert flash state ----------
alert_active = False
alert_timer = 0
alert_cooldown = random.randint(120, 240)
progress = 0.0  # 0..100 "hacking progress"

frame = 0
running = True
while running:
    clock.tick(30)
    frame += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.fill(BLACK)

    # ================= MATRIX RAIN =================
    for i in range(n_cols):
        x = i * COL_W
        drops[i] += speeds[i]
        if drops[i] * COL_W > HEIGHT and random.random() < 0.02:
            drops[i] = random.randint(-20, 0)
            speeds[i] = random.uniform(0.3, 1.2)

        head_row = int(drops[i])
        for j in range(18):
            row = head_row - j
            if row < 0 or row * COL_W > HEIGHT:
                continue
            y = row * COL_W
            if random.random() < 0.02:
                col_chars[i][row % len(col_chars[i])] = random.choice(CHARS)
            ch = col_chars[i][row % len(col_chars[i])]

            if j == 0:
                color = WHITE
            else:
                fade = max(0, 255 - j * 16)
                color = (0, fade, int(fade * 0.35))

            glyph = FONT_MONO.render(ch, True, color)
            screen.blit(glyph, (x, y))

    # ================= TERMINAL LOG PANEL =================
    log_timer -= 1
    if log_timer <= 0:
        line = random.choice(LOG_POOL)
        log_lines.append(f"[{frame % 10000:04d}] {line}")
        if len(log_lines) > 12:
            log_lines.pop(0)
        log_timer = random.randint(8, 20)
        progress = min(100, progress + random.uniform(1, 4))

    panel_x, panel_y = 20, HEIGHT - 230
    panel_w, panel_h = 380, 210
    panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    pygame.draw.rect(panel_surf, (0, 20, 0, 190), (0, 0, panel_w, panel_h))
    pygame.draw.rect(panel_surf, DARK_GREEN, (0, 0, panel_w, panel_h), 2)
    screen.blit(panel_surf, (panel_x, panel_y))

    for idx, line in enumerate(log_lines):
        txt = FONT_SMALL.render(line, True, GREEN)
        screen.blit(txt, (panel_x + 10, panel_y + 10 + idx * 16))

    # progress bar di bawah panel
    bar_x, bar_y, bar_w, bar_h = panel_x, panel_y + panel_h + 10, panel_w, 14
    pygame.draw.rect(screen, DARK_GREEN, (bar_x, bar_y, bar_w, bar_h), 1)
    pygame.draw.rect(screen, GREEN, (bar_x, bar_y, int(bar_w * progress / 100), bar_h))
    pct_txt = FONT_SMALL.render(f"BREACH PROGRESS: {int(progress)}%", True, GREEN)
    screen.blit(pct_txt, (bar_x, bar_y - 18))

    # ================= GLITCH TITLE =================
    glitch_timer -= 1
    offset_x, offset_y = 0, 0
    display_text = title_text
    if glitch_timer <= 0:
        glitch_timer = random.randint(4, 14)
    if random.random() < 0.15:
        offset_x = random.randint(-6, 6)
        offset_y = random.randint(-3, 3)
        chars = list(title_text)
        if chars:
            idx = random.randint(0, len(chars) - 1)
            chars[idx] = random.choice(CHARS)
        display_text = "".join(chars)

    title_x, title_y = WIDTH // 2, 60
    for dx, dy, col in [(-3, 0, RED), (3, 0, (0, 255, 255)), (0, 0, WHITE)]:
        t = FONT_BIG.render(display_text, True, col)
        rect = t.get_rect(center=(title_x + dx + offset_x, title_y + dy + offset_y))
        screen.blit(t, rect)

    # ================= SCANLINES =================
    scan_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for y in range(0, HEIGHT, 3):
        pygame.draw.line(scan_surf, (0, 0, 0, 40), (0, y), (WIDTH, y))
    screen.blit(scan_surf, (0, 0))

    # ================= RANDOM ALERT FLASH (serem-seremnya di sini) =================
    alert_cooldown -= 1
    if alert_cooldown <= 0 and not alert_active:
        alert_active = True
        alert_timer = random.randint(10, 20)

    if alert_active:
        alert_timer -= 1
        flash_alpha = 90 if frame % 4 < 2 else 20
        flash_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        flash_surf.fill((*RED, flash_alpha))
        screen.blit(flash_surf, (0, 0))

        warn = FONT_BIG.render("INTRUSION DETECTED", True, RED)
        rect = warn.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        if frame % 6 < 4:
            screen.blit(warn, rect)

        pygame.draw.rect(screen, RED, (0, 0, WIDTH, HEIGHT), 8)

        if alert_timer <= 0:
            alert_active = False
            alert_cooldown = random.randint(150, 300)

    pygame.display.flip()

pygame.quit()