"""
1. 考慮有多少class
- Pizza有咩特性
- 有咩特性係同Order有關
2. 考慮有多少attributes
3. 諗有咩function
4. 之後點落order？
"""
from typing import List

# Class Definition
class Pizza:
# Init Function
  def __init__(self, name: str, price: float):
    self.name: str = name
    self.size: str = 'S'
    self.sauce: str = 'tomato'
    self.base_price: float = price
    self.toppings: List[str] = []
    
  def sauce_type(self) -> str:
    return(self.sauce)
  
  def toppings(self) -> list:
    return(self.toppings)

  def set_toppings(self, t: List[str]) -> None:
    self.toppings = t

  def add_topping(self, t: str) -> None:
    self.toppings.append(t)

  def set_size(self, s: str) -> None:
    if s not in ['S', 'M', 'L']:
      print(f"Unable to set incorrect size {s}")
    else:
      self.size = s

  def set_base_price(self, p: float) -> None:
    if p > 0:
      self.base_price = p
    else:
      print("Unable to set negative base price")

  def get_price(self) -> float:
    if self.base_price <= 0:
      raise Exception("Base price is not correct")
    if self.size == 'M':
      mul = 4/3
    elif self.size == 'L':
      mul = 5/3
    else:
      mul = 1
    return(self.base_price * mul)

class Order:
    def __init__(self) -> None:
        self.pizzas: List[Pizza] = []

    def add_pizza(self, p: Pizza) -> None:
        self.pizzas.append(p)

    def get_price(self) -> float:
        total_price = 0.0
        for p in self.pizzas:
            total_price += p.get_price()
        return(total_price)


canadian = Pizza('Canadian',124)
canadian.set_size('L')
int(canadian.get_price())
new_order = Order()
new_order.add_pizza(canadian)
pepperoni = Pizza('Pepperoni',118)
new_order.add_pizza(pepperoni)
new_order.get_price()