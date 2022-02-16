from dataclasses import dataclass
from typing import Type, List, Dict, ClassVar


@dataclass(repr=False, eq=False)
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        result: str = (f'Тип тренировки: {self.training_type}; '
                       f'Длительность: {self.duration:.3f} ч.; '
                       f'Дистанция: {self.distance:.3f} км; '
                       f'Ср. скорость: {self.speed:.3f} км/ч; '
                       f'Потрачено ккал: {self.calories:.3f}.')
        return result


@dataclass(repr=False, eq=False)
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[float] = 1000.
    MINS: ClassVar[float] = 60.

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('get_spent_calories() не определен'
                                  ' в классах наследниках: Running,'
                                  ' SportsWalking, Swimming')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        obj_InfoMessage: InfoMessage = InfoMessage(self.__class__.__name__,
                                                   self.duration,
                                                   self.get_distance(),
                                                   self.get_mean_speed(),
                                                   self.get_spent_calories())
        return obj_InfoMessage


@dataclass(repr=False, eq=False)
class Running(Training):
    """Тренировка: бег."""
    CALORIES_SPEED_MULTIPLIER: ClassVar[float] = 18
    CALORIES_SPEED_SUBTRACTION: ClassVar[float] = 20

    def get_spent_calories(self):
        return ((self.CALORIES_SPEED_MULTIPLIER * self.get_mean_speed()
                - self.CALORIES_SPEED_SUBTRACTION) * self.weight
                / self.M_IN_KM * self.duration * self.MINS)


@dataclass(repr=False, eq=False)
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: ClassVar[float] = 0.035
    CALORIES_WEIGHT_GENERATION: ClassVar[float] = 0.029

    height: float

    def get_spent_calories(self):
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.CALORIES_WEIGHT_GENERATION * self.weight)
                * self.duration * self.MINS)


@dataclass(repr=False, eq=False)
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    CALORIES_SPEED_ADDITION: ClassVar[float] = 1.1
    CALORIES_SPEED_MULTIPLIER: ClassVar[float] = 2.

    length_pool: int
    count_pool: int

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self):
        return ((self.get_mean_speed() + self.CALORIES_SPEED_ADDITION)
                * self.CALORIES_SPEED_MULTIPLIER * self.weight)


def read_package(workout_type: str, data: List) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_options: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_options.get(workout_type):
        return workout_options[workout_type](*data)
    else:
        print('Тренировка не определина')


def main(training: Training) -> None:
    """Главная функция."""
    info_message: InfoMessage = training.show_training_info()
    print(info_message.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
