# searchAgents.py

from game import Directions
import random, util
from collections import deque

from game import Agent

##this is example agents 
class LeftTurnAgent(Agent):
  "An agent that turns left at every opportunity"
  
  def getAction(self, state):
    legal = state.getLegalPacmanActions()
    current = state.getPacmanState().configuration.direction
    if current == Directions.STOP: current = Directions.NORTH
    left = Directions.LEFT[current]
    if left in legal: return left
    if current in legal: return current
    if Directions.RIGHT[current] in legal: return Directions.RIGHT[current]
    if Directions.LEFT[left] in legal: return Directions.LEFT[left]
    return Directions.STOP

class GreedyAgent(Agent):
  def __init__(self, evalFn="scoreEvaluation"):
    self.evaluationFunction = util.lookup(evalFn, globals())
    assert self.evaluationFunction != None
        
  def getAction(self, state):
    # Generate candidate actions
    legal = state.getLegalPacmanActions()
    if Directions.STOP in legal: legal.remove(Directions.STOP)
      
    successors = [(state.generateSuccessor(0, action), action) for action in legal] 
    scored = [(self.evaluationFunction(state), action) for state, action in successors]
    bestScore = max(scored)[0]
    bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
    return random.choice(bestActions)

class BFSAgent(Agent):
  def getAction(self, gameState):
    visitedNodes = set()
    unexploredNodes = deque()
    unexploredNodes.append((gameState, []))
    visitedNodes.add(gameState)
    x, y = gameState.getPacmanPosition()
    x1, y1 = gameState.getFood().asList()[0]
    with open('result.txt', 'a') as result:
      result.write("Agent location = " + f"{x-9, y-1}" + " | Reward location = " +  f"{x1-9, y1-1}\n")
      while unexploredNodes:
        state, path = unexploredNodes.popleft()
        if state.isWin():
          if path:
            return path[0]
        legal = state.getLegalActions()
        for action in legal[::-1]:
          successor = state.generateSuccessor(0, action)
          if successor not in visitedNodes:
            visitedNodes.add(successor)
            unexploredNodes.append((successor, path + [action]))

class DFSAgent(Agent):
  def __init__(self):
    self.path = []
    self.visited = set()
    self.initial_call = True
  def getAction(self, gameState):
    if self.initial_call:
      start = gameState.getPacmanPosition()
      goal = gameState.getFood().asList()[0]
      self.dfs(gameState, start, goal)
      self.initial_call = False
    return self.path.pop(0) if self.path else "Stop"

  def dfs(self, gameState, current, goal):
    x, y = gameState.getPacmanPosition()
    x1, y1 = goal
    
    if current == goal:
      return True
    self.visited.add(current)
    
    legal = gameState.getLegalPacmanActions()
    for action in legal:
      successor = gameState.generateSuccessor(0, action)
      next_position = successor.getPacmanPosition()
      if next_position not in self.visited:
        if self.dfs(successor, next_position, goal): # Recursive DFS
          with open('result.txt', 'a') as result:
            result.write("Agent location = " + f"{x-9, y-1}" + " | Reward location = " +  f"{x1-9, y1-1}\n")
          self.path.insert(0, action)
          return True
    return False

