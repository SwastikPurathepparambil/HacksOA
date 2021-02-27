from flask import Flask, render_template, request
from models import setup_db, db, Resident, BoardMember, BoardInfo, ExpensesItem, HoaUpdates
app = Flask(__name__)
setup_db(app)

@app.route('/')
def index():
    return render_template('front_page.html')

@app.route('/signup')
def sign_up():
    return render_template('signup/board_members/bm_signup.html')

@app.route('/dashboard/board_members/<int:board_id>')
def show_hoa_dashboard(board_id):
    board = BoardInfo.query.get(board_id)
    board_members = BoardMember.query.filter(board.id == BoardMember.board_group_id).with_entities(BoardMember.name, BoardMember.email).all()
    expenses = ExpensesItem.query.filter(board.id == ExpensesItem.expense_id).with_entities(ExpensesItem.expense_item, ExpensesItem.expense_amount).all()

    return render_template('board_members/dashboard.html', expenses=expenses, board_members=board_members, board_name=board.name)


@app.route('dashboard/residents/<int:resident_id')
def show_resident_dashboard(resident_id):
    resident = Resident.query.get(resident_id)
    resident_hoa = resident.hoa_group
    hoa_update = HoaUpdates.query.filter(resident_hoa == HoaUpdates.query.with_entities(HoaUpdates.hoa_group).all()).all()
    contacts = BoardMember.query.filter(
        resident_hoa == BoardInfo.query.with_entities(BoardInfo.name).all()
        ).with_entities(BoardMember.name, BoardMember.email).all()
    return render_template('residents/dashboard.html', hoa_updates = hoa_update, contacts=contacts)
if __name__ == '__main__':
    app.run(debug=True)
