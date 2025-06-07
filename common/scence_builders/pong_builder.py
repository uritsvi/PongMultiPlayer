from common.entities.ball import Ball
from common.scene import Scene


def build_pong_scene():
    scene = Scene()
    scene.add_entity(Ball())

    return scene
