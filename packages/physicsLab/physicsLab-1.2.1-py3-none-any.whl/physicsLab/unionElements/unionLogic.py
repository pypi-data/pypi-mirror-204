#coding=utf-8
# 模块化电路
import physicsLab._tools as _tools
import physicsLab.electricity as eletricity

# 任意引脚加法电路
class union_Sum:
    def __init__(self, x : _tools.numType = 0, y : _tools.numType = 0, z : _tools.numType = 0, bitCount : int = 1):
        if not (
                isinstance(x, (float, int)) and isinstance(y, (float, int)) and
                isinstance(z, (float, int)) and isinstance(bitCount, int) and bitCount > 0
        ):
            raise RuntimeError('Error in input parameters')
        x, y, z = _tools.roundData(x), _tools.roundData(y), _tools.roundData(z)
        eletricity.Full_Adder(x, y, z)
        for count in range(1, bitCount):
            if count % 8 != 0:
                y = _tools.roundData(y + 0.2)
                eletricity.crt_Wire(
                    eletricity.Full_Adder(x, y, z).i_low,
                    eletricity.get_Element(x, y - 0.2, z).o_low
                )
            else:
                y -= 1.4
                z = _tools.roundData(z + 0.1)
                eletricity.crt_Wire(
                    eletricity.Full_Adder(x, y, z).i_low,
                    eletricity.get_Element(x, y + 1.4, z - 0.1).o_low
                )

# 任意引脚减法电路
class union_Sub:
    pass

# 2-4译码器
class union_2_4_Decoder:
    def __init__(self, x : _tools.numType = 0, y : _tools.numType = 0, z : _tools.numType = 0):
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float)) and isinstance(z, (int, float))):
            raise RuntimeError('illegal argument')
        self.x = x
        self.y = y
        self.z = z
        obj1 = eletricity.Nor_Gate(x, y, z)
        obj2 = eletricity.Nimp_Gate(x, y + 0.1, z)
        obj3 = eletricity.Nimp_Gate(x, y + 0.2, z)
        obj4 = eletricity.And_Gate(x, y + 0.3, z)
        eletricity.crt_Wire(obj1.i_up, obj2.i_low), eletricity.crt_Wire(obj2.i_low, obj3.i_up), eletricity.crt_Wire(obj3.i_up, obj4.i_up)
        eletricity.crt_Wire(obj1.i_low, obj2.i_up), eletricity.crt_Wire(obj2.i_up, obj3.i_low), eletricity.crt_Wire(obj3.i_low, obj4.i_low)

    @property
    def i_up(self):
        return eletricity.element_Pin(eletricity.get_Element(self.x, self.y + 0.3, self.z), 0)

    @property
    def i_low(self):
        return eletricity.element_Pin(eletricity.get_Element(self.x, self.y + 0.3, self.z), 1)

