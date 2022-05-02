from flask import Flask, render_template, request
from genetic import Genetic


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        population  = int(request.form.get('population'))
        chromosome  = int(request.form.get('chromosome'))
        iterations = int(request.form.get('iterations'))
        mutation = float(request.form.get('mutation'))
        crossing_over = request.form.get('crossing_over')
        selection = request.form.get('selection')
        fitnes = request.form.get('fitnes')
        genetic = Genetic(population,
                            chromosome,
                            iterations,
                            mutation,
                            crossing_over,
                            selection,
                            fitnes
                        )
        # genetic.parse(data)
        # genetic.fitnes([1,0,1,0])
        genetic.generate_population()
        genetic.mutation()

        return render_template('index.html')

    return render_template('index.html')
