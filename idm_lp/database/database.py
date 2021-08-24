from pydantic import BaseModel, validator
from typing import List

import os
from idm_lp import const

import json

from . import (
    Alias,
    ChatEnterModel,
    IgnoredMembers,
    IgnoredGlobalMembers,
    MutedMembers,
    ContextInstanceMixin,
    RegexDeleter,
    RolePlayCommand,
    TrustedUser,
    SlouMo,
    DatabaseError,
    DatabaseWarning
)
from idm_lp import database


class Database(BaseModel, ContextInstanceMixin):
    secret_code: str = ""
    ru_captcha_key: str = ""
    repeater_word: str = ".."
    dd_prefix: str = "дд"

    bio_reply: bool = False
    repeater_active: bool = False

    delete_all_notify: bool = False
    auto_exit_from_chat: bool = False
    auto_exit_from_chat_delete_chat: bool = False
    auto_exit_from_chat_add_to_black_list: bool = False
    disable_notifications: bool = False

    nometa_enable: bool = False
    nometa_message: str = "nometa.xyz"
    nometa_attachments: List[str] = []
    nometa_delay: float = 5 * 60

    tokens: List[str] = []
    service_prefixes: List[str] = [".слп", "!слп"]
    self_prefixes: List[str] = [".л", "!л"]
    duty_prefixes: List[str] = [".лд", "!лд"]

    ignored_members: List[IgnoredMembers] = []
    ignored_global_members: List[IgnoredGlobalMembers] = []
    muted_members: List[MutedMembers] = []
    aliases: List[Alias] = []
    role_play_commands: List[RolePlayCommand] = []
    trusted: List[TrustedUser] = []
    add_to_friends_on_chat_enter: List[ChatEnterModel] = []
    sloumo: List[SlouMo] = []
    regex_deleter: List[RegexDeleter] = []

    @validator('tokens')
    def name_must_contain_space(cls, v):
        if not v:
            raise DatabaseError(
                name='Нет токенов',
                description='Укажите токены в файле конфигурации'
            )
        return v

    @staticmethod
    def get_path() -> str:
        if const.USE_APP_DATA:
            local_data_path = os.environ["APPDATA"]
            return os.path.abspath(
                os.path.join(
                    local_data_path,
                    "IDM",
                    const.CONFIG_PATH
                )
            )
        return os.path.abspath(const.CONFIG_PATH)

    @staticmethod
    def load() -> 'Database':
        path_to_file = Database.get_path()
        try:
            with open(path_to_file, 'r', encoding='utf-8') as file:
                db = Database(**json.loads(file.read()))
        except FileNotFoundError:
            db = None

        if not db:
            raise DatabaseError(
                'IDMLP не установлен',
                f"Для начала запустите процесс установки командой setup"
            )

        if not db.tokens:
            raise DatabaseError(
                'Нет токенов',
                f"Укажите токены в файле конфигурации по пути: {path_to_file}"
            )
        return db

    def save(self):
        path_to_file = Database.get_path()
        with open(path_to_file, 'w', encoding='utf-8') as file:
            file.write(
                self.json(**{"ensure_ascii": False, "indent": 2})
            )
