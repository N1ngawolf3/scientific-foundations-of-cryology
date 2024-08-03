import CoolProp.CoolProp as CP
import traceback
from config import sat_liquid, sat_vapor, qoc, t1, eta_isot, t_ned, t_pre, ql
from math import log

# aa
def to_kvalues(kvalue):
    return round(kvalue/1000, 3)


def to_4_digits(decimal_value):
    return round(decimal_value, 4)



#Добавить БД для сохранения решённых задач, фамилий, варианта и тд и тп


def simple_throttling_liq():
    while True:
        try:
            fluid = input('Введите рабочее тело:  ')
            p1 = int(input("Введите первое давление нагн. [бар]: "))
            p2 = int(input("Введите второе давление нагн. [бар]: "))
            p_in = float(input('Введите давление вс. [бар]:  '))
            p = {'p1': p1*10**5, 'p2': p2*10**5}
            t5 = t1 - t_ned
            t6 = t1
            h_liq = [CP.PropsSI("H", "P", p_in * 10 ** 5, "Q", 0, fluid),
                     CP.PropsSI("H", "P", p_in * 10 ** 5, "Q", 0, fluid)]
            s_liq = [CP.PropsSI("S", "P", p_in * 10 ** 5, "Q", 0, fluid),
                     CP.PropsSI("S", "P", p_in * 10 ** 5, "Q", 0, fluid)]
            h1 = [CP.PropsSI("H", "P", p['p1'], 'T', t1, fluid),
                  CP.PropsSI("H", "P", p['p2'], 'T', t1, fluid)]
            s1 = [CP.PropsSI("S", "P", p['p1'], 'T', t1, fluid),
                  CP.PropsSI("S", "P", p['p2'], 'T', t1, fluid)]
            h5 = [CP.PropsSI("H", "P", p_in*10**5, 'T', t5, fluid),
                  CP.PropsSI("H", "P", p_in*10**5, 'T', t5, fluid)]
            h6 = [CP.PropsSI("H", "P", p_in*10**5, 'T', t6, fluid),
                  CP.PropsSI("H", "P", p_in*10**5, 'T', t6, fluid)]
            s6 = [CP.PropsSI("S", "P", p_in*10**5, 'T', t6, fluid),
                  CP.PropsSI("S", "P", p_in*10**5, 'T', t6, fluid)]
            x = []
            l_compr = []
            ne0 = []
            l_min = []
            therm_degree = []
            for i in range(2):
                x_temp = (h5[i] - h1[i] - qoc)/(h5[i] - h_liq[i])
                l_compr_temp = (t1*(s6[i] - s1[i]) - (h6[i] - h1[i]))/eta_isot
                l_min_temp = t1 * (s6[i] - s_liq[i]) - (h6[i] - h_liq[i])
                ne0_temp = l_compr_temp/x_temp
                x.append(x_temp)
                l_compr.append(l_compr_temp)
                l_min.append(l_min_temp)
                ne0.append(ne0_temp)
                therm_degree.append(l_min_temp/ne0_temp)
            return {'fluid': fluid,
                    'x': list(map(to_4_digits, x)),
                    'l_compr': list(map(to_kvalues, l_compr)),
                    'Ne0': list(map(to_kvalues, ne0)),
                    'l_min': list(map(to_kvalues, l_min)),
                    'therm_degree': list(map(to_4_digits, therm_degree))}
        except Exception as ex:
            print('Проверьте верность введённых данных')
            print(ex)


