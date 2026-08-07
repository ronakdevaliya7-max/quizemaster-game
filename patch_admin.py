import os

base_dir = r"d:\project\qgame\qgame"
admin_dir = os.path.join(base_dir, "templates", "admin")
app_path = os.path.join(base_dir, "app.py")

# 1. Update Admin Dashboard to show new links
dashboard_path = os.path.join(admin_dir, "dashboard.html")
if os.path.exists(dashboard_path):
    with open(dashboard_path, "r", encoding="utf-8") as f:
        dash = f.read()
    
    new_sidebar = """
            <div class="list-group list-group-flush shadow-sm mb-4">
                <a href="{{ url_for('admin_dashboard') }}" class="list-group-item list-group-item-action bg-primary text-white border-0"><i class="fas fa-tachometer-alt me-2"></i> Dashboard</a>
                <a href="{{ url_for('admin_users') }}" class="list-group-item list-group-item-action border-0"><i class="fas fa-users me-2"></i> Manage Users</a>
                <a href="#" class="list-group-item list-group-item-action border-0"><i class="fas fa-university me-2"></i> Manage Boards</a>
                <a href="#" class="list-group-item list-group-item-action border-0"><i class="fas fa-layer-group me-2"></i> Manage Standards</a>
                <a href="#" class="list-group-item list-group-item-action border-0"><i class="fas fa-book me-2"></i> Manage Subjects</a>
                <a href="{{ url_for('admin_categories') }}" class="list-group-item list-group-item-action border-0"><i class="fas fa-tags me-2"></i> Manage Topics (Categories)</a>
                <a href="{{ url_for('admin_questions') }}" class="list-group-item list-group-item-action border-0"><i class="fas fa-question-circle me-2"></i> Manage Questions</a>
                <a href="#" class="list-group-item list-group-item-action border-0 text-success"><i class="fas fa-robot me-2"></i> AI Question Generator</a>
                <a href="{{ url_for('admin_quizzes') }}" class="list-group-item list-group-item-action border-0"><i class="fas fa-chart-line me-2"></i> Quiz Results & Analytics</a>
            </div>
    """
    
    if 'class="list-group list-group-flush' in dash:
        import re
        dash = re.sub(r'<div class="list-group list-group-flush.*?</div>', new_sidebar, dash, flags=re.DOTALL)
        with open(dashboard_path, "w", encoding="utf-8") as f:
            f.write(dash)

print("Admin dashboard patched with all new links!")
