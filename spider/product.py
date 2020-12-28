class Product:
    def __init__(self, name, desc, price):
        self.name = name
        self.desc = desc
        self.price = price

    def __eq__(self, o: object) -> bool:
        return self.name == o.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return f"商品名：{self.name} 描述：{self.desc} 价格：{self.price}"