def simple_throttling_refr():
    while True:
        try:
            fluid = input('Введите рабочее тело:  ')
            p1 = int(input("Введите первое давление нагн. [бар]: "))
            p2 = int(input("Введите второе давление нагн. [бар]: "))
            p = {'p1': p1*10**5, 'p2': p2*10**5}
            tx = int(input('Введите Tx для вашего варианта [K]: '))
            p_in = CP.PropsSI('P', 'T', tx, 'Q', 0, fluid)
            t3 = tx
            t4 = t3
            t5 = t1 - t_ned
            t6 = t1
            h1 = [CP.PropsSI("H", "P", p['p1'], 'T', t1, fluid),
                  CP.PropsSI("H", "P", p['p2'], 'T', t1, fluid)]
            s1 = [CP.PropsSI("S", "P", p['p1'], 'T', t1, fluid),
                  CP.PropsSI("S", "P", p['p2'], 'T', t1, fluid)]
            h5 = [CP.PropsSI("H", "P", p_in, 'T', t5, fluid),
                  CP.PropsSI("H", "P", p_in, 'T', t5, fluid)]
            h6 = [CP.PropsSI("H", "P", p_in, 'T', t6, fluid),
                  CP.PropsSI("H", "P", p_in, 'T', t6, fluid)]
            s6 = [CP.PropsSI("S", "P", p_in, 'T', t6, fluid),
                  CP.PropsSI("S", "P", p_in, 'T', t6, fluid)]
            qx = []
            l_compr = []
            refr_coef = []
            refr_coef_carno = t4/(t1-t4)
            therm_degree = []
            for i in range(2):
                qx_temp = h5[i] - h1[i] - qoc
                l_compr_temp = (t1*(s6[i] - s1[i]) - (h6[i] - h1[i]))/eta_isot
                refr_coef_temp = qx_temp/l_compr_temp
                qx.append(qx_temp)
                l_compr.append(l_compr_temp)
                refr_coef.append(refr_coef_temp)
                therm_degree.append(refr_coef_temp/refr_coef_carno)
            return {'fluid': fluid,
                    'p1': p['p1']/(10 ** 5),
                    'p2': p['p2']/(10 ** 5),
                    'T1': t1,
                    'Tx': tx,
                    'T5': t5,
                    'h1': list(map(to_kvalues, h1)),
                    'h5': list(map(to_kvalues, h5)),
                    'h6': list(map(to_kvalues, h6)),
                    's1': list(map(to_kvalues, s1)),
                    's6': list(map(to_kvalues, s6)),
                    'qx': list(map(to_kvalues, qx)),
                    'l_compr': list(map(to_kvalues, l_compr)),
                    'refr_coef': list(map(to_4_digits, refr_coef)),
                    'refr_coef_carno': to_4_digits(refr_coef_carno),
                    'therm_degree': list(map(to_4_digits, therm_degree))}
        except ValueError as ex:
            print('Проверьте верность введённых данных')
            print(ex)