# 4-16译码器
class union_4_16_Decoder:
    def __init__(self, x : _tools.numType = 0, y : _tools.numType = 0, z : _tools.numType = 0):
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float)) and isinstance(z, (int, float))):
            raise RuntimeError('illegal argument')
        self.x = x
        self.y = y
        self.z = z
        obj1 = eletricity.Nor_Gate(x, y, z); obj2 = eletricity.Nimp_Gate(x, y + 0.1, z)
        obj3 = eletricity.Nimp_Gate(x, y + 0.2, z); obj4 = eletricity.And_Gate(x, y + 0.3, z)
        obj5 = eletricity.Nor_Gate(x + 0.15, y, z); obj6 = eletricity.Nimp_Gate(x + 0.15, y + 0.1, z)
        obj7 = eletricity.Nimp_Gate(x + 0.15, y + 0.2, z); obj8 = eletricity.And_Gate(x + 0.15, y + 0.3, z)
        eletricity.crt_Wire(obj1.i_up, obj2.i_low), eletricity.crt_Wire(obj2.i_low, obj3.i_up), eletricity.crt_Wire(obj3.i_up, obj4.i_up)
        eletricity.crt_Wire(obj5.i_up, obj6.i_low), eletricity.crt_Wire(obj6.i_low, obj7.i_up), eletricity.crt_Wire(obj7.i_up, obj8.i_up)
        eletricity.crt_Wire(obj1.i_low, obj2.i_up), eletricity.crt_Wire(obj2.i_up, obj3.i_low), eletricity.crt_Wire(obj3.i_low, obj4.i_low)
        eletricity.crt_Wire(obj5.i_low, obj6.i_up), eletricity.crt_Wire(obj6.i_up, obj7.i_low), eletricity.crt_Wire(obj7.i_low, obj8.i_low)
        for i in [0.3, 0.45, 0.6, 0.75]:
            for j in [0.05, 0.25]:
                obj = eletricity.Multiplier(x + i, y + j, z)
                if j == 0.05:
                    eletricity.crt_Wire(obj1.o, obj.i_low)
                    eletricity.crt_Wire(obj2.o, obj.i_up)
                else:
                    eletricity.crt_Wire(obj3.o, obj.i_low)
                    eletricity.crt_Wire(obj4.o, obj.i_up)
                eval(f'crt_Wire(obj{round((i - 0.3) / 0.15) + 5}.o, obj.i_upmid)')
                eval(f'crt_Wire(obj{round((i - 0.3) / 0.15) + 5}.o, obj.i_lowmid)')

    @property
    def i_up(self):
        return eletricity.element_Pin(eletricity.get_Element(self.x + 0.15, self.y + 0.3, self.z), 0)

    @property
    def i_upmid(self):
        return eletricity.element_Pin(eletricity.get_Element(self.x + 0.15, self.y + 0.3, self.z), 1)

    @property
    def i_lowmid(self):
        return eletricity.element_Pin(eletricity.get_Element(self.x, self.y + 0.3, self.z), 0)

    @property
    def i_low(self):
        return eletricity.element_Pin(eletricity.get_Element(self.x, self.y + 0.3, self.z), 1)

    @property
    def o0(self):
        return eletricity.get_Element(self.x + 0.3, self.y + 0.05, self.z).o_lowmid

    @property
    def o1(self):
        return eletricity.get_Element(self.x + 0.3, self.y + 0.05, self.z).o_upmid

    @property
    def o2(self):
        return eletricity.get_Element(self.x + 0.3, self.y + 0.25, self.z).o_lowmid

    @property
    def o3(self):
        return eletricity.get_Element(self.x + 0.45, self.y + 0.25, self.z).o_upmid

    @property
    def o4(self):
        return eletricity.get_Element(self.x + 0.45, self.y + 0.05, self.z).o_lowmid

    @property
    def o5(self):
        return eletricity.get_Element(self.x + 0.45, self.y + 0.05, self.z).o_upmid

    @property
    def o6(self):
        return eletricity.get_Element(self.x + 0.45, self.y + 0.25, self.z).o_lowmid

    @property
    def o7(self):
        return eletricity.get_Element(self.x + 0.45, self.y + 0.25, self.z).o_upmid

    @property
    def o8(self):
        return eletricity.get_Element(self.x + 0.6, self.y + 0.05, self.z).o_lowmid

    @property
    def o9(self):
        return eletricity.get_Element(self.x + 0.6, self.y + 0.05, self.z).o_upmid

    @property
    def o10(self):
        return eletricity.get_Element(self.x + 0.6, self.y + 0.25, self.z).o_lowmid

    @property
    def o11(self):
        return eletricity.get_Element(self.x + 0.6, self.y + 0.25, self.z).o_upmid

    @property
    def o12(self):
        return eletricity.get_Element(self.x + 0.3, self.y + 0.05, self.z).o_lowmid

    @property
    def o13(self):
        return eletricity.get_Element(self.x + 0.3, self.y + 0.05, self.z).o_upmid

    @property
    def o14(self):
        return eletricity.get_Element(self.x + 0.3, self.y + 0.25, self.z).o_lowmid

    @property
    def o15(self):
        return eletricity.get_Element(self.x + 0.3, self.y + 0.25, self.z).o_upmid