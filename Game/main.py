import pygame as pg
import os
from gui_elements import FieldsButtons
import database.connectors as cn
import mysql.connector
pg.init()

FPS = 60
YELLOW_SPACESHIP_IMAGE = pg.image.load(os.path.join('assets','regi.png'))
WIDTH, HEIGHT = 1280,720
WHITE = (255,255,255)
screen = pg.display.set_mode((WIDTH,HEIGHT))

pg.display.set_caption("ULTIMATE REFLEX FIGHTER")



def main():
    clock = pg.time.Clock()
    input_box1 = FieldsButtons.InputBox(550, 400, 140, 32)
    input_box2 = FieldsButtons.InputBox(550, 450, 140, 32)
    input_boxes = [input_box1, input_box2]
    run=True
    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            for box in input_boxes:
                box.handle_event(event)
        for box in input_boxes:
            box.update()
        
        screen.blit(YELLOW_SPACESHIP_IMAGE,(0,0))
        #screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)
        
        pg.display.flip()
        clock.tick(30)
        #draw_window()
    pg.quit()

if __name__ == "__main__":
    main()