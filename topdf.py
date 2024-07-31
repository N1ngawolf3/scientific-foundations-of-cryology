import jinja2
import pdfkit
from main import *
import base64


def get_image_vaporcomprdiagram():
    with open('VaporcomprDiagram.png', 'rb') as image_file:
        return str(base64.b64encode(image_file.read()))[2:]


def main():
    context = steam_compression_cycle()
    context['image'] = get_image_vaporcomprdiagram()
    template_loader = jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)

    template = template_env.get_template('template.html')
    output_text = template.render(context)

    config = pdfkit.configuration(wkhtmltopdf="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
    pdfkit.from_string(output_text, 'steam_compression_cycle.pdf',
                       configuration=config, css='vaporcompr.css')


if __name__ == '__main__':
    main()
    print('File has been created')
