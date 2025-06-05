from flask import Flask, render_template_string, request
import subprocess

app = Flask(__name__)
process = None

html_form = """
<!DOCTYPE html>
<html>
<head>
    <title>Lancer la simulation V2X</title>
</head>
<body>
    <h2>Simulation V2X - Configuration</h2>
    <form action="/" method="post">
        <label>Voitures connectées : <span id="nb_connected_val">10</span></label><br>
        <input type="range" name="nb_connected" min="1" max="100" value="10"
               oninput="nb_connected_val.innerText = this.value"><br><br>

        <label>Voitures attaquantes : <span id="nb_attackers_val">5</span></label><br>
        <input type="range" name="nb_attackers" min="0" max="100" value="5"
               oninput="nb_attackers_val.innerText = this.value"><br><br>

        <label>Voitures non connectées : <span id="nb_unconnected_val">5</span></label><br>
        <input type="range" name="nb_unconnected" min="0" max="100" value="5"
               oninput="nb_unconnected_val.innerText = this.value"><br><br>

        <label>Nombre de pas : <span id="steps_val">100</span></label><br>
        <input type="range" name="steps" min="10" max="10000" value="100"
               oninput="steps_val.innerText = this.value"><br><br>

        <label>Portée communication (en m) : <span id="comm_range_val">150</span></label><br>
        <input type="range" name="comm_range" min="10" max="500" value="150"
               oninput="comm_range_val.innerText = this.value"><br><br>

        <label>Mécanismes de défense :</label><br>
        <input type="checkbox" name="sanity" checked/> Sanity<br>
        <input type="checkbox" name="reputation" checked/> Réputation<br>
        <input type="checkbox" name="pheromone" checked/> Phéromone<br><br>

        <input type="submit" name="action" value="Start">
        <input type="submit" name="action" value="Stop">
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    global process
    if request.method == "POST":
        action = request.form.get("action")
        if action == "Start":
            if not process:
                args = [r"C:\\Users\\gerbe\\OneDrive\\Bureau\\evan2025\\.venv\\Scripts\\python.exe", "run.py"]
                args += ["--nb_connected", request.form["nb_connected"]]
                args += ["--nb_attackers", request.form["nb_attackers"]]
                args += ["--nb_unconnected", request.form["nb_unconnected"]]
                args += ["--steps", request.form["steps"]]

                if "sanity" in request.form:
                    args.append("--sanity")
                if "reputation" in request.form:
                    args.append("--reputation")
                if "pheromone" in request.form:
                    args.append("--pheromone")

                process = subprocess.Popen(args)
        elif action == "Stop":
            if process:
                process.terminate()
                process = None

    return render_template_string(html_form)

if __name__ == "__main__":
    app.run(port=8080, debug=True)
