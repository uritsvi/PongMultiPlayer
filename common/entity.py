from abc import abstractmethod


class Entity:
    NEXT_ID = 0

    def __init__(self):
        self.position = (0, 0)

        self.id = self.NEXT_ID
        self.NEXT_ID += 1

    @abstractmethod
    def update(self, inputs):
        """
        Update the entity's state based on the provided inputs.

        :param inputs: A dictionary containing input data for the update.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    @abstractmethod
    def render(self, window):
        """
        Render the entity on the provided window.

        :param window: The window object where the entity will be rendered.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

