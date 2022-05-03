from flask import Flask, render_template, request
from genetic import Genetic


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        params = {
        'population':int(request.form.get('population')),
        'chromosome': int(request.form.get('chromosome')),
        'iterations': int(request.form.get('iterations')),
        'mutation': float(request.form.get('mutation')),
        'crossing_over': float(request.form.get('crossing_over')),
        'selection':float(request.form.get('selection')),
        'fitness': request.form.get('fitness'),
        'trend': request.form.get('trend')
        }
        genetic = Genetic(params)
        # genetic.parse(data)
        # genetic.fitnes([1,0,1,0])
        
        genetic.generate_population()
        for i in range(genetic.iterations):
            genetic.epoch()

        genetic.population.sort(key=genetic.fitness)

        min_fit = genetic.population[-1]
        max_fit = genetic.population[0]

        return render_template('index.html',
                                params=params,
                                avg=genetic.avg_fitness,
                                max=genetic.max_fitness,
                                graph_lables=list(range(genetic.iterations)),
                                min_fit=min_fit,
                                max_fit=max_fit
                                )

    return render_template('index.html')
