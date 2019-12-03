import pymunk
# Import pymunk..

if __name__ == '__main__':

    space = pymunk.space()  # Create a Space which contain the simulation
    space.gravity = 0, -1000  # Set its gravity

    body = pymunk.body(1, 1666)  # Create a Body with mass and moment
    body.position = 50, 100  # Set the position of the body

    poly = pymunk.poly.create_box(body)  # Create a box shape and attach to body
    space.add(body, poly)  # Add both body and shape to the simulation

    while True:  # Infinite loop simulation
        space.step(0.02)  # Step the simulation one step forward
