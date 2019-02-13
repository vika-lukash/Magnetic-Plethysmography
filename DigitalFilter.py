import matplotlib.pyplot as plt



def processing(port1, port2) :
    koef_nomb_max =5
    koef_nomb = 5
    na = 0
    Aa = 1300
    Bb = 730
    Bbd = 530
    MU3 = []
    MdU = []
    x1 = []
    x2 = []
    x3 = []
    for r in range(2000):  # 6 строк
        MU3.append([])  # создаем пустую строку
        for c in range(200):  # в каждой строке - 10 элементов
            MU3[r].append(0)  # добавляем очередной элемент в строку
    for r in range(2000):  # 6 строк
        MI3.append([])  # создаем пустую строку
        for c in range(200):  # в каждой строке - 10 элементов
            MI3[r].append(0)  # добавляем очередной элемент в строку




    for ind in range(0,99):
        n = str(ind)
        if ind<10:
            n = '000'+n
        else:
            n = '00'+n
        for i in range(0, Aa - 1):
            if (port1[i] > 10 ** 7) and (port1[i] < -10 ** 7):
                port1[i] = 0
            if (port2[i] > 10 ** 7) and (port2[i] < -10 ** 7):
                port2[i] = 0

        MU = []
        MU2 = []
        MI = []
        MI2 = []

        for i in range(0, Aa - 1):
            MI2.append(port1[i])
            MU2.append(port1[i])
            MI.append(0)
            MU.append(0)
        U11 = MU2[2]
        U12 = MU2[2]
        U10 = MU2[2]
        U21 = MU2[2]
        U22 = MU2[2]
        U20 = MU2[2]
        U31 = MU2[2]
        U32 = MU2[2]
        U30 = MU2[2]
        U41 = MU2[2]
        U42 = MU2[2]
        U40 = MU2[2]
        I11 = MI2[2]
        I12 = MI2[2]
        I10 = MI2[2]
        I21 = MI2[2]
        I22 = MI2[2]
        I20 = MI2[2]
        I31 = MI2[2]
        I32 = MI2[2]
        I30 = MI2[2]
        I41 = MI2[2]
        I42 = MI2[2]
        I40 = MI2[2]
        for i in range(3, Aa - 1):
            U12 = U11
            U11 = U10
            U10 = ((MU2[i] * 14347) - (MU2[i - 1] * 28323) + (MU2[i - 2] * 14347) + (U11 * 64160) - (
                        U12 * 31763)) / 32768
            U22 = U21
            U21 = U20
            U20 = ((U10 * 11410) - (U11 * 22411) + (U12 * 11410) + (U21 * 61967) - (U22 * 29608)) / 32768
            U32 = U31
            U31 = U30
            U30 = ((U20 * 6184) - (U21 * 11876) + (U22 * 6184) + (U31 * 59367) - (U32 * 27090)) / 32768
            U42 = U41
            U41 = U40
            U40 = ((U30 * 1020) - (U31 * 1464) + (U32 * 1020) + (U41 * 57112) - (U42 * 24919)) / 32768
            MU[i] = U40
            I12 = I11
            I11 = I10
            I10 = ((MI2[i] * 14347) - (MI2[i - 1] * 28323) + (MI2[i - 2] * 14347) + (I11 * 64160) - (
                        I12 * 31763)) / 32768
            I22 = I21
            I21 = I20
            I20 = ((I10 * 11410) - (I11 * 22411) + (I12 * 11410) + (I21 * 61967) - (I22 * 29608)) / 32768
            I32 = I31
            I31 = I30
            I30 = ((I20 * 6184) - (I21 * 11876) + (I22 * 6184) + (I31 * 59367) - (I32 * 27090)) / 32768
            I42 = I41
            I41 = I40
            I40 = ((I30 * 1020) - (I31 * 1464) + (I32 * 1020) + (I41 * 57112) - (I42 * 24919)) / 32768
            MI[i] = I40
        for i in range(0, Aa - 1):
            MI[i] = (MI[i] * 1.2 * 4.6) / (2 ** 24 * 10000000)  # / 33554431999999.996
            MU[i] = (MU[i] * 1.2 * 4.6) / 2 ** 24  # (8388608 / 5)
            MU1[i] = 0
            # MU1(i, ind1 + 1) = 0
        tmi = MI[Bb - 3]
        tmu = MU[Bb - 3]
        for i in range(0, Aa - 1):
            MI[i] = MI[i] - tmi
            MU[i] = MU[i] - tmu
        for i in range(0, 49):
            MU[i] = 0
        for i in range(Aa - 51, Aa - 1):
            MU[i] = 0
        for i in range(0, Aa - 1):
            MI3[i][ind+1] = MI[i]
            MU3[i][ind + 1] = MU[i]
    plt.figure(3)
    plt.plot(range(len(MU2)), MU2)
    plt.figure(4)
    plt.plot(range(len(MI)), MI)
    for ind in range(0, 99):
        for i in range(0, Aa - 1):
            MI[i] = MI3[i][ind1]
            MU[i] = MU3[i][ind1]
        for i in range(1, Aa - 2):
            MdU[i].append(((MU[i + 1] - MU[i - 1])) / (2 / 1953))
        Q = []
        for cl in range(Bb-1, Bbd+Bb-1):
            for kon in range(0, koef_nomb-1):
                Q[cl][kon] = MU[cl] ** (kon)
            Q[cl][koef_nomb + 1] = MdU[cl]
        A = []
        B = []
        for kon1 in range(0, koef_nomb):
            for kon2 in range(0, koef_nomb):
                for c1 in range(Bd-1, Bbd+Bb - 1):
                    A[kon1][kon2] = A[kon1][kon2] + (Q[cl][kon1] .* Q[cl][kon2])
            for c1 in range(Bd - 1, Bbd + Bb - 1):
                B[1][kon1] = B[1][kon1] + (MI[cl].* Q[cl][kon1])
        x(1: (koef_nomb + 1)) = B / A

        for kon in range(0,koef_nomb):
            x2[kon] = x[kon]
        x2[koef_nomb + 3] = x2[0] - 3.37 * 10 ** -8
        x2[koef_nomb + 1] = 1 / x2[koef_nomb + 3]
        for kon in range(0,koef_nomb + 3):
            x3[ind][kon] = x2[kon]
    plt.figure(5)
    plt.plot(range(len(x3)), x3)
    plt.show()


















