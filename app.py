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
        crossing_over = float(request.form.get('crossing_over'))
        selection = float(request.form.get('selection'))
        fitness = request.form.get('fitness')
        genetic = Genetic(population,
                            chromosome,
                            iterations,
                            mutation,
                            crossing_over,
                            selection,
                            fitness
                        )
        # genetic.parse(data)
        # genetic.fitnes([1,0,1,0])
        
        genetic.generate_population()
        for i in range(genetic.iterations):
            genetic.epoch()

        

        return render_template('index.html',
                                data=True,
                                avg=genetic.avg_fitness,
                                max=genetic.max_fitness,
                                graph_lables=list(range(genetic.iterations))
                                )

    return render_template('index.html')
