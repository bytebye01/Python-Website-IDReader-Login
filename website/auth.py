from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from .models import IDCard

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            # if check_password_hash(user.password, password): #เปรียบเทียบแบบเข้ารหัส
            if user.password == password:
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('auth.id_list'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist or Sign up contact Admin.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated and current_user.role == 'admin':
        if request.method == 'POST':
            username = request.form.get('username')
            name = request.form.get('Name')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')
            role = request.form.get('role')
            
            user = User.query.filter_by(username=username).first()
            if user:
                flash('Username already exists.', category='error')
            elif len(username) < 4:
                flash('Username must be greater than 3 characters.', category='error')
            elif len(name) < 2:
                flash('Name must be greater than 1 character.', category='error')
            elif password1 != password2:
                flash('Passwords don\'t match.', category='error')
            elif len(password1) < 7:
                flash('Password must be at least 7 characters.', category='error')
            elif role not in ['admin', 'user']:  # เพิ่มเงื่อนไขในการตรวจสอบ role
                flash('Role must be: admin, user', category='error')
            else:
                # new_user = User(username=username, name=name, password=generate_password_hash(password1, method='pbkdf2:sha256'), role=role) #เก็บรหัสแบบปลอดภัยแต่ดูไม่ได้
                new_user = User(username=username, name=name, password=password1, role=role)
                db.session.add(new_user)
                db.session.commit()
                login_user(current_user, remember=True)
                flash('Account created!', category='success')
                return redirect(url_for('views.home'))
    else:
        flash('You are not authorized to access this page.', category='error')
        return redirect(url_for('auth.login'))
    
    return render_template("sign_up.html", user=current_user)


@auth.route('/user-list')
def user_list():
    if current_user.is_authenticated and current_user.role == 'admin':
        users = User.query.all()
        return render_template('user_list.html', users=users, user=current_user)  # เพิ่มตัวแปร user=current_user
    else:
        # ถ้าไม่ใช่ admin ให้ทำการ redirect หรือแสดงข้อความผิดพลาด
        return "You do not have access to view this page."



@auth.route('/user-edit/<int:user_id>', methods=['GET', 'POST'])
def user_edit(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.is_authenticated and current_user.role == 'admin':
        if request.method == 'POST':
            name = request.form.get('name')
            password = request.form.get('password')

            if len(name) < 2:
                flash('Name must be greater than 1 character.', category='error')
            elif len(password) > 0 and len(password) < 7:
                flash('Password must be at least 7 characters.', category='error')
            else:
                user.name = name
                if len(password) > 0:
                    user.password = password

                db.session.commit()
                flash('User updated successfully!', category='success')
                return redirect(url_for('auth.user_list'))
        
        return render_template('user_edit.html', user=user)
    else:
        flash('You are not authorized to access this page.', category='error')
        return redirect(url_for('auth.login'))


@auth.route('/user-delete/<int:user_id>')
def user_delete(user_id):
    if current_user.is_authenticated and current_user.role == 'admin':
        user = User.query.get(user_id)
        if not user:
            return "User not found"

        if user.id == 1:
            return "Cannot delete user with ID 1"

        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('auth.user_list'))
    else:
        return "You do not have access to view this page."
    

@auth.route('/')
def id_list():
        id_cards = IDCard.query.all()
        return render_template('id_list.html', id_cards=id_cards, user=current_user)

def delete_id_card(id_number):
    try:
        # Find the ID card by id_number
        id_card = IDCard.query.get(id_number)
        
        if id_card:
            # Delete the ID card
            db.session.delete(id_card)
            db.session.commit()
            return True, "ID Card deleted successfully"
        else:
            return False, "ID Card not found"
    except Exception as e:
        return False, str(e)

# Route to handle ID card deletion
@auth.route('/delete_id_card', methods=['POST'])
def delete_id_card_route():
    id_number = request.form.get('id_number')
    success, message = delete_id_card(id_number)
    return {'success': success, 'message': message}