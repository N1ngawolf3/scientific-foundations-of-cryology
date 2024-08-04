import jinja2
import pdfkit
from main import *
import base64

funcs = {'ЦПДО': simple_throttling_liq,
         'ЦПДР': simple_throttling_refr,
         'ДЦПОР': throttling_prerefr_refr,
         'ДЦПОО': throttling_prerefr_liq,
         'ДДР': double_throttling_refr,
         'ДДО': double_throttling_refr,
         'ПКЦ': steam_compression_cycle
         }


def get_graph_image(cycle_name):
    with open(f'diagrams/{funcs[cycle_name].__name__}_graph.jpg', 'rb') as image_file:
        return str(base64.b64encode(image_file.read()))[2:]


def main():
    problem = input(f'Выберите задачу из списка: {list(funcs.keys())}\n'
                    f'Введите задачу (для завершения оставьте поле пустым): ')
    while problem != '':
        context = funcs[problem]()
        surname = input('Введите фамилию: ')
        number = input('Введите номер варианта: ')
        context['image'] = get_graph_image(problem)
        template_loader = jinja2.FileSystemLoader('./')
        template_env = jinja2.Environment(loader=template_loader)

        template = template_env.get_template(f'html_templates/{funcs[problem].__name__}_template.html')
        output_text = template.render(context)

        config = pdfkit.configuration(wkhtmltopdf="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
        pdfkit.from_string(output_text, f'created_pdf/{problem}_{surname}_{number}.pdf',
                           configuration=config, css='html_templates/vaporcompr.css')
        print('Файл успешно создан')
        problem = input(f'Выберите задачу из списка: {list(funcs.keys())}\n'
                        f'Введите задачу (для завершения оставьте поле пустым): ')


if __name__ == '__main__':
    main()
