import pygame 
import random
import time

from pygame.constants import K_ESCAPE, K_KP_ENTER, K_RETURN, K_SPACE, K_r, K_x

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE= (0, 0, 255)
RED = (255, 0, 0)
GRAY = (189, 189, 189)
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BALL_SIZE = 25
Count = 0
beforeCount = 0


class Ball:
    '''공을 표현하는 클래스'''
    def __init__(self):
        #공의 중심 좌표를 임의로 지정 
        self.x = random.randrange(BALL_SIZE, SCREEN_WIDTH - BALL_SIZE)
        self.y = random.randrange(BALL_SIZE, SCREEN_HEIGHT - BALL_SIZE)

        #다음 이동 방향을 설정
        self.change_x = 0
        while self.change_x == 0 or self.change_y == 0:
            self.change_x = random.randint(-4, 4)
            self.change_y = random.randint(-4, 4)

        #공의 색상을 지정 
        r = random.randint(1, 255)
        g = random.randint(1, 255)
        b = random.randint(1, 255)
        self.color = (r, g, b)

        
# 메인 프로그램
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("파이썬 미니 프로젝트") 
clock = pygame.time.Clock()

# 여러 볼의 갖는 리스트 생성
lstballs = []

# 시작시간 체크
startTime = int(time.time())
remainTime = 0
gameState = 3

