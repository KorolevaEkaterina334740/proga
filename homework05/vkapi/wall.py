import textwrap
import time
import typing as tp
from string import Template

owner_id = 888
domain = 111
code = (
    f'return [API.wall.get({{"owner_id": {owner_id}, "domain": {domain}, "offset": 0, "count": 1, '
    f'"filter": {owner_id}, "extended": 0, "fields": "", "v": 5.126,}})];'
)
print(code)

import pandas as pd
from pandas import json_normalize
from vkapi import config, session
from vkapi.exceptions import APIError
from vkapi.session import Session


def get_posts_2500(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> tp.Dict[str, tp.Any]:
    pass


def get_wall_execute(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
    progress=None,
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.

    @see: https://vk.com/dev/wall.get

    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param max_count: Максимальное число записей, которое может быть получено за один запрос.
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param progress: Callback для отображения прогресса.
    """
    token = config.VK_CONFIG["access_token"]
    v = config.VK_CONFIG["version"]
    s = Session(config.VK_CONFIG["domain"])
    all_data = []
    for call in range(((count - 1) // max_count) + 1):
        try:
            code = Template(
                """var posts = []; var i = 0; while (i < $attempts) 
                {posts = posts + API.wall.get({"owner_id":$owner_id,"domain":"$domain","offset":$offset + i*100,
                "count":"$count","filter":"$filter","extended":$extended,"fields":'$fields',"v":$version})['items'];
                 i=i+1;} return {"count": posts.length, "items": posts};"""
            ).substitute(
                owner_id=owner_id,
                domain=domain,
                offset=offset + max_count * call,
                count=count - max_count * call if count - max_count * call < 101 else 100,
                attempts=(count - max_count * call - 1) // 100 + 1,
                filter=filter,
                extended=extended,
                fields=fields,
                version=v,
            )
            wall_data = s.post(
                "execute",
                data={
                    "code": code,
                    "access_token": token,
                    "v": v,
                },
            )
            time.sleep(1)

            all_data = [post for post in wall_data.json()["response"]["items"]]
        except:
            pass

    return json_normalize(all_data)
