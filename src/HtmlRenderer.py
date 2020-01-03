import jinja2
import codecs


def render_html(template_name, context, target):
    html_content = (
        jinja2.Environment(loader=jinja2.FileSystemLoader("./templates"))
        .get_template(template_name)
        .render(context)
    )
    with codecs.open(target, "wb", encoding="utf8") as f:
        f.write(html_content)
