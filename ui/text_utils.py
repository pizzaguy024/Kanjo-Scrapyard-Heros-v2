import pygame


def draw_wrapped_text(surface, text, x, y, max_width, line_height, font, color, max_y):
    lines = []

    for raw_line in text.split("\n"):
        if raw_line.strip() == "":
            lines.append("")
            continue

        words = raw_line.split(" ")
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "

        lines.append(current_line)

    for line in lines:
        if y > max_y:
            more = font.render("...press ENTER to continue", True, (220, 40, 50))
            surface.blit(more, (x, y))
            break

        rendered = font.render(line, True, color)
        surface.blit(rendered, (x, y))
        y += line_height
