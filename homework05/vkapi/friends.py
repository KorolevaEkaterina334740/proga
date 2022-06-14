import dataclasses
import math
import time
import typing as tp

from vkapi import config
from vkapi.session import Session

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    domain = config.VK_CONFIG["domain"]
    access_token = config.VK_CONFIG["access_token"]
    v = config.VK_CONFIG["version"]

    url = (
        f"friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&offset={offset}&count"
        f"={count}&v={v}"
    )
    base_url = f"{domain}"
    s = Session(base_url)
    response = s.get(url)
    friends = FriendsResponse(
        response.json()["response"]["count"], response.json()["response"]["items"]
    )
    return friends


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    domain = config.VK_CONFIG["domain"]
    access_token = config.VK_CONFIG["access_token"]
    v = config.VK_CONFIG["version"]
    s = Session(base_url=domain)
    resp = []

    if target_uid:
        url = f"friends.getMutual?access_token={access_token}&source_uid={source_uid}&order={order}&target_uid={target_uid}&offset={offset}&count={count}"
        friends = s.get(url)
        resp = friends.json()["response"]
    else:
        tries = ((len(target_uids) - 1) // 100) + 1  # type: ignore
        for i in range(tries):
            try:
                url = f"friends.getMutual?access_token={access_token}&source_uid={source_uid}&target_uid={target_uid}&target_uids={','.join([str(t) for t in target_uids])}&count={count}&offset={i * 100}&v={v}"  # type: ignore
                friends = s.get(url)
                for friend in friends.json()["response"]:
                    resp.append(
                        MutualFriends(
                            id=friend["id"],
                            common_friends=[int(f) for f in friend["common_friends"]],
                            common_count=friend["common_count"],
                        )
                    )
            except:
                pass
            time.sleep(0.34)

    return resp


if __name__ == "__main__":
    print(get_friends("360892520"))
