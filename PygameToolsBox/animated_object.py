import pygame
from pygame import Surface, Rect
from pygame.event import Event
from pygame.sprite import Sprite

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


class AnimatedObject(Sprite):
    def __init__(self, images: [Surface], cooling: int):
        """
        Automate animation of game object, You can specify different action to object and switch
        between these actions to switch animation sequence.
        :param images: All the image needed for the object
        :param cooling: Frames spacing between switching image
        """
        super().__init__()
        self._images = [MaskImage(i) for i in images]
        self._actions = dict[str, ActionSequence]()
        self._current_action: ActionSequence | None = None
        self._cooling = cooling
        self._cool_down = cooling
        self._image_index = 0
        self.rect = True

    @property
    def image(self) -> Surface:
        return self._images[self._image_index].image

    @property
    def mask(self) -> Surface:
        return self._images[self._image_index].mask

    @property
    def rect(self) -> Rect:
        return self._images[self._image_index].rect

    @rect.setter
    def rect(self, value: Rect):
        self._images[self._image_index].rect = value

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

    def update(self, pos: Rect):
        """
        Call every frame for adjust animation and object position
        :param pos: New position for the sprite
        """
        self.rect = pos

        if self._cool_down > 0:
            self._cool_down -= 1
            return

        self._cool_down = self._cooling
        self._image_index = self._current_action.get_next()

    def draw(self, win: Surface):
        """
        Display object to the screen
        :param win: Surface to draw
        """
        win.blit(self.image, self.rect)
