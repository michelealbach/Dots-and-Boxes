# Dots-and-Boxes
A player for the game Dots and Boxes
basicplay - a basic player for a 3x3 board that avoids unsafe moves and captures boxes
doublecrossing - basicplay with chain lengths, looks for shorter chains and doublecrosses
largerboard - allows for boards larger than 3x3 by changing naming convention
chainsandloops - the main strategy player, attempts to better account for loops and actually count remaining chains, added other strategies, and loop avoidance (since it is not great at accounting for loops)
search - uses minimax searching with alphabeta pruning, is too slow for anything larger than 2x2