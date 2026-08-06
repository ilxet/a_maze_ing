from dataclasses import dataclass

@dataclass(frozen = True)
class Position:
	
	x: int
	y: int

@dataclass
class Cell:

	north: bool = True
	east: bool = True
	west: bool = True
	south: bool = True
	visited: bool = False
	blocked: bool = False

	def wall_count(self) -> int:

		return sum(
			(
			self.north, 
			self.east, 
			self.west, 
			self.south,
			)
		)