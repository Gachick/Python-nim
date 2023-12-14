from random import randint

from nim_game.common.models import NimStateChange


STONE_AMOUNT_MIN = 1        # минимальное начальное число камней в кучке
STONE_AMOUNT_MAX = 10       # максимальное начальное число камней в кучке


class EnvironmentNim:
    """
    Класс для хранения и взаимодействия с кучками
    """

    _heaps: list[int]       # кучки

    def __init__(self, heaps_amount: int) -> None:
        heaps_amount = int(heaps_amount)
        if not 2 <= heaps_amount <= 10:
            raise ValueError("Invalid amount is outside of range [2, 10]")

        self._heaps = [randint(STONE_AMOUNT_MIN, STONE_AMOUNT_MAX)
                       for _ in range(heaps_amount)]

    def get_state(self) -> list[int]:
        """
        Получение текущего состояния кучек

        :return: копия списка с кучек
        """
        return self._heaps.copy()

    def change_state(self, state_change: NimStateChange) -> None:
        """
        Изменения текущего состояния кучек

        :param state_change: структура описывающая изменение состояния
        """
        heap_id = state_change.heap_id - 1
        if not isinstance(state_change, NimStateChange):
            raise ValueError("Invalid state change argument")
        if not 0 <= heap_id < len(self._heaps):
            raise ValueError("Invalid heap id")
        if not 0 < state_change.decrease <= self._heaps[heap_id]:
            raise ValueError("Invalid heap decrease amount")

        self._heaps[heap_id] -= state_change.decrease
