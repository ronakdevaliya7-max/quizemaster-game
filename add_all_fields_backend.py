import os

base_dir = r"d:\project\qgame\qgame"
app_path = os.path.join(base_dir, "app.py")

with open(app_path, "r", encoding="utf-8") as f:
    app_code = f.read()

import ast

def replace_register_function(code):
    lines = code.split('\n')
    start_idx = -1
    end_idx = -1
    
    for i, line in enumerate(lines):
        if line.startswith("@app.route('/register'"):
            start_idx = i
            break
            
    if start_idx != -1:
        # find end of function
        for i in range(start_idx + 2, len(lines)):
            if lines[i].startswith("@app.route"):
                end_idx = i
                break
                
        if end_idx != -1:
            new_reg = '''@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        name = request.form.get('name')
        
        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('register'))
        
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        gender = request.form.get('gender')
        dob = request.form.get('dob')
        country = request.form.get('country')
        state = request.form.get('state')
        city = request.form.get('city')
        
        education_level = request.form.get('education_level')
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))
            
        hashed_password = generate_password_hash(password, method='scrypt')
        new_user = User(username=username, password_hash=hashed_password, name=name, role='user')
        
        # New profile fields
        try:
            new_user.email = email
            new_user.mobile = mobile
            new_user.gender = gender
            new_user.dob = dob
            new_user.country = country
            new_user.state = state
            new_user.city = city
            new_user.education_level = education_level
        except Exception as e:
            pass # Ignore if DB hasn't been migrated
            
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! You can now log in.')
        return redirect(url_for('login'))
        
    return render_template('register.html')
'''
            new_lines = lines[:start_idx] + new_reg.split('\n') + lines[end_idx:]
            return '\n'.join(new_lines)
    return code

updated_app = replace_register_function(app_code)
with open(app_path, "w", encoding="utf-8") as f:
    f.write(updated_app)

print("Registration logic updated!")
