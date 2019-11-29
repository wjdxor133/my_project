import pygame # pygame 라이브러리를 import한다.
import random
import time
from time import sleep
#pip install pygame 해야 실행됨

WHITE = (255, 255, 255) # 게임 창을 바탕을 흰색으로 지정
BLACK = (0,0,0)
# 게임 창의 너비와 높이 설정
pad_width = 1024 
pad_height = 512

#게임 안에서 모든 캐릭터 크기를 동일하게 맞출려고 선언
characters_width = 149
characters_height = 145

#생명선 초기값
healthvalue = 295

#보물상자 크기
box_width = 109
box_height = 105

#적 이미지 크기
bad_width = 149
bad_height = 145

#장애물의 이미지 크기를 변수에 참조하게 설정
fireball1_width = 140
fireball1_height = 80
fireball2_width = 86
fireball2_height = 80



""" 내가 쓸려고 만든 함수들 """   

#내가 조정할 캐릭터를 게임판 위(x,y) 위치에 그린다.    
def playerpos(x,y): 
    gamepad.blit(player, (x,y))

#배경화면 그리는 함수 선언
def back(x,y):
    gamepad.blit(background, (x,y))

#박스 그리는 함수
def Box(obj,x,y):
    gamepad.blit(box, (x,y))

#생명바 표시
def healthBar(obj,x,y):
    gamepad.blit(healthbar, (x,y))
    

#장애물 그리는 함수
def fireball(obj,x,y):
    gamepad.blit(obj, (x,y))
    

#적 그리는 함수
def badboy(x,y):
    gamepad.blit(bad, (x,y))

#총알 그리는 함수
def hit(obj,x,y):
    gamepad.blit(bullet, (x,y))

#적이 총에 맞았을 때 함수
def shotBat(obj,x,y):
    gamepad.blit(bad,(x,y))

#적이 총에 맞아서 사라질 때 함수
def BoomBoom(obj,x,y):
    gamepad.blit(boom,(x,y))
    
