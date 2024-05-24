import jinja2
import pdfkit
from main import steam_compression_cycle
import base64


def get_image_file_as_base64_data():
    with open('VaporcomprDiagram.png', 'rb') as image_file:
        return base64.b64encode(image_file.read())


def main():
    context = steam_compression_cycle()
    context['image'] = str(get_image_file_as_base64_data())[2:]
    template_loader = jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)

    template = template_env.get_template('template.html')
    output_text = template.render(context)

    config = pdfkit.configuration(wkhtmltopdf="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
    pdfkit.from_string(output_text, 'steam_compression_cycle.pdf', configuration=config)


if __name__ == '__main__':
    main()
    print('File has been created')

