import pygame
import random

background_image = pygame.image.load('images/image_with_nachos_cowboy.jpg')
icon = pygame.image.load('images/icon.png')
apple_pie_image = pygame.image.load('images/apple_pie_image.png')
medal_image = pygame.image.load('images/medal.png')
tim_image = pygame.image.load('images/tim_image.png')
boot_image = pygame.image.load('images/cowboy_boots.png')

class RewardsBombs():
    def __init__(self):
        pygame.init()
        self.screen_width = 1280
        self.screen_height = 720
        self.sound_type = 'none'
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/background_music.mp3'), -1)
        self.play_sound()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Стоять, ковбой!")
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        self.green_pos = [self.screen_width // 2, self.screen_height - 30]
        self.red_positions = []
        self.red_speed = 3
        self.score = 0
        self.step = 20
        self.record = open('record.txt','r').read()
        
        self.font = pygame.font.SysFont("Calibri", 50)
        self.run()

    def play_sound(self):
        if self.sound_type == 'win':
            pygame.mixer.music.load('sounds/win_sound.mp3')
            pygame.mixer.music.play(1)
        elif self.sound_type == 'lose':
            pygame.mixer.Channel(0).pause()
            pygame.mixer.music.load('sounds/loser_sound.mp3')
            pygame.mixer.music.play(1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.green_pos[0] - self.step >= 0:
                            self.green_pos[0] -= self.step
                    elif event.key == pygame.K_RIGHT:
                        if self.green_pos[0] + self.step <= self.screen_width:
                            self.green_pos[0] += self.step
                    elif event.key == pygame.K_UP:
                        if self.green_pos[1] - self.step >= 0:
                            self.green_pos[1] -= self.step
                    elif event.key == pygame.K_DOWN:
                        if self.green_pos[1] + self.step <= self.screen_height:
                            self.green_pos[1] += self.step

            # движение ботинок
            for i in range(len(self.red_positions)):
                self.red_positions[i][1] += self.red_speed

            # создание бомб и призов
            if random.random() < 0.1:
                x = random.randint(0, self.screen_width)
                num = random.randint(1, 21)
                if num % 20 == 0:
                    self.red_positions.append([x, 0, 'medal'])
                elif num % 2 == 0:
                    self.red_positions.append([x, 0, 'pie'])
                else:
                    self.red_positions.append([x, 0, 'boot'])
            
            # проверка столкновений с игроком
            for pos in self.red_positions:
                if pos[2] == 'pie':
                    if abs(pos[0] + 32 - self.green_pos[0]) <= 32 and abs(pos[1] + 32 - self.green_pos[1]) <= 32:
                        self.score += 1
                        self.sound_type = 'win'
                        self.play_sound()
                        self.red_positions.remove(pos)
                elif pos[2] == 'medal':
                    if abs(pos[0] + 32 - self.green_pos[0]) <= 32 and abs(pos[1] + 32 - self.green_pos[1]) <= 32:
                        self.score += 10
                        self.sound_type = 'win'
                        self.play_sound()
                        self.red_positions.remove(pos)
                elif pos[2] == 'boot':
                    if abs(pos[0] + 32 - self.green_pos[0]) <= 22 and abs(pos[1] + 32 - self.green_pos[1]) <= 32:
                        self.sound_type = 'lose'
                        self.play_sound()
                        self.game_over()

            

            # убираем бомбы за пределами окна
            self.red_positions = [pos for pos in self.red_positions if pos[1] < self.screen_height]

            #выводим фон
            self.screen.blit(background_image,(0, 0))

            #жесткая ковбойская музыка
            


            for pos in self.red_positions:
                if pos[2] == 'pie':
                    self.screen.blit(apple_pie_image, (pos[:2]))
                elif pos[2] == 'medal':
                    self.screen.blit(medal_image, (pos[:2]))
                else:
                    self.screen.blit(boot_image, (pos[:2]))

            self.screen.blit(tim_image, (self.green_pos[0] - 32, self.green_pos[1] - 32))
            
            self.draw_score()
            pygame.display.update()
            self.clock.tick(60)

    def check_record(self):
        self.record = open('record.txt','r').read()
        
        if self.score > int(self.record):
            open('record.txt', 'w').close()
            f2 = open('record.txt','r+')
            f2.write(str(self.score))
            f2.close()

    def draw_score(self):
        score_surface = self.font.render(f"Очки: {self.score}", True, (255, 255, 255))
        record_surface = self.font.render(f"Рекорд: {self.record}", True, (255, 255, 255))
        self.screen.blit(score_surface, (10, 60))
        self.screen.blit(record_surface, (10, 10))

    def game_over(self):
        self.check_record()
        message_surface = self.font.render(f"Игра закончена! Очки: {self.score}", True, (255, 0, 0))
        self.screen.blit(message_surface, (self.screen_width // 2 - message_surface.get_width() // 2, self.screen_height // 2 - message_surface.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(5000)
        pygame.quit()
        exit()

if __name__ == "__main__":
    RewardsBombs()