import CoolProp.CoolProp as CP
import traceback
from config import sat_liquid, sat_vapor, qoc, T1, eta_isot, T_ned
from math import log


def to_kvalues(value):
    return round(value/1000, 3)


def to_4_digits(value):
    return round(value, 4)


def simple_throttling_liq():
    while True:
        try:
            fluid = input('Введите рабочее тело:  ')
            p1 = int(input("Введите первое давление нагн. [бар]: "))
            p2 = int(input("Введите второе давление нагн. [бар]: "))
            p_in = float(input('Введите давление вс. [бар]:  '))
            p = {'p1': p1*10**5, 'p2': p2*10**5}
            T5 = T1 - T_ned
            T6 = T1
            h_liq = [CP.PropsSI("H", "P", p_in * 10 ** 5, "Q", 0, fluid),
                     CP.PropsSI("H", "P", p_in * 10 ** 5, "Q", 0, fluid)]
            s_liq = [CP.PropsSI("S", "P", p_in * 10 ** 5, "Q", 0, fluid),
                     CP.PropsSI("S", "P", p_in * 10 ** 5, "Q", 0, fluid)]
            h1 = [CP.PropsSI("H", "P", p['p1'], 'T', T1, fluid),
                  CP.PropsSI("H", "P", p['p2'], 'T', T1, fluid)]
            s1 = [CP.PropsSI("S", "P", p['p1'], 'T', T1, fluid),
                  CP.PropsSI("S", "P", p['p2'], 'T', T1, fluid)]
            h5 = [CP.PropsSI("H", "P", p_in*10**5, 'T', T5, fluid),
                  CP.PropsSI("H", "P", p_in*10**5, 'T', T5, fluid)]
            s5 = [CP.PropsSI("S", "P", p_in*10**5, 'T', T5, fluid),
                  CP.PropsSI("S", "P", p_in*10**5, 'T', T5, fluid)]
            h6 = [CP.PropsSI("H", "P", p_in*10**5, 'T', T6, fluid),
                  CP.PropsSI("H", "P", p_in*10**5, 'T', T6, fluid)]
            s6 = [CP.PropsSI("S", "P", p_in*10**5, 'T', T6, fluid),
                  CP.PropsSI("S", "P", p_in*10**5, 'T', T6, fluid)]
            x = []
            l_compr = []
            Ne0 = []
            l_min = []
            therm_degree = []
            for i in range(2):
                x_temp = (h5[i] - h1[i] - qoc)/(h5[i] - h_liq[i])
                l_compr_temp = (T1*(s6[i] - s1[i]) - (h6[i] - h1[i]))/eta_isot
                l_min_temp = T1 * (s6[i] - s_liq[i]) - (h6[i] - h_liq[i])
                Ne0_temp = l_compr_temp/x_temp
                x.append(x_temp)
                l_compr.append(l_compr_temp)
                l_min.append(l_min_temp)
                Ne0.append(Ne0_temp)
                therm_degree.append(l_min_temp/Ne0_temp)
            return {'fluid': fluid,
                    'x': list(map(to_4_digits, x)),
                    'l_compr': list(map(to_kvalues, l_compr)),
                    'Ne0': list(map(to_kvalues, Ne0)),
                    'l_min': list(map(to_kvalues, l_min)),
                    'therm_degree': list(map(to_4_digits, therm_degree))}
        except Exception as e:
            print('Проверьте верность введённых данных')
            traceback.print_exception(e)


def simple_throttling_refr():
    while True:
        try:
            fluid = input('Введите рабочее тело:  ')
            p1 = int(input("Введите первое давление нагн. [бар]: "))
            p2 = int(input("Введите второе давление нагн. [бар]: "))
            p = {'p1': p1*10**5, 'p2': p2*10**5}
            Tx = int(input('Введите Tx для вашего варианта [K]: '))
            p_in = CP.PropsSI('P', 'T', Tx, 'Q', 0 , fluid)
            T3 = Tx
            T4 = T3
            T5 = T1 - T_ned
            T6 = T1
            h1 = [CP.PropsSI("H", "P", p['p1'], 'T', T1, fluid),
                  CP.PropsSI("H", "P", p['p2'], 'T', T1, fluid)]
            s1 = [CP.PropsSI("S", "P", p['p1'], 'T', T1, fluid),
                  CP.PropsSI("S", "P", p['p2'], 'T', T1, fluid)]
            h5 = [CP.PropsSI("H", "P", p_in, 'T', T5, fluid),
                  CP.PropsSI("H", "P", p_in, 'T', T5, fluid)]
            s5 = [CP.PropsSI("S", "P", p_in, 'T', T5, fluid),
                  CP.PropsSI("S", "P", p_in, 'T', T5, fluid)]
            h6 = [CP.PropsSI("H", "P", p_in, 'T', T6, fluid),
                  CP.PropsSI("H", "P", p_in, 'T', T6, fluid)]
            s6 = [CP.PropsSI("S", "P", p_in, 'T', T6, fluid),
                  CP.PropsSI("S", "P", p_in, 'T', T6, fluid)]
            qx = []
            l_compr = []
            Ne0 = []
            refr_coef_carno = T4/(T1-T4)
            therm_degree = []
            for i in range(2):
                qx_temp = h5[i] - h1[i] - qoc
                l_compr_temp = (T1*(s6[i] - s1[i]) - (h6[i] - h1[i]))/eta_isot
                refr_coef_temp = qx_temp/l_compr_temp
                qx.append(qx_temp)
                l_compr.append(l_compr_temp)
                Ne0.append(refr_coef_temp)
                therm_degree.append(refr_coef_temp/refr_coef_carno)
            return {'fluid': fluid,
                    'q_refr': list(map(to_kvalues, qx)),
                    'l_compr': list(map(to_kvalues, l_compr)),
                    'Ne0': list(map(to_4_digits, Ne0)),
                    'refr_coef_carno': to_4_digits(refr_coef_carno),
                    'therm_degree': list(map(to_4_digits, therm_degree))}
        except Exception as e:
            print('Проверьте верность введённых данных')
            traceback.print_exception(e)


def throttling_prerefr_refr():
    while True:
        try:
            fluid = input('Введите рабочее тело:  ')
            p1 = int(input("Введите первое давление нагн. [бар]: "))
            p2 = int(input("Введите второе давление нагн. [бар]: "))
            Tx = int(input('Введите Tx для вашего варианта [K]: '))
            T_pre = int(input('Введите температуру ПО [К]: '))
            ql = float(input('Введите уд. работу ПО [КДж]: '))
            p = {'p1': p1*10**5, 'p2': p2*10**5}
            p_in = CP.PropsSI('P', "T", Tx, 'Q', 0, fluid)
            T3 = T_pre
            T7 = T_pre - T_ned
            T9 = T1
            T8 = T1 - T_ned
            h1 = [CP.PropsSI("H", "P", p['p1'], 'T', T1, fluid),
                  CP.PropsSI("H", "P", p['p2'], 'T', T1, fluid)]
            s1 = [CP.PropsSI("S", "P", p['p1'], 'T', T1, fluid),
                  CP.PropsSI("S", "P", p['p2'], 'T', T1, fluid)]
            h3 = [CP.PropsSI("H", "P", p['p1'], 'T', T3, fluid),
                  CP.PropsSI("H", "P", p['p2'], 'T', T3, fluid)]
            h7 = [CP.PropsSI("H", "P", p_in, 'T', T7, fluid),
                  CP.PropsSI("H", "P", p_in, 'T', T7, fluid)]
            h8 = [CP.PropsSI("H", "P", p_in, 'T', T8, fluid),
                  CP.PropsSI("H", "P", p_in, 'T', T8, fluid)]
            s8 = [CP.PropsSI("S", "P", p_in, 'T', T8, fluid),
                  CP.PropsSI("S", "P", p_in, 'T', T8, fluid)]
            qx = []
            l_compr = []
            l = []
            l_pre = []
            refr_coef = []
            refr_coef_Carno = [Tx/(T1-Tx), Tx/(T1-Tx)]
            eta_T = []
            for i in range(2):
                qx_temp = h7[i] - h3[i] - qoc
                l_compr_temp = (T1 * (s8[i] - s1[i]) - (h8[i] - h1[i]))/eta_isot
                l_pre_temp = qx_temp/ql
                l_temp = l_compr_temp + l_pre_temp
                refr_coef_temp = qx_temp/l_temp
                eta_T_temp = refr_coef_temp/refr_coef_Carno[0]
                qx.append(qx_temp)
                l_compr.append(l_compr_temp)
                l_pre.append(l_pre_temp)
                refr_coef.append(refr_coef_temp)
                eta_T.append(eta_T_temp)
            return {'fluid': fluid,
                    'qx [кДж]': list(map(to_kvalues, qx)),
                    'l_compr [кДж]': list(map(to_kvalues, l_compr)),
                    'l [кДж]': list(map(to_kvalues, l)),
                    'refr_coef [-]': list(map(to_4_digits, refr_coef)),
                    'l_pre [кДж]': list(map(to_kvalues, l_pre)),
                    'eta_T [-]': list(map(to_4_digits, eta_T))}
        except Exception as e:
            print('Проверьте верность введённых данных')
            traceback.print_exception(e)


