from common.entities.ball import Ball
from server_scene import ServerScene


def build_pong_scene(send_player_events):
    scene = ServerScene(send_player_events)
    scene.add_entity(Ball())

    return scene
