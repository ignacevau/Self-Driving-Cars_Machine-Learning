# CarAI
Cars learn to drive a custom created track.

<h3><b>Track Generator</b></h3>
<i>Create a custom track which the cars will learn to drive
(a premade track is already present so this is not abitrary)</i>
<p></p>
<ul>
<li>1. Draw the inner wall of the track
<li>2. Draw the outer wall of the track
<li>3. Set the checkpoints for the track : The amount of checkpoints a car collects decides how well it performs
<li>4. Set the start point : Where will the cars spawn every new generation

<li><b>5. Export the track</b>
<p>- Click the export button once the track is finished</p>
<p>- Go to the 'Car Simulation' folder and replace the 'Track.json' with the new exported JSON file</p>
<p>- You can import this track in the generator again by pressing the import button</p>
</ul>
<br>
<h3><b>Car Simulation</b></h3>
<i>Cars get trained using a genetic neural network to improve every generation</i>
<p></p>
<li>All variables to change the simulation can be found in the 'data.py' file
<li>The car 'sees' the walls through sensors and is rated on how many checkpoints it has collected
<li>Every car contains its own neural network which takes as inputs the lengths
of every sensor.
<li>The neural network outputs a single float between 0 and 1 with < 0.5 equals left and > 0.5 equals right
<li>Cars which keep rotating without collecting any checkpoints get automatically killed
<li>The way every new population is generated can be found in the 'optimizer.py' file and can be tweaked in the 'data.py' file