def throttling_prerefr_liq():
    while True:
        try:
            fluid = input('Введите рабочее тело:  ')
            p1 = int(input("Введите первое давление нагн. [бар]: "))
            p2 = int(input("Введите второе давление нагн. [бар]: "))
            p_in = float(input('Введите давление вс. [бар]:  '))
            T_pre = int(input('Введите температуру ПО [К]: '))
            ql = float(input('Введите уд. работу ПО [КДж]: '))
            p = {'p1': p1*10**5, 'p2': p2*10**5}
            T3 = T_pre
            T7 = T_pre - T_ned
            T9 = T1
            h1 = [CP.PropsSI("H", "P", p['p1'], 'T', T1, fluid),
                  CP.PropsSI("H", "P", p['p2'], 'T', T1, fluid)]
            s1 = [CP.PropsSI("S", "P", p['p1'], 'T', T1, fluid),
                  CP.PropsSI("S", "P", p['p2'], 'T', T1, fluid)]
            h3 = [CP.PropsSI("H", "P", p['p1'], 'T', T3, fluid),
                  CP.PropsSI("H", "P", p['p2'], 'T', T3, fluid)]
            h7 = [CP.PropsSI("H", "P", p_in*10**5, 'T', T7, fluid),
                  CP.PropsSI("H", "P", p_in*10**5, 'T', T7, fluid)]
            h9 = [CP.PropsSI("H", "P", p_in*10**5, 'T', T9, fluid),
                  CP.PropsSI("H", "P", p_in*10**5, 'T', T9, fluid)]
            s9 = [CP.PropsSI("S", "P", p_in*10**5, 'T', T9, fluid),
                  CP.PropsSI("S", "P", p_in*10**5, 'T', T9, fluid)]
            T_liq = CP.PropsSI('T', "P", p_in*10**5, 'Q', sat_vapor, fluid)
            h_liq = CP.PropsSI('H', "P", p_in*10**5, 'Q', sat_liquid, fluid)
            s_liq = CP.PropsSI('S', "P", p_in*10**5, 'Q', sat_liquid, fluid)
            qx = []
            l_compr = []
            l_compr_iz = []
            l = []
            l_min = []
            Ne0 = []
            x = []
            l_pre = []
            eta_T = []
            for i in range(2):
                qx_temp = h7[i] - h3[i] - qoc
                l_compr_temp_iz = (T1*(s9[i] - s1[i]) - (h9[i] - h1[i]))
                l_compr_temp = l_compr_temp_iz/eta_isot
                l_pre_temp = qx_temp/ql
                l_temp = l_compr_temp + l_pre_temp
                x_temp = ((h7[i] - h3[i])-qoc)/(h7[i] - h_liq)
                Ne0_temp = l_temp/x_temp
                l_min_temp = T1*(s9[i] - s_liq) - (h9[i] - h_liq)
                eta_T_temp = l_min_temp/Ne0_temp
                qx.append(qx_temp)
                l_compr.append(l_compr_temp)
                l_compr_iz.append(l_compr_temp_iz)
                l.append(l_temp)
                l_min.append(l_min_temp)
                Ne0.append(Ne0_temp)
                x.append(x_temp)
                l_pre.append(l_pre_temp)
                eta_T.append(eta_T_temp)
            return {'fluid': fluid,
                    'qx [кДж]': list(map(to_kvalues, qx)),
                    'l_compr [кДж]': list(map(to_kvalues, l_compr)),
                    'l_compr_iz [кДж]': list(map(to_kvalues, l_compr_iz)),
                    'l [кДж]': list(map(to_kvalues, l)),
                    'l_min [кДж]': list(map(to_kvalues, l_min)),
                    'Ne0 [кДж]': list(map(to_kvalues, Ne0)),
                    'x [-]': list(map(to_4_digits, x)),
                    'l_pre [кДж]': list(map(to_kvalues, l_pre)),
                    'eta_T [-]': list(map(to_4_digits, eta_T))}
        except Exception as e:
            print('Проверьте верность введённых данных')
            traceback.print_exception(e)


