# import pyglet
# from pyglet.gl import *
#
# win = pyglet.window.Window()
#
# @win.event
# def on_draw():
#
#     # Clear buffers
#     glClear(GL_COLOR_BUFFER_BIT)
#
#     # Draw outlines only
#     glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
#
#     # Draw some stuff
#     glBegin(GL_TRIANGLE_FAN)
#     glVertex2i(200, 200)
#     glVertex2i(200, 300)
#     glVertex2i(250, 250)
#     glVertex2i(300, 200)
#     glVertex2i(250, 150)
#     glVertex2i(200, 100)
#     glEnd()
#
# pyglet.app.run()
import gym
env = gym.make('CartPole-v0')
env.reset()
for _ in range(1000):
    env.render()
    env.step(env.action_space.sample()) # take a random action
env.close()
