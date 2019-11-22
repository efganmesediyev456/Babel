import os

from flask import Flask, render_template, url_for, request, redirect
from flask_babel import Babel

from app.Pofile import Pofile

app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE']='az'
babel = Babel(app)


@babel.localeselector
def get_locale():
    return 'az'


@app.route('/')
def messages():
    pofiles=os.listdir(os.path.join(os.getcwd(),r'app\translations'))
    direct=[]
    for directory in pofiles:
        direct.append(directory)
    return render_template('po/messages.html', direct=direct)

@app.route('/message/<locale>')
def message(locale):
    po = Pofile(locale)
    filter = request.args.get('filter')
    po_entries = po.poFilterValues(filter)
    send = po.filterPagination(filter)
    return render_template('po/index.html', po_entries=send['pagination_entries'],
                           page=send['page'],
                           per_page=send['per_page'],
                           pagination=send['pagination'], locale=locale)


@app.route('/message/po/update', methods=['POST'])
def po_update():
    po = Pofile(request.form.get('locale'))
    msgid=request.form.getlist('msgid')
    msgstr=request.form.getlist('msgstr')
    print(msgid, msgstr)
    po.poUpdate(msgid, msgstr)
    return redirect(url_for('message', locale=request.form.get('locale')))

@app.route('/babel/run', methods=['POST'])
def babel_po_run():
    po = Pofile()
    po.poScan()
    return redirect(url_for('message', locale=request.form.get('locale')))


@app.route('/po/file/create', methods=['POST'])
def po_file_create():
    language=request.form.get('language')
    po = Pofile()
    po.poCreate(language)
    return redirect(url_for('messages'))


@app.route('/test')
def test():
    return render_template('test.html')

if __name__ == '__main__':
    app.run()
