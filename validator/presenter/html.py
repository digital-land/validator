from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader('validator', 'templates'),
    autoescape=select_autoescape(['html'])
)

template = env.get_template('result.html')


class HtmlResultPresenter:

    def __init__(self, result):
        self.result = result

    def __str__(self):
        return template.render(result=self.result)