def throttling_prerefr_refr():
    while True:
        try:
            fluid = input('Введите рабочее тело:  ')
            p1 = int(input("Введите первое давление нагн. [бар]: "))
            p2 = int(input("Введите второе давление нагн. [бар]: "))
            tx = int(input('Введите Tx для вашего варианта [K]: '))
            if fluid == 'Argon' and tx < 83.706:
                print('Температурный уровень для данного вещества слишком низкий,'
                      'необходимо использовать вещество, с меньшей температурой кипения'
                      'при данном давлении')
                break
            p = {'p1': p1*10**5, 'p2': p2*10**5}
            p_in = CP.PropsSI('P', "T", tx, 'Q', 0, fluid)
            t3 = t_pre
            t7 = t_pre - t_ned
            t8 = t1 - t_ned
            h1 = [CP.PropsSI("H", "P", p['p1'], 'T', t1, fluid),
                  CP.PropsSI("H", "P", p['p2'], 'T', t1, fluid)]
            s1 = [CP.PropsSI("S", "P", p['p1'], 'T', t1, fluid),
                  CP.PropsSI("S", "P", p['p2'], 'T', t1, fluid)]
            h3 = [CP.PropsSI("H", "P", p['p1'], 'T', t3, fluid),
                  CP.PropsSI("H", "P", p['p2'], 'T', t3, fluid)]
            h7 = [CP.PropsSI("H", "P", p_in, 'T', t7, fluid),
                  CP.PropsSI("H", "P", p_in, 'T', t7, fluid)]
            h8 = [CP.PropsSI("H", "P", p_in, 'T', t8, fluid),
                  CP.PropsSI("H", "P", p_in, 'T', t8, fluid)]
            s8 = [CP.PropsSI("S", "P", p_in, 'T', t8, fluid),
                  CP.PropsSI("S", "P", p_in, 'T', t8, fluid)]
            qx = []
            l_compr = []
            l = []
            l_pre = []
            refr_coef = []
            refr_coef_carno = [tx/(t1-tx), tx/(t1-tx)]
            eta_t = []
            for i in range(2):
                qx_temp = h7[i] - h3[i] - qoc
                l_compr_temp = (t1 * (s8[i] - s1[i]) - (h8[i] - h1[i]))/eta_isot
                l_pre_temp = qx_temp/ql
                l_temp = l_compr_temp + l_pre_temp
                refr_coef_temp = qx_temp/l_temp
                eta_t_temp = refr_coef_temp/refr_coef_carno[0]
                qx.append(qx_temp)
                l_compr.append(l_compr_temp)
                l_pre.append(l_pre_temp)
                refr_coef.append(refr_coef_temp)
                eta_t.append(eta_t_temp)
            return {'fluid': fluid,
                    'qx [кДж]': list(map(to_kvalues, qx)),
                    'l_compr [кДж]': list(map(to_kvalues, l_compr)),
                    'l [кДж]': list(map(to_kvalues, l)),
                    'refr_coef [-]': list(map(to_4_digits, refr_coef)),
                    'l_pre [кДж]': list(map(to_kvalues, l_pre)),
                    'eta_T [-]': list(map(to_4_digits, eta_t))}
        except Exception as ex:
            print('Проверьте верность введённых данных')
            print(ex)


def throttling_prerefr_liq():
    while True:
        try:
            fluid = input('Введите рабочее тело:  ')
            p1 = int(input("Введите первое давление нагн. [бар]: "))
            p2 = int(input("Введите второе давление нагн. [бар]: "))
            p_in = float(input('Введите давление вс. [бар]:  '))
            p = {'p1': p1*10**5, 'p2': p2*10**5}
            t3 = t_pre
            t7 = t_pre - t_ned
            t9 = t1
            h1 = [CP.PropsSI("H", "P", p['p1'], 'T', t1, fluid),
                  CP.PropsSI("H", "P", p['p2'], 'T', t1, fluid)]
            s1 = [CP.PropsSI("S", "P", p['p1'], 'T', t1, fluid),
                  CP.PropsSI("S", "P", p['p2'], 'T', t1, fluid)]
            h3 = [CP.PropsSI("H", "P", p['p1'], 'T', t3, fluid),
                  CP.PropsSI("H", "P", p['p2'], 'T', t3, fluid)]
            h7 = [CP.PropsSI("H", "P", p_in*10**5, 'T', t7, fluid),
                  CP.PropsSI("H", "P", p_in*10**5, 'T', t7, fluid)]
            h9 = [CP.PropsSI("H", "P", p_in*10**5, 'T', t9, fluid),
                  CP.PropsSI("H", "P", p_in*10**5, 'T', t9, fluid)]
            s9 = [CP.PropsSI("S", "P", p_in*10**5, 'T', t9, fluid),
                  CP.PropsSI("S", "P", p_in*10**5, 'T', t9, fluid)]
            h_liq = CP.PropsSI('H', "P", p_in*10**5, 'Q', sat_liquid, fluid)
            s_liq = CP.PropsSI('S', "P", p_in*10**5, 'Q', sat_liquid, fluid)
            qx = []
            l_compr = []
            l_compr_iz = []
            l = []
            l_min = []
            ne0 = []
            x = []
            l_pre = []
            eta_t = []
            for i in range(2):
                qx_temp = h7[i] - h3[i] - qoc
                l_compr_temp_iz = (t1*(s9[i] - s1[i]) - (h9[i] - h1[i]))
                l_compr_temp = l_compr_temp_iz/eta_isot
                l_pre_temp = qx_temp/ql
                l_temp = l_compr_temp + l_pre_temp
                x_temp = ((h7[i] - h3[i])-qoc)/(h7[i] - h_liq)
                ne0_temp = l_temp/x_temp
                l_min_temp = t1*(s9[i] - s_liq) - (h9[i] - h_liq)
                eta_t_temp = l_min_temp/ne0_temp
                qx.append(qx_temp)
                l_compr.append(l_compr_temp)
                l_compr_iz.append(l_compr_temp_iz)
                l.append(l_temp)
                l_min.append(l_min_temp)
                ne0.append(ne0_temp)
                x.append(x_temp)
                l_pre.append(l_pre_temp)
                eta_t.append(eta_t_temp)
            return {'fluid': fluid,
                    'qx [кДж]': list(map(to_kvalues, qx)),
                    'l_compr [кДж]': list(map(to_kvalues, l_compr)),
                    'l_compr_iz [кДж]': list(map(to_kvalues, l_compr_iz)),
                    'l [кДж]': list(map(to_kvalues, l)),
                    'l_min [кДж]': list(map(to_kvalues, l_min)),
                    'Ne0 [кДж]': list(map(to_kvalues, ne0)),
                    'x [-]': list(map(to_4_digits, x)),
                    'l_pre [кДж]': list(map(to_kvalues, l_pre)),
                    'eta_T [-]': list(map(to_4_digits, eta_t))}
        except Exception as ex:
            print('Проверьте верность введённых данных')
            print(ex)


