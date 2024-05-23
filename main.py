import CoolProp.CoolProp as CP


sat_liquid = 1
sat_vapor = 0

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

            p1 = CP.PropsSI('P', "T", temp_con, 'Q', 0, fluid)
            p2 = CP.PropsSI('P', "T", temp_ev, 'Q', 1, fluid)

            s4 = CP.PropsSI('S', "T", T4, 'Q', sat_liquid, fluid)

            h1 = CP.PropsSI("H", "P", p1, 'S', s4, fluid)
            h2 = CP.PropsSI("H", "T", temp_con, 'Q', sat_vapor, fluid)
            h3 = h2
            h4 = CP.PropsSI("H", "P", p2, 'Q', sat_liquid, fluid)

            T1 = CP.PropsSI("T", "P", p1, 'S', s4, fluid)

            # print(f'p1 = {round(p1/10**5, 3)} бар', f'p2 = {round(p2/10**5, 3)} бар')
            # print(f'T1 = {round(T1)} K', f'T2 = {T2} K', f'T3 = {T3} K', f'T4 = {T4} K')
            # print(f'h1 = {round(h1/1000, 3)} кДж/кг',
            #       f'h2 = {round(h2/1000, 3)} кДж/кг',
            #       f'h3 = {round(h3/1000, 3)} кДж/кг',
            #       f'h4 = {round(h4/1000, 3)} кДж/кг')

            q_refr = h4 - h3
            l_compr = h1 - h4
            refr_coef = q_refr/l_compr
            refr_coef_carno = T4/(T2-T4)
            therm_degree = refr_coef/refr_coef_carno

            return {'qx':q_refr,
                    'lсж': l_compr,
                    'холод_коэф': refr_coef,
                    'холод_коэф_Карно': refr_coef_carno,
                    'Термод_соверш': therm_degree}
        except Exception as ex:
            print('Проверьте верность введённых данных')
            print(ex)


print(steam_compression_cycle())
