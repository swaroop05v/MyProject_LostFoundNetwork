import pygame


def _pt(center, size, x, y):
    """Map a point in unit space (-0.5..0.5) to screen space."""
    cx, cy = center
    return (round(cx + x * size), round(cy + y * size))


def _pts(center, size, points):
    return [_pt(center, size, x, y) for x, y in points]


def draw_rock(surface, center, size):
    outline_w = max(2, round(size * 0.05))

    body = _pts(center, size, [
        (-0.42, 0.14), (-0.36, -0.16), (-0.14, -0.37), (0.14, -0.36), (0.37, -0.17),
        (0.45, 0.10), (0.31, 0.34), (-0.04, 0.40), (-0.33, 0.32),
    ])
    top_face = _pts(center, size, [
        (-0.30, -0.10), (-0.12, -0.29), (0.12, -0.28), (0.28, -0.12), (0.10, -0.02), (-0.14, -0.02),
    ])
    crack = _pts(center, size, [(0.06, 0.02), (0.14, 0.16), (0.08, 0.30)])

    pygame.draw.polygon(surface, (128, 128, 138), body)
    pygame.draw.polygon(surface, (168, 168, 178), top_face)
    pygame.draw.lines(surface, (85, 85, 95), False, crack, max(1, round(size * 0.03)))
    pygame.draw.polygon(surface, (60, 60, 70), body, outline_w)


def draw_paper(surface, center, size):
    outline_w = max(2, round(size * 0.04))
    left, right, top, bottom = -0.31, 0.31, -0.40, 0.40
    fold = 0.18

    sheet = _pts(center, size, [
        (left, top), (right - fold, top), (right, top + fold), (right, bottom), (left, bottom),
    ])
    flap = _pts(center, size, [(right - fold, top), (right - fold, top + fold), (right, top + fold)])

    pygame.draw.polygon(surface, (245, 245, 240), sheet)
    pygame.draw.polygon(surface, (205, 208, 215), flap)

    line_w = max(1, round(size * 0.03))
    for y, end_x in ((-0.12, 0.23), (0.02, 0.23), (0.16, 0.23), (0.28, 0.05)):
        pygame.draw.line(surface, (150, 165, 195), _pt(center, size, left + 0.08, y), _pt(center, size, end_x, y), line_w)

    pygame.draw.polygon(surface, (70, 75, 90), sheet, outline_w)
    pygame.draw.polygon(surface, (70, 75, 90), flap, outline_w)


def draw_scissors(surface, center, size):
    blade_w = max(2, round(size * 0.08))
    ring_r = max(3, round(size * 0.13))
    ring_w = max(2, round(size * 0.05))

    # Each blade runs from its handle ring, through the pivot, to the opposite tip
    blades = [((0.20, 0.30), (-0.30, -0.42)), ((-0.20, 0.30), (0.30, -0.42))]

    for ring, tip in blades:
        start, end = _pt(center, size, *ring), _pt(center, size, *tip)
        pygame.draw.line(surface, (55, 58, 68), start, end, blade_w + 2)
        pygame.draw.line(surface, (205, 210, 220), start, end, blade_w)

    for ring, _ in blades:
        c = _pt(center, size, *ring)
        pygame.draw.circle(surface, (55, 58, 68), c, ring_r + 1, ring_w + 2)
        pygame.draw.circle(surface, (215, 60, 60), c, ring_r, ring_w)

    pygame.draw.circle(surface, (55, 58, 68), _pt(center, size, 0, 0.012), max(2, round(size * 0.045)))


_DRAWERS = {
    "ROCK": draw_rock,
    "PAPER": draw_paper,
    "SCISSORS": draw_scissors,
}


def draw_icon(surface, choice, center, size):
    _DRAWERS[choice](surface, center, size)