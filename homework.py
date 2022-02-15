from dataclasses import dataclass
from typing import Type, Union, List, Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        result: Union[str, float] = (f'Тип тренировки: {self.training_type}; '
                                     f'Длительность: {self.duration:.3f} ч.; '
                                     f'Дистанция: {self.distance:.3f} км; '
                                     f'Ср. скорость: {self.speed:.3f} км/ч; '
                                     f'Потрачено ккал: {self.calories:.3f}.')
        return result


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MINS = 60

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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        obj_InfoMessage: InfoMessage = InfoMessage(self.__class__.__name__,
                                                   self.duration,
                                                   self.get_distance(),
                                                   self.get_mean_speed(),
                                                   self.get_spent_calories())
        return obj_InfoMessage


@dataclass
class Running(Training):
    """Тренировка: бег."""
    COEFF_KCAL_RUN_1 = 18
    COEFF_KCAL_RUN_2 = 20

    def get_spent_calories(self):
        return ((self.COEFF_KCAL_RUN_1 * self.get_mean_speed()
                - self.COEFF_KCAL_RUN_2) * self.weight
                / self.M_IN_KM * self.duration * self.MINS)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_KCAL_WALK_1 = 0.035
    COEFF_KCAL_WALK_2 = 0.029

    height: float

    def get_spent_calories(self):
        return ((self.COEFF_KCAL_WALK_1 * self.weight + (self.get_mean_speed()
                ** 2 // self.height) * self.COEFF_KCAL_WALK_2 * self.weight)
                * self.duration * self.MINS)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    COEFF_KCAL_SWIM_1 = 1.1
    COEFF_KCAL_SWIM_2 = 2

    length_pool: int
    count_pool: int

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self):
        return ((self.get_mean_speed() + self.COEFF_KCAL_SWIM_1)
                * self.COEFF_KCAL_SWIM_2 * self.weight)


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
