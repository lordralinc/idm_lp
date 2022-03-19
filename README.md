### IDM multi - LP module
![PyPI](https://img.shields.io/pypi/v/idm-lp)
![GitHub](https://img.shields.io/github/license/lordralinc/idm_lp)
![GitHub repo size](https://img.shields.io/github/repo-size/lordralinc/idm_lp)
[![Downloads](https://pepy.tech/badge/idm-lp)](https://pepy.tech/project/idm-lp)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Flordralinc%2Fidm_lp.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Flordralinc%2Fidm_lp?ref=badge_shield)

LP модуль позволяет работать приемнику сигналов «IDM multi» работать в любых чатах.
Так же он добавляет игнор, глоигнор, мут и алиасы.

<!--
4: 252535322122234232
  1  2  3  4  5
1 a  b  c  d  e
2 f  g  h  ij k
3 l  m  n  o  p
4 q  r  s  y  u
5 v  w  x  y  z
-->

## Оглавление
1. [Установка](#установка)
2. [Аргументы запуска](#аргументы-запуска)
3. [Структура конфигурационного файла config.json](#структура-кофигурационного-файла-configjson)
4. [Команды модуля ЛП](#команды-модуля-лп)

## Установка
### Heroku 
_Инструкцию ~~любезно~~ предоставил [Юн Дэмин](https://vk.com/id616052556)_

`<nick>` - ваш ник в гитхабе.<br>
`<name>` - имя репозитория.

1. Регистрируемся на [GitHub](https://github.com)
2. Создаем закрытый репозиторий
    ![](https://sun9-5.userapi.com/ZdunWUy0_UtICPscb8DDDXlKXrYpjY2GRHZK1Q/-tt19NoXdC4.jpg)
3. Заходим в термукс или гит на ПК и пишем следующие команды:
    ```shell script
    git clone --bare https://github.com/lordralinc/idm_lp.git
    cd idm_lp.git
    git push --mirror https://github.com/<nick>/<name>.git
    ```
    _Может появится просьба войти в аккаунт, вводим логин и пароль от аккаунта и все готово_
    ```shell script
    cd ..
    rm -rf idm_lp.git
    ```
4. Заходим на наш закрытый репозиторий и там где написано `2.0` изменяем на `master`.<br>
5. Далее заходим в `config.json`, вставляем токен от Kate Mobile и секретный код IDM.
6. Регистрируемся на [Heroku](https://heroku.com) и выбираем python.
7. Переходим по ссылке: [dashboard.heroku.com/apps](https://dashboard.heroku.com/apps) и создаем приложение. 
    Выбираем европу и название приложение любое, чтоб угодить хероку.
8. После создания мы окажемся в панели управления, нажимаем на GitHub и входим в аккаунт.
    ![](https://sun9-47.userapi.com/pLLeZCAo1P4sQR1brlFdBwHtfBWhBQGfuILR-g/edHTCYYZ2CE.jpg)
9. Нам нужно имя закрытого репозитория, вставляем и нажимаем `Search`, выбираем нужный нам репозиторий и нажимаем на `Connect`.
10. Листаем вниз и видим кнопку `Deploy Branch`, рядом с кнопкой будет `2.0`, нажимаем и выбираем `master`, далее тыкаем на кнопку `Deploy Branch` и ждем.
11. Вверху нажимаем на кнопку `Resources`.
12. Нажимаем на карандашик слева, включаем и тыкаем на `Confirm`.
13. Переходим обратно в `Deploy` и мотаем вниз делаем все как по пункту 10

### Windows

Скачиваем и устанавливаем:
1. [Visual C++](https://support.microsoft.com/ru-ru/help/2977003/the-latest-supported-visual-c-downloads) (Если не установленно)
2. [Python](https://www.python.org/ftp/python/3.7.7/python-3.7.7-amd64.exe)

Открываем CMD (Win + R и вводим cmd)
Вводим команды:
```shell script
cd путь_до_папки
py -m venv env
env\Scripts\activate.bat
py -m pip install -U idm_lp
py -m idm_lp setup

Запуск:
cd путь_до_папки
env\Scripts\activate.bat
cd idm_lp
py -m idm_lp 
```

### Linux (Ubuntu 16.04 Server)
```shell script
sudo apt-get update -y
sudo apt-get install build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev -y

wget https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tar.xz
tar xf Python-3.7.7.tar.xz
cd Python-3.7.7
./configure
make -j {число ядер} && sudo make altinstall
```
`{число ядер}` можно узнать командой `nproc`
```shell script
cd /root/
sudo apt-get install git nano -y

python3.7 -m venv env
/root/env/bin/pip install idm_lp
/root/env/bin/python3.7 -m idm_lp setup
```
Создаем сервис для запуска
```shell script
nano /etc/systemd/system/idmlp.service
```
Вводим
```shell script
[Unit]
Description=LP
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/root/idm_lp
ExecStart=/root/env/bin/python3.7 -m idm_lp --config_path /root/idm_lp/config.json

[Install]
WantedBy=multi-user.target
```
Нажимаем `ctrl + x` выходим
```shell script
systemctl enable idmlp
service idmlp start
```

## Аргументы запуска 
- `--logger_level [DEBUG | INFO | WARNING | ERROR | CRITICAL]` — Уровень логгирования
- `--config_path CONFIG_PATH` — Путь до файла с конфингом
- `--use_app_data` — Использовать папку AppData/IDM (Windows). При использовании этой настройки AppData/IDM и config_path складываются
- `--log_to_path` — Логи в файл
- `--base_domain BASE_DOMAIN` — Базовый домен


## Структура конфигурационного файла config.json

- `tokens`            - Токены вк в количестве 3х штук. Получить можно [здесь](https://oauth.vk.com/authorize?client_id=2685278&scope=1073737727&redirect_uri=https://oauth.vk.com/blank.html&display=page&response_type=token&revoke=1)
- `secret_code`       - Секретный код дежурного. Можно получить на странице настроек дежурного в графе `секретный код`
- `service_prefixes`  - Префиксы для выполнения команд модуля ЛП (добавление в мутлист, создание алиасов и тд.)
- `self_prefixes`     - Префиксы для высылки команд для себя (аналог !с .с ...)
- `duty_prefixes`     - Префиксы для высылки команд для дежурного (аналог !д .д ...)

**! Остальные поля заполняются программно**

![](https://sun1-86.userapi.com/10hU2v5Z8sV0ZBeDGWtOn4alEdiYZy2qY4_Ajw/_BeWOFmtcdw.jpg "Пример заполнения config.json")

## Команды модуля ЛП
- `{сервисный префикс}` пинг/кинг/пиу — пинг
- `{сервисный префикс}` инфо — информация о модуле ЛП
***
- `{сервисный префикс}` префиксы свои — просмотр своих префиксов
- `{сервисный префикс}` префиксы дежурный — просмотр префиксов для дежурного
- `{сервисный префикс}` +префикс `[свой/дежурный]` — создание префикса
- `{сервисный префикс}` -префикс `[свой/дежурный]` — удаление префикса
***
- `{сервисный префикс}` алиасы - просмотр алиасов
- `{сервисный префикс}` +алиас `{имя}` {enter} `{команда которую получает модуль ЛП}` {enter} `{команда которую отсылает модуль ЛП}`  — создание алиаса
- `{сервисный префикс}` -алиас `{имя}` — удаление алиаса
- `{сервисный префикс}` алиасы паки — просмотр паков алиасов
- `{сервисный префикс}` алиасы пак `{имя пака}` — просмотр пака алиасов
- `{сервисный префикс}` алиасы импорт `{имя пака}` — импорт пака алиасов
***
- `{сервисный префикс}` игнорлист — просмотр игнорлиста
- `{сервисный префикс}` игнорлист все — просмотр игнорлиста по всем чатам
- `{сервисный префикс}` +игнор `[{ссылка}/{упоминание}/{реплай}]` — добавить в игнорлист
- `{сервисный префикс}` -игнор `[{ссылка}/{упоминание}/{реплай}]` — удалить из игнорлиста
***
- `{сервисный префикс}` глоигнорлист — просмотр глоигнорлиста
- `{сервисный префикс}` +глоигнор `[{ссылка}/{упоминание}/{реплай}]` — добавить в глоигнорлист
- `{сервисный префикс}` -глоигнор `[{ссылка}/{упоминание}/{реплай}]` — удалить из глоигнорлиста
***
- `{сервисный префикс}` мутлист — просмотр мутлиста
- `{сервисный префикс}` мутлист все — просмотр мутлиста по всем чатам
- `{сервисный префикс}` +мут `[{ссылка}/{упоминание}/{реплай}]` `{задержка}` — добавить в мутлист
- `{сервисный префикс}` -мут `[{ссылка}/{упоминание}/{реплай}]` — удалить из мутлиста
***
- `{сервисный префикс}` довы — просмотр доверенных пользователей
- `{сервисный префикс}` +дов `[{ссылка}/{упоминание}/{реплай}]` — добавить в дов-лист
- `{сервисный префикс}` -дов `[{ссылка}/{упоминание}/{реплай}]` — удалить из дов-листа
***
- `{сервисный префикс}` regex — Просмотр шаблонов для удаления
- `{сервисный префикс}` +regex `{имя}` `{regex}` `{для всех:да|нет}` — Добавить шаблон
- `{сервисный префикс}` -regex `{имя}` — Удалить шаблон
***
- `{сервисный префикс}` +потворялка — включить повторялку
- `{сервисный префикс}` -потворялка — выключить повторялку
- `{триггер повторялки}``{сообщение}` — повторить сообщение
***
- `{сервисный префикс}` eval/exec `{script}` — выполнение скрипта
***
- `{сервисный префикс}` -уведы — модуль будет удалять упоминания типа `@all`, `@online`...
- `{сервисный префикс}` +уведы — не будет удалять упоминания типа `@all`, `@online`...
***
- `{сервисный префикс}` рп — просмотр РП команд
- `{сервисный префикс}` +мрп `{имя}` `{падеж}`\n`{форматер для мужчин}`\n`{форматер для женщин}`\n`{окончание для всех}` — просмотр РП команд
- `{сервисный префикс}` -мрп `{имя}` — просмотр РП команд
***
- `{сервисный префикс}` секретный код `{код}` — установка секретного кода
- `{сервисный префикс}` токен каптчи `{токен}` — установка токена рукаптчи
***
- `{сервисный префикс}` +автовыход — включить автовыход из бесед в которые вас пригласили
- `{сервисный префикс}` -автовыход — выключить автовыход из бесед в которые вас пригласили
- `{сервисный префикс}` автовыход +удаление — удалять диалог при выходе
- `{сервисный префикс}` автовыход -удаление — неудалять диалог при выходе
- `{сервисный префикс}` автовыход +чс — включить добавление в ЧС пригласившего 
- `{сервисный префикс}` автовыход -чс — выключить добавление в ЧС пригласившего 
***
- `{сервисный префикс}` +слоумо `{время}`\n`{текст}` — установка слоумо режима
- `{сервисный префикс}` -слоумо — удаление слоумо режима
- `{сервисный префикс}` слоумо — просмотр настроек слоумо режима
- `{сервисный префикс}` слоумо +белый список `{пользователь}` — добавление пользователя в белый список
- `{сервисный префикс}` слоумо -белый список `{пользователь}` — удаление пользователя из белого списка
- `{сервисный префикс}` слоумо время `{время}` — изменение времени задержки
- `{сервисный префикс}` слоумо текст `{текст}` — изменение текста предупреждения
***
- `{сервисный префикс}` +добавление `{текст}` — включить отправку запросов в друзья, пользователям, которые заходят в чат. При этом будет отправляться приветственный `{текст}`.
- `{сервисный префикс}` -добавление — отключить отправку запросов в друзья, пользователям, которые заходят в чат.
***
- `{сервисный префикс}` выключать уведы — включить выключение уведомлений при входе в беседу 
- `{сервисный префикс}` не выключать уведы — выключить выключение уведомлений при входе в беседу 
***
- `{сервисный префикс}` +заражение — включить ответное заражение.
- `{сервисный префикс}` -заражение — отключить ответное заражение.
***
- `{сервисный префикс}` +nometa — включить nometa.
- `{сервисный префикс}` -nometa — отключить nometa.
- `{сервисный префикс}` nometa сообщение `{текст}` — изменить текст сообщения.
- `{сервисный префикс}` nometa задержка `{задержка}` — изменить задержку.

## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Flordralinc%2Fidm_lp.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Flordralinc%2Fidm_lp?ref=badge_large)