class BaseScene:
    def __init__(self):
        self.entities = []

    def add_entity(self, entity):
        self.entities.append(entity)

    def remove_entity(self, entity_id):
        pass

    def get_entities(self):
        return self.entities

    def get_entity_by_id(self, entity_id):
        for entity in self.entities:
            if entity.id == entity_id:
                return entity
        return None

    def set_entity_by_id(self, entity_id, entity):
        for i, existing_entity in enumerate(self.entities):
            if existing_entity.id == entity_id:
                self.entities[i] = entity
                return
        raise ValueError("Entity with ID not found in the scene.")