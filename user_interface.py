from pygame.font import Font
from pygame import Surface
from pygame.draw import rect

class Info_Box:
    def __init__(self, screen: Surface) -> None:
        self.screen = screen
        self.days = 0
        self.font1 = Font("freesansbold.ttf", 20)

    def show_days(self) -> None:
        text = self.font1.render("Days: %.2f" % self.days, True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.topleft = (30, 10)
        self.screen.blit(text, textRect)

    def show_object_status(self, info: dict) -> None:
        pos = [30, 60]
        for key, item in info.items():
            text = self.font1.render(f"{key}: {item}", True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.topleft = pos
            self.screen.blit(text, textRect)
            pos[1] += 30


class Terminal:
    def __init__(self, screen: Surface, position: list[int, int]) -> None:
        self.screen = screen
        self.position = position
        self.text = f"Terminal: "
        self.font1 = Font("freesansbold.ttf", 15)
        self.active = False
        self.height = 50
    
    def show_terminal(self) -> None:
        color = (255, 255, 255) if self.active == True else (150, 150, 150)
        text = self.font1.render(self.text, True, color)
        textRect = text.get_rect()
        textRect.topleft = self.position
        self.screen.blit(text, textRect)