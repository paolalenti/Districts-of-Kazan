import pandas as pd


class ConvexHullBuilder:
    def __init__(self, points: pd.DataFrame):
        self.__points = points

    def get_convex_hull(self) -> pd.DataFrame:
        """
        Формат выходного датафрейма:
        - district
            Название района
        - points
            Список точек выпуклой оболочки района
        - center
            Кортеж центра района (lat, lon)
        - color
            Цвет оболочки района
        """
        data = {
            "district": [],
            "points": [],
            "center": [],
            "color": ["green", "blue", "yellow", "red", "pink", "white", "black", "brown"]
        }
        districts = {}
        for d in self.__points['district'].unique():
            lats = self.__points[self.__points["district"] == d]['lat'].to_list()
            lons = self.__points[self.__points["district"] == d]['lon'].to_list()

            districts[d] = [(lats[i], lons[i]) for i in range(len(lons))]

            points = self.graham_scan(districts[d])
            center = self.get_center(points)

            data["district"].append(d)
            data["points"].append(points)
            data["center"].append(center)

        res = pd.DataFrame(data)
        return res

    @staticmethod
    def get_center(points) -> tuple:
        n = len(points)
        lats_sum = lons_sum = 0
        for i in range(n):
            lats_sum += points[i][0]
            lons_sum += points[i][1]
        lat = lats_sum / n
        lon = lons_sum / n

        return lat, lon

    @staticmethod
    def rotate(a, b, c) -> float:  # "косое произведение"
        return (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])

    def graham_scan(self, points) -> list:
        n = len(points)
        points_idxs = list(range(n))

        for i in range(1, n):  # Самая левая точка
            if points[points_idxs[i]][0] < points[points_idxs[0]][0]:
                points_idxs[i], points_idxs[0] = points_idxs[0], points_idxs[i]

        for i in range(2, n):  # Сортируем точки относительно самой левой
            j = i

            while j > 1 and (
                    self.rotate(points[points_idxs[0]], points[points_idxs[j - 1]], points[points_idxs[j]]) < 0):
                points_idxs[j], points_idxs[j - 1] = points_idxs[j - 1], points_idxs[j]
                j -= 1

        stack = [points_idxs[0], points_idxs[1]]
        for i in range(2, n):  # Само формирование оболочки, где отбрасываем векторы, которые поворачивают по часовой стрелке
            while self.rotate(points[stack[-2]], points[stack[-1]], points[points_idxs[i]]) < 0:
                stack.pop(-1)
            stack.append(points_idxs[i])

        return [points[i] for i in stack]