def double_throttling_liq():
    while True:
        try:
            fluid = input('Введите рабочее тело:  ')
            p1 = int(input("Введите первое давление нагн. [бар]: "))
            p2 = int(input("Введите второе давление нагн. [бар]: "))
            pD = int(input("Введите промежуточное давление [бар]: "))
            p_in = float(input('Введите давление вс. [бар]:  '))
            D = float(input('Введите долю промежуточного потока:  '))
            p = {'p1': p1*10**5, 'p2': p2*10**5}
            R = float(input('Введите газовую постоянную [Дж/кг*К]: '))
            T4 = CP.PropsSI('T', 'P', pD * 10 ** 5, 'Q', 0, fluid)
            T8 = T4
            T5 = CP.PropsSI('T', 'P', p_in * 10 ** 5, 'Q', 0, fluid)
            T7 = T1 - T_ned
            T9 = T1 - T_ned
            h1 = [CP.PropsSI("H", "P", p['p1'], 'T', T1, fluid),
                  CP.PropsSI("H", "P", p['p2'], 'T', T1, fluid)]
            s1 = [CP.PropsSI("S", "P", p['p1'], 'T', T1, fluid),
                  CP.PropsSI("S", "P", p['p2'], 'T', T1, fluid)]
            h1_I = [CP.PropsSI("H", "P", p_in * 10 ** 5, 'T', T1, fluid),
                    CP.PropsSI("H", "P", p_in * 10 ** 5, 'T', T1, fluid)]
            s1_I = [CP.PropsSI("S", "P", p_in * 10 ** 5, 'T', T1, fluid),
                    CP.PropsSI("S", "P", p_in * 10 ** 5, 'T', T1, fluid)]
            h1_II = [CP.PropsSI("H", "P", pD * 10 ** 5, 'T', T1, fluid),
                     CP.PropsSI("H", "P", pD * 10 ** 5, 'T', T1, fluid)]
            c_p7 = [CP.PropsSI("C", "P", p_in * 10 ** 5, 'T', T7, fluid),
                    CP.PropsSI("C", "P", p_in * 10 ** 5, 'T', T7, fluid)]
            c_p9 = [CP.PropsSI("C", "P", pD, 'T', T9, fluid),
                    CP.PropsSI("C", "P", pD, 'T', T9, fluid)]
            h7 = [CP.PropsSI("H", "P", p_in * 10 ** 5, 'T', T7, fluid),
                  CP.PropsSI("H", "P", p_in * 10 ** 5, 'T', T7, fluid)]
            h_liq = [CP.PropsSI("H", "P", p_in * 10 ** 5, 'Q', 0, fluid),
                     CP.PropsSI("H", "P", p_in * 10 ** 5, 'Q', 0, fluid)]
            s_liq = [CP.PropsSI("S", "P", p_in * 10 ** 5, 'Q', 0, fluid),
                     CP.PropsSI("S", "P", p_in * 10 ** 5, 'Q', 0, fluid)]
            delta_hT1 = [h1_I[0] - h1[0], h1_I[1] - h1[1]]
            delta_hT2 = [h1_I[0] - h1_II[0], h1_I[1] - h1_II[1]]
            x = []
            l_compr = []
            l_min = []
            Ne0 = []
            eta_T = []
            for i in range(2):
                x_temp = (delta_hT1[i] - D*delta_hT2[i] - (c_p7[i] * T_ned - D*c_p9[i]*T_ned) - qoc)/(h7[i] - c_p7[i] * T_ned - h_liq[i])
                l_compr_temp_1 = ((1 - D) * R * T1 * log(pD/p_in))/eta_isot
                l_compr_temp_2 = (R * T1 * log(p[f'p{i+1}']/(pD * 10 ** 5)))/eta_isot
                l_compr_temp = l_compr_temp_2 + l_compr_temp_1
                Ne0_temp = l_compr_temp/x_temp
                l_min_temp = T1 * (s1_I[i] - s_liq[i]) - (h1_I[i] - h_liq[i])
                eta_T_temp = l_min_temp/Ne0_temp
                x.append(x_temp)
                l_compr.append(l_compr_temp)
                Ne0.append(Ne0_temp)
                eta_T.append(eta_T_temp)
                l_min.append(l_min_temp)
            return {'fluid': fluid,
                    'x [-]': list(map(to_4_digits, x)),
                    'l_compr [кДж]': list(map(to_kvalues, l_compr)),
                    'l_min [кДж]': list(map(to_kvalues, l_min)),
                    'Ne0 [кДж]': list(map(to_kvalues, Ne0)),
                    'eta_T [-]': list(map(to_4_digits, eta_T))}
        except Exception as e:
            print('Проверьте верность введённых данных')
            traceback.print_exception(e)


