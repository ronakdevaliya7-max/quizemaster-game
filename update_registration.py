import os

base_dir = r"d:\project\qgame\qgame"
app_path = os.path.join(base_dir, "app.py")
register_path = os.path.join(base_dir, "templates", "register.html")

# --- 1. Update app.py register route ---
with open(app_path, "r", encoding="utf-8") as f:
    app_code = f.read()

old_register_route = """@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))
            
        hashed_password = generate_password_hash(password, method='scrypt')
        new_user = User(username=username, password_hash=hashed_password, name=name, role='user')
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! You can now log in.')
        return redirect(url_for('login'))
        
    return render_template('register.html')"""

new_register_route = """@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        
        # New dynamic fields
        education_level = request.form.get('education_level')
        board = request.form.get('board')
        standard = request.form.get('standard')
        stream = request.form.get('stream')
        course = request.form.get('course')
        semester = request.form.get('semester')
        exam = request.form.get('exam')
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))
            
        hashed_password = generate_password_hash(password, method='scrypt')
        new_user = User(username=username, password_hash=hashed_password, name=name, role='user')
        
        # Store dynamic profile (we'll store strings in department/college temporarily for the old UI compatibility, or use new fields if available)
        new_user.education_level = education_level
        
        # Depending on the models you have, we can use the extra fields we added
        # new_user.board_id = None # Requires lookup
        # For simplicity, we just save the text info into the profile for now so the dashboard can filter
        new_user.department = board if board else (course if course else exam)
        new_user.semester = standard if standard else semester
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! You can now log in.')
        return redirect(url_for('login'))
        
    return render_template('register.html')"""

if old_register_route in app_code:
    app_code = app_code.replace(old_register_route, new_register_route)
    with open(app_path, "w", encoding="utf-8") as f:
        f.write(app_code)
    print("Updated app.py register route.")
else:
    print("Could not find the exact old register route in app.py")


# --- 2. Update register.html ---
new_register_html = """{% extends 'base.html' %}

{% block title %}Register - Smart Education Quiz{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6 col-lg-5">
        <div class="card shadow-sm border-0 mt-5">
            <div class="card-body p-4">
                <h3 class="text-center mb-4"><i class="fas fa-user-plus text-primary"></i> Create Account</h3>
                <form method="POST" action="{{ url_for('register') }}">
                    <div class="mb-3">
                        <label class="form-label">Full Name</label>
                        <input type="text" class="form-control" name="name" required placeholder="John Doe">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Username</label>
                        <input type="text" class="form-control" name="username" required placeholder="johndoe123">
                    </div>
                    
                    <!-- Dynamic Education Profile Section -->
                    <div class="mb-3">
                        <label class="form-label">Education Level</label>
                        <select class="form-select" name="education_level" id="educationLevel" onchange="updateForm()">
                            <option value="">Select Level...</option>
                            <option value="School">School</option>
                            <option value="Diploma">Diploma</option>
                            <option value="Graduation">Graduation</option>
                            <option value="Post Graduation">Post Graduation</option>
                            <option value="Competitive Exam">Competitive Exam</option>
                        </select>
                    </div>

                    <!-- School Fields -->
                    <div id="schoolFields" style="display: none;">
                        <div class="mb-3">
                            <label class="form-label">Board</label>
                            <select class="form-select" name="board">
                                <option value="GSEB">GSEB</option>
                                <option value="CBSE">CBSE</option>
                                <option value="ICSE">ICSE</option>
                                <option value="IB">IB</option>
                                <option value="NIOS">NIOS</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Standard</label>
                            <select class="form-select" name="standard" id="standardSelect" onchange="updateStream()">
                                <option value="1">1</option><option value="2">2</option><option value="3">3</option>
                                <option value="4">4</option><option value="5">5</option><option value="6">6</option>
                                <option value="7">7</option><option value="8">8</option><option value="9">9</option>
                                <option value="10" selected>10</option><option value="11">11</option><option value="12">12</option>
                            </select>
                        </div>
                        <div class="mb-3" id="streamField" style="display: none;">
                            <label class="form-label">Stream</label>
                            <select class="form-select" name="stream">
                                <option value="Science">Science</option>
                                <option value="Commerce">Commerce</option>
                                <option value="Arts">Arts</option>
                            </select>
                        </div>
                    </div>

                    <!-- Graduation Fields -->
                    <div id="graduationFields" style="display: none;">
                        <div class="mb-3">
                            <label class="form-label">Course</label>
                            <select class="form-select" name="course">
                                <option value="BCA">BCA</option>
                                <option value="BBA">BBA</option>
                                <option value="B.Com">B.Com</option>
                                <option value="BA">BA</option>
                                <option value="B.Sc">B.Sc</option>
                                <option value="B.Tech">B.Tech</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Semester</label>
                            <select class="form-select" name="semester">
                                <option value="1">1</option><option value="2">2</option><option value="3">3</option>
                                <option value="4">4</option><option value="5">5</option><option value="6">6</option>
                                <option value="7">7</option><option value="8">8</option>
                            </select>
                        </div>
                    </div>

                    <!-- Competitive Exam Fields -->
                    <div id="examFields" style="display: none;">
                        <div class="mb-3">
                            <label class="form-label">Exam</label>
                            <select class="form-select" name="exam">
                                <option value="UPSC">UPSC</option>
                                <option value="GPSC">GPSC</option>
                                <option value="SSC">SSC</option>
                                <option value="Banking">Banking</option>
                                <option value="NEET">NEET</option>
                                <option value="JEE">JEE</option>
                            </select>
                        </div>
                    </div>

                    <div class="mb-4">
                        <label class="form-label">Password</label>
                        <input type="password" class="form-control" name="password" required>
                    </div>
                    <button type="submit" class="btn btn-primary w-100 mb-3 fw-bold">Sign Up</button>
                    <p class="text-center text-muted mb-0">Already have an account? <a href="{{ url_for('login') }}">Log in here</a>.</p>
                </form>
            </div>
        </div>
    </div>
</div>

<script>
function updateForm() {
    var level = document.getElementById('educationLevel').value;
    document.getElementById('schoolFields').style.display = (level === 'School') ? 'block' : 'none';
    document.getElementById('graduationFields').style.display = (level === 'Graduation' || level === 'Diploma' || level === 'Post Graduation') ? 'block' : 'none';
    document.getElementById('examFields').style.display = (level === 'Competitive Exam') ? 'block' : 'none';
    updateStream();
}

function updateStream() {
    var standard = parseInt(document.getElementById('standardSelect').value);
    document.getElementById('streamField').style.display = (standard >= 11) ? 'block' : 'none';
}
</script>
{% endblock %}
"""

with open(register_path, "w", encoding="utf-8") as f:
    f.write(new_register_html)

print("Updated register.html with dynamic UI.")
