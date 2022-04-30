import math
def calAngle(p1, p2, p3):
    def calDist(p1, p2):
        return pow(((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2), 0.5)
    a = calDist(p2, p3)
    b = calDist(p1, p2)
    c = calDist(p1, p3)
    cosA = (b * b + c * c - a * a) / (2 * b * c)
    angle = math.acos(cosA) * 180 / math.pi
    return f'{angle:.2f}'
a = (0, 0)
b = (1, 0)
c = (0, 1)
print(calAngle(a, b, c))