import warnings
import math



def scalar_multiplication(operand1, operand2):
    if type(operand2) == int or type(operand2) == float: # scalar multiplication
        if operand1.is_vector():
            return [x * operand2 for x in operand1.value]
        else:
            warnings.warn("Incorrect type provided fpr scalar multiplication")
    else:
        warnings.warn("Use integer or float for scalar multiplication")
    return []


def scalar_division(operand1, operand2):
    if type(operand2) == int or type(operand2) == float: # scalar division
        if operand1.is_vector():
            return [x / operand2 for x in operand1.value]
        else:
            warnings.warn("Incorrect type provided fpr scalar division")
    else:
        warnings.warn("Use integer or float for scalar division")
    return []


def dot_product(operand1, operand2):
    if type(operand1) == Element and type(operand2) == Element:
        return sum([math.prod(x) for x in zip(operand1.value, operand2.value)])
    else:
        warnings.warn("Incompatible types for dot product")
    return []


def cross_product(operand1, operand2):
    if type(operand1) == Element and type(operand2) == Element:
        if len(operand1.value) == 4 and len(operand2.value) == 4:
            if operand1.is_vector() and operand2.is_vector():
                return [operand1.value[2] * operand2.value[3] - operand1.value[3] * operand2.value[2],
                        operand1.value[3] * operand2.value[1] - operand1.value[1] * operand2.value[3],
                        operand1.value[1] * operand2.value[2] - operand1.value[2] * operand2.value[1],
                        0
                        ]
            else:
                warnings.warn("Both operands have to be vectors")
        else:
            warnings.warn("Both operands have to be 3D vectors")
    else:
        warnings.warn("Both Operands have to be Element objects")
    return []



"""
Elements can be vectors or points, dependent on the last digit in its value. (1 = point, 0 = vector)
"""
class Element:
    def __init__(self, value=None):
        if value is None:
            value = []
        self.value = value


    def __add__(self, other):
        if type(other) == Element:
            if (self.is_vector() and other.is_vector()) or (self.is_point() and other.is_vector()):
                for i in range(0, len(self.value)):
                    return [sum(x) for x in zip(self.value, other.value)]
            else:
                warnings.warn("Incorrect combination of vectors and points for addition")
        else:
            warnings.warn("Both Operands have to be Element objects")
        return []


    def __sub__(self, other):
        if type(other) == Element:
            if (self.value[-1] == other.value[-1]) or (self.is_point() and other.is_vector()):
                for i in range(0, len(self.value)):
                    return [sum(x) for x in zip(self.value, scalar_multiplication(other, -1))]
            else:
                warnings.warn("Incorrect combination of vectors and points for subtraction")
        else:
            warnings.warn("Both Operands have to be Element objects")
        return []


    def __mul__(self, other):
        return scalar_multiplication(self, other)


    def __rmul__(self, other):
        return scalar_multiplication(self, other)


    def __truediv__(self, other):
        return scalar_division(self, other)


    def __rtruediv__(self, other):
        return scalar_division(self, other)


    def is_point(self):
        return self.value[-1] == 1


    def is_vector(self):
        return self.value[-1] == 0