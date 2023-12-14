from app import app, USERS, EXPRS, QUEST

@app.route('/')
def index():
    response = ( f'<h1> Hello world <h1>'
                 f" USERS { '<br>'.join([user.repr() for user in USERS])}<br>"
                 f" EXPRESSIONS { '<br>'.join([expr.repr() for expr in EXPRS])}<br>"
                 f" QUESTIONS{ '<br>'.join([quest.repr() for quest in QUEST])}<br>"
                 )
    return response
