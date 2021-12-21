from typing import Dict, List, Type, Union
from dataclasses import dataclass, field


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    TRAINING_MESSAGE: str = field(default=('Тип тренировки: {training_type}; '
                                           'Длительность: {duration_hours} ч.; '
                                           'Дистанция: {distance} км; '
                                           'Ср. скорость: {speed} км/ч; '
                                           'Потрачено ккал: {calories}.'),
                                  init=False)
    training_type: str
    duration: str
    distance: str
    speed: str
    calories: str

    def get_message(self) -> str:
        """Получить сообщение с информацией о тренировке"""
        return self.TRAINING_MESSAGE.format(training_type=self.training_type,
                                            duration_hours='%.3f' % self.duration,
                                            distance='%.3f' % self.distance,
                                            speed='%.3f' % self.speed,
                                            calories='%.3f' % self.calories)


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: float = 1000
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: float = action
        self.duration_hours: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance: float = self.get_distance()
        return distance / self.duration_hours

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Метод не определен в наследнике!')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration_hours,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1: float = 18
    COEFF_CALORIE_2: float = 20
    MINS_IN_HOUR: float = 60

    def get_spent_calories(self) -> float:
        mean_speed: float = super().get_mean_speed()
        duration_min: float = self.duration_hours * self.MINS_IN_HOUR
        return ((self.COEFF_CALORIE_1 * mean_speed - self.COEFF_CALORIE_2)
                * self.weight / self.M_IN_KM * duration_min)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029
    MINS_IN_HOUR: float = 60

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight
                         )
        self.height: float = height

    def get_spent_calories(self) -> float:
        mean_speed: float = super().get_mean_speed()
        duration_min: float = self.duration_hours * self.MINS_IN_HOUR
        return (((self.COEFF_CALORIE_1 * self.weight)
                 + ((mean_speed ** 2 // self.height)
                 * self.COEFF_CALORIE_2 * self.weight))
                * duration_min)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    COEFF_CALORIE_1: float = 1.1
    COEFF_CALORIE_2: float = 2

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight
                         )
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_mean_speed(self) -> float:
        return ((self.length_pool * self.count_pool)
                / self.M_IN_KM
                / self.duration_hours)

    def get_spent_calories(self) -> float:
        mean_speed: float = self.get_mean_speed()
        return ((mean_speed + self.COEFF_CALORIE_1)
                * self.COEFF_CALORIE_2
                * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_codes: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return training_codes[workout_type](*data)


def main(training: Type[Training]) -> None:
    """Главная функция."""
    info: Type[InfoMessage] = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: List[Union[str, List]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Type[Training] = read_package(workout_type, data)
        main(training)
