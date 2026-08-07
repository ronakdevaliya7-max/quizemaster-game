import os

register_path = r"d:\project\qgame\qgame\templates\register.html"
with open(register_path, "r", encoding="utf-8") as f:
    html = f.read()

# Fix the lack of spacing and formatting on the dropdowns by wrapping them in proper bootstrap classes
# Looking at their screenshot, the styling was weird because the inputs were packed tightly and maybe missing form-select if they were overriding it.
# Actually my injected HTML DID have class="form-select". But it looked broken because it didn't have margin bottom.
# Wait, my HTML had: class="col-md-6 mb-3" for the standard.
# Let's just make sure it's cleanly formatted. We will replace the entire file with a slightly better layout just in case.

html = html.replace('class="form-select"', 'class="form-select form-control custom-select p-2 w-100"')
html = html.replace('class="col-12"', 'class="col-12 mb-3"')

with open(register_path, "w", encoding="utf-8") as f:
    f.write(html)
