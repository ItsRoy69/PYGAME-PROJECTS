
import math
import pygame
import random
from .misc import VelocityVector, VectorAddition


'''Pig'''
class Pig(pygame.sprite.Sprite):
    def __init__(self, screen, imagepaths, loc_info, velocity=None, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        assert len(loc_info) == 3
        assert len(imagepaths) == 3
        # Set the necessary property constant
        self.screen = screen
        self.loc_info = list(loc_info)
        self.imagepaths = imagepaths
        self.velocity = VelocityVector() if velocity is None else velocity
        self.type = 'pig'
        self.is_dead = False
        self.elasticity = 0.8
        self.switch_freq = 20
        self.animate_count = 0
        self.inverse_friction = 0.99
        self.gravity = VelocityVector(0.2, math.pi)
        # The screen size
        self.screen_size = screen.get_rect().size
        self.screen_size = (self.screen_size[0], self.screen_size[1] - 50)
        # Import the image
        self.pig_images = []
        for imagepath in imagepaths: self.pig_images.append(pygame.image.load(imagepath))
        # 设置当前图像
        self.image = random.choice(self.pig_images[:2])
    '''Draw to the screen'''
    def draw(self):
        self.animate_count += 1
        if (self.animate_count % self.switch_freq == 0) and (not self.is_dead):
            self.animate_count = 0
            self.image = random.choice(self.pig_images[:2])
        position = self.loc_info[0] - self.loc_info[2], self.loc_info[1] - self.loc_info[2]
        self.screen.blit(self.image, position)
    '''Move the pig'''
    def move(self):
        # Change the pig's velocity vector according to gravity
        self.velocity = VectorAddition(self.velocity, self.gravity)
        self.loc_info[0] += self.velocity.magnitude * math.sin(self.velocity.angle)
        self.loc_info[1] -= self.velocity.magnitude * math.cos(self.velocity.angle)
        self.velocity.magnitude *= self.inverse_friction
        # Width exceeds the screen
        if self.loc_info[0] > self.screen_size[0] - self.loc_info[2]:
            self.loc_info[0] = 2 * (self.screen_size[0] - self.loc_info[2]) - self.loc_info[0]
            self.velocity.angle *= -1
            self.velocity.magnitude *= self.elasticity
        elif self.loc_info[0] < self.loc_info[2]:
            self.loc_info[0] = 2 * self.loc_info[2] - self.loc_info[0]
            self.velocity.angle *= -1
            self.velocity.magnitude *= self.elasticity
        # Height exceeds the screen
        if self.loc_info[1] > self.screen_size[1] - self.loc_info[2]:
            self.loc_info[1] = 2 * (self.screen_size[1] - self.loc_info[2]) - self.loc_info[1]
            self.velocity.angle = math.pi - self.velocity.angle
            self.velocity.magnitude *= self.elasticity
        elif self.loc_info[1] < self.loc_info[2]:
            self.loc_info[1] = 2 * self.loc_info[2] - self.loc_info[1]
            self.velocity.angle = math.pi - self.velocity.angle
            self.velocity.magnitude *= self.elasticity
    '''The pig died'''
    def setdead(self):
        self.is_dead = True
        self.image = self.pig_images[-1]


'''birdie'''
class Bird(pygame.sprite.Sprite):
    def __init__(self, screen, imagepaths, loc_info, velocity=None, color=(255, 255, 255), **kwargs):
        pygame.sprite.Sprite.__init__(self)
        assert len(loc_info) == 3
        assert len(imagepaths) == 1
        # Set the necessary property constant
        self.color = color
        self.screen = screen
        self.loc_info = list(loc_info)
        self.imagepaths = imagepaths
        self.velocity = VelocityVector() if velocity is None else velocity
        self.type = 'bird'
        self.fly_path = []
        self.is_dead = False
        self.elasticity = 0.8
        self.is_loaded = False
        self.is_selected = False
        self.inverse_friction = 0.99
        self.gravity = VelocityVector(0.2, math.pi)
        # The screen size
        self.screen_size = screen.get_rect().size
        self.screen_size = (self.screen_size[0], self.screen_size[1] - 50)
        # Import the image
        self.image = pygame.image.load(imagepaths[0])
    '''Draw to the screen'''
    def draw(self):
        if not self.is_loaded:
            for point in self.fly_path:
                pygame.draw.ellipse(self.screen, self.color, (point[0], point[1], 3, 3), 1)
        position = self.loc_info[0] - self.loc_info[2], self.loc_info[1] - self.loc_info[2]
        self.screen.blit(self.image, position)
    '''Determine if it has been selected by the mouse'''
    def selected(self):
        pos = pygame.mouse.get_pos()
        dx, dy = pos[0] - self.loc_info[0], pos[1] - self.loc_info[1]
        dist = math.hypot(dy, dx)
        if dist < self.loc_info[2]:
            return True
        return False
    '''Load onto the slingshot'''
    def load(self, slingshot):
        self.loc_info[0], self.loc_info[1] = slingshot.x, slingshot.y
        self.is_loaded = True
    '''Reset the position'''
    def reposition(self, slingshot):
        pos = pygame.mouse.get_pos()
        if self.selected:
            self.loc_info[0], self.loc_info[1] = pos[0], pos[1]
            dx, dy = slingshot.x - self.loc_info[0], slingshot.y - self.loc_info[1]
            self.velocity.magnitude = min(int(math.hypot(dx, dy) / 2), 80)
            self.velocity.angle = math.pi / 2 + math.atan2(dy, dx)
    '''Displays the path to launch the bird'''
    def projectpath(self):
        if self.is_loaded:
            path = []
            bird = Bird(self.screen, self.imagepaths, self.loc_info, velocity=self.velocity)
            for i in range(30):
                bird.move()
                if i % 5 == 0: path.append((bird.loc_info[0], bird.loc_info[1]))
            for point in path:
                pygame.draw.ellipse(self.screen, self.color, (point[0], point[1], 2, 2))
    '''Move the bird'''
    def move(self):
        # Change the bird's velocity vector according to gravity
        self.velocity = VectorAddition(self.velocity, self.gravity)
        self.loc_info[0] += self.velocity.magnitude * math.sin(self.velocity.angle)
        self.loc_info[1] -= self.velocity.magnitude * math.cos(self.velocity.angle)
        self.velocity.magnitude *= self.inverse_friction
        # Width exceeds the screen
        if self.loc_info[0] > self.screen_size[0] - self.loc_info[2]:
            self.loc_info[0] = 2 * (self.screen_size[0] - self.loc_info[2]) - self.loc_info[0]
            self.velocity.angle *= -1
            self.velocity.magnitude *= self.elasticity
        elif self.loc_info[0] < self.loc_info[2]:
            self.loc_info[0] = 2 * self.loc_info[2] - self.loc_info[0]
            self.velocity.angle *= -1
            self.velocity.magnitude *= self.elasticity
        # Height exceeds the screen
        if self.loc_info[1] > self.screen_size[1] - self.loc_info[2]:
            self.loc_info[1] = 2 * (self.screen_size[1] - self.loc_info[2]) - self.loc_info[1]
            self.velocity.angle = math.pi - self.velocity.angle
            self.velocity.magnitude *= self.elasticity
        elif self.loc_info[1] < self.loc_info[2]:
            self.loc_info[1] = 2 * self.loc_info[2] - self.loc_info[1]
            self.velocity.angle = math.pi - self.velocity.angle
            self.velocity.magnitude *= self.elasticity


'''The pieces of wood in the map'''
class Block(pygame.sprite.Sprite):
    def __init__(self, screen, imagepaths, loc_info, velocity=None, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        assert len(loc_info) == 3
        assert len(imagepaths) == 2
        # Set the necessary property constant
        self.type = 'block'
        self.screen = screen
        self.loc_info = list(loc_info)
        self.imagepaths = imagepaths
        self.velocity = VelocityVector() if velocity is None else velocity
        self.elasticity = 0.7
        self.is_destroyed = False
        self.inverse_friction = 0.99
        self.gravity = VelocityVector(0.2, math.pi)
        # Import the image
        self.block_images = []
        for imagepath in imagepaths: self.block_images.append(pygame.transform.scale(pygame.image.load(imagepath), (100, 100)))
        # The screen size
        self.screen_size = screen.get_rect().size
        self.screen_size = (self.screen_size[0], self.screen_size[1] - 50)
        # Set the current image
        self.image = self.block_images[0]
        self.rect = self.image.get_rect()
        self.rotate_angle = math.radians(0)
    '''Set the current image'''
    def draw(self):
        pygame.transform.rotate(self.image, self.rotate_angle)
        self.screen.blit(self.image, (self.loc_info[0] - self.rect.width // 2, self.loc_info[1]))
    '''Set to damaged'''
    def setdestroy(self):
        self.is_destroyed = True
        self.image = self.block_images[1]
    '''Move the wooden block'''
    def move(self):
        # Change the velocity vector of the block according to gravity
        self.velocity = VectorAddition(self.velocity, self.gravity)
        self.loc_info[0] += self.velocity.magnitude * math.sin(self.velocity.angle)
        self.loc_info[1] -= self.velocity.magnitude * math.cos(self.velocity.angle)
        self.velocity.magnitude *= self.inverse_friction
        # Width exceeds the screen
        if self.loc_info[0] > self.screen_size[0] - self.rect.width:
            self.loc_info[0] = 2 * (self.screen_size[0] - self.rect.width) - self.loc_info[0]
            self.velocity.angle *= -1
            self.rotate_angle = -self.velocity.angle
            self.velocity.magnitude *= self.elasticity
        elif self.loc_info[0] < self.rect.width:
            self.loc_info[0] = 2 * self.rect.width - self.loc_info[0]
            self.velocity.angle *= -1
            self.rotate_angle = -self.velocity.angle
            self.velocity.magnitude *= self.elasticity
        # Height exceeds the screen
        if self.loc_info[1] > self.screen_size[1] - self.rect.height:
            self.loc_info[1] = 2 * (self.screen_size[1] - self.rect.height) - self.loc_info[1]
            self.velocity.angle = math.pi - self.velocity.angle
            self.rotate_angle = math.pi - self.velocity.angle
            self.velocity.magnitude *= self.elasticity
        elif self.loc_info[1] < self.rect.height:
            self.loc_info[1] = 2 * self.rect.height - self.loc_info[1]
            self.velocity.angle = math.pi - self.velocity.angle
            self.rotate_angle = math.pi - self.velocity.angle
            self.velocity.magnitude *= self.elasticity


'''slingshot'''
class Slingshot(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, width, height, color=(66, 73, 73), line_color=(100, 30, 22), **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.screen = screen
        self.line_color = line_color
        self.type = 'slingshot'
    '''Draw to the screen'''
    def draw(self, bird=None):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y + self.height * 1 / 3, self.width, self.height * 2 / 3))
        if bird is not None and bird.is_loaded:
            pygame.draw.line(self.screen, self.line_color, (self.x, self.y + self.height / 6), (bird.loc_info[0], bird.loc_info[1] + bird.loc_info[2] / 2), 10)
            pygame.draw.line(self.screen, self.line_color, (self.x + self.width, self.y + self.height / 6), (bird.loc_info[0] + bird.loc_info[2], bird.loc_info[1] + bird.loc_info[2] / 2), 10)
        pygame.draw.rect(self.screen, self.color, (self.x - self.width / 4, self.y, self.width / 2, self.height / 3), 5)
        pygame.draw.rect(self.screen, self.color, (self.x + self.width * 3 / 4, self.y, self.width / 2, self.height / 3), 5)


'''Wall'''
class Slab(pygame.sprite.Sprite):
    def __init__(self, screen, imagepaths, x, y, width, height, color=(255, 255, 255)):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.screen = screen
        self.imagepaths = imagepaths
        if self.width > self.height:
            self.image = pygame.image.load(self.imagepaths[0])
        else:
            self.image = pygame.image.load(self.imagepaths[1])
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.type = 'wall'
    '''Draw to the screen'''
    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))


'''Button class'''
class Button(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, width, height, action=None, color_not_active=(189, 195, 199), color_active=(189, 195, 199)):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        self.screen = screen
        self.color_active = color_active
        self.color_not_active = color_not_active
    '''Add text'''
    def addtext(self, text, size=20, font='Times New Roman', color=(0, 0, 0)):
        self.font = pygame.font.Font(font, size)
        self.text = self.font.render(text, True, color)
        self.text_pos = self.text.get_rect()
        self.text_pos.center = (self.x + self.width / 2, self.y + self.height / 2)
    '''Whether it is selected by the mouse'''
    def selected(self):
        pos = pygame.mouse.get_pos()
        if (self.x < pos[0] < self.x + self.width) and (self.y < pos[1] < self.y + self.height):
            return True
        return False
    '''Draw to the screen'''
    def draw(self):
        if self.selected():
            pygame.draw.rect(self.screen, self.color_active, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(self.screen, self.color_not_active, (self.x, self.y, self.width, self.height))
        if hasattr(self, 'text'):
            self.screen.blit(self.text, self.text_pos)


'''The text label class'''
class Label(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
    '''Add text'''
    def addtext(self, text, size=20, font='Times New Roman', color=(0, 0, 0)):
        self.font = pygame.font.Font(font, size)
        self.text = self.font.render(text, True, color)
        self.text_pos = self.text.get_rect()
        self.text_pos.center = (self.x + self.width / 2, self.y + self.height / 2)
    '''Draw to the screen'''
    def draw(self):
        if hasattr(self, 'text'):
            self.screen.blit(self.text, self.text_pos)