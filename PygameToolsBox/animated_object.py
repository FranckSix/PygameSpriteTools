import itertools

import pygame.sprite
from pygame import Surface, Rect, Vector2
from pygame.event import Event

from PygameToolsBox.mask_image import MaskImage

ANIMATION_END = pygame.USEREVENT + 99


class ActionSequence:
    def __init__(self, name: str, repeat: int, images_index: [int]):
        """
        Params:
            name: name of the action in dictionary
            repeat: number of repetition -1 run forever
            images_index: Index of the image in the spread sheet if same index
                          specified more than one time the image will be showed
                          multiple time.
        """
        self.name = name
        self.repeat = repeat
        self.images_index = images_index
        self.iteration = 0
        self.repeated = 0

    def start(self):
        """
        Initialize sequence animation. Start from initial settings
        """
        self.repeated = self.repeat
        self.iteration = 0

    def get_next(self) -> int | None:
        """
        Go to next index image
        """
        self.iteration += 1

        if self.iteration >= len(self.images_index):
            if self.repeated > 0:
                self.repeated -= 1
                self.iteration = 0
            elif self.repeated < 0:
                self.iteration = 0
            else:
                pygame.event.post(Event(ANIMATION_END))
                self.iteration = len(self.images_index) - 1

        return self.images_index[self.iteration]


class AnimatedObject:
    def __init__(self, images: [Surface], cooling: int):
        """
        Automate animation of game object, You can specify different action to object and switch
        between these actions to switch animation sequence.
        :param images: All the image needed for the object
        :param cooling: Frames spacing between switching image
        """
        self.images = [MaskImage(i) for i in images]
        self._actions = dict[str, ActionSequence]()
        self._current_action: ActionSequence | None = None
        self._current_image = self.images[0]
        self.cooling = cooling
        self.cool_down = cooling
        self._pos = Vector2(0, 0)

    def add_action(self, name: str, repeat: int, index_start: int, index_end: int):
        """
        Define action for further call
        :param name: Name of the action (suggest to use Enum to simplify)
        :param repeat: Number of time to repeat the animation before end. Set to -1 to infinite loop
        :param index_start: Index in the list of the first image
        :param index_end: Index in the list of the last image
        """
        self._actions[name] = ActionSequence(name, repeat, list(range(index_start, index_end + 1)))

    def set_action(self, action: str):
        """
        Assign action and start animation. Each time an animation ended ANIMATION_END event raised.
        If you catch event you can manage witch action to do next. Otherwise, last image of current
        animation stay at screen.
        :param action: Action name
        """
        if action in self._actions:
            self._current_action = self._actions[action]
            self._current_action.start()

    def get_action(self) -> str | None:
        """
        :return: Action currently set otherwise return None
        """
        return self._current_action.name if self._current_action else None

    @property
    def pos(self) -> Vector2:
        """
        :return: Rectangle of the current position of the sprite
        """
        return self._pos

    def update(self, pos: Vector2):
        """
        Call every frame for adjust animation and object position
        :param pos: New position for the sprite
        """
        self._pos = pos

        if self.cool_down > 0:
            self.cool_down -= 1
            return

        self.cool_down = self.cooling
        action_sequence = self._current_action.get_next()
        if action_sequence is not None:
            self._current_image = self.images[action_sequence]
        else:
            self._current_image = None

    def is_collide_with(self, other: MaskImage):
        """
        :param other: The other object (sprite) to test collision
        :return: True if the object is colliding with another object else return False
        """
        self._current_image.rect.center = (self._pos.x, self.pos.y)
        if self._current_image and pygame.sprite.collide_rect(self._current_image, other):
            if pygame.sprite.collide_mask(self._current_image, other):
                return True
        return False

    def draw(self, win: Surface):
        """
        Display object to the screen
        :param win: Surface to draw
        """
        if self._current_image:
            self._current_image.rect.center = (self._pos.x, self.pos.y)
            win.blit(self._current_image.image, self._current_image.rect)
