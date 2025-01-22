"""*расстояния до пункта назначения:*

- более 30 км: +300 рублей к доставке;
- до 30 км: +200 рублей к доставке;
- до 10 км: +100 рублей к доставке;
- до 2 км: +50 рублей к доставке;



*габаритов груза:*

- большие габариты: +200 рублей к доставке;
- маленькие габариты: +100 рублей к доставке;



*хрупкости груза.* Если груз хрупкий — +300 рублей к доставке. Хрупкие грузы нельзя возить на расстояние более 30 км;



*загруженности службы доставки*. Стоимость умножается на коэффициент доставки:

- очень высокая загруженность — 1.6;
- высокая загруженность — 1.4;
- повышенная загруженность — 1.2;
- во всех остальных случаях коэффициент равен 1.



Минимальная сумма доставки — 400 рублей. Если сумма доставки меньше минимальной, выводится минимальная сумма.

На входе функция получает расстояние до пункта назначения, габариты, информацию о хрупкости, загруженность службы на текущий момент. На выходе пользователь получает стоимость доставки."""

from math import ceil as math_ceil

class DeliveryDemensions:
    small = "small"
    big = "big"

class DeliveryWorkload:
    very_high = "very_high"
    high = "high"
    heightened = "heightened"
    regular = "regular"

calculate_by_delivery_demensions = {DeliveryDemensions.small: 100, DeliveryDemensions.big: 200}

calculate_by_delivery_workload = {DeliveryWorkload.very_high: 1.6, DeliveryWorkload.high: 1.4,
                             DeliveryWorkload.heightened: 1.2, DeliveryWorkload.regular: 1}

def calculate_cost_by_delivery_distance(distance: int) -> int:
    if 0 <= distance <= 2:
        cost_by_distance = 50
    elif 2 < distance <= 10:
        cost_by_distance = 100
    elif 10 < distance <= 30:
        cost_by_distance = 200
    else:
        cost_by_distance = 300
    return cost_by_distance

def calculate_delivery_cost(distance: int | float, delivery_dimensions: str,
                            delivery_workload: str, delivery_fragility: bool) -> int | str:
    if delivery_workload not in calculate_by_delivery_workload or distance < 0 or delivery_dimensions not in calculate_by_delivery_demensions:
        return "Неверно введенные данные"
    if delivery_fragility and distance > 30:
        return "Хрупкий груз нельзя доставить дальше 30 км"
    else:
        cost_by_distance = calculate_cost_by_delivery_distance(distance=distance)
        cost_by_demensions = calculate_by_delivery_demensions[delivery_dimensions]
        cost_by_workload = calculate_by_delivery_workload[delivery_workload]
        delivery_cost = cost_by_distance + cost_by_demensions
        if delivery_fragility:
            delivery_cost += 300
        if delivery_cost * cost_by_workload >= 400:
            return math_ceil(delivery_cost * cost_by_workload)
        else:
            return 400

# проверки написаны, как будто у меня нет доступа к коду

# позитивные проверки подсчета доставки, которые включают разные варианты каждого значения,
# так, чтобы сумма была больше мин стоимости и доставка могла быть посчитана

assert calculate_delivery_cost(distance=1, delivery_dimensions=DeliveryDemensions.big,
        delivery_workload=DeliveryWorkload.heightened, delivery_fragility=True) == 660

assert calculate_delivery_cost(distance=6, delivery_dimensions=DeliveryDemensions.small,
        delivery_workload=DeliveryWorkload.regular, delivery_fragility=True) == 500

assert calculate_delivery_cost(distance=25, delivery_dimensions=DeliveryDemensions.big,
        delivery_workload=DeliveryWorkload.very_high, delivery_fragility=False) == 640

assert calculate_delivery_cost(distance=40, delivery_dimensions=DeliveryDemensions.small,
        delivery_workload=DeliveryWorkload.high, delivery_fragility=False) == 560

# проверка минимальной стоимости доставки, если доставка посчитана меньше 400 рублей

assert calculate_delivery_cost(distance=1, delivery_dimensions=DeliveryDemensions.small,
        delivery_workload=DeliveryWorkload.regular, delivery_fragility=False) == 400

# проверки граничных значений дистанции

assert calculate_delivery_cost(distance=0, delivery_dimensions=DeliveryDemensions.big,
        delivery_workload=DeliveryWorkload.high, delivery_fragility=True) == 770

assert calculate_delivery_cost(distance=2, delivery_dimensions=DeliveryDemensions.big,
        delivery_workload=DeliveryWorkload.high, delivery_fragility=True) == 770

assert calculate_delivery_cost(distance=3, delivery_dimensions=DeliveryDemensions.big,
        delivery_workload=DeliveryWorkload.high, delivery_fragility=True) == 840

assert calculate_delivery_cost(distance=9, delivery_dimensions=DeliveryDemensions.big,
        delivery_workload=DeliveryWorkload.high, delivery_fragility=True) == 840

assert calculate_delivery_cost(distance=10, delivery_dimensions=DeliveryDemensions.big,
        delivery_workload=DeliveryWorkload.high, delivery_fragility=True) == 840

assert calculate_delivery_cost(distance=11, delivery_dimensions=DeliveryDemensions.big,
        delivery_workload=DeliveryWorkload.high, delivery_fragility=True) == 980

assert calculate_delivery_cost(distance=29, delivery_dimensions=DeliveryDemensions.big,
        delivery_workload=DeliveryWorkload.high, delivery_fragility=True) == 980

assert calculate_delivery_cost(distance=30, delivery_dimensions=DeliveryDemensions.big,
        delivery_workload=DeliveryWorkload.high, delivery_fragility=True) == 980

assert calculate_delivery_cost(distance=31, delivery_dimensions=DeliveryDemensions.big,
        delivery_workload=DeliveryWorkload.high, delivery_fragility=False) == 700

# негативные проверки, что стоимость груза не будет рассчитана

assert (calculate_delivery_cost(distance=40, delivery_dimensions=DeliveryDemensions.small,
        delivery_workload=DeliveryWorkload.regular, delivery_fragility=True)
        == "Хрупкий груз нельзя доставить дальше 30 км")

assert (calculate_delivery_cost(distance=-1, delivery_dimensions=DeliveryDemensions.small,
        delivery_workload=DeliveryWorkload.regular, delivery_fragility=False)
        == "Неверно введенные данные")

assert (calculate_delivery_cost(distance=10, delivery_dimensions="regular",
        delivery_workload=DeliveryWorkload.regular, delivery_fragility=False)
        == "Неверно введенные данные")

assert (calculate_delivery_cost(distance=20, delivery_dimensions=DeliveryDemensions.small,
        delivery_workload="small", delivery_fragility=False)
        == "Неверно введенные данные")



