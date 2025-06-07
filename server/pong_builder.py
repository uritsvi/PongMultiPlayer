from common.entities.ball import Ball
from scene import Scene


def build_pong_scene(send_player_events):
    scene = Scene(send_player_events)
    scene.add_entity(Ball())

    return scene
