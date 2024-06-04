import pygame as pg
import sys, random, time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
TROLL_COLOR = (0, 255, 0)
FOOD_COLOR = (125, 125, 0)
OBSTICALE_COLOR = (150, 150, 150)

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700

ITEM_WIDTH_HEIGHT = 40

FPS = 60

SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

class Game:
    def __init__(self):
        # Initialize Pygame
        pg.init()
        
        self.foods = []
        self.score = 0  # Initialize score

        # Create the main window
        self.screen = pg.display.set_mode(SIZE)
        pg.display.set_caption("Pac-troll")

        # Create a clock
        self.clock = pg.time.Clock()
        
        self.running = True
        self.obstacles = []  # Initialize obstacles list

        # Initialize font
        self.font = pg.font.Font(None, 36)  # Use default font, size 36

    # Method to run the game
    def run(self):
        self.player = Player(ITEM_WIDTH_HEIGHT, TROLL_COLOR, 2)
        self.foods = self.create_foods(3)  # Create three food blocks
        
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        
        print(f"Du beveget deg ut av banen, men du fikk {self.score} i score")
        pg.quit()
        sys.exit()
        
    # Method to handle events
    def events(self):
        # Loop through events
        for event in pg.event.get():
            # Check if we want to close the window
            if event.type == pg.QUIT:
                self.running = False

    # Method to update the game state
    def update(self):
        self.player.update()
        
        # Check for player collision with food
        for food in self.foods[:]:  # Iterate over a copy of the list
            if self.player.player_rect.colliderect(food.food_rect):
                obstacle = Obstacle(food.item_length, OBSTICALE_COLOR)
                obstacle.make_rect(food.food_x, food.food_y)
                self.obstacles.append(obstacle)
                
                self.foods.remove(food)
                self.foods = self.create_foods(1)
                self.score += 1  # Increment score
                self.player.player_speed += 0.25
        
        current_time = time.time()
        for obstacle in self.obstacles[:]:  # Iterate over a copy of the list
            if self.player.player_rect.colliderect(obstacle.obstacle_rect) and current_time - obstacle.creation_time > 1:
                print("Du traff en hindring!")
                self.running = False
        
    # Method to draw everything on the screen
    def draw(self):
        # Fill the screen with a color
        self.screen.fill(BLACK)
        
        self.player.draw(self.screen)
        
        # Draw the obstacles
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        # Draw the foods
        for food in self.foods:
            food.draw(self.screen)
        
        # Render the score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))  # Draw score at top left corner
        
        # Flip the display to show what we have drawn
        pg.display.flip()

    def create_foods(self, num_foods):
        
        for _ in range(num_foods):
            while True:
                new_food = Food(ITEM_WIDTH_HEIGHT, FOOD_COLOR)
                if not any(new_food.food_rect.colliderect(existing_food.food_rect) for existing_food in self.foods) and \
                   not new_food.food_rect.colliderect(self.player.player_rect) and \
                   not any(new_food.food_rect.colliderect(obstacle.obstacle_rect) for obstacle in self.obstacles):
                    self.foods.append(new_food)
                    break
        return self.foods

class Items:
    def __init__(self, item_length, color):
        self.item_length = item_length
        self.item_color = color

class Player(Items):
    def __init__(self, player_length, player_color, speed):
        super().__init__(player_length, player_color)
        self.player_speed = speed
        self.player_x = WINDOW_WIDTH / 2 - self.item_length / 2
        self.player_y = WINDOW_HEIGHT / 2 - self.item_length / 2
        
        self.last_pressed = ""
        
        self.player_rect = pg.Rect(self.player_x, self.player_y, player_length, player_length)
        
    def update(self):
        keys = pg.key.get_pressed()
        
        if keys[pg.K_LEFT]:
            self.player_x -= self.player_speed
            self.last_pressed = "l"
        elif keys[pg.K_DOWN]:
            self.player_y += self.player_speed
            self.last_pressed = "d"
        elif keys[pg.K_RIGHT]:
            self.player_x += self.player_speed
            self.last_pressed = "r"
        elif keys[pg.K_UP]:
            self.player_y -= self.player_speed
            self.last_pressed = "u"
        elif self.last_pressed == "l":
            self.player_x -= self.player_speed
        elif self.last_pressed == "r":
            self.player_x += self.player_speed
        elif self.last_pressed == "u":
            self.player_y -= self.player_speed
        elif self.last_pressed == "d":
            self.player_y += self.player_speed
            
        # Update player_rect with the new position
        self.player_rect.x = self.player_x
        self.player_rect.y = self.player_y
        
        if (self.player_x < 0) or (self.player_x > WINDOW_WIDTH - self.item_length) or (self.player_y < 0) or (self.player_y > WINDOW_HEIGHT - self.item_length):
            game_object.running = False
    
    def draw(self, screen):
        pg.draw.rect(screen, self.item_color, self.player_rect)
        
class Food(Items):
    def __init__(self, food_length, food_color):
        super().__init__(food_length, food_color)
        self.food_x = random.randint(0, WINDOW_WIDTH - self.item_length)
        self.food_y = random.randint(0, WINDOW_HEIGHT - self.item_length)
        
        self.food_rect = pg.Rect(self.food_x, self.food_y, food_length, food_length)
        
    def draw(self, screen):
        pg.draw.rect(screen, self.item_color, self.food_rect)
        
class Obstacle(Food):
    def __init__(self, item_length, color):
        super().__init__(item_length, color)
        self.creation_time = time.time()  # Add creation time
        
    def make_rect(self, x, y):
        self.obstacle_rect = pg.Rect(x, y, self.item_length, self.item_length)
        
    def draw(self, screen):
        pg.draw.rect(screen, self.item_color, self.obstacle_rect)
        

# Create a game object
game_object = Game()

# Game loop
game_object.run()