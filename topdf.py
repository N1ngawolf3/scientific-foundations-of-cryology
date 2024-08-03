import jinja2
import pdfkit
from main import *
import base64


def get_image_vaporcomprdiagram():
    with open('diagrams/steam_compr_graph.png', 'rb') as image_file:
        return str(base64.b64encode(image_file.read()))[2:]


def main():
    context = simple_throttling_refr()
    surname = input('Введите фамилию: ')
    context['image'] = get_image_vaporcomprdiagram()
    template_loader = jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)

    template = template_env.get_template('html_temlpates/SimpleThrottlingRefr.html')
    output_text = template.render(context)

    config = pdfkit.configuration(wkhtmltopdf="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
    pdfkit.from_string(output_text, f'created_pdf/SimpleThrottlingRefr_{surname}.pdf',
                       configuration=config, css='html_temlpates/vaporcompr.css')


if __name__ == '__main__':
    main()
    print('File has been created')