def double_throttling_refr():
    while True:
        try:
            fluid = input('Введите рабочее тело:  ')
            p1 = int(input("Введите первое давление нагн. [бар]: "))
            p2 = int(input("Введите второе давление нагн. [бар]: "))
            pD = int(input("Введите промежуточное давление [бар]: "))
            Tx = int(input('Введите Tx для вашего варианта [К]: '))
            D = float(input('Введите долю промежуточного потока: '))
            p = {'p1': p1*10**5, 'p2': p2*10**5}
            p_in = CP.PropsSI('P', "T", Tx, 'Q', 1, fluid)
            T5 = Tx
            T6 = T5
            T7 = T1 - T_ned
            T9 = T1 - T_ned
            h1 = [CP.PropsSI("H", "P", p['p1'], 'T', T1, fluid),
                  CP.PropsSI("H", "P", p['p2'], 'T', T1, fluid)]
            s1 = [CP.PropsSI("S", "P", p['p1'], 'T', T1, fluid),
                  CP.PropsSI("S", "P", p['p2'], 'T', T1, fluid)]
            h7 = [CP.PropsSI("H", "P", p_in, 'T', T7, fluid),
                  CP.PropsSI("H", "P", p_in, 'T', T7, fluid)]
            h9 = [CP.PropsSI("H", "P", pD * 10 ** 5, 'T', T9, fluid),
                  CP.PropsSI("H", "P", pD * 10 ** 5, 'T', T9, fluid)]
            s9 = [CP.PropsSI("S", "P", pD * 10 ** 5, 'T', T9, fluid),
                  CP.PropsSI("S", "P", pD * 10 ** 5, 'T', T9, fluid)]
            qx = []
            l_compr = []
            refr_coef = []
            eta_T = []
            for i in range(2):
                qx_temp = (h7[i] - h1[i]) - D * (h7[i] - h9[i]) - qoc
                l_compr_temp_1 = (T1*(s9[i] - s1[i]) - (h9[i] - h1[i]))/eta_isot
                l_compr_temp_2 = (1 - D) * (T1*(s9[i] - s1[i]) - (h9[i] - h1[i]))/eta_isot
                l_compr_temp = l_compr_temp_2 + l_compr_temp_1
                refr_coef_temp = qx_temp/l_compr_temp
                refr_coef_Carno = T6/(T1-T6)
                qx.append(qx_temp)
                l_compr.append(l_compr_temp)
                refr_coef.append(refr_coef_temp)
                eta_T.append(refr_coef_temp/refr_coef_Carno)
            return {'fluid': fluid,
                    'qx [кДж]': list(map(to_kvalues, qx)),
                    'l_compr [кДж]': list(map(to_kvalues, l_compr)),
                    'refr_coef_Carno [кДж]': to_4_digits(refr_coef_Carno),
                    'refr_coef [кДж]': list(map(to_4_digits, refr_coef)),
                    'eta_T [-]': list(map(to_4_digits, eta_T))}
        except Exception as e:
            print('Проверьте верность введённых данных')
            traceback.print_exception(e)