def double_throttling_liq():
    while True:
        try:
            fluid = input('Введите рабочее тело:  ')
            p1 = int(input("Введите первое давление нагн. [бар]: "))
            p2 = int(input("Введите второе давление нагн. [бар]: "))
            pd = int(input("Введите промежуточное давление [бар]: "))
            p_in = float(input('Введите давление вс. [бар]:  '))
            d = float(input('Введите долю промежуточного потока:  '))
            p = {'p1': p1*10**5, 'p2': p2*10**5}
            r = float(input('Введите газовую постоянную [Дж/кг*К]: '))
            t7 = t1 - t_ned
            t9 = t1 - t_ned
            h1 = [CP.PropsSI("H", "P", p['p1'], 'T', t1, fluid),
                  CP.PropsSI("H", "P", p['p2'], 'T', t1, fluid)]
            h1_i = [CP.PropsSI("H", "P", p_in * 10 ** 5, 'T', t1, fluid),
                    CP.PropsSI("H", "P", p_in * 10 ** 5, 'T', t1, fluid)]
            s1_i = [CP.PropsSI("S", "P", p_in * 10 ** 5, 'T', t1, fluid),
                    CP.PropsSI("S", "P", p_in * 10 ** 5, 'T', t1, fluid)]
            h1_ii = [CP.PropsSI("H", "P", pd * 10 ** 5, 'T', t1, fluid),
                     CP.PropsSI("H", "P", pd * 10 ** 5, 'T', t1, fluid)]
            c_p7 = [CP.PropsSI("C", "P", p_in * 10 ** 5, 'T', t7, fluid),
                    CP.PropsSI("C", "P", p_in * 10 ** 5, 'T', t7, fluid)]
            c_p9 = [CP.PropsSI("C", "P", pd, 'T', t9, fluid),
                    CP.PropsSI("C", "P", pd, 'T', t9, fluid)]
            h7 = [CP.PropsSI("H", "P", p_in * 10 ** 5, 'T', t7, fluid),
                  CP.PropsSI("H", "P", p_in * 10 ** 5, 'T', t7, fluid)]
            h_liq = [CP.PropsSI("H", "P", p_in * 10 ** 5, 'Q', 0, fluid),
                     CP.PropsSI("H", "P", p_in * 10 ** 5, 'Q', 0, fluid)]
            s_liq = [CP.PropsSI("S", "P", p_in * 10 ** 5, 'Q', 0, fluid),
                     CP.PropsSI("S", "P", p_in * 10 ** 5, 'Q', 0, fluid)]
            delta_ht1 = [h1_i[0] - h1[0], h1_i[1] - h1[1]]
            delta_ht2 = [h1_i[0] - h1_ii[0], h1_i[1] - h1_ii[1]]
            x = []
            l_compr = []
            l_min = []
            ne0 = []
            eta_t = []
            for i in range(2):
                x_temp = ((delta_ht1[i] - d*delta_ht2[i] -
                          (c_p7[i] * t_ned - d*c_p9[i]*t_ned) - qoc)
                          / (h7[i] - c_p7[i] * t_ned - h_liq[i]))
                l_compr_temp_1 = ((1 - d) * r * t1 * log(pd/p_in))/eta_isot
                l_compr_temp_2 = (r * t1 * log(p[f'p{i+1}']/(pd * 10 ** 5)))/eta_isot
                l_compr_temp = l_compr_temp_2 + l_compr_temp_1
                ne0_temp = l_compr_temp/x_temp
                l_min_temp = t1 * (s1_i[i] - s_liq[i]) - (h1_i[i] - h_liq[i])
                eta_t_temp = l_min_temp/ne0_temp
                x.append(x_temp)
                l_compr.append(l_compr_temp)
                ne0.append(ne0_temp)
                eta_t.append(eta_t_temp)
                l_min.append(l_min_temp)
            return {'fluid': fluid,
                    'x [-]': list(map(to_4_digits, x)),
                    'l_compr [кДж]': list(map(to_kvalues, l_compr)),
                    'l_min [кДж]': list(map(to_kvalues, l_min)),
                    'Ne0 [кДж]': list(map(to_kvalues, ne0)),
                    'eta_T [-]': list(map(to_4_digits, eta_t))}
        except Exception as ex:
            print('Проверьте верность введённых данных')
            print(ex)


