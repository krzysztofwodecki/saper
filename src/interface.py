import pygame as pg

black = (0, 0, 0)
white = (255, 255, 255)


def set_window(size=(400, 400), title=" ", color=white):
    """
    Funkcja tworząca okienko.
    :param size: rozmiar okna
    :param title: tytuł okna
    :param color: kolor tła
    :return: okno
    """
    pg.init()
    screen = pg.display.set_mode(size)
    pg.display.set_caption(title)
    screen.fill(color)
    pg.display.flip()
    return screen


def write_text(font, screen, text=" ", position=(0, 0), color=(0, 0, 0)):
    """
    Funkcja wypisująca zadany tekst w podanym miejscu.
    :param font: Używa wybranego przez nas fonta
    :param screen: Wyświetla tekst w zadanym oknie
    :param text: Tekst do wyświetlenia
    :param position: Pozycja tekstu na ekranie
    :param color: Kolor tekstu
    """
    img = font.render(text, True, color)
    screen.blit(img, position)


class FunctionalRectangle:
    def __init__(self, x, y, w, h, color=white):
        self.left = x
        self.top = y
        self.width = w
        self.height = h
        self.rect = pg.Rect(x, y, w, h)
        self.default_color = color
        self.color = color

    def draw(self, screen, thickness):
        pg.draw.rect(screen, self.color, self.rect, thickness)


class TextBox(FunctionalRectangle):
    def __init__(self, x, y, w, h, font, default_color=white):
        super().__init__(x, y, w, h, default_color)
        self.rect = pg.Rect(x, y, w, h)
        self.text = ""
        self.font = font
        self.txt_surface = font.render(self.text, True, self.color)
        self.active = False

    def event_handler(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = (0, 0, 0) if self.active else self.default_color
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key in [pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4,
                                   pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9]:
                    self.text += event.unicode
                    if len(self.text) > self.width // 10:
                        self.text = self.text[:-1]
                self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen, thickness=2):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        super().draw(screen, thickness)

    def get_value(self):
        try:
            value = int(self.text)
        except ValueError:
            value = 0
        return value

    def clear(self):
        self.text = ""
        self.txt_surface = self.font.render(self.text, True, self.color)


class Button(FunctionalRectangle):
    def __init__(self, x, y, w, h, default_color=white):
        super().__init__(x, y, w, h, default_color)

    def highlight(self, screen, thickness=0):
        mouse = pg.mouse.get_pos()

        if self.rect.x <= mouse[0] <= self.rect.x + self.rect.w \
                and self.rect.y <= mouse[1] <= self.rect.y + self.rect.h:
            a, b, c = self.default_color
            self.color = (a + 10 if a < 245 else 255, b + 10 if b < 245 else 255, c + 10 if c < 245 else 255)
            super().draw(screen, thickness)
        else:
            self.color = self.default_color
            super().draw(screen, thickness)

    def event_handler(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
            else:
                return False


class Interface:
    def __init__(self, screen, font, background_color):
        self.screen = screen
        self.font = font
        self.background_color = background_color
        self.boxes = [TextBox(5, 23, 45, 25, font), TextBox(75, 23, 45, 25, font),
                      TextBox(5, 73, 115, 25, font)]
        self.button = Button(295, 5, 95, 95, (160, 100, 100))
        self.attributes = []

    def display(self):
        self.screen.fill(self.background_color)

        for box in self.boxes:
            box.draw(self.screen)

        write_text(self.font, self.screen, "Rozmiar planszy:", (5, 5))
        write_text(self.font, self.screen, "Liczba min:", (5, 55))
        write_text(self.font, self.screen, "x", (59, 27))

        pg.draw.rect(self.screen, (160, 100, 100), pg.Rect(5, 160, 385, 385))

        pg.draw.line(self.screen, (0, 0, 0), (0, 105), (400, 105), 2)

        self.button.highlight(self.screen)

        pg.draw.polygon(self.screen, (0, 220, 0), [(325, 27), (325, 77), (365, 50)])

    def event_handler(self, event):
        self.attributes = []
        if self.button.event_handler(event):
            for box in self.boxes:
                if box.get_value() != 0:
                    self.attributes.append(box.get_value())
                box.clear()

        for box in self.boxes:
            box.event_handler(event)

        return self.attributes


class Field(FunctionalRectangle):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

    def event_handler(self, event):
        pass


class FieldWithMine(Field):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

    def event_handler(self, event):
        pass
