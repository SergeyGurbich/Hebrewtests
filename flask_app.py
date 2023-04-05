'''Код для сайта с ивритскими тестами
В этой версии добавляется поддержка нескольких языков через flask-babel'''

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from forms import testform
from flask_babel import Babel, _
from config import Config
import random


app = Flask(__name__)
'''
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])
    #return request.accept_languages.best_match(app.config['LANGUAGES'].keys())
'''

def get_locale():
    # Если юзер выбрал язык из меню, он сохранился через ф-цию set_local in session['language']
    try:
        language = session['language']
    except KeyError:
        language = None
    if language is not None:
        return language
    return request.accept_languages.best_match(app.config['LANGUAGES'])

babel = Babel(app)
babel.init_app(app, locale_selector=get_locale)

app.config["SECRET_KEY"] = "green"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Hebrewtests.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['LANGUAGES'] = ['uk', 'ru'] # Эта конфигурация прописана в файле config, класс Config
#app.config['LANGUAGES'] = {'ee':'Estonian', 'uk':'Ukrainian', 'ru':'Russian'}
#app.config['BABEL_DEFAULT_LOCALE'] = ['ru']
app.config['JSON_AS_ASCII'] = False

grade=[]
mist=[]

with app.app_context():
    # Таблица для названий теста и связанная таблица для вопросов по каждому тесту
    db = SQLAlchemy(app)

    class Tests(db.Model):
        id = db.Column(db.Integer, primary_key = True) 
        title = db.Column(db.String(100), index = True, unique = False) 
        title_uk = db.Column(db.String(100), index = True, unique = False)
        mes_before = db.Column(db.String(400), index = True, unique = False) 
        mes_before_uk = db.Column(db.String(400), index = True, unique = False)
        mes_after = db.Column(db.String(400), index = True, unique = False) 
        mes_after_uk = db.Column(db.String(400), index = True, unique = False) 
        level = db.Column(db.Integer, index = True, unique = False) 
        questions = db.relationship('Questions', backref='test', lazy='dynamic')

        def __repr__(self):
            return '<{}>'.format(self.title)

    class Questions(db.Model):
        id = db.Column(db.Integer, primary_key = True) 
        question = db.Column(db.String(100), index = True, unique = False) 
        answers = db.Column(db.String(100), index = True, unique = False)
        correct = db.Column(db.String(100), index = True, unique = False)
        test_id = db.Column(db.Integer, db.ForeignKey('tests.id'))
        topic = db.Column(db.String(100), index = True, unique = False)
        topic_uk = db.Column(db.String(100), index = True, unique = False)

        def __repr__(self):
            return '<{}>'.format(self.question)

    class Audiotests(db.Model):
        id = db.Column(db.Integer, primary_key = True) 
        title = db.Column(db.String(100), index = True, unique = False) 
        title_uk = db.Column(db.String(100), index = True, unique = False)
        mes_before = db.Column(db.String(400), index = True, unique = False)
        mes_before_uk = db.Column(db.String(400), index = True, unique = False)  
        mes_after = db.Column(db.String(400), index = True, unique = False)
        mes_after_uk = db.Column(db.String(400), index = True, unique = False) 
        link=db.Column(db.String(100), index = True, unique = False)
        level = db.Column(db.Integer, index = True, unique = False) 
        questions = db.relationship('AudioQuestions', backref='test', lazy='dynamic')

        def __repr__(self):
            return '<{}>'.format(self.title)

    class AudioQuestions(db.Model):
        id = db.Column(db.Integer, primary_key = True) 
        question = db.Column(db.String(100), index = True, unique = False) 
        answers = db.Column(db.String(100), index = True, unique = False)
        correct = db.Column(db.String(100), index = True, unique = False)
        test_id = db.Column(db.Integer, db.ForeignKey('audiotests.id'))
        topic = db.Column(db.String(100), index = True, unique = False)

        def __repr__(self):
            return '<{}>'.format(self.question)

    class Videotests(db.Model):
        id = db.Column(db.Integer, primary_key = True) 
        title = db.Column(db.String(100), index = True, unique = False)
        title_uk = db.Column(db.String(100), index = True, unique = False) 
        mes_before = db.Column(db.String(400), index = True, unique = False)
        mes_before_uk = db.Column(db.String(400), index = True, unique = False) 
        mes_after = db.Column(db.String(400), index = True, unique = False)
        mes_after_uk = db.Column(db.String(400), index = True, unique = False) 
        link=db.Column(db.String(100), index = True, unique = False)
        level = db.Column(db.Integer, index = True, unique = False) 
        questions = db.relationship('VideoQuestions', backref='test', lazy='dynamic')

        def __repr__(self):
            return '<{}>'.format(self.title)

    class VideoQuestions(db.Model):
        id = db.Column(db.Integer, primary_key = True) 
        question = db.Column(db.String(100), index = True, unique = False) 
        answers = db.Column(db.String(100), index = True, unique = False)
        correct = db.Column(db.String(100), index = True, unique = False)
        test_id = db.Column(db.Integer, db.ForeignKey('videotests.id'))
        topic = db.Column(db.String(100), index = True, unique = False)

        def __repr__(self):
            return '<{}>'.format(self.question)

    db.create_all()

