from flask import Flask, render_template, request, flash, redirect
from models import setup_db, db, Resident, BoardMember, BoardInfo, ExpensesItem, HoaUpdates
app = Flask(__name__)
setup_db(app)

@app.route('/')
def index():
    return render_template('dashboards/front_page.html')

@app.route('/signup')
def sign_up():
    return render_template('dashboards/login.html')

@app.route('/dashboards/board/<int:board_id>')
def show_hoa_dashboard(board_id):
    board = BoardInfo.query.get(board_id)
    board_members = BoardMember.query.filter(board.id == BoardMember.board_group_id).with_entities(BoardMember.name, BoardMember.email).all()
    expenses = ExpensesItem.query.filter(board.id == ExpensesItem.expense_list_id).with_entities(ExpensesItem.expense_item, ExpensesItem.expense_amount).all()
    return render_template('dashboards/board.html', expenses=expenses, board_members=board_members, board_name=board.name)


@app.route('/dashboards/residents/<int:resident_id>')
def show_resident_dashboard(resident_id):
    resident = Resident.query.get(resident_id)
    resident_hoa = resident.hoa_group
    # hoa_update = HoaUpdates.query.filter(resident_hoa == HoaUpdates.query.with_entities(HoaUpdates.hoa_group).all()).all()
    # contacts = BoardMember.query.filter(resident.id == BoardMember.board_group_id).with_entities(BoardMember.name, BoardMember.email).all()
    hoa_update = HoaUpdates.query.all()
    board_members = BoardMember.query.filter(resident.hoa_group == BoardMember.board_group_id)
    return render_template('dashboards/residents.html', hoa_updates=hoa_update, board_members=board_members)

@app.route('/sendmail')
def show_sendmail():
    return render_template('dashboards/sendmailer.html')

if __name__ == '__main__':
    app.run(debug=True)
