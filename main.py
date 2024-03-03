import pygame
import random

#изображения для игры
background_image = pygame.image.load('images/image_with_nachos_cowboy.jpg')
icon = pygame.image.load('images/icon.png')
apple_pie_image = pygame.image.load('images/apple_pie_image.png')
medal_image = pygame.image.load('images/medal.png')
tim_image = pygame.image.load('images/tim_image.png')
boot_image = pygame.image.load('images/cowboy_boots.png')

# инициализатор
class CowboyGame:
    def __init__(self):
        pygame.init()
        self.screen_width = 1280
        self.screen_height = 720
        self.sound_type = 'none'
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/stop_cowboy_meme_song.mp3'), -1)
        self.play_sound()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Стоять, ковбой!")
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        self.good_positions = [self.screen_width // 2, self.screen_height - 30]
        self.bad_positions = []
        self.bad_speed = 3
        self.score = 0
        self.step = 30
        self.record = int(open('texts/record.txt','r').read())
        
        self.font = pygame.font.SysFont("Calibri", 50)
        self.run()

    # звуковая реакция на события
    def play_sound(self):
        if self.sound_type == 'win':
            pygame.mixer.music.load('sounds/toha_win_sound.mp3')
            pygame.mixer.music.play(1)
        elif self.sound_type == 'lose':
            pygame.mixer.Channel(0).pause()
            pygame.mixer.music.load('sounds/tim_loser_sound.mp3')
            pygame.mixer.music.play(1)

    # начало игры
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if self.good_positions[0] - self.step >= 0:
                            self.good_positions[0] -= self.step
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if self.good_positions[0] + self.step <= self.screen_width:
                            self.good_positions[0] += self.step
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        if self.good_positions[1] - self.step >= 0:
                            self.good_positions[1] -= self.step
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if self.good_positions[1] + self.step <= self.screen_height:
                            self.good_positions[1] += self.step

            # движение элементов
            for i in range(len(self.bad_positions)):
                self.bad_positions[i][1] += self.bad_speed

            # создание элементов
            if random.random() < 0.1:
                x = random.randint(0, self.screen_width)
                num = random.randint(1, 21)
                if num % 20 == 0:
                    self.bad_positions.append([x, 0, 'medal'])
                elif num % 2 == 0:
                    self.bad_positions.append([x, 0, 'pie'])
                else:
                    self.bad_positions.append([x, 0, 'boot'])
            
            # проверка столкновений с игроком
            for pos in self.bad_positions:
                if pos[2] == 'pie':
                    if abs(pos[0] + 32 - self.good_positions[0]) <= 32 and abs(pos[1] + 32 - self.good_positions[1] + 16) <= 32:
                        self.score += 1
                        self.sound_type = 'win'
                        self.play_sound()
                        self.bad_positions.remove(pos)
                elif pos[2] == 'medal':
                    if abs(pos[0] + 32 - self.good_positions[0]) <= 20 and abs(pos[1] + 32 - self.good_positions[1] + 20) <= 32:
                        self.score += 10
                        self.sound_type = 'win'
                        self.play_sound()
                        self.bad_positions.remove(pos)
                elif pos[2] == 'boot':
                    if abs(pos[0] + 32 - self.good_positions[0]) <= 16 and abs(pos[1] + 32 - self.good_positions[1] + 16) <= 32:
                        self.sound_type = 'lose'
                        self.play_sound()
                        self.game_over()

            # обновление рекорда на экране во время игры
            if self.score > self.record:
                self.record = self.score

            # убираем элементы за пределами окна
            self.bad_positions = [pos for pos in self.bad_positions if pos[1] < self.screen_height]

            # вывод фона
            self.screen.blit(background_image,(0, 0))

            # отрисовка элементов
            for pos in self.bad_positions:
                if pos[2] == 'pie':
                    self.screen.blit(apple_pie_image, (pos[:2]))
                elif pos[2] == 'medal':
                    self.screen.blit(medal_image, (pos[:2]))
                else:
                    self.screen.blit(boot_image, (pos[:2]))

            # отрисовка персонажа
            self.screen.blit(tim_image, (self.good_positions[0] - 32, self.good_positions[1] - 32))
            
            # обновление экрана
            self.draw_score()
            pygame.display.update()
            self.clock.tick(60)

    # проверка рекорда
    def check_record(self):
        self.record = open('texts/record.txt','r').read()
        if self.score > int(self.record):
            open('texts/record.txt', 'w').close()
            f2 = open('texts/record.txt','r+')
            f2.write(str(self.score))
            f2.close()

    # отрисовка очков и рекорда
    def draw_score(self):
        score_surface = self.font.render(f"Очки: {self.score}", True, (255, 255, 255))
        record_surface = self.font.render(f"Рекорд: {self.record}", True, (255, 255, 255))
        self.screen.blit(score_surface, (10, 60))
        self.screen.blit(record_surface, (10, 10))

    # проигрыш
    def game_over(self):
        self.check_record()
        message_surface = self.font.render(f"Игра закончена! Очки: {self.score}", True, (255, 0, 0))
        self.screen.blit(message_surface, (self.screen_width // 2 - message_surface.get_width() // 2, self.screen_height // 2 - message_surface.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(5000)
        pygame.quit()
        exit()

if __name__ == "__main__":
    CowboyGame()