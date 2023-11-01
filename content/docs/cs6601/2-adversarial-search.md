# Adversarial Search

- Adversarial search aims to solve the game problems that have two or more agents with conflicting goals, such as Go, chess, and poker.
## Observable games (e.g. isolation)

**Observable game** means the game is visible to all players, such as chess, Go. It's also called **perfect information**. In comparison, **imperfect information** means the game is not visible to all players such as poker where not all cards are visible to all players.

**Isolation** is a game that two or more players take turns to fill out the square in a N by N board. Each player can only move multiple steps horizontally, vertically and diagonally as long as there isn't a block on the way. Once the player leave the previous square, the square becomes inactive and can't be occupied again by any players. To win the game, the player need to avoid no steps to move and block the opponent to have more moves. 

Let's design an AI player that plays to win.
### Minimax

**Minmax** is an algorithm that enumerates the moves as many as possible and pick the  "winning"(most likely) node for next step. We assign a score(**utility value**) to every potential moves and pick the one with "max" score.

Take the figure below as an example. On the first layer, the AI player goes first, it pick the "Max" node, and the second layer, the opponent pick the "Min" node, and so on.

![](https://i.imgur.com/Pc1CVgT.png)

There are several ways to calculate the score(utility value). A simple one is, the number of "my moves". In each turn, the AI player picks the node that has the maximum of active moves.

### Alpha-beta pruning

The number of the nodes in the tree increases exponentially. No algorithm can avoid that. But sometimes, it can be cut to half or eliminate some of the nodes by **pruning**, particularly **alpha-beta pruning**.

The principle is, if the player has a better choice than node **n** either at the same level or at any point higher up in the tree, then it will never move to **n**.

![](https://i.imgur.com/fOHJZA4.png)

The psudo-code:

![](https://i.imgur.com/WtXnCVJ.png)

#### Performance improvement

If this could be done perfectly, alpha–beta would need to examine only $O(b^{m/2})$ nodes to pick the best move, instead of $O(b^m)$ for minimax.

### Utility and evaluation functions

#### Sensitivity

### Optimization tricks

- Move-ordering
- Symmetry

### Iterative deepening
### Multiplayer games

### Probabilistic games
### Partially observable games (e.g. poker)

