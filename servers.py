#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import abstractmethod, ABC
from typing import Optional, List
import re


class Product:

    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str)
    #  i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu
    #  float)
    def __init__(self, name_: str, price_: float):
        self.name = name_
        self.price = price_

        form = "[a-zA-Z]+\d+"
        if re.fullmatch(form, self.name) is None:
            raise ValueError
    pass

    def __eq__(self, other):
        if (self.price == other.price) and (self.name == other.name):
            return True
        else:
            return False  # FIXME: zwróć odpowiednią wartość

    def __hash__(self):
        return hash((self.name, self.price))


class TooManyProductsFoundError(Exception):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    def __init__(self, msg):
        super().__init__(msg)

    pass


# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#  (1) metodę inicjalizacyjną przyjmującą listę obiektów
#  typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#  (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną
#  dopuszczalną liczbę wyników wyszukiwania,
#  (3) możliwość odwołania się do metody `get_entries(self, n_letters)`
#  zwracającą listę produktów spełniających kryterium wyszukiwania

class Server(ABC):
    n_max_returned_entries = 3

    @abstractmethod
    def get_entries(self, n_letters=1) -> List[Product]:
        pass


class ListServer(Server):
    def __init__(self, lst: List[Product]):
        self.product = lst

    def get_entries(self, n_letters=1) -> List[Product]:
        form = "[a-zA-Z]" * n_letters
        form += "\d{2,3}"
        to_return = []
        for i in self.product:
            if re.fullmatch(form, i.name) is not None:
                to_return.append(i)
            to_return = list(set(to_return))
            if len(to_return) > super().n_max_returned_entries:
                raise TooManyProductsFoundError
        return sorted(to_return, key=lambda x: x.price)

    pass


class MapServer(Server):
    def __init__(self, lst: List[Product]):
        self.product = {i.name: i for i in lst}

    def get_entries(self, n_letters=1):
        form = "[a-zA-Z]" * n_letters
        form += "\d{2,3}"
        to_return = []
        for i in self.product.keys():
            if re.fullmatch(form, i) is not None:
                to_return.append(self.product[i])
            to_return = list(set(to_return))
            if len(to_return) > super().n_max_returned_entries:
                raise TooManyProductsFoundError
        return sorted(to_return, key=lambda x: x.price)


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    def __init__(self, server_: ListServer):
        self.server = server_
        pass

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:

        try:
            Product_List = self.server.get_entries(n_letters)
            if len(Product_List) == 0:
                return None
            sum = 0
            for i in Product_List:
                sum += i.price
            return sum

        except:
            return None