@app.context_processor # Создает словарь как глобальную переменную, доступную в шаблонах
def inject_conf_var():
    return dict(AVAILABLE_LANGUAGES=app.config['LANGUAGES'], CURRENT_LANGUAGE=session.get('language', request.accept_languages.best_match(app.config['LANGUAGES'])))

@app.route('/set_locale', methods=['POST'])
def set_locale():
    lang = request.form['lang']
    session['language'] = lang 
    return redirect(request.referrer or url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/about')
def about():
    return render_template('professor.html')

@app.route('/textbook')
def textbook():
    return render_template('textbook.html')

@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/api_info')
def api_info():
    return render_template('api_info.html')

@app.route('/tests_general')
def tests_gen():
    tests=Tests.query.order_by(Tests.id)
    audiotests=Audiotests.query.order_by(Audiotests.id)
    videotests=Videotests.query.order_by(Videotests.id)
    lang=get_locale()
    return render_template('tests_general.html', rows = tests, rows_audio=audiotests, rows_video=videotests, lang=lang)

@app.route('/tests/<quiz_num>')
def start_quiz(quiz_num):
    return redirect(url_for('tests', quiz_num=quiz_num, question_number=1))

@app.route('/tests/<quiz_num>/<int:question_number>', methods=["GET", "POST"])
def tests(quiz_num, question_number):
    
    questions = Tests.query.get(quiz_num).questions.all()
    #raw = Tests.query.get(quiz_num)
    radioform = testform()
    if request.method == "GET":

        quest = questions[question_number-1].question #!!!
        choices = questions[question_number-1].answers.split('|')
        
        radioform.quest.choices = choices
        
        return render_template('test_quest.html', quest = quest, answs = choices, 
                               id=quiz_num, form=radioform, i=question_number)
    
    if request.method == "POST":
        lang = get_locale() 
        correct = questions[question_number-1].correct
        answer = radioform.quest.data
        if answer == correct:
            grade.append(question_number) 
        else:
            if lang =='uk':
                mist.append(questions[question_number-1].topic_uk)
            else:
                mist.append(questions[question_number-1].topic)

        if question_number < 10:
            return redirect(url_for('tests', quiz_num = quiz_num, question_number = question_number+1))
        else: 
            grade1 = set(grade) # избежать повторного прохождения вопроса, вернувшись назад
            points = len(grade1)
            grade.clear()
            grade1.clear()
            if points == 10:
                if lang =='uk':
                    txt=Tests.query.get(quiz_num).mes_after_uk
                else:
                    txt=Tests.query.get(quiz_num).mes_after
                txt1=''
            else:
                if lang =='uk':
                    txt=Tests.query.get(quiz_num).mes_before_uk
                else:
                    txt=Tests.query.get(quiz_num).mes_before
                txt1=_('Возможно, вам стоит повторить следующие темы:')
    
            a=[ele for ele in mist]
            mist.clear()

            return render_template('grade.html', points = points, mist1=a, txt=txt, txt_mist=txt1)
        
@app.route('/audiotests/<quiz_num>')
def start_audioquiz(quiz_num):
    return redirect(url_for('audiotests', quiz_num=quiz_num, question_number=1))

@app.route('/audiotests/<quiz_num>/<int:question_number>', methods=["GET", "POST"])
def audiotests(quiz_num, question_number):
    
    questions = Audiotests.query.get(quiz_num).questions.all()
    link = Audiotests.query.get(quiz_num).link
    file='audiotest'+quiz_num+'.mp3'
    audio_url = url_for('static', filename='audio/' + link) # or + file
    radioform = testform()
    if request.method == "GET":

        quest = questions[question_number-1].question #!!!
        choices = questions[question_number-1].answers.split('|')
        
        radioform.quest.choices = choices
        
        return render_template('audiotest_quest.html', quest = quest, answs = choices, 
                               id=quiz_num, form=radioform, i=question_number, audio_url=audio_url)

    if request.method == "POST":
        lang = get_locale() 
        correct = questions[question_number-1].correct
        answer = radioform.quest.data
        if answer == correct:
            grade.append(question_number) 
        else:
            mist.append(question_number)
        
        if question_number < 10:
            return redirect(url_for('audiotests', quiz_num = quiz_num, question_number = question_number+1))
        else:
            grade1 = set(grade) # избежать повторного прохождения вопроса, вернувшись назад
            points = len(grade1)
            grade.clear()
            grade1.clear()
            if points == 10:
                if lang =='uk':
                    txt=Audiotests.query.get(quiz_num).mes_after_uk
                else:
                    txt=Audiotests.query.get(quiz_num).mes_after
                txt1=''
            else:
                if lang =='uk':
                    txt=Audiotests.query.get(quiz_num).mes_before_uk
                else:
                    txt=Audiotests.query.get(quiz_num).mes_before
                txt1=_('Ошибки были допущены при ответе на следующие вопросы:')
    
            a=[ele for ele in mist]
            mist.clear()

            return render_template('grade.html', points = points, mist1=a, txt=txt, txt_mist=txt1)

@app.route('/videotests/<quiz_num>')
def start_videoquiz(quiz_num):
    return redirect(url_for('videotests', quiz_num=quiz_num, question_number=1))

@app.route('/videotests/<quiz_num>/<int:question_number>', methods=["GET", "POST"])
def videotests(quiz_num, question_number):
    
    questions = Videotests.query.get(quiz_num).questions.all()
    link = Videotests.query.get(quiz_num).link
    video_url = link 
    radioform = testform()
    if request.method == "GET":

        quest = questions[question_number-1].question #!!!
        choices = questions[question_number-1].answers.split('|')
        
        radioform.quest.choices = choices
        
        return render_template('videotest_quest.html', quest = quest, answs = choices, 
                               id=quiz_num, form=radioform, i=question_number, video_url=video_url)

    if request.method == "POST":
        lang = get_locale() 
        correct = questions[question_number-1].correct
        answer = radioform.quest.data
        if answer == correct:
            grade.append(question_number) 
        else:
            mist.append(question_number)
        
        if question_number < 10:
            return redirect(url_for('videotests', quiz_num = quiz_num, question_number = question_number+1))
        else:
            grade1 = set(grade) # избежать повторного прохождения вопроса, вернувшись назад
            points = len(grade1)
            grade.clear()
            grade1.clear()
            if points == 10:
                if lang =='uk':
                    txt=Videotests.query.get(quiz_num).mes_after_uk
                else:
                    txt=Videotests.query.get(quiz_num).mes_after
                txt1=''
            else:
                if lang =='uk':
                    txt=Videotests.query.get(quiz_num).mes_before_uk
                else:
                    txt=Videotests.query.get(quiz_num).mes_before
                txt1=_('Ошибки были допущены при ответе на следующие вопросы:')
    
            a=[ele for ele in mist]
            mist.clear()

            return render_template('grade.html', points = points, mist1=a, txt=txt, txt_mist=txt1)

@app.route('/api')
def api():
    level = request.args.get('level')
    if level == 'A1':
        num = random.randint(1, 30)
    elif level == 'A2':
        num = random.randint(31, 60)
    else:
        num = random.randint(1, 60)
    RandQuest = Questions.query.get(num)
    quest = RandQuest.question
    choices = RandQuest.answers.split('|')
    correct = RandQuest.correct

    dct = {'question':quest, 'choices':choices, 'correct_answer': correct}
    return jsonify(dct) 

if __name__ == '__main__':
    app.run(debug=True)
