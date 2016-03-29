# rock [![PyPI](https://img.shields.io/pypi/v/rock-cli.svg)](https://pypi.python.org/pypi/rock-cli)

```bash
$ rock register
Phone: +79991270001
Введите код из SMS: 7313
$ rock balance
Введите рокеткод: ****
1110.61 RUB, 1488 рокетрублей
```

## Установка

Рекомендуемый способ установки — [pipsi][]. С ним зависимости rock не будут установлены для всей системы и ничего не сломается:

```bash
$ pipsi install --python python3 rock-cli
```

Если по каким-то причинам не хочется использовать pipsi, можно установить с помощью обычного PIP:

```bash
$ [sudo] pip3 install rock-cli
```

Для установки необходим Python 3.4+. Версии ниже 3.4 не поддерживаются.

[pipsi]: https://github.com/mitsuhiko/pipsi
