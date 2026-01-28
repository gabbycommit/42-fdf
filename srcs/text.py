
def title(text, dashboard, x, y):
    surf = dashboard.font_medium.render(text, True, (255, 255, 255))
    surf_rect = surf.get_rect(topleft=(x, y))
    dashboard.dashboard_surface.blit(surf, surf_rect)
    y += 30

    return y


def item(text, dashboard, x, y):
    surf = dashboard.font_small.render(text, True, (220, 220, 220))
    surf_rect = surf.get_rect(topleft=(x, y))
    dashboard.dashboard_surface.blit(surf, surf_rect)
    y += 20

    return surf_rect, y


def value(text, dashboard, item_rect, padding):
    surf = dashboard.font_small.render(text, True, (255, 157, 0))
    surf_rect = surf.get_rect(
        midleft=(item_rect.right + padding, item_rect.centery)
    )
    dashboard.dashboard_surface.blit(surf, surf_rect)