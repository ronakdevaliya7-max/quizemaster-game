import os

base_dir = r"d:\project\qgame\qgame"
register_path = os.path.join(base_dir, "templates", "register.html")

full_register_html = """{% extends 'base.html' %}

{% block title %}Register - Smart Education Quiz{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8 col-lg-6">
        <div class="card shadow-sm border-0 mt-4 mb-5">
            <div class="card-body p-4">
                <h3 class="text-center mb-4"><i class="fas fa-user-plus text-primary"></i> Create Account</h3>
                <form method="POST" action="{{ url_for('register') }}" enctype="multipart/form-data">
                    <div class="row">
                        <!-- Profile Photo -->
                        <div class="col-12 mb-3">
                            <label class="form-label">Profile Photo</label>
                            <input type="file" class="form-control" name="profile_photo" accept="image/*">
                        </div>
                        
                        <!-- Personal Info -->
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Full Name</label>
                            <input type="text" class="form-control" name="name" required placeholder="John Doe">
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Username</label>
                            <input type="text" class="form-control" name="username" required placeholder="johndoe123">
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Email</label>
                            <input type="email" class="form-control" name="email" required placeholder="john@example.com">
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Mobile Number</label>
                            <input type="tel" class="form-control" name="mobile" required placeholder="9876543210">
                        </div>
                        
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Gender</label>
                            <select class="form-select" name="gender" required>
                                <option value="">Select Gender</option>
                                <option value="Male">Male</option>
                                <option value="Female">Female</option>
                                <option value="Other">Other</option>
                            </select>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Date of Birth</label>
                            <input type="date" class="form-control" name="dob" required>
                        </div>
                        
                        <!-- Location Info -->
                        <div class="col-md-4 mb-3">
                            <label class="form-label">Country</label>
                            <input type="text" class="form-control" name="country" required placeholder="India">
                        </div>
                        <div class="col-md-4 mb-3">
                            <label class="form-label">State</label>
                            <input type="text" class="form-control" name="state" required placeholder="Gujarat">
                        </div>
                        <div class="col-md-4 mb-3">
                            <label class="form-label">City</label>
                            <input type="text" class="form-control" name="city" required placeholder="Surat">
                        </div>

                        <!-- Dynamic Education Profile Section -->
                        <div class="col-12 mb-3 mt-3 border-top pt-3">
                            <h5 class="text-secondary mb-3">Education Profile</h5>
                            <label class="form-label">Education Level</label>
                            <select class="form-select" name="education_level" id="educationLevel" onchange="updateForm()" required>
                                <option value="">Select Level...</option>
                                <option value="School">School</option>
                                <option value="Diploma">Diploma</option>
                                <option value="Graduation">Graduation</option>
                                <option value="Post Graduation">Post Graduation</option>
                                <option value="Competitive Exam">Competitive Exam</option>
                                <option value="Other">Other</option>
                            </select>
                        </div>

                        <!-- School Fields -->
                        <div id="schoolFields" class="col-12" style="display: none;">
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Board</label>
                                    <select class="form-select" name="board">
                                        <option value="GSEB">GSEB</option>
                                        <option value="CBSE">CBSE</option>
                                        <option value="ICSE">ICSE</option>
                                        <option value="IB">IB</option>
                                        <option value="NIOS">NIOS</option>
                                        <option value="Other">Other</option>
                                    </select>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Standard</label>
                                    <select class="form-select" name="standard" id="standardSelect" onchange="updateStream()">
                                        <option value="1">1</option><option value="2">2</option><option value="3">3</option>
                                        <option value="4">4</option><option value="5">5</option><option value="6">6</option>
                                        <option value="7">7</option><option value="8">8</option><option value="9">9</option>
                                        <option value="10" selected>10</option><option value="11">11</option><option value="12">12</option>
                                    </select>
                                </div>
                                <div class="col-md-12 mb-3" id="streamField" style="display: none;">
                                    <label class="form-label">Stream</label>
                                    <select class="form-select" name="stream">
                                        <option value="Science">Science</option>
                                        <option value="Commerce">Commerce</option>
                                        <option value="Arts">Arts</option>
                                    </select>
                                </div>
                            </div>
                        </div>

                        <!-- Diploma Fields -->
                        <div id="diplomaFields" class="col-12" style="display: none;">
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Branch</label>
                                    <select class="form-select" name="diploma_branch">
                                        <option value="Computer Engineering">Computer Engineering</option>
                                        <option value="Mechanical">Mechanical</option>
                                        <option value="Civil">Civil</option>
                                        <option value="Electrical">Electrical</option>
                                        <option value="Automobile">Automobile</option>
                                        <option value="IT">IT</option>
                                        <option value="Electronics">Electronics</option>
                                    </select>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Semester</label>
                                    <select class="form-select" name="diploma_semester">
                                        <option value="1">1</option><option value="2">2</option><option value="3">3</option>
                                        <option value="4">4</option><option value="5">5</option><option value="6">6</option>
                                    </select>
                                </div>
                            </div>
                        </div>

                        <!-- Graduation Fields -->
                        <div id="graduationFields" class="col-12" style="display: none;">
                            <div class="row">
                                <div class="col-md-12 mb-3">
                                    <label class="form-label">University</label>
                                    <input type="text" class="form-control" name="university" placeholder="Example University">
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Course</label>
                                    <select class="form-select" name="grad_course">
                                        <option value="BCA">BCA</option>
                                        <option value="BBA">BBA</option>
                                        <option value="B.Com">B.Com</option>
                                        <option value="BA">BA</option>
                                        <option value="B.Sc">B.Sc</option>
                                        <option value="B.Tech">B.Tech</option>
                                        <option value="BE">BE</option>
                                        <option value="B.Ed">B.Ed</option>
                                        <option value="LLB">LLB</option>
                                    </select>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Semester</label>
                                    <select class="form-select" name="grad_semester">
                                        <option value="1">1</option><option value="2">2</option><option value="3">3</option>
                                        <option value="4">4</option><option value="5">5</option><option value="6">6</option>
                                        <option value="7">7</option><option value="8">8</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Post Graduation Fields -->
                        <div id="postGradFields" class="col-12" style="display: none;">
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Course</label>
                                    <select class="form-select" name="pg_course">
                                        <option value="MCA">MCA</option>
                                        <option value="MBA">MBA</option>
                                        <option value="M.Com">M.Com</option>
                                        <option value="M.Sc">M.Sc</option>
                                        <option value="MA">MA</option>
                                        <option value="ME">ME</option>
                                        <option value="M.Tech">M.Tech</option>
                                    </select>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Semester</label>
                                    <select class="form-select" name="pg_semester">
                                        <option value="1">1</option><option value="2">2</option>
                                        <option value="3">3</option><option value="4">4</option>
                                    </select>
                                </div>
                            </div>
                        </div>

                        <!-- Competitive Exam Fields -->
                        <div id="examFields" class="col-12" style="display: none;">
                            <div class="mb-3">
                                <label class="form-label">Exam</label>
                                <select class="form-select" name="exam">
                                    <option value="UPSC">UPSC</option>
                                    <option value="GPSC">GPSC</option>
                                    <option value="SSC">SSC</option>
                                    <option value="RRB">RRB</option>
                                    <option value="Banking">Banking</option>
                                    <option value="Police">Police</option>
                                    <option value="Forest">Forest</option>
                                    <option value="Army">Army</option>
                                    <option value="Air Force">Air Force</option>
                                    <option value="Navy">Navy</option>
                                    <option value="NEET">NEET</option>
                                    <option value="JEE">JEE</option>
                                    <option value="GUJCET">GUJCET</option>
                                    <option value="CAT">CAT</option>
                                    <option value="CLAT">CLAT</option>
                                    <option value="GATE">GATE</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>
                        </div>

                        <!-- Security -->
                        <div class="col-md-6 mb-4 mt-3 border-top pt-3">
                            <label class="form-label">Password</label>
                            <input type="password" class="form-control" name="password" required>
                        </div>
                        <div class="col-md-6 mb-4 mt-3 border-top pt-3">
                            <label class="form-label">Confirm Password</label>
                            <input type="password" class="form-control" name="confirm_password" required>
                        </div>
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
    document.getElementById('diplomaFields').style.display = (level === 'Diploma') ? 'block' : 'none';
    document.getElementById('graduationFields').style.display = (level === 'Graduation') ? 'block' : 'none';
    document.getElementById('postGradFields').style.display = (level === 'Post Graduation') ? 'block' : 'none';
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
    f.write(full_register_html)

models_path = os.path.join(base_dir, "models.py")
with open(models_path, "r", encoding="utf-8") as f:
    m = f.read()

new_fields = """
    email = db.Column(db.String(150), unique=True, nullable=True)
    mobile = db.Column(db.String(20), nullable=True)
    dob = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
"""
if "email = db.Column" not in m:
    m = m.replace("name = db.Column(db.String(150), nullable=False)", "name = db.Column(db.String(150), nullable=False)" + new_fields)
    with open(models_path, "w", encoding="utf-8") as f:
        f.write(m)