def double_throttling_refr():
    while True:
        try:
            fluid = input('Введите рабочее тело:  ')
            p1 = int(input("Введите первое давление нагн. [бар]: "))
            p2 = int(input("Введите второе давление нагн. [бар]: "))
            pd = int(input("Введите промежуточное давление [бар]: "))
            tx = int(input('Введите Tx для вашего варианта [К]: '))
            if fluid == 'Argon' and tx < 83.706:
                print('Температурный уровень для данного вещества слишком низкий,'
                      'необходимо использовать вещество, с меньшей температурой кипения'
                      'при данном давлении')
                break
            d = float(input('Введите долю промежуточного потока: '))
            p = {'p1': p1*10**5, 'p2': p2*10**5}
            p_in = CP.PropsSI('P', "T", tx, 'Q', 1, fluid)
            t5 = tx
            t6 = t5
            t7 = t1 - t_ned
            t9 = t1 - t_ned
            h1 = [CP.PropsSI("H", "P", p['p1'], 'T', t1, fluid),
                  CP.PropsSI("H", "P", p['p2'], 'T', t1, fluid)]
            s1 = [CP.PropsSI("S", "P", p['p1'], 'T', t1, fluid),
                  CP.PropsSI("S", "P", p['p2'], 'T', t1, fluid)]
            h7 = [CP.PropsSI("H", "P", p_in, 'T', t7, fluid),
                  CP.PropsSI("H", "P", p_in, 'T', t7, fluid)]
            h9 = [CP.PropsSI("H", "P", pd * 10 ** 5, 'T', t9, fluid),
                  CP.PropsSI("H", "P", pd * 10 ** 5, 'T', t9, fluid)]
            s9 = [CP.PropsSI("S", "P", pd * 10 ** 5, 'T', t9, fluid),
                  CP.PropsSI("S", "P", pd * 10 ** 5, 'T', t9, fluid)]
            qx = []
            l_compr = []
            refr_coef = []
            eta_t = []
            refr_coef_carno = t6 / (t1 - t6)
            for i in range(2):
                qx_temp = (h7[i] - h1[i]) - d * (h7[i] - h9[i]) - qoc
                l_compr_temp_1 = (t1*(s9[i] - s1[i]) - (h9[i] - h1[i]))/eta_isot
                l_compr_temp_2 = (1 - d) * (t1*(s9[i] - s1[i]) - (h9[i] - h1[i]))/eta_isot
                l_compr_temp = l_compr_temp_2 + l_compr_temp_1
                refr_coef_temp = qx_temp/l_compr_temp
                qx.append(qx_temp)
                l_compr.append(l_compr_temp)
                refr_coef.append(refr_coef_temp)
                eta_t.append(refr_coef_temp/refr_coef_carno)
            return {'fluid': fluid,
                    'qx [кДж]': list(map(to_kvalues, qx)),
                    'l_compr [кДж]': list(map(to_kvalues, l_compr)),
                    'refr_coef_carno [кДж]': to_4_digits(refr_coef_carno),
                    'refr_coef [кДж]': list(map(to_4_digits, refr_coef)),
                    'eta_T [-]': list(map(to_4_digits, eta_t))}
        except Exception as ex:
            print('Проверьте верность введённых данных')
            print(ex)


