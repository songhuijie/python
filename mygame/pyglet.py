import pyglet

game_window = pyglet.window.Window(400, 300)

def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2

if __name__ == '__main__':
    pyglet.resource.path = ['./resources']
    pyglet.resource.reindex()

    player_image = pyglet.resource.image("1.png")
    bullet_image = pyglet.resource.image("2.png")
    asteroid_image = pyglet.resource.image("3.png")

    pyglet.app.run()
