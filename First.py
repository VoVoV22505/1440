import yaml
import json
import math

with open("test.yaml") as file:
    data = yaml.safe_load(file)

from matplotlib import image

img = image.imread("test2.png")

# тестовые функции


def position_test():
    difference_y = position[0] - data["position"][0]
    difference_x = position[1] - data["position"][1]
    difference = [difference_y, difference_x]
    return difference


def dispersion_test():
    dispersion = math.sqrt(position[0] ** 2 + position[1] ** 2) - data["dispersion"]
    return dispersion


def std_test():
    std = math.sqrt(dispersion_test())
    return std


# вычислние координат центра объекта
x = 0
y = 0
n = 0
x_c = 0
y_c = 0

for i in range(0, img.shape[1]):
    for j in range(0, img.shape[0]):
        if list(img[j, i]) == [0, 0, 0]:
            pass
        else:
            n += 1
            x += i
            y += j

x_c = int(x / n)
y_c = int(y / n)

if (x / n) % x_c >= 0.5:
    x_c += 1
if (y / n) % y_c >= 0.5:
    y_c += 1

position = [y_c - img.shape[0] / 2, x_c - img.shape[1] / 2]

# запись результатов в файл в формате json
result = {
    "position": position_test(),
    "dispersion": dispersion_test(),
    "std": std_test(),
}

with open("result.json", "w") as file:
    json.dump(result, file)


# отправление данных в базу данных InfluxDB
from influxdb import InfluxDBClient

database = InfluxDBClient(
    host="test.com",
    port=8086,
    username="test",
    password="passfortest",
    ssl=True,
    verify_ssl=True,
)

database.create_database("testdatabase")
database.switch_database("testdatabase")
database.write_points(result)

# запись проекций изображения в txt файл
ox = [[0] * 3] * (img.shape[1])
oy = [[0] * 3] * (img.shape[0])

for i in range(0, img.shape[1]):
    for j in range(0, img.shape[0]):
        ox[i] = [k + l for k, l in zip(ox[i], list(img[j][i]))]

for i in range(0, img.shape[0]):
    for j in range(0, img.shape[1]):
        oy[i] = [k + l for k, l in zip(oy[i], list(img[i][j]))]


with open("result.txt", "w") as file:
    for c, s in zip(ox, oy):
        file.write(f"{c}")
        file.write(f"{s}\n")
