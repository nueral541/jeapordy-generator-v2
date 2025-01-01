import pygame
import tkinter as tk
from question_gen import question_gen

questions = question_gen()

pygame.init()
screen = pygame.display.set_mode((1201, 721))
clock = pygame.time.Clock()
running = True

rects = []
completed_rects = set()

for x in range(0, 1201, 240):
    for y in range(120, 721, 120):
        rects.append(pygame.Rect(x, y, 240, 120))

def draw_grids(screen):
    for x in range(0, 1201, 240):
        pygame.draw.line(screen, "white", (x, 0), (x, 720), 7)
    for y in range(0, 721, 120):
        pygame.draw.line(screen, "white", (0, y), (1200, y), 7)

def draw_text(screen, questions):
    font = pygame.font.Font(None, 36)
    e = 0
    for category in questions.keys():
        # Wrap the category text
        wrapped_text = wrap_text(category, font, 200)
        
        # Render and display each wrapped line
        y_offset = 50  # Starting position for the category text
        for line in wrapped_text:
            text = font.render(line, True, "white")
            screen.blit(text, (20 + (e * 240), y_offset))
            y_offset += font.get_height()  # Move to the next line vertically

        # Now render the point values for the category
        x = 1
        for points in questions[category].keys():
            text = font.render(points, True, "white")
            screen.blit(text, (20 + (e * 240), 50 + (x * 120)))
            x += 1
        
        e += 1

def draw_rects(screen, rects, hovered_rect):
    for rect in rects:
        if (rect.x, rect.y, rect.width, rect.height) in completed_rects:

            color = (0, 0, 0, 180)  # Darker color with transparency
        elif rect == hovered_rect:
            color = (0, 0, 255, 60)  # Hover color
        else:
            color = (0, 0, 255, 0)  # Default color
        
        transparent_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        transparent_surface.fill(color)
        screen.blit(transparent_surface, rect.topleft)

def handle_square_click(rect):
    if (rect.x, rect.y, rect.width, rect.height) in completed_rects:
        return

    category_index = int(rect.x / rect.width)
    category = list(questions.keys())[category_index]
    points_index = int((rect.y - 120) / rect.height)
    points = list(questions[category].keys())[points_index]

    question = questions[category][points]['question']
    answer = questions[category][points]['answer']
    create_text_window(category, points, question, answer)


def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = []

    for word in words:
        # Create a test line by adding the word
        test_line = ' '.join(current_line + [word])

        # If the line fits within the max width, add the word to the line
        if font.size(test_line)[0] <= max_width:
            current_line.append(word)
        else:
            # If the line doesn't fit, start a new line with the current word
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    # Add the last line
    if current_line:
        lines.append(' '.join(current_line))

    return lines

# Modify the create_text_window to use the wrap_text function
def create_text_window(category, points, question, answer):
    reveal_answer = False
    font = pygame.font.Font(None, 36)
    max_width = 600  # Maximum width for text wrapping
    wrapped_text = wrap_text(question, font, max_width)

    line_height = font.get_height()
    total_height = len(wrapped_text) * line_height + 20

    question_surface = pygame.Surface((max_width + 40, total_height))
    answer_surface = font.render(answer, True, (255, 255, 255))
    question_surface.fill('darkblue')

    y_offset = 10
    for line in wrapped_text:
        text_surface = font.render(line, True, (255, 255, 255))
        question_surface.blit(text_surface, (20, y_offset))
        y_offset += line_height

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reveal_answer = not reveal_answer

        screen.fill('darkblue')
        if not reveal_answer:
            screen.blit(question_surface, ((1200 - (max_width + 40)) // 2, (720 - total_height) // 2))
        else:
            screen.blit(answer_surface, ((1200 - (max_width + 40)) // 2, (720 - total_height) // 2))

            rect_to_remove = next(
                (rect for rect in rects if rect.x == 240 * list(questions.keys()).index(category) and rect.y == 120 + 120 * list(questions[category].keys()).index(points)),
                None
            )
            if rect_to_remove:
                completed_rects.add((rect_to_remove.x, rect_to_remove.y, rect_to_remove.width, rect_to_remove.height))

        pygame.display.flip()


while running:
    hovered_rect = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for rect in rects:

                if rect.collidepoint(event.pos) and (rect.x, rect.y, rect.width, rect.height) not in completed_rects:
                    handle_square_click(rect)

    screen.fill(("darkblue"))
    mouse_pos = pygame.mouse.get_pos()

    for rect in rects:
        if rect.collidepoint(mouse_pos):
            hovered_rect = rect
            break

    draw_grids(screen)
    draw_text(screen, questions)
    draw_rects(screen, rects, hovered_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
