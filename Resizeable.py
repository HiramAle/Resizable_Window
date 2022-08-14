import pygame
import sys
import ctypes

ctypes.windll.user32.SetProcessDPIAware()

# Colors
white = (255, 255, 255)
red = (255, 114, 118)


def get_aspect_ratio(width, height):
    division = width / height
    if division == 16 / 9:
        aspect_ratio = "16:9"
    elif division == 16 / 10:
        aspect_ratio = "16:10"
    elif division == 4 / 3:
        aspect_ratio = "4:3"
    elif division == 5 / 4:
        aspect_ratio = "5:4"
    else:
        aspect_ratio = "None Detected"
    return aspect_ratio


class Game:
    def __init__(self):
        pygame.init()
        # Display Info
        self.display_width = pygame.display.Info().current_w
        self.display_height = pygame.display.Info().current_h
        self.aspect_ratio = get_aspect_ratio(self.display_width, self.display_height)
        # Set display
        self.display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("Resizable Window")
        # Game utilities
        self.game_canvas = pygame.surface.Surface((self.display_width, self.display_height))
        self.clock = pygame.time.Clock()
        # Font
        self.font_50 = pygame.font.Font("monogram.ttf", 50)
        # Instructions
        self.instructions_render = self.font_50.render("Change Size", False, white)
        self.instructions_rect = self.instructions_render.get_rect()
        # AspectRatio / Sizes
        self.sizes = pygame.display.list_modes()
        # Mouse
        self.mouse_x = 0
        self.mouse_y = 0
        # Resolution options
        self.resolution = self.sizes[0]
        self.resolution_options_render = None
        self.resolution_options_rect = None
        self.resolution_options_color = white
        # Display Mode
        self.display_mode = "Windowed"
        self.display_modes = ["Fullscreen", "Windowed"]
        self.display_mode_render = None
        self.display_mode_rect = None
        self.display_mode_color = white
        # Apply Button
        self.apply_btn_render = self.font_50.render("Apply", False, white)
        self.apply_btn_rect = self.apply_btn_render.get_rect(center=(self.display_width / 2, 800))
        self.apply_btn_color = white

    def set_display_info(self):
        self.display_width = self.resolution[0]
        self.display_height = self.resolution[1]
        pygame.display.set_caption("Resizable Window")

    def display_percentage(self, axis, pos):
        if axis == "x":
            return (float(self.display_width)) * float(pos) / 1920
        elif axis == "y":
            return (float(self.display_height) * float(pos)) / 1080

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if self.resolution_options_rect.collidepoint(self.mouse_x, self.mouse_y):
                    index = self.sizes.index(self.resolution)
                    if index < len(self.sizes) - 1:
                        self.resolution = self.sizes[index + 1]
                    else:
                        self.resolution = self.sizes[0]
                elif self.display_mode_rect.collidepoint(self.mouse_x, self.mouse_y):
                    index = self.display_modes.index(self.display_mode)
                    if index < len(self.display_modes) - 1:
                        self.display_mode = self.display_modes[index + 1]
                    else:
                        self.display_mode = self.display_modes[0]
                elif self.apply_btn_rect.collidepoint(self.mouse_x, self.mouse_y):
                    pygame.display.quit()
                    pygame.display.init()
                    if self.display_mode == "Fullscreen":
                        self.display = pygame.display.set_mode((self.resolution[0], self.resolution[1]),
                                                               pygame.FULLSCREEN)
                    else:
                        self.display = pygame.display.set_mode((self.resolution[0], self.resolution[1]))
                    self.set_display_info()


    def render(self):
        # Blit and fill game canvas
        self.display.blit(self.game_canvas, (0, 0))
        self.game_canvas.fill("#262626")
        # Instructions
        self.instructions_rect = self.instructions_render.get_rect(
            center=(self.display_width / 2, self.display_percentage("y", 200)))
        # Mouse coords
        mouse_pos = self.font_50.render(f"({self.mouse_x},{self.mouse_y})", False, white)
        # Resolution Options
        self.resolution_options_render = self.font_50.render(f"{self.resolution[0]} x {self.resolution[1]}", False,
                                                             self.resolution_options_color)
        self.resolution_options_rect = self.resolution_options_render.get_rect(
            center=(self.display_width / 2, self.display_percentage("y", 500)))
        # Display mode
        self.display_mode_render = self.font_50.render(f"{self.display_mode}", False, self.display_mode_color)
        self.display_mode_rect = self.display_mode_render.get_rect(
            center=(self.display_width / 2, self.display_percentage("y", 600)))
        # Apply button
        self.apply_btn_render = self.font_50.render("Apply", False, self.apply_btn_color)
        self.apply_btn_rect = self.apply_btn_render.get_rect(
            center=(self.display_width / 2, self.display_percentage("y", 800)))
        # Blit ON game canvas
        self.game_canvas.blit(mouse_pos, (0, 0))
        self.game_canvas.blit(self.resolution_options_render, self.resolution_options_rect)
        self.game_canvas.blit(self.display_mode_render, self.display_mode_rect)
        self.game_canvas.blit(self.apply_btn_render, self.apply_btn_rect)
        self.game_canvas.blit(self.instructions_render, self.instructions_rect)
        pygame.display.update()

    def update(self):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        if self.resolution_options_rect.collidepoint(self.mouse_x, self.mouse_y):
            self.resolution_options_color = red
        else:
            self.resolution_options_color = white

        if self.display_mode_rect.collidepoint(self.mouse_x, self.mouse_y):
            self.display_mode_color = red
        else:
            self.display_mode_color = white

        if self.apply_btn_rect.collidepoint(self.mouse_x, self.mouse_y):
            self.apply_btn_color = red
        else:
            self.apply_btn_color = white

    def main_loop(self):
        while True:
            self.event_loop()
            self.render()
            self.update()
            self.clock.tick(60)


if __name__ == '__main__':
    game = Game()
    game.main_loop()
