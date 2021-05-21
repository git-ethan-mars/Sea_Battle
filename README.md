# Sea_Battle
Авторы: Нестеров Дмитрий и Усов Егор
# Запуск
Для запуска игры нужно запустить `sea_battle.py` через консоль (python sea_battle.py) или любую IDLE.
## Требования
* `Python 3.8`
* `Pygame` (установленный через pip) 
## Описание разделов игры
* В `Опции` можно выбрать интеллект соперника. 
* В разделе `Новая игра` необходимо выбрать расстановку своих кораблей, путем нажатия на определенный корабль левой клавишей мыши. После нужно кликнуть левой или правой клавишей мыши на клетку вашего поля (левого). Если нажать левую клавишу мыши при установке, корабль будет установлен горизонтально, а при правой - вертикально. 
* В разделе `Быстрая игра` ваши корабли ставятся случайным образом.
## Настройка кораблей
В файле `ships.txt` можно установить количество и размер кораблей. Следуйте инструкции в файле.
## Структура
* `sea_battle.py` - отвечает за обработку событий
* `game.py`, `players.py`, `shipsSet.py` - модули
* `tests.py` - тесты
