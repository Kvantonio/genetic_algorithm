from flask import Flask, render_template, request
from genetic import Genetic
import time

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
        start = time.time()
        genetic.generate_population()
        for i in range(genetic.iterations):
            genetic.epoch()

        genetic.population.sort(key=genetic.fitness)

        end = time.time()
        print(end-start)
        min_fit = genetic.population[-1]
        max_fit = genetic.max_fitness[-1]
        graph = None
        if len(genetic.fitness_f.free_symbols) == 1:
            scatter = genetic.get_coord_one()
            scatter = str(scatter).replace("\'", '')
            graph = genetic.get_graph()
        else:
            scatter = genetic.get_coord_two()
            scatter = str(scatter).replace("\'", '')
            max_fit = genetic.decode(genetic.population[0].chromosome, 2)


        return render_template('index.html',
                                params=params,
                                avg=genetic.avg_fitness,
                                max=genetic.max_fitness,
                                graph_lables=list(range(genetic.iterations)),
                                min_fit=min_fit,
                                max_fit=max_fit,
                                scatter=scatter,
                                graph=graph
                                )

    return render_template('index.html')
