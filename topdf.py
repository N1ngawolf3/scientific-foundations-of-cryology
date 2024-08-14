import jinja2
import pdfkit
from main import *
import base64
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

full_funcs_name = ['Цикл простого дросселирования: Ожижительный режим',
                   'Цикл простого дросселирования: Рефрижераторный режим',
                   'Дроссельный цикл с предварительный охлаждением: Рефрижераторный режим',
                   'Дроссельный цикл с предварительный охлаждением: Ожижительный режим',
                   'Цикл двойного дросселирования: Рефрижераторный режим',
                   'Цикл двойного дросселирования: Ожижительный режим',
                   'Парокомпрессионный цикл']

funcs_list = dict(zip(full_funcs_name, funcs.values()))
# funcs_name_list = dict(zip(full_funcs_name, funcs.keys()))


def get_graph_image(cycle_name):
    with open(f'graphs/{funcs_list[cycle_name].__name__}_graph.jpg', 'rb') as image_file:
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


def topdf(func_name, surname, number, context):
    context['image_cycle'] = get_graph_image(func_name)
    template_loader = jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)
    output_text = template_gen(context, template_env, funcs_list[func_name].__name__)
    config = pdfkit.configuration(wkhtmltopdf="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
    pdfkit.from_string(output_text, f'created_pdf/{func_name}_{surname}_{number}.pdf',
                       configuration=config, css='html_templates/style.css')


if __name__ == '__main__':
    # topdf()
    pass
