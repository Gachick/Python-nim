from random import choice, randint

from nim_game.common.enumerations import AgentLevels
from nim_game.common.models import NimStateChange


class Agent:
    """
    В этом классе реализованы стратегии игры для уровней сложности
    """

    _level: AgentLevels         # уровень сложности

    def __init__(self, level: str) -> None:
        level = str(level)
        match level:
            case "easy":
                self._level = AgentLevels.EASY
            case "normal":
                self._level = AgentLevels.NORMAL
            case "hard":
                self._level = AgentLevels.HARD
            case _:
                raise ValueError("Invalid bot difficulty level")

    def make_step(self, state_curr: list[int]) -> NimStateChange:
        """
        Сделать шаг, соотвутствующий уровню сложности

        :param state_curr: список целых чисел - состояние кучек
        :return: стуктуру NimStateChange - описание хода
        """
        match(self._level):
            case AgentLevels.HARD:
                return Agent.get_optimal_move(state_curr)
            case AgentLevels.EASY:
                return Agent.get_random_move(state_curr)
            case AgentLevels.NORMAL:
                if choice([True, False]):
                    return Agent.get_optimal_move(state_curr)
                else:
                    return Agent.get_random_move(state_curr)

    @staticmethod
    def get_optimal_move(state_curr: list[int]) -> NimStateChange:
        nim_sum = 0
        for heap_id, amount in enumerate(state_curr):
            nim_sum ^= amount

        for heap_id, amount in enumerate(state_curr):
            optimal = nim_sum ^ amount
            if 0 <= optimal <= state_curr[heap_id]:
                return NimStateChange(heap_id, state_curr[heap_id] - optimal)

        return Agent.get_random_move(state_curr)

    @staticmethod
    def get_random_move(state_curr: list[int]) -> NimStateChange:
        heap_id = 0
        while state_curr[heap_id] == 0:
            heap_id = randint(0, len(state_curr) - 1)
        decrease = randint(1, state_curr[heap_id])
        return NimStateChange(heap_id, decrease)
