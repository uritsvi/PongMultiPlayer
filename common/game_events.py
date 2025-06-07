from abc import abstractmethod

from win32comext.mapi.mapitags import PR_MOVE_TO_FOLDER_ENTRYID

from common.base_scene import BaseScene


class GameEvent:
    @abstractmethod
    def apply_to_client(self, scene: BaseScene):
        raise NotImplementedError("Subclasses must implement apply_to_client method.")

class GameEventEntityCreated(GameEvent):
    def __init__(self, entity):
        self.entity = entity

    def apply_to_client(self, scene: BaseScene):
        scene.add_entity(self.entity)

class GameEventEntityDestroyed(GameEvent):
    def __init__(self, entity):
        self.entity = entity

    def apply_to_client(self, scene: BaseScene):
        scene.remove_entity(self.entity.id)

class GameEventEntityUpdated(GameEvent):
    def __init__(self, entity):
        self.entity = entity

    def apply_to_client(self, scene: BaseScene):
        scene.set_entity_by_id(self.entity.id, self.entity)


