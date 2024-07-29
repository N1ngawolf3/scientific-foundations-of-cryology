import CoolProp.CoolProp as CP
import traceback
import pprint

sat_liquid = 0
sat_vapor = 1


def to_kvalues(value):
    return round(value/1000, 3)


def to_4_digits(value):
    return round(value, 4)




def simple_throttling_refr():
    while True:
        try:
            fluid = input('Введите рабочее тело:  ')
            p1 = int(input("Введите первое давление нагн. [бар]: "))
            p2 = int(input("Введите второе давление нагн. [бар]: "))
            p_in = float(input('Введите давление вс. [бар]:  '))
            p = {'p1': p1*10**5, 'p2': p2*10**5}
            qoc = 2000  # J
            Tx = int(input('Введите Tx для вашего варианта [K]: '))
            T1 = 300  # К
            T3 = Tx
            T4 = T3
            T_ned = 15
            T5 = T1 - T_ned
            T6 = T1
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
            qx = []
            l_compr = []
            refr_coef = []
            refr_coef_carno = T4/(T1-T4)
            therm_degree = []
            for i in range(2):
                qx_temp = h5[i] - h1[i] - qoc
                l_compr_temp = (T1*(s6[i] - s1[i]) - (h6[i] - h1[i]))/0.7
                refr_coef_temp = qx_temp/l_compr_temp
                qx.append(qx_temp)
                l_compr.append(l_compr_temp)
                refr_coef.append(refr_coef_temp)
                therm_degree.append(refr_coef_temp/refr_coef_carno)
            return {'fluid': fluid,
                    'q_refr': list(map(to_kvalues, qx)),
                    'l_compr': list(map(to_kvalues, l_compr)),
                    'refr_coef': list(map(to_4_digits, refr_coef)),
                    'refr_coef_carno': to_4_digits(refr_coef_carno),
                    'therm_degree': list(map(to_4_digits, therm_degree))}
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
            # fluid = 'Air'
            # p1 = 250
            # p2 = 430
            # p_in = 1.5
            # T_pre = 250
            # ql = 2.8
            p = {'p1': p1*10**5, 'p2': p2*10**5}
            qoc = 2000  # J
            T_ned = 15
            T1 = 300  # К
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
                l_compr_temp = l_compr_temp_iz/0.7
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

            p1 = CP.PropsSI('P', "T", temp_con, 'Q', sat_liquid, fluid)
            p2 = CP.PropsSI('P', "T", temp_ev, 'Q', sat_vapor, fluid)

            s4 = CP.PropsSI('S', "T", T4, 'Q', sat_liquid, fluid)

            h1 = CP.PropsSI("H", "P", p1, 'S', s4, fluid)
            h2 = CP.PropsSI("H", "T", temp_con, 'Q', sat_vapor, fluid)
            h3 = h2
            h4 = CP.PropsSI("H", "P", p2, 'Q', sat_liquid, fluid)

            T1 = CP.PropsSI("T", "P", p1, 'S', s4, fluid)

            q_refr = h4 - h3
            l_compr = h1 - h4
            refr_coef = q_refr/l_compr
            refr_coef_carno = T4/(T2-T4)
            therm_degree = refr_coef/refr_coef_carno

            return {"p1 [бар]": round(p1/10**5, 3),
                    "p2 [бар]": round(p2/10**5, 3),
                    'T_con [К]': temp_con,
                    'T_ev [К]': temp_ev,
                    "h1 [кДж]": round(h1/1000, 3),
                    "h2 [кДж]": round(h2/1000, 3),
                    "h3 [кДж]": round(h3/1000, 3),
                    "h4 [кДж]": round(h4/1000, 3),
                    "T1 [К]": round(T1),
                    "T2 [К]": T2,
                    "T3 [К]": T3,
                    "T4 [К]": T4,
                    'fluid': fluid,
                    'q_refr [кДж]': round(q_refr/1000, 3),
                    'l_compr [кДж]': round(l_compr/1000, 3),
                    'refr_coef [-]': round(refr_coef, 3),
                    'refr_coef_carno [-]': round(refr_coef_carno, 3),
                    'therm_degree [-]': round(therm_degree, 3)}
        except Exception as ex:
            print('Проверьте верность введённых данных')
            print(ex)


if __name__ == '__main__':
    # pprint.pprint(simple_throttling_refr())
    # pprint.pprint(steam_compression_cycle())
    pprint.pprint(throttling_prerefr_liq())

