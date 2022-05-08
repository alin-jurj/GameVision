import pygame
from gui_elements import login_page,buttons
from database import queries

bkg_reg = pygame.image.load('assets/leaderboardbkg.png')
trophy_img = pygame.image.load('assets/trophy.png')
trophy_img = pygame.transform.scale(trophy_img,(100,100))
gold_img = pygame.image.load('assets/gold.png')
gold_img = pygame.transform.scale(gold_img,(40,50))
silver_img = pygame.image.load('assets/silver.png')
silver_img = pygame.transform.scale(silver_img,(40,50))
bronze_img = pygame.image.load('assets/bronze.png')
bronze_img = pygame.transform.scale(bronze_img,(40,50))
back_arrow = pygame.image.load('assets/back_arrow.png')
back_arrow = pygame.transform.scale(back_arrow,(40,50))

medals=[gold_img,silver_img,bronze_img]
FONT = pygame.font.Font(None, 68)
page_name=FONT.render("LEADERBOARD",True,"white")


FONT = pygame.font.Font(None, 50)
wins_text=FONT.render("W",True,"white")
losses_text=FONT.render("L",True,"white")
win_rate_text=FONT.render("WIN_RATE",True,"white")
#WIDTH, HEIGHT = 1280, 720
counter=0
old_win_rate=0
counter_medals=-1
count_given_medals=0
err=False
def print_fighter(screen,username,wins, losses,x):
    global old_win_rate,counter_medals,count_given_medals,err
    
    aux=(wins/(losses+wins))*100
    aux=int(aux)
    if err==False:
        if aux==old_win_rate:
            screen.blit(medals[counter_medals],(150, 300 + (50*count_given_medals)))
            count_given_medals=count_given_medals+1
        else:
            counter_medals=counter_medals+1
            if counter_medals==3:
                err=True
            if err==False:
                screen.blit(medals[counter_medals],(150, 300 + (50*count_given_medals)))  
                count_given_medals=count_given_medals+1
        if err==False:
            username=FONT.render(username,True,'white')
            screen.blit(username,(200, x))
            wins=FONT.render(str(wins),True,'white')
            screen.blit(wins,(550, x))
            losses=FONT.render(str(losses),True,'white')
            screen.blit(losses,(650, x))
            win_rate=FONT.render(str(aux)+"%",True,'white')
            screen.blit(win_rate,(750, x))
      
        old_win_rate=aux
def draw(screen):
    global counter, err,old_win_rate,counter_medals,count_given_medals
    back_button = buttons.Button('BACK',100,30,(100,50))
    running=True
    while running:
        
        screen.fill((0, 0, 0))
        screen.blit(bkg_reg, (0, 0))
        screen.blit(page_name,(460, 100))
        screen.blit(trophy_img,(350, 80))
        screen.blit(trophy_img,(820, 80))
        screen.blit(wins_text,(550,250))
        screen.blit(losses_text,(650,250))
        screen.blit(win_rate_text,(750,250))

    
        if back_button.draw(screen) == True:
           running=False
        #clock.tick(FPS)
        rows=queries.all_ordered_users_by_win_rate()
        counter=250
        for row in rows:
            counter=counter+50
            print_fighter(screen,row[1], row[4], row[5],counter)
        counter=0
        old_win_rate=0
        counter_medals=-1
        count_given_medals=0
        err=False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
                pygame.quit()
        pygame.display.update()