from gameEngine.game import Game
from interface.renderer import Renderer
import queue

if __name__ == "__main__":
    q=queue.Queue()
    renderer = Renderer(q)
    nouvelle_partie = Game(renderer,q)
    renderer.playersNames()
