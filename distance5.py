import math


class Scanner():
    def __init__(self, file_name):
        with open(file_name, "rt") as input_file:
            self.inp = input_file.read().split()[::-1]

    def read_float(self):
        return float(self.inp.pop())

    def read_vec(self):
        x = self.read_float()
        y = self.read_float()
        return Vec(x, y)

    def read_line(self):
        a = self.read_float()
        b = self.read_float()
        c = self.read_float()
        return Line.from_abc(a, b, c)


class Vec():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vec({self.x!r}, {self.y!r})"

    def __str__(self):
        return f"{self.x} {self.y}"

    def left(self):
        return Vec(-self.y, self.x)

    def right(self):
        return Vec(self.y, -self.x)

    def __sub__(self, v):
        return Vec(self.x - v.x, self.y - v.y)

    def __add__(self, v):
        return Vec(self.x + v.x, self.y + v.y)

    def __mul__(self, a):
        if type(a) is Vec:
            return self.x * a.x + self.y * a.y
        return Vec(self.x * a, self.y * a)

    def __mod__(self, a):
        return self * a.right()

    def len2(self):
        return self.x**2 + self.y**2

    def length(self):
        return self.len2() ** 0.5

    def angle_a(self):
        return math.atan2(self.y, self.x) % (2 * math.pi)

    def angle(self, v):
        d = v.angle_a() - self.angle_a()
        if d < -math.pi:
            d += 2 * math.pi
        elif d > math.pi:
            d -= 2 * math.pi
        return abs(d)

    def base(self, u, v):
        x = (self * u) / (u * u)
        y = (self * v) / (v * v)
        return x, y

    def unit(self):
        return self * (1 / self.length())

    def __lt__(self, other):
        if x1 != x2:
            return x1 < x2
        return  y1 < y2

    def int_segments(A, B, C, D):
        u = B - A
        v = D - C
        AC = C - A
        if u % v != 0:
            t1 = (AC % v) / (u % v)
            t2 = (AC % u) / (u % v)
            if 0 <= t1 and t1 <= 1 and 0 <= t2 and t2 <= 1:
                return True
            return False
        if AC % u == 0:
            L = max(min(A, B), min(C, D))
            R = min(max(A, B), max(C, D))
            if R < L:
                return False
            return True
        return False

    def dist_point_ray(C, A, B):
        v = C - A
        u = B - A
        n = u.left()
        x, y = v.base(u, n)
        if x >= 0:
            d = abs((v * n) / n.length())
        else:
            d = v.length()
        return d

    def dist_point_segment(C, A, B):
        v = C - A
        u = B - A
        n = u.left()
        x, y = v.base(u, n)
        if x >= 1:
            d = (C - B).length()
        elif x <= 0:
            d = v.length()
        else:
            d = abs((v * n) / n.length())
        return d

    def dist_segment_segment(A, B, C, D):
        d1 = A.dist_point_segment(D, C)
        d2 = B.dist_point_segment(D, C)
        d3 = C.dist_point_segment(A, B)
        d4 = D.dist_point_segment(A, B)
        return min(d1, d2, d3, d4)


class Line:

    def __init__(self, point, direction):
        self.point = point
        self.direct = direction
        self.normal = direction.left()

    def __repr__(self):
        return f"Line({self.point!r}, {self.direct!r})"

    def __str__(self):
        c = (Vec(0, 0) - self.point) * self.normal
        return f"{self.normal} {c}"

    def from_abc(a, b, c):
        n = Vec(a, b)
        p0 = n * (-c / n.len2())
        return Line(p0, n.right())

    def from_points(A, B):
        return Line(A, B - A)

    def contains(self, point):
        return abs((point - self.point) * self.normal) < EPS

    def get_abc(self):
        a = int(-self.normal.x)
        b = int(-self.normal.y)
        c = int(-a * self.point.x - b * self.point.y)
        return a, b, c

    def int_line(self, other):
        A = self.point
        C = other.point
        u = self.direct
        v = other.direct
        AC = C - A
        t1 = (AC % v) / (u % v)
        P = A + u * t1
        return P

    def dist_line_point(self, C):
        A = self.point
        B = A + self.direct
        n = self.normal
        d = abs(((C - A) * n) / n.length())
        return d


if __name__ == "__main__":
    with open("distance5.out", "w") as f:
        s = Scanner("distance5.in")
        A = s.read_vec()
        B = s.read_vec()
        C = s.read_vec()
        D = s.read_vec()
        f.write(str(A.dist_segment_segment(B, C, D)))
