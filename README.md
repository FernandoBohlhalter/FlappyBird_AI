# FlappyBird_AI
Flappy bird clone with in-built AI that plays the game.
<br></br>
<img src="https://github.com/FernandoBohlhalter/FlappyBird_AI/assets/82450429/06b642e3-a890-47a4-86a0-eb19f47582b9" width="400"></img>

# The Project
<h3>The final goal of the project was to create and train a <b>Neural network</b> that was able to play the famous mobile game <b>Flappy Bird</b>.</h3>

<ol>
<li>The first step was developing a Flappy Bird clone. For this, the best approach found was to use python and it's library called <a href="https://www.pygame.org/news">pygame.</a></li>
<li>The second step was creating and training an AI that was able to play the game. On this step was used the <a href="https://neat-python.readthedocs.io/en/latest/">Neat-Python</a> library.</li>
</ol>

# The AI
<h3>For the NEAT AI to learn it requires outputs, rewards and punishment, read more on the NEAT-Python Documentation.</h3>
  <ul>
    <li>Outputs: The outputs choosen to teach the AI were the Bird Y axis position, and the bird distance to the top pipe and the bottom pipe.</li>
    <li>Rewards: The AI gained fitness(the "AI score") as a reward whenever it did a good action for it's progress in the game. It was given 5 fitness for each pipe passed and 0.1 fitness for each frame it stayed alive.</li>
    <li>Punishment: The AI lost fitness as a punishment each time it made a bad action for it's progress in the game. It was taken away 1 fitness whenever the bird hit an pipe, the ground or the top of the screen</li>
  </ul>

# Requirements
<ol>
  <li><a href="https://www.python.org">Python</a></li>
  <li><a href="https://www.pygame.org/news">Pygame</a></li>
  <li><a href="https://neat-python.readthedocs.io/en/latest/">NEAT-Python</a></li>
</ol>

# How to use

<h3>If you want to run an old model:</h3>
<ol>
  <li>You must have a "winner.p" file(the trained model binary file) on the main folder.</li>
  <li>Set the "train" variable as False(line 344);</li>
  <li>Run the Python File.</li>
</ol>

<h3>If you want to train a new model:</h3>
<ol>
  <li>Set the "train" variable as True(line 344);</li>
  <li>Change the number of generations as you wish(line 316);</li>
  <li>On training, whenever a bird reaches the score of x(line 299), the game passes to the next generation. (explanation on code commments);</li>
  <li>To get different model results you can change the "config-feedForward.txt" as you wish;</li>
  <li>Run the python file;</li>
  <li>After excution the application must have updated the "winner.p" file, which is the trained model binary file.</li>
</ol>




  
