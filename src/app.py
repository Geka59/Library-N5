from flask import Flask, render_template
import pathlib

class WebApp():
    def __init__(self):
        self.app = Flask(__name__, template_folder='../templates', static_folder='../static')
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            data_recomend,data_popular = self.collect_data()
            return self.render_page(data_recomend,data_popular)

        @self.app.route('/about')
        def about():
            return render_template('about.html')

    def collect_data(self):
        recom_dict = {
            'Тарас Бульба': ['Автор1','Описание1'],
            'ПИТарас Бульба': ['Автор2','Описание2'],
        }
        popular_dict = {
            'Октавия на сверхзвуке': ['Автор Октави', 'Описание Октавии'],
            'Земледельие': ['Автор Земледелия', 'Земледел'],
        }
        return recom_dict,popular_dict

    def render_page(self, data1, data2):
        return render_template('index.html',text=data1,popular=data2)

    def app_start(self):
        self.app.run(debug=True)

