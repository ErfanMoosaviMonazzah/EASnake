import pygame as pg


# visual settings
# - sizes
board_size = 38 # blocks
block_size = 10 # px
signal_size = 1
dis_width = dis_heigh = board_size * block_size # px
# - timing
snake_speed = 20 # px per seconds
# - colors
back_color = (45, 50, 56)
snake_color = (175, 188, 204)
food_color = (195, 132, 137)
text_color = (74, 128, 176)
signal_success_color = (144, 255, 205)
signal_failure_color = (255, 113, 117)


# intializing pygame
pg.init()

# creating main display
dis = pg.display.set_mode((dis_width, dis_heigh))
pg.display.set_caption('Snake Game Simulation')

# create game clock object
clock = pg.time.Clock()

# - fonts
general_font = pg.font.SysFont('bahnschrift', 15)
score_font = pg.font.SysFont('comicsansms', 15)

# simulation params
list_head_locs = [[19,19], [20, 19], [21, 19], [21, 20], [21, 21], [21, 22], [21, 23], [21, 24], [21, 25],
                  [20,25], [19,25], [18,25], [17,25], [16,25], [15, 25], [14, 25], [13, 25], [12, 25], [11, 25], [10,25],
                  [9, 25], [8, 25]]
with open('heads.txt', 'r') as file:
    lines = file.readlines()
    lines = [line[0:-1].split('-') for line in lines]
    list_head_locs = [[int(l[0]), int(l[1])] for l in lines]
    
#list_head_locs = [[hl[0] * 10, hl[1] * 10] for hl in list_head_locs]
list_foods = [[21,25], [8, 25]]
with open('foods.txt', 'r') as file:
    lines = file.readlines()
    lines = [line[0:-1].split('-') for line in lines]
    list_foods = [[int(l[0]), int(l[1])] for l in lines]
#list_foods = [[f[0] * 10, f[1] * 10] for f in list_foods]
#head_loc = [180, 190] # x, y
head_loc = [list_head_locs.pop(0)]
list_snake_body = [head_loc]
score = 0
game_over = False

# rendering methods
# - render text
def render_score():
    rscore = score_font.render(f'Scored: {score}', True, text_color)
    dis.blit(rscore, [5, 5])
def render_general_text(text):
    rtext = general_font.render(text, True, text_color)
    dis.blit(rtext, [5, 20])
# - render block
def render_block(locs, size, color):
    rect = pg.Rect([locs[0], locs[1], size, size])
    pg.draw.rect(dis, color, rect)
    return color, rect
def render_snake():
    rects = []
    for body in list_snake_body:
        rects.append(render_block(body, block_size, snake_color))
    return rects
def render_block_line(list_locs, size, color):
    rects = []
    for locs in list_locs:
        rects.append(render_block(locs, size, color))
    return rects
def render_signal_line(direction):
    list_locs = [[head_loc[0]+((block_size-signal_size)//2)-1, head_loc[1]+((block_size-signal_size)//2)-1]]
    if direction == 'n':
        while list_locs[-1][1] > 0:
            list_locs.append([list_locs[-1][0], list_locs[-1][1]-10])
        color = signal_success_color if (head_loc[1] > food_loc[1]) and (food_loc[0] == head_loc[0]) else signal_failure_color
    if direction == 's':
        while list_locs[-1][1] < dis_heigh:
            list_locs.append([list_locs[-1][0], list_locs[-1][1]+10])
        color = signal_success_color if (head_loc[1] < food_loc[1]) and (food_loc[0] == head_loc[0]) else signal_failure_color
    if direction == 'w':
        while list_locs[-1][0] > 0:
            list_locs.append([list_locs[-1][0]-10, list_locs[-1][1]])
        color = signal_success_color if (head_loc[1] == food_loc[1]) and (food_loc[0] < head_loc[0]) else signal_failure_color
    if direction == 'e':
        while list_locs[-1][0] < dis_width:
            list_locs.append([list_locs[-1][0]+10, list_locs[-1][1]])
        color = signal_success_color if (head_loc[1] == food_loc[1]) and (food_loc[0] > head_loc[0]) else signal_failure_color
    
    return render_block_line(list_locs, signal_size, color)
def render_signal():
    rects = []
    for direcion in 'news':
        rects.append(render_signal_line(direcion))
    return rects

frames = []
def render_frame(frame = None):
    dis.fill(back_color)
    render_score()
    if frame == None:
        r_snake = render_snake()
        r_food = render_block(food_loc, block_size, food_color)
        render_general_text(f'Game Speed: {snake_speed} px/s')
        r_signal = render_signal()
        pg.display.update()
        frames.append([r_snake, r_food, r_signal])
    else:
        render_general_text(f'Frame Inspection ({frames.index(frame)}/{len(frames)-1})')
        rects = frame[0] + [frame[1]]
        for rects_list in frame[2]:
            rects += rects_list
        for r in rects:
            #print(r)
            pg.draw.rect(dis, r[0], r[1])
        pg.display.update()


# game loop
exists_food = False
shift_pressed = False
ctrl_pressed = False
pause = False
while not game_over:
    # render the next food on field
    if not exists_food:
        food_loc = list_foods.pop(0)
        exists_food = True
    
    # check for frame inspection
    if not pause:
        current_frame_index = len(frames) - 1
        
    # get up and down keyboard keys event to control game speed
    for event in pg.event.get():
        #print(event)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if pause:
                    pause = False
                else:
                    pause = True
            if event.key == pg.K_RCTRL or event.key == pg.K_LCTRL:
                ctrl_pressed = True
            if event.key == pg.K_RSHIFT or event.key == pg.K_LSHIFT:
                shift_pressed = True
            if event.key == pg.K_UP:
                snake_speed += 100 if ctrl_pressed and shift_pressed else 20 if shift_pressed else 5
            if event.key == pg.K_DOWN:
                snake_speed -= 100 if ctrl_pressed and shift_pressed else 20 if shift_pressed else 5
            if event.key == pg.K_LEFT:
                current_frame_index -= 1 if current_frame_index != 0 else 0
            if event.key == pg.K_RIGHT:
                current_frame_index += 1 if current_frame_index != len(frames)-1 else 0
        if event.type == pg.KEYUP:
            if event.key == pg.K_RSHIFT or event.key == pg.K_LSHIFT:
                shift_pressed = False
            if event.key == pg.K_RCTRL or event.key == pg.K_LCTRL:
                ctrl_pressed = False
    
    # check for pause
    if pause:
        render_frame(frames[current_frame_index])
        continue
    
    # set new head location
    head_loc = list_head_locs.pop(0)
    
    # check food eating
    if head_loc[0] == food_loc[0] and head_loc[1] == food_loc[1]:
        list_snake_body = [head_loc] + list_snake_body    
        exists_food = False
        score += 1
    else:
        list_snake_body.insert(0, head_loc)
        del list_snake_body[-1]
    
    # render on display
    render_frame()
        
    # game speed syncing
    clock.tick(snake_speed)
    if len(list_head_locs) == 0:
        game_over = True
        
    
pg.quit()