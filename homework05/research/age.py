import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    today = dt.datetime.today()
    year = float(today.year)
    items = get_friends(user_id=user_id, fields="bdate").items  # type: ignore

    age = [year - float(i["bdate"][-4:]) for i in items if "bdate" in i and len(i["bdate"]) >= 9]  # type: ignore
    age_mean = statistics.median(age) if age else None
    return age_mean
if __name__ == '__main__':
    print(age_predict("58801"))