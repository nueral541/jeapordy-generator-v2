import pygame

questions = {
    "Geography": {
        '100': {'question': 'What is the capital of France?', 'answer': 'Paris'},
        '200': {'question': 'Which continent is the Sahara Desert located in?', 'answer': 'Africa'},
        '300': {'question': 'What is the longest river in the world?', 'answer': 'The Nile River'},
        '400': {'question': 'Which country has the most islands?', 'answer': 'Sweden'},
        '500': {'question': 'What is the largest country in the world by area?', 'answer': 'Russia'}
    },
    "History": {
        '100': {'question': 'Who was the first President of the United States?', 'answer': 'George Washington'},
        '200': {'question': 'What year did World War II end?', 'answer': '1945'},
        '300': {'question': 'Which ancient civilization built the pyramids?', 'answer': 'The Egyptians'},
        '400': {'question': 'Who was the famous British Prime Minister during WWII?', 'answer': 'Winston Churchill'},
        '500': {'question': 'What was the name of the ship that sank in 1912 after hitting an iceberg?', 'answer': 'The Titanic'}
    },
    "Science": {
        '100': {'question': 'What planet is known as the Red Planet?', 'answer': 'Mars'},
        '200': {'question': 'What is the chemical symbol for water?', 'answer': 'H2O'},
        '300': {'question': 'What gas do plants absorb from the atmosphere?', 'answer': 'Carbon dioxide'},
        '400': {'question': 'What is the speed of light in a vacuum?', 'answer': '299,792 kilometers per second'},
        '500': {'question': 'What is the powerhouse of the cell?', 'answer': 'The mitochondria'}
    },
    "Literature": {
        '100': {'question': 'Who wrote "Romeo and Juliet"?', 'answer': 'William Shakespeare'},
        '200': {'question': 'What is the title of the first Harry Potter book?', 'answer': 'Harry Potter and the Philosopher\'s Stone'},
        '300': {'question': 'Who wrote "To Kill a Mockingbird"?', 'answer': 'Harper Lee'},
        '400': {'question': 'What is the name of the fictional land in "The Chronicles of Narnia"?', 'answer': 'Narnia'},
        '500': {'question': 'Which book begins with the line: "It was the best of times, it was the worst of times"?', 'answer': 'A Tale of Two Cities'}
    },
    "Pop Culture": {
        '100': {'question': 'Who is the lead singer of the band Queen?', 'answer': 'Freddie Mercury'},
        '200': {'question': 'What year was the first Star Wars movie released?', 'answer': '1977'},
        '300': {'question': 'Who voiced Woody in "Toy Story"?', 'answer': 'Tom Hanks'},
        '400': {'question': 'Which superhero is known as the "Caped Crusader"?', 'answer': 'Batman'},
        '500': {'question': 'What is the highest-grossing movie of all time?', 'answer': 'Avatar'}
    }
}

pygame.init()
screen = pygame.display.set_mode((1201, 721))
clock = pygame.time.Clock()
running = True

rects = []
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
    for i in questions.keys():
        text = font.render(i, True, "white")
        screen.blit(text, (20 + (e * 240), 50))
        x = 1
        for j in questions[i].keys():
            text = font.render(j, True, "white")
            screen.blit(text, (20 + (e * 240), 50 + (x * 120)))
            x += 1
        e += 1

def draw_rects(screen, rects, hovered_rect):
    for rect in rects:
        color = (0, 0, 255, 0)
        if rect == hovered_rect:
            color = (0, 0, 255, 80)
        transparent_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        transparent_surface.fill(color)
        screen.blit(transparent_surface, rect.topleft)

def handle_square_click(rect):
    category = "placeholder"
    question = "placeholder"
    answer = "placeholder"
    points = "placeholder"

while running:
    hovered_rect = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for rect in rects:
                if rect.collidepoint(event.pos):
                    handle_square_click(rect)


    mouse_pos = pygame.mouse.get_pos()

    for rect in rects:
        if rect.collidepoint(mouse_pos):
            hovered_rect = rect
            break

    screen.fill("darkblue")

    draw_grids(screen)
    draw_text(screen, questions)
    draw_rects(screen, rects, hovered_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