def steam_compression_cycle():
    while True:
        try:
            fluid = input('Введите хладагент: ')
            temp_con = int(input('Введите температуру конденсации в '
                                 '[C]: ')) + 273  # K
            temp_ev = int(input('Введите температуру испарение в '
                                '[C]: ')) + 273  # K
            t2 = temp_con
            t3 = temp_ev
            t4 = t3
            p1 = CP.PropsSI('P', "T", temp_con, 'Q', sat_vapor, fluid)
            p2 = CP.PropsSI('P', "T", temp_ev, 'Q', sat_liquid, fluid)
            s4 = CP.PropsSI('S', "T", t4, 'Q', sat_vapor, fluid)
            h1 = CP.PropsSI("H", "P", p1, 'S', s4, fluid)
            h2 = CP.PropsSI("H", "T", temp_con, 'Q', sat_liquid, fluid)
            h3 = h2
            h4 = CP.PropsSI("H", "P", p2, 'Q', sat_vapor, fluid)
            t1_sc = CP.PropsSI("T", "P", p1, 'S', s4, fluid)
            q_refr = h4 - h3
            l_compr = h1 - h4
            refr_coef = q_refr/l_compr
            refr_coef_carno = t4/(t2-t4)
            therm_degree = refr_coef/refr_coef_carno
            return {"p1": round(p1/10**5, 3),  # bar
                    "p2": round(p2/10**5, 3),   # bar
                    'temp_con': temp_con,  # K
                    'temp_ev': temp_ev,  # K
                    "h1": to_kvalues(h1),  # KJ/kg
                    "h2": to_kvalues(h2),  # KJ/kg
                    "h3": to_kvalues(h3),  # KJ/kg
                    "h4": to_kvalues(h4),  # KJ/kg
                    "T1": round(t1_sc),  # K
                    "T2": t2,  # K
                    "T3": t3,  # K
                    "T4": t4,  # K
                    'fluid': fluid,
                    'q_refr': to_kvalues(q_refr),  # KJ/kg
                    'l_compr': to_kvalues(l_compr),  # KJ/kg
                    'refr_coef': round(refr_coef, 3),
                    'refr_coef_carno': round(refr_coef_carno, 3),  # [-]
                    'therm_degree': round(therm_degree, 3)}  # [-]
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    answer = simple_throttling_liq()
    # answer = simple_throttling_refr()
    # answer = throttling_prerefr_liq()
    # answer = throttling_prerefr_refr() тут ошибка с аргоном
    # answer = double_throttling_liq()
    # answer = double_throttling_refr() тут ошибка с аргоном
    # answer = steam_compression_cycle()
    for variable, value in answer.items():
        print(f"{variable} --- {value}")
