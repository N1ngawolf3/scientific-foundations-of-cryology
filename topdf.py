import jinja2
import pdfkit
from main import *
import base64
from db import add_solved_task, check_presence, connection
import traceback

# TODO каким-то хером отследить одно отрицательное, одно положительное значение
funcs = {'ЦПДО': simple_throttling_liq,
         'ЦПДР': simple_throttling_refr,
         'ДЦПОР': throttling_prerefr_refr,
         'ДЦПОО': throttling_prerefr_liq,
         'ДДР': double_throttling_refr,
         'ДДО': double_throttling_liq,
         'ПКЦ': steam_compression_cycle
         }


def get_graph_image(cycle_name):
    with open(f'graphs/{funcs[cycle_name].__name__}_graph.jpg', 'rb') as image_file:
        return str(base64.b64encode(image_file.read()))[2:]


def get_argon_graph_image():
    with open('graphs/argon_phase_graph.jpg', 'rb') as image_file:
        return str(base64.b64encode(image_file.read()))[2:]


def template_gen(context, template_env, func_name):
    if 'argon_error' in context:
        context['phase_graph'] = get_argon_graph_image()
        template = template_env.get_template(f'html_templates/{func_name}_'
                                             f'argon_error_template.html')
        output_text = template.render(context)
        return output_text
    else:
        try:
            for el in context['qx']:
                if el < 0:
                    template = template_env.get_template(f'html_templates/{func_name}_negative_template.html')
                    output_text = template.render(context)
                else:
                    template = template_env.get_template(f'html_templates/{func_name}_template.html')
                    output_text = template.render(context)
            return output_text
        except KeyError:
            for el in context['x']:
                if el < 0:
                    template = template_env.get_template(f'html_templates/{func_name}_negative'
                                                         f'_template.html')
                    output_text = template.render(context)
                else:
                    template = template_env.get_template(f'html_templates/{func_name}_template.html')
                    output_text = template.render(context)
            return output_text


def main():
    problem = input(f'Выберите задачу из списка: {list(funcs.keys())}\n'
                    f'Введите задачу (для завершения оставьте поле пустым): ')
    while problem != '':
        try:
            context = funcs[problem]()
            surname = input('Введите фамилию: ')
            number = input('Введите номер варианта: ')
            if 'Tx' in context:
                context['p_in'] = None
            if context['p_in'] is not None:
                context['Tx'] = None
            if 'Tcond' not in context:
                context['Tcond'] = None
                context['Tev'] = None
            context['image_cycle'] = get_graph_image(problem)
            template_loader = jinja2.FileSystemLoader('./')
            template_env = jinja2.Environment(loader=template_loader)
            output_text = template_gen(context, template_env, funcs[problem].__name__)
            config = pdfkit.configuration(wkhtmltopdf="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
            pdfkit.from_string(output_text, f'created_pdf/{problem}_{surname}_{number}.pdf',
                               configuration=config, css='html_templates/style.css')
            add_solved_task(number, surname, problem, context['fluid'], context['p'][0],
                            context['p'][1], context['p_in'], context['Tx'], context['Tcond'], context['Tev'])
            problem = input(f'Выберите задачу из списка: {list(funcs.keys())}\n'
                            f'Введите задачу (для завершения оставьте поле пустым): ')
            # else:
            #    print('Данная задача уже решена')
            #    problem = input(f'Выберите задачу из списка: {list(funcs.keys())}\n'
            #                    f'Введите задачу (для завершения оставьте поле пустым): ')
        except KeyError as ex:
            traceback.print_exception(ex)
            print(f'Видимо ты указал что-то не так: {ex}')
            problem = input('Введите задачу (для завершения оставьте поле пустым): ')
    connection.close()
    print('Файлы успешно созданы')


if __name__ == '__main__':
    main()
