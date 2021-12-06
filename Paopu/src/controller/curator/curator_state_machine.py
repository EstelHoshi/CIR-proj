from time import time
from playsound import playsound
#from jetbot import Camera, Robot
from multiprocessing import Process

from ..state_machine import StateMachine, transition
#from ..vision import Detector, PaopuDetector, MovementDetector


class CuratorStateMachine(StateMachine):
    """State Machine to represent the Curator playing role."""

    DEFAULT_STATE = "idle"
    FACE_WALL = "face_wall"
    FACE_PLAYERS = "face_players"
    WALL_ALIGNMENT = "wall_alignment"

    IS_HAND_THRESHOLD = .9
    IS_PAOPU_THRESHOLD = .94
    MOVEMENT_THRESHOLD = .9
    TIME_FACING_PLAYERS = 2 # Would be nice to use a function that reduces over time

    _player_timer: float
    _green_music_subprocess: Process
    #_paopu_detector: Detector
    #_movement_detector: Detector

    def __init__(self, paopu_model_path, movement_model_path, image_width, image_height):
        self.state = self.DEFAULT_STATE
        #self._robot = Robot()
        #self._camera = Camera.instance(width=image_width, height=image_height)
        #self._paopu_detector = PaopuDetector(paopu_model_path)
        #self._movement_detector = MovementDetector(movement_model_path)

    @staticmethod
    def green_audio():
        playsound("../Audio/greenlight_fast.mp3")
        #playsound("../Audio/greenlight.mp3")

    @staticmethod
    def eliminated_audio(player=1):
        playsound(f"../Audio/P{player}_E.mp3")

    @staticmethod
    def winning_audio():
        playsound("../Audio/P2_E.mp3")
        #playsound("../Audio/win.mp3")

    def is_hand_detected(self):
        #is_hand_probability = self._paopu_detector.predict(self._camera.value)[0]
        #return is_hand_probabilitypass > self.IS_HAND_THRESHOLD
        return False

    def is_movement_detected(self):
        #movement_probability = self._movement_detector.predict(self._camera.value)
        #return movement_probability > self.MOVEMENT_THRESHOLD
        return False

    def is_paopu_detected(self):
        #is_paopu_probability = self._paopu_detector.predict(self._camera.value)[2]
        #return is_paopu_probability > self.IS_PAOPU_THRESHOLD
        return True

    def is_green_music_playing(self):
        return self._green_music_subprocess.is_alive()

    def has_green_music_stopped(self):
        return not self._green_music_subprocess.is_alive()

    def is_facing_players_over(self):
        return time() - self._player_timer > self.TIME_FACING_PLAYERS

    @transition(source=DEFAULT_STATE, target=WALL_ALIGNMENT)
    def start_game(self):
        pass

    @transition(source=FACE_WALL, target=FACE_PLAYERS, conditions=[has_green_music_stopped])
    def turn_to_players(self):
        #self._robot.right(0.15)
        #self._robot.stop()
        self._player_timer = time()

    @transition(source=FACE_WALL, target=DEFAULT_STATE, conditions=[is_hand_detected, is_green_music_playing])
    def end_lost_game(self):
        self._play_green_music.terminate()
        CuratorStateMachine.winning_audio()
        #self._robot.stop()

    @transition(source=FACE_PLAYERS, target=WALL_ALIGNMENT, conditions=[is_facing_players_over])
    def turn_to_wall(self):
        #self._robot.right(0.15)
        print("ROTATING .15 to the RIGHT")

    @transition(source=FACE_PLAYERS, target=DEFAULT_STATE, conditions=[is_movement_detected])
    def end_won_game(self):
        CuratorStateMachine.eliminated_audio()
        #self._robot.stop()

    @transition(source=WALL_ALIGNMENT, target=WALL_ALIGNMENT)
    def align_with_wall(self):
        #self._robot.right(0.12)
        print("ROTATING .12 to the RIGHT")

    @transition(source=WALL_ALIGNMENT, target=FACE_WALL, conditions=[is_paopu_detected])
    def start_facing_wall(self):
        self._green_music_subprocess = Process(target=CuratorStateMachine.green_audio)
        self._green_music_subprocess.start()