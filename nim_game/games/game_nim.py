import json

from nim_game.environments.environment_nim import EnvironmentNim
from nim_game.common.models import NimStateChange, GameState
from nim_game.common.enumerations import Players
from nim_game.agents.agent import Agent


class GameNim:
    _environment: EnvironmentNim        # состояния кучек
    _agent: Agent                       # бот

    def __init__(self, path_to_config: str) -> None:
        with open(path_to_config) as config_file:
            config = json.load(config_file)
        self._environment = EnvironmentNim(config["heaps_amount"])
        self._agent = Agent(config["opponent_level"])

    def make_steps(self, player_step: NimStateChange) -> GameState:
        """
        Изменение среды ходом игрока + ход бота

        :param player_step: изменение состояния кучек игроком
        """
        self._environment.change_state(player_step)
        if self.is_game_finished():
            return GameState(winner=Players.USER)

        bot_move = self._agent.make_step(self.heaps_state)
        bot_move.heap_id += 1
        self._environment.change_state(bot_move)
        if self.is_game_finished():
            return GameState(winner=Players.BOT)

        return GameState(opponent_step=bot_move, heaps_state=self.heaps_state)

    def is_game_finished(self) -> bool:
        """
        Проверить, завершилась ли игра, или нет

        :return: True - игра окончена, False - иначе
        """
        return all(amount == 0 for amount in self.heaps_state)

    @property
    def heaps_state(self) -> list[int]:
        return self._environment.get_state()
