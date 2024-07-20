import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

class IntroScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("2D Game - Intro")
        self.init_opengl()
        self.intro_texture = self.load_texture('assets/images/WhatsApp Image 2024-07-15 at 11.28.57 PM.jpeg')
        self.intro_music = 'assets/music/THE BATMAN Theme Michael Giacchino (Main Trailer Music).mp3'
        self.running = True

    def init_opengl(self):
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.width, 0, self.height)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glEnable(GL_TEXTURE_2D)

    def load_texture(self, image_path):
        img = pygame.image.load(image_path)
        img_data = pygame.image.tostring(img, "RGBA", 1)
        width, height = img.get_size()
        
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        
        return texture

    def run(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.intro_music)
        pygame.mixer.music.play(-1)

        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.running = False

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.draw_intro()

            pygame.display.flip()
            clock.tick(60)  # Limit frames per second to 60

        pygame.mixer.music.stop()

    def draw_intro(self):
        glBindTexture(GL_TEXTURE_2D, self.intro_texture)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(0, 0)
        glTexCoord2f(1, 0); glVertex2f(self.width, 0)
        glTexCoord2f(1, 1); glVertex2f(self.width, self.height)
        glTexCoord2f(0, 1); glVertex2f(0, self.height)
        glEnd()

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("2D Game")
        self.init_opengl()
        self.character_texture = self.load_texture('assets/images/imgbin_pixel-art-batman-png.png')
        self.item_texture = self.load_texture('assets/images/toppng.com-batman-logo-png-batman-symbol-black-and-white-2400x1303.png')
        self.obstacle_texture = self.load_texture('assets/images/—Pngtree—tips obstacle warning_1034699.png')
        self.platform_texture = self.load_texture('assets/images/WhatsApp Image 2024-07-19 at 10.49.25 PM.jpeg')
        self.background_texture = self.load_texture('assets/images/Gotham City Backgrounds - Wallpaper Cave.jpeg')
        self.character_pos = [width // 4, height // 4]
        self.character_velocity = 0
        self.gravity = -0.5
        self.jump_power = 10
        self.items = []
        self.obstacles = []
        self.score = 0
        self.lives = 5
        self.platform_y = 50
        self.running = True
        self.level = 1

        # Initialize Pygame mixer
        pygame.mixer.init()

    def init_opengl(self):
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.width, 0, self.height)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glEnable(GL_TEXTURE_2D)

    def load_texture(self, image_path):
        img = pygame.image.load(image_path)
        img_data = pygame.image.tostring(img, "RGBA", 1)
        width, height = img.get_size()
        
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        
        return texture

    def draw_quad(self, texture, x, y, width, height):
        glBindTexture(GL_TEXTURE_2D, texture)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(x, y)
        glTexCoord2f(1, 0); glVertex2f(x + width, y)
        glTexCoord2f(1, 1); glVertex2f(x + width, y + height)
        glTexCoord2f(0, 1); glVertex2f(x, y + height)
        glEnd()

    def spawn_item(self):
        x = self.width
        y = random.randint(self.platform_y + 20, self.height - 40)
        self.items.append([x, y])

    def spawn_obstacle(self):
        x = self.width
        y = random.randint(self.platform_y + 20, self.height - 40)
        self.obstacles.append([x, y])

    def run(self):
        pygame.mixer.music.load('assets/music/The Dark Knight Rises Official Soundtrack Despair Hans Zimmer WaterTower.mp3')
        pygame.mixer.music.play(-1)

        clock = pygame.time.Clock()
        item_timer = 0
        obstacle_timer = 0

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            if keys[K_SPACE] and self.character_pos[1] <= self.platform_y + 20:
                self.character_velocity = self.jump_power
            if keys[K_LEFT]:
                self.character_pos[0] -= 5
            if keys[K_RIGHT]:
                self.character_pos[0] += 5

            self.character_velocity += self.gravity
            self.character_pos[1] += self.character_velocity
            if self.character_pos[1] < self.platform_y:
                self.character_pos[1] = self.platform_y
            if self.character_pos[0] < 0:
                self.character_pos[0] = 0
            if self.character_pos[0] > self.width - 50:
                self.character_pos[0] = self.width - 50

            item_timer += 1
            obstacle_timer += 1
            if item_timer > 60:  # Spawn an item every second
                item_timer = 0
                self.spawn_item()
            if obstacle_timer > 90:  # Spawn an obstacle every 1.5 seconds
                obstacle_timer = 0
                self.spawn_obstacle()

            for item in self.items:
                item[0] -= 5
                if item[0] < 0:
                    self.items.remove(item)
                if self.character_pos[0] < item[0] < self.character_pos[0] + 50 and self.character_pos[1] < item[1] < self.character_pos[1] + 50:
                    self.items.remove(item)
                    self.score += 1

            for obstacle in self.obstacles:
                obstacle[0] -= 7
                if obstacle[0] < 0:
                    self.obstacles.remove(obstacle)
                if self.character_pos[0] < obstacle[0] < self.character_pos[0] + 50 and self.character_pos[1] < obstacle[1] < self.character_pos[1] + 50:
                    self.lives -= 1
                    self.obstacles.remove(obstacle)
                    if self.lives <= 0:
                        self.running = False  # End the game if lives are depleted

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.draw_quad(self.background_texture, 0, 0, self.width, self.height)
            self.draw_quad(self.character_texture, self.character_pos[0], self.character_pos[1], 50, 50)
            for item in self.items:
                self.draw_quad(self.item_texture, item[0], item[1], 30, 30)
            for obstacle in self.obstacles:
                self.draw_quad(self.obstacle_texture, obstacle[0], obstacle[1], 50, 50)
            self.draw_quad(self.platform_texture, 0, self.platform_y, self.width, 20)

            # Draw the score
            font = pygame.font.SysFont('Arial', 24)
            score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
            self.window.blit(score_text, (10, self.height - 30))

            # Draw the lives
            lives_text = font.render(f'Lives: {self.lives}', True, (255, 255, 255))
            self.window.blit(lives_text, (self.width - 150, self.height - 30))

            pygame.display.flip()
            clock.tick(60)  # Limit frames per second to 60

        pygame.mixer.music.stop()
        pygame.quit()
        print(f"Game Over! Your score: {self.score}")

if __name__ == "__main__":
    pygame.init()
    intro = IntroScreen(800, 600)
    intro.run()
    game = Game(800, 600)
    game.run()
