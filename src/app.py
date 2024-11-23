from flask import Flask, render_template
import pathlib
import random
from postgre_database import DatabasePostgre


class WebApp:
    def __init__(self, database):
        self.app = Flask(__name__, template_folder='../templates', static_folder='../static')
        self.setup_routes()
        self.bd = database

    def setup_routes(self):
        @self.app.route('/')
        def index():
            print('Вызов Главной')
            data_recomend, data_popular, readers_choise = self.collect_data()
            return self.render_page_index(data_recomend, data_popular, readers_choise)

        @self.app.route('/about')
        def about():
            return render_template('about.html')

        @self.app.errorhandler(404)
        def page_not_found(e):
            return render_template('404.html'), 404

    def collect_data(self):  # todo в класс
        recom_dict = self.recomendations()
        popular_dict = self.popular()
        readers_choise = self.readers_choise()
        return recom_dict, popular_dict, readers_choise

    def recomendations(self):
        list_id_recomend=(random.sample(range(2, 13), 7))
        feetback_base=self.bd.get_base_info_of_books(list_id_recomend)
        print(list_id_recomend,feetback_base)
        recomend_dict = {}
        for i in feetback_base:
            recomend_dict[i[0]] = {"book_name": i[1], 'authors': i[2]}
        return  recomend_dict
            # 2: {'book_name': 'Октавия на сверхзвуке', 'authors':['И.Такуми','Товарищ фудживаров'],'description':'Занимательная аэродиниммика для всех'},
            # 3: {'book_name': 'Книга2', 'authors': ['А.Такуми1'],'description':'чисто тст тема'},

    def popular(self):
        list_id_popular = (random.sample(range(2, 13), 6))
        list_id_popular[1]=19
        feetback_base = self.bd.get_base_info_of_books(list_id_popular)
        popular_dict = {}
        for i in feetback_base:
            popular_dict[i[0]] = {"book_name": i[1], 'authors': i[2]}
        return popular_dict

    def readers_choise(self):
        list_id_readers_choise = (random.sample(range(2, 13), 6))
        feetback_base = self.bd.get_base_info_of_books(list_id_readers_choise)
        readers_choise_dict = {}
        for i in feetback_base:
            readers_choise_dict[i[0]] = {"book_name": i[1], 'authors': i[2]}
        return readers_choise_dict

    def render_page_index(self, data1, data2, data3):
        return render_template('index.html', recomend=data1, popular=data2, readers_choise=data3)

    def app_start(self):
        self.app.run(debug=True)