def steam_compression_cycle():
    while True:
        try:
            fluid = input('Введите хладагент: ')
            temp_con = int(input('Введите температуру конденсации в '
                                 '!!градусах Цельсия!!: ')) + 273  # K
            temp_ev = int(input('Введите температуру испарение в '
                                '!!градусах Цельсия!!: ')) + 273  # K
            T2 = temp_con
            T3 = temp_ev
            T4 = T3
            p1 = CP.PropsSI('P', "T", temp_con, 'Q',sat_vapor , fluid)
            p2 = CP.PropsSI('P', "T", temp_ev, 'Q', sat_liquid, fluid)
            s4 = CP.PropsSI('S', "T", T4, 'Q', sat_vapor, fluid)
            h1 = CP.PropsSI("H", "P", p1, 'S', s4, fluid)
            h2 = CP.PropsSI("H", "T", temp_con, 'Q', sat_liquid, fluid)
            h3 = h2
            h4 = CP.PropsSI("H", "P", p2, 'Q', sat_vapor, fluid)
            T1 = CP.PropsSI("T", "P", p1, 'S', s4, fluid)
            q_refr = h4 - h3
            l_compr = h1 - h4
            Ne0 = q_refr/l_compr
            refr_coef_carno = T4/(T2-T4)
            therm_degree = Ne0/refr_coef_carno
            return {"p1": round(p1/10**5, 3),
                    "p2": round(p2/10**5, 3),
                    'T_con': temp_con,
                    'T_ev': temp_ev,
                    "h1": round(h1/1000, 3),
                    "h2": round(h2/1000, 3),
                    "h3": round(h3/1000, 3),
                    "h4": round(h4/1000, 3),
                    "T1": round(T1),
                    "T2": T2,
                    "T3": T3,
                    "T4": T4,
                    'fluid': fluid,
                    'q_refr': round(q_refr/1000, 3),
                    'l_compr': round(l_compr/1000, 3),
                    'Ne0': round(Ne0, 3),
                    'refr_coef_carno': round(refr_coef_carno, 3),
                    'therm_degree': round(therm_degree, 3)}
        except Exception as ex:
            print('Проверьте верность введённых данных')
            traceback.print_exception(ex)


if __name__ == '__main__':
    # answer = simple_throttling_liq()
    # answer = simple_throttling_refr()
    # answer = throttling_prerefr_liq()
    # answer = throttling_prerefr_refr()
    # answer = double_throttling_liq()
    # answer = steam_compression_cycle()
    answer = double_throttling_refr()
    for variable, value in answer.items():
        print(f"{variable} --- {value}")
