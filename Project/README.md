# Artificial Intelligence Project - Implement four different game tree search agents for the game of Pacman

The project handout is 'PacmanProject.pdf' above.

There are four parts to this project:
* The implementation of a Minimax agent – The Minimax algorithm works with any number of ghosts. The search tree consists of multiple layers - a max layer for Pacman, and a min layer for each ghost.
* The implementation of a Minimax agent with Alpha-Beta Pruning - The Alpha-Beta Pruning algorithm works with any number of ghosts, and is similar to the original Minimax algorithm.
* The implementation of an Expectimax agent - The Expectimax algorithm works with any number of ghosts, similarly to the MinimaxAgent and AlphaBetaAgent classes.
* The implementation of a Monte-Carlo Tree Search (MCTS) agent with UCB.

To run the grading scripts, cd into the project folder. 
* Type 'python autograder.py' to grade the project.

You can also see the Pacman agents play real-time. To do this, simply type 'python pacman.py' followed by the appropriate arguments listed below:

* -p Allows you to select a game agent for controlling pacman, e.g., -p GreedyAgent. These are the available agents:
    * GreedyAgent
    * MinimaxAgent
    * AlphaBetaAgent
    * ExpectimaxAgent
    * MonteCarloAgent

* -l Allows you to select a map for playing Pacman, e.g., -l smallClassic. There are 9 playable maps, listed.
    * minimaxClassic
    * trappedClassic
    * testClassic
    * smallClassic
    * capsuleClassic
    * openClassic
    * contestClassic
    * mediumClassic
    * originalClassic

* -a Allows you to specify agent specific arguments. For instance, for any agent that is a subclass of MultiAgentSearchAgent, you can specify the depth that you limit your search tree by typing -a depth=3

* -n Allows you to specify the amount of games that are played consecutively by Pacman, e.g., -n 100 will cause Pacman to play 100 consecutive games.

* -x Allows you to specify an amount of training cases. The results of these cases are not displayed in theterminal.Forexample,-x 50willallowyoutorunPacmanover50trainingcasesbeforestarting to play games where the output is visible. This will be useful when testing you Monte-Carlo Agent.

* -k Allows you to specify how many ghosts will appear on the map. For instance, to have 3 ghosts chase Pacman on the contestClassic map, you can type -l contestClassic -k 3 (Note: There is a max number of ghosts that can be initialized on each map, if the number specified exceeds this number, you will only see the max amount of ghosts.)

* -g Allows you to specify whether the ghost will be a RandomGhost (which is the default) or a DirectionalGhost that chases Pacman on the map. For instance, to have DirectionalGhost charac- ters type -g DirectionalGhost

* -q Allows you to run Pacman with no graphics.

* --frameTime Specifies the frame time for each frame in the Pacman visualizer (e.g., --frameTime 0).

An example of a command you might want to run is:

* python pacman.py -p GreedyAgent -l contestClassic -n 100 -k 2 -g DirectionalGhost -q

This will run a GreedyAgent over 100 cases on the contestClassic level with 2 DirectionalGhost characters, while supressing the visual output.