done = False
while not done:
    clock.tick(60) 
    screen.fill(WHITE)
    if gameState == 0:
        # 제한시간 30초
        remainTime = 30 - (int(time.time()) - startTime)

        # 0초가 되면 게임오버
        if remainTime  <= 0:
            gameState = 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # 스페이스 바를 누르면 일시정지
            elif event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    gameState = 2
                

            # 마우스로 공을 클릭하면 공이 사라지고 점수가 올라감
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for ball in lstballs: 
                    if x + BALL_SIZE/2 > ball.x >  x - BALL_SIZE/2 and y + BALL_SIZE/2 > ball.y  > y- BALL_SIZE/2:
                        Count += 1
                
                    if Count > beforeCount:
                        lstballs.remove(ball)
                        beforeCount = Count

        for ball in lstballs:
            # 볼의 중심 좌표를 이동
            ball.x += ball.change_x
            ball.y += ball.change_y

            # 윈도 벽에 맞고 바운싱
            # x 좌표가 위 이래를 벗어나면   
            if ball.x > SCREEN_WIDTH - BALL_SIZE or ball.x < BALL_SIZE:
                ball.change_x *= -1 #다음 이동 좌표의 증가 값을 부호 변경 

            #y 좌표가 위 이래를 벗어나면   
            if ball.y > SCREEN_HEIGHT - BALL_SIZE or ball.y < BALL_SIZE:
                ball.change_y *= -1 #다음 이동 좌표의 증가 값을 부호 변경 

        # 공이 0개가 되면 랜덤하게 공을 출력
        if len(lstballs) == 0:
            for i in range(random.randint(1, 5)):
                lstballs.append(Ball())

        # 공의 개수를 우측상단에 나타냄
        countFont = pygame.font.SysFont(None, 30)  #폰트 설정
        countText = countFont.render('Ball Count {}'.format(len(lstballs)),True,BLUE)
        screen.blit(countText,(650, 20)) 

        # 점수카운트
        pointFont = pygame.font.SysFont(None, 30)  #폰트 설정
        pointText = pointFont.render('Point {}'.format(Count),True,BLUE)
        screen.blit(pointText,(30, 20)) 

        # 남은 시간 표시
        timeFont = pygame.font.SysFont(None, 50)  #폰트 설정
        timeText = timeFont.render('Time {}'.format(remainTime),True,BLUE)
        screen.blit(timeText,(SCREEN_WIDTH // 2 - timeText.get_width() // 2, 20)) 

    # 게임 오버
    elif gameState == 1:
        # 게임 오버 출력
        gameOverFont = pygame.font.SysFont(None, 80)
        gameOverText = gameOverFont.render('GameOver', True, RED)
        screen.blit(gameOverText, (SCREEN_WIDTH // 2 - gameOverText.get_width() // 2, SCREEN_HEIGHT // 3 - gameOverText.get_height() // 2))

        # 안내 문자 출력
        guideFont = pygame.font.SysFont(None, 50)
        guideText = guideFont.render('Retry Press "R" and Quit Press "X" ', True, BLACK)
        screen.blit(guideText, (SCREEN_WIDTH // 2 - guideText.get_width() // 2, (SCREEN_HEIGHT // 2 - gameOverText.get_height() // 2 ) + 80))

        pointFont = pygame.font.SysFont(None, 50)  #폰트 설정
        pointText = pointFont.render('Point {}'.format(Count),True,BLUE)
        screen.blit(pointText,(30, 20)) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # r키를 누르면 다시시작 x키를 누르면 종료
            if event.type == pygame.KEYDOWN:
                if event.key == K_r:
                    gameState = 0
                    startTime = int(time.time())
                    Count = 0
                    beforeCount = 0
                    lstballs = []
                if event.key == K_x:
                    done = True

    # 일시정지
    elif gameState == 2:
        # 일시정지 문자 출력
        gamePauseFont = pygame.font.SysFont(None, 80)
        gamePauseText = gamePauseFont.render('Pause', True, GRAY)
        screen.blit(gamePauseText, (SCREEN_WIDTH // 2 - gamePauseText.get_width() // 2, SCREEN_HEIGHT // 3 - gamePauseText.get_height() // 2))
        
        # 안내 문자 출력
        guideFont = pygame.font.SysFont(None, 50)
        guideText = guideFont.render('Return Press "R" and Quit Press "X" ', True, BLACK)
        screen.blit(guideText, (SCREEN_WIDTH // 2 - guideText.get_width() // 2, (SCREEN_HEIGHT // 2 - gamePauseText.get_height() // 2 ) + 80))
        
        # r을 누르면 게임화면으로 돌아가고 x를 누르면 게임 종료
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_r:
                    gameState = 0
                if event.key == K_x:
                    done = True

    # 시작화면
    elif gameState == 3:
        # 게임 이름 출력
        gameStartFont = pygame.font.SysFont(None, 80)
        gameStartText = gameStartFont.render('BouncingBall Click Game', True, BLACK)
        screen.blit(gameStartText, (SCREEN_WIDTH // 2 - gameStartText.get_width() // 2, SCREEN_HEIGHT // 3 - gameStartText.get_height() // 2))

        # 시작 문자 출력
        startFont = pygame.font.SysFont(None, 50)
        startText = startFont.render('Start', True, BLUE)
        screen.blit(startText, (SCREEN_WIDTH // 2 - startText.get_width() // 2, (SCREEN_HEIGHT // 2 - gameStartText.get_height() // 2 ) + 80))
        
        # 나가기 출력
        quitFont = pygame.font.SysFont(None, 50)
        quitText = quitFont.render('QUIT', True, BLUE)
        screen.blit(quitText, (SCREEN_WIDTH // 2 - quitText.get_width() // 2, (SCREEN_HEIGHT // 2 - gameStartText.get_height() // 2 ) + 140))

        # start를 클릭하면 시작되고 quit를 클릭하면 종료된다.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if (SCREEN_WIDTH // 2 - startText.get_width() // 2) <= x <= ((SCREEN_WIDTH // 2 - startText.get_width() // 2) + startText.get_width()) and ((SCREEN_HEIGHT // 2 - gameStartText.get_height() // 2 ) + 80) <= y <= (((SCREEN_HEIGHT // 2 - gameStartText.get_height() // 2 ) + 80) + startText.get_height()):
                    gameState = 0
                    for i in range(3):
                        lstballs.append(Ball())
                if (SCREEN_WIDTH // 2 - quitText.get_width() // 2) <= x <= ((SCREEN_WIDTH // 2 - quitText.get_width() // 2) + quitText.get_width()) and ((SCREEN_HEIGHT // 2 - gameStartText.get_height() // 2 ) + 140) <= y <= (((SCREEN_HEIGHT // 2 - gameStartText.get_height() // 2 ) + 140) + quitText.get_height()):
                    done = True

    # 볼 그리기
    for ball in lstballs:
        pygame.draw.circle(screen, ball.color, [ball.x, ball.y], BALL_SIZE )
    
    pygame.display.flip()
pygame.quit()