#게임화면에 표시될 텍스트 모양과 영역 설정 함수
def textObj(text,font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

#게임 다시시작 함수
def play_again():
    global gamepad, youlose, countdown
    
    largeText = pygame.font.Font("freesansbold.ttf",72)
    TextSurf,TextRect = textObj("Replay?",largeText)
    TextRect.center = ((pad_width/2),(pad_height/1.8))
    gamepad.blit(TextSurf, TextRect)
    pygame.display.update()
    sleep(0.8)
    youlose.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                    #R키를 누르면 다시 시작
                    if event.key == pygame.K_r:     
                        countdown = 31
                        runGame()

#게임 끝 함수
def play_end():
    global gamepad, youwinsound
    
    largeText = pygame.font.Font("freesansbold.ttf",72)
    TextSurf,TextRect = textObj("END",largeText)
    TextRect.center = ((pad_width/2),(pad_height/1.8))
    gamepad.blit(TextSurf, TextRect)
    pygame.display.update()
    youwinsound.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            

#시간 텍스트로 나타내기
def timer():
    font = pygame.font.Font("freesansbold.ttf",24)
    survivedtext = font.render(str(countdown),True, (0,0,0))
    textRect = survivedtext.get_rect()
    textRect.topright=[1024,5]
    gamepad.blit(survivedtext, textRect)

#게임화면 중앙에 텍스트 띄우는 함수
def dispMessage(code):
    global gamepad
    
    if code == 1:
        gamepad.blit(youwin,(0,0))
        play_end()

    else:
        gamepad.blit(gameover,(0,0))
        play_again()

    
            
#적들에게 공격을 받았을 때 함수
def crash():
    dispMessage(0)

#이겼을 때 함수
def win():
    dispMessage(1)


   
    
""" 실제 게임이 구동되는 함수 """

def runGame():
     #runGame()함수에서 쓰여지는 전역변수 선언
    global gamepad, player, keys, clock, health, healthbar, healthvalue, start_time, countdown, firelocation, badlocation 
    global bad, fires, bullet, boom
    global shoot, damage1, damage2, smallness, youwinsound, still, youlose    

    x = pad_width *0.05 #캐릭터의 위치를 뜻하는 변수
    y = pad_height * 0.05

    bullet_xy = [] # Ctrl키를 누를 때마다, 총알의 위치를 나타내는 좌표

    #파이어볼, 적 나오는 위치 설정
    firelocation = [59.6, 159.6, 259.6, 359.6]
    badlocation = [9.6, 109.6, 209.6, 309.6]

    #적이 날아오는 위치 설정
    bad_x = pad_width                               # x축은 게임판 맨 오른쪽 끝
    bad_y = random.choice(badlocation)         # y축은 게임판 높이에서 무작위로 선택

    #장애물 날아오는 위치 설정(자료형이 리스트인 fires를 무작위로 섞고, 첫번째 요소를 선택
    fire_x = pad_width                              # x축은 게임판 맨 오른쪽 끝
    fire_y = random.choice(firelocation)       #0 ~ 게임 창 높이까지 무작위로 뽑을 범위 설정
    random.shuffle(fires)                           #shuffle() 함수를 이용해서 fires[]안에 있는 요소들을 뒤죽박죽 섞어 놓는 함수
    fire = fires[0]                                 # 섞은 후 첫번째 요소를 선택해서 참조 변수에 담음 -> 즉, 랜덤으로 파이어볼이 담길 수도 있고, None값이 담길 수도 있음

    #캐릭터의 방향을 조절 공간
    keys = [False,False,False,False]
    
    #공격키
    attack = [False]

    #총알이 적을 명중했는지 안했는지 판단하기 위한 변수
    isShotBat = False
    
    #폭발 이미지가 화면에 표시되는 시간을 나타내는 변수
    boom_count = 0


    #초기 제한시간
    countdown = 30
        
    
    while True:

        character_now = x                           # 캐릭터 원래 위치
        if start_time < (int(time.time())):         #제한시간 설정
                countdown -= 1
                start_time = (int(time.time()))
        
        for event in pygame.event.get():            #pygame.event.get() 게임 창에서 발생한 이벤트를 리턴해줌
            if event.type == pygame.QUIT:
                pygame.quit()                       #게임을 중지시키고
                exit(0)                             #종료

           
            #키가 눌러졌을 때
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    
                    keys[0]= True
                elif event.key == pygame.K_LEFT:
                    keys[1]= True
                elif event.key == pygame.K_RIGHT:
                    keys[2]= True                    
                elif event.key == pygame.K_DOWN:
                    keys[3]= True
                elif event.key == pygame.K_LCTRL:
                    attack[0] = True
                    shoot.play()
               
            #키가 눌러지지 않았을 때
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP: 
                        keys[0]= False
                elif event.key == pygame.K_LEFT:
                        keys[1]= False
                elif event.key == pygame.K_RIGHT:
                        keys[2]= False
                elif event.key == pygame.K_DOWN:
                        keys[3]= False
                elif event.key == pygame.K_LCTRL:
                        attack[0] = False

            if keys[0]:
                y = y - 100
            elif keys[1]:
                x = x - 100
            elif keys[2]:
                x = x + 100
            elif keys[3]:
                y = y + 100

            #주인공 이동 범위 
            if y > 400:
                y = 9.6
            elif y < 0:
                y = 309.6

            # 캐릭터의 위치가 보물 상자 뒤로 가지 못하게 설정
            if x < 0:
                x = character_now
                
            
            #총알이 나오는 위치 설정
            if attack[0]:                                   #총알을 쏘면 총알이 나오는 위치를 캐릭터 크기에 맞게 설정
                bullet_x = x + characters_width 
                bullet_y = y + characters_height/2          #캐릭터 키의 나누기 2한 값
                bullet_xy.append([bullet_x,bullet_y])

        
        
        gamepad.fill(WHITE)                                 #게임 창 화면 흰색 적용
        back(0,0)                                           #배경 이미지를 게임 창과 같은 크기로 설정 해 놓았기 때문에 x,y의 값은 각각 0,0이어야 화면이 다 채워짐
        
        #박스의 위치
        Box(box, 0,70)
        Box(box, 0,160)
        Box(box, 0,255)
        Box(box, 0,345)

        #보여질 시간 호출 함수
        timer()
       
        
        
        #시간 안에 안죽으면 이기게 설정
        if countdown == 0:
            win()
            
        #생명선이 다 없어지면 게임 끝나게 설정   
        if healthvalue <= 0:
            crash()

      
        #생명바의 위치와 생명바의 생명줄 시작위치를 x,y축으로 표시
        healthBar(healthbar, 5,5)
        for health1 in range(healthvalue):
            gamepad.blit(health, (health1+8,8))
            
        


        #적이 나와서 지나가서 사라지게 설정
        bad_x -= 5                                                      # 적이 나오면서 계속 -5씩 픽셀값이 감소
        if bad_x <= 0:
            healthvalue -= random.randint(20,40)                         # 적에게 보물을 내어줬을 때, 생명선 깍이게 설정
            bad_x = pad_width                                           # 다시 원래 맨 오른쪽으로 감
            bad_y = random.randrange(100, (pad_height - 120))           # 다시 랜덤으로 높이에서 아무데서 적이 나옴
            still.play()

            
        #장애물의 지가나는 속도 설정
        if fire == None:
                fire_x -= 30
        else:
                fire_x -= 15
                
                
        #장애물(파이어볼)이 나와서 사라지게 끔 설정
        if fire_x <= 0:
                fire_x = pad_width
                fire_y = random.choice(firelocation)
                random.shuffle(fires)
                fire = fires[0]
            
            
        
                
                

        #총알로 공격 설정
        if len(bullet_xy) != 0:
            for i, bxy in enumerate(bullet_xy):
                bxy[0] += 15                                            #총알 속도를 설정
                bullet_xy[i][0] = bxy[0]
                hit(bullet, bxy[0], bxy[1])                             #총을 그리게 설정
                if bxy[0] > bad_x:
                    if bxy[1] > bad_y and bxy[1] < bad_y + characters_height:
                        bullet_xy.remove(bxy)                           #총알이 사리지고
                        isShotBat = True                                #적을 명중 했을 때의 값을  True로 설정
                                                                        #게임 화면 창에서 벗어나면 사라지게 설정
                        

                if bxy[0] >= pad_width:                                 #총알이 게임화면을 벗어나면
                    try:
                        bullet_xy.remove(bxy)                           #사라지게 설정
                    except:
                        pass


        
        #적과 충돌했는지 체크하는 알고리즘
        if x + characters_width/2 > bad_x:  #캐릭터 x축 위치 + 캐릭터 너비/2한 값> 적의 x축 값보다 크면
            if(y> bad_y and y < bad_y + bad_height) or (y + characters_height/2 > bad_y and y + characters_height/2 < bad_y + bad_height ):                 
                damage1.play()
                crash()

        #파이어볼 크기 설정
        if fire[1] != None:
            if fire[0] == 0:
                fireball_width = fireball1_width
                fireball_height = fireball1_height
            elif fire[0] == 1:
                fireball_width = fireball2_width
                fireball_height = fireball2_height
        #장애물 출동 체크 알고리즘
            if x + characters_width > fire_x:
                if(y > fire_y + fireball_height and y < fire_y + fireball_height) or ((y + characters_height/2 > fire_y) and (y + characters_height/2 < fire_y + fireball_height)):
                    damage2.play()
                    crash()
                    
        #적이 총에 맞았을 때
        if not isShotBat:
            shotBat(bad, bad_x, bad_y) # 총에 맞아서 적이 사라지는게 하는 함수

        else:
            BoomBoom(boom, bad_x,bad_y) 
            boom_count +=1          # 적이 사라질 때의 쿨타임
            if boom_count > 5:      # 적이 나오고 나서 사라지는 알고리즘
                boom_count = 0      # while문 5번 돌때까지, 화면에 표시 된 후, 다시 등장
                bad_x = pad_width
                bad_y = random.choice(badlocation)
                isShotBat = False
            smallness.play() 
                
                
            
        badboy(bad_x, bad_y)        # 적이 화면에 보이는 함수
                
        if fire[1] != None:         # 장애물[1]이 None이 아니면 화면에 fire[1]을 화면에 그림 
            fireball(fire[1], fire_x, fire_y)
            

            
        
        playerpos(x,y)              # 캐릭터 위치
        pygame.display.update()
        clock.tick(60)
            
                       





""" 게임을 초기화하고 시작하는 함수 """

def initGame():
    global gamepad, player, clock, background, box, health, healthbar, gameover, youwin, start_time
    global bad, fires, bullet, boom
    global shoot, damage1, damage2, smallness, youwinsound, still, youlose

    fires = []                                                                              #불덩어리 2개와 None 객체 5개를 담을 리스
                     
    pygame.init()                                                                           # pygame을 활용하려면 최초에 항상 pygame.init()을 호출해야 함
                                                                                            # 즉, 우리의 코드는 이제 pygame에서 제공하는 다양한 기능을 사용할 준비가 됬다는 뜻
    gamepad = pygame.display.set_mode((pad_width, pad_height))
    pygame.display.set_caption('MyGame')                                                    #게임 창에 뜨는 제목
    player = pygame.image.load("resource/images/pygame_me.png")                             #캐릭터 이미지
    background = pygame.image.load("resource/images/background.jpg")                        # 배경 이미지
    box = pygame.image.load("resource/images/box.png")
    health =  pygame.image.load("resource/images/health.png")
    healthbar =  pygame.image.load("resource/images/healthbar.png")
    bad = pygame.image.load("resource/images/bad.png")                                      # 적 이미지
    gameover = pygame.image.load("resource/images/gameover.png")
    youwin = pygame.image.load("resource/images/youwin.png") 
    fires.append((0,pygame.image.load("resource/images/fireball.png")))                         # 파이어 볼01 이미지
    fires.append((1,pygame.image.load("resource/images/fireball2.png")))                        # 파이어 볼02 이미지
    #리스트 변수인 fire의 멤버를(숫자,이미지 객체)로 수정
    #이는 불덩어리의 이미지 크기가 다르므로 어떤 불덩어리 이미지에 우리 비행기가 충돌했는지 체크그하기 위해서

    for i in range(3):
            fires.append((i+2,None))
                 
    bullet = pygame.image.load("resource/images/bullet.png")                                # 총알 이미지
    boom = pygame.image.load("resource/images/boom.png")                                    # 적이 죽었을 때 이미

    #효과음 모음
    pygame.mixer.music.load("resource/audio/34 - Absolute Death!.mp3")
    pygame.mixer.music.play(-1,0.0)         #BGM 무한반복
    pygame.mixer.music.set_volume(0.25)     #소리 크기   
    shoot = pygame.mixer.Sound("resource/audio/shoot.wav")
    damage1 = pygame.mixer.Sound("resource/audio/die1.wav")
    damage2 = pygame.mixer.Sound("resource/audio/die2.wav")
    smallness = pygame.mixer.Sound("resource/audio/smallenss.wav")
    youwinsound = pygame.mixer.Sound("resource/audio/youwin.wav")
    still = pygame.mixer.Sound("resource/audio/helpme.wav")
    youlose = pygame.mixer.Sound("resource/audio/youlose.wav")
    shoot.set_volume(0.05)                  # 소리 크기
    damage1.set_volume(0.05)
    damage2.set_volume(0.05)
    smallness.set_volume(0.03)
    youwinsound.set_volume(1)
    still.set_volume(1)
    youlose.set_volume(1)

    clock = pygame.time.Clock()                                                             #게임의 초당 프레임 설정을 위해 클락을 생성(사람 눈에 자연스럽게 보이는 FPS로 설정)
    start_time = time.time()            #window의 시간
    runGame()                           #게임 시작

initGame()
