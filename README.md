**This librairy contain so far 2 classes**

_ParallaxBackground_ : 

This class allows you to automate the parallax effect. It is possible to stack background images and classify 
displays on the screen allowing continuous scrolling to the right or left. Each layer scrolls at an increasing 
speed the closer you get to the top of the stack.

**Example:**

     win = pygame.display.set_mode((800, 447))
     background = ParallaxBackground()
     background.add_background(Path("bg0.png"))
     background.add_background(Path("bg1.png"))
     background.add_background(Path("bg2.png"))
    
     #by default speed is 5, but you can
     # ex: background.speed = 4
    
     while(run):
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 run = False

    keys = pygame.key.get_pressed()
    # -1 for left scrolling or 1 for right scrolling
    if keys[pygame.K_LEFT]:
        background.update(-1)
    elif keys[pygame.K_RIGHT]:
        background.update(1)
    else:
        background.update(0)

    background.draw(win)
    pygame.display.update()`

_SpriteSheet_ :

This class simplifies the use of sprite sheets to produce animations. For a sprite sheet it is possible 
to extract an image at a position by its column, row. The class also allows you to extract images from the 
sprite sheet dna an iterable list

**Example:**

    win = pygame.display.set_mode((800, 447))

    #for a sprite sheet of images 90px X 90px on 2 rows and 5 columns
    sprites = SpriteSheet(Path("chess_set.png"), 90, 90, 2, 5)

    while(run):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    x = 0
    sprite:Surface
    for sprite in sprites.get_sprite_list():
        win.blit(sprite, (x,0))
        x += sprite.get_width()

    pygame.display.update()
