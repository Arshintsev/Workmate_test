from abc import ABC, abstractmethod
from typing import Dict, List


class BaseReport(ABC):
    """
    Абстрактный базовый класс для всех отчётов.
    Наследники должны реализовать метод value.
    """

    @abstractmethod
    def value(self, data: List[Dict[str, str]]) -> List[Dict[str, float]]:
        """
        Вычисляет отчёт на основе переданных данных.

        Args:
            data (List[Dict[str, str]]): Список строк из CSV (каждая строка как словарь)

        Returns:
            List[Dict[str, float]]: Список словарей с результатами
        """
        pass




class AveragePerformance(BaseReport):
    """
    Отчёт:средняя эффективность
    """

    def value(self, data: List[Dict[str, str]]) -> List[Dict[str, float]]:
        position_sum = {}
        position_count = {}

        for item in data:
            position = item.get('position')
            rating = float(item.get('performance',0))
            if position in position_sum:
                position_sum[position] += rating
                position_count[position] += 1
            else:
                position_sum[position] = rating
                position_count[position] = 1


        result = [
            {"position": position,
             "performance": round((position_sum[position]/position_count[position]) * 20) / 20}
            for position in position_sum
        ]

        return result
