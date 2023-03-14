from typing import List


class test:
    a: int

    def __init__(self, a):
        self.a = a


class test2(test):
    b: int

    def __init__(self, b, a):
        super().__init__(a)
        self.b = b


b = test(11)
c = test2(12, 13)

d: List[test2] = [c]

print(isinstance(d[0], test))
