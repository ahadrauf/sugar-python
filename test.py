class A:
    def __init__(self, **kwargs):
        self.a = 1
        self.__dict__.update(kwargs)

class B(A):
    def __init__(self, a, b):
        super().__init__(**a.__dict__)
        self.b = b

if __name__ == '__main__':
    a = A()

    b = B(a, 3)
    print(b.a)
    print(b.b)

    a2 = A(c=3)
    c = B(a2, b)
    print(c.a)
    print(c.b)
    print(c.c)