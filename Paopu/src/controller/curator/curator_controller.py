from .curator_state_machine import CuratorStateMachine
from .multi_curator_state_machine import MultiPlayerCuratorStateMachine

class CuratorController:
    def __init__(self, paopu_model_path, movement_model_path, digit_model_path=None, image_width=224, image_height=224, multi_player=False):
        self._multi_player = multi_player
        if multi_player:
            self._state_machine = MultiPlayerCuratorStateMachine(paopu_model_path, movement_model_path, digit_model_path, image_width, image_height)
        else:
            self._state_machine = CuratorStateMachine(paopu_model_path, movement_model_path, image_width, image_height)

    def run(self):
        self._state_machine.start_game()
        print("STATE:", self._state_machine.state)
        while True:
            if self._state_machine.state == self._state_machine.FACE_WALL:
                if self._state_machine.end_lost_game()[1]:
                    print("LOST THE GAME")
                    print("STATE:", self._state_machine.state)
                    break
                elif self._state_machine.turn_to_players()[1]:
                    print("TURNING AROUND TO PLAYERS")
                    print("STATE:", self._state_machine.state)
            elif self._state_machine.state == self._state_machine.FACE_PLAYERS:
                if self._multi_player and self._state_machine.eliminate_player()[1]:
                    print("ELIMINATED PLAYER")
                elif self._state_machine.end_won_game()[1]:
                    print("WON THE GAME")
                    print("STATE:", self._state_machine.state)
                    break
                elif self._state_machine.turn_to_wall()[1]:
                    print("TURNING AROUND TO WALL")
                    print("STATE:", self._state_machine.state)
            elif self._state_machine.state == self._state_machine.WALL_ALIGNMENT:
                if self._state_machine.start_facing_wall()[1]:
                    print("FACING WALL")
                    print("STATE:", self._state_machine.state)
                else:
                    self._state_machine.align_with_wall()
                    print("ALIGNING WITH WALL")
        print("GAME ENDS")
        print("STATE:", self._state_machine.state)