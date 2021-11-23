#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import abstractmethod, ABC
from copy import copy
from typing import Optional, List
import re


class Product:

    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str)
    #  i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu
    #  float)
    def __init__(self, name_: str, price_: float) -> None:
        try:
            self.name: str = name_
            if float(price_) < 0:
                raise ValueError
            self.price: float = float(price_)

            form = "[a-zA-Z]+\d+"
            if re.fullmatch(form, self.name) is None:
                raise ValueError
        except:
            raise ValueError

    def __eq__(self, other) -> bool:
        if (self.price == other.price) and (self.name == other.name):
            return True
        else:
            return False  # FIXME: zwróć odpowiednią wartość

    def __hash__(self):
        return hash((self.name, self.price))


class ServerError(Exception):
    # Reprezentuje klasę macierzystą wyjątku związanego ze znalezieniem zbyt dużej liczby produktów.
    def __init__(self, msg: str):
        super().__init__(msg)


class TooManyProductsFoundError(ServerError):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    def __init__(self, msg: str):
        super().__init__(msg)


# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#  (1) metodę inicjalizacyjną przyjmującą listę obiektów
#  typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#  (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną
#  dopuszczalną liczbę wyników wyszukiwania,
#  (3) możliwość odwołania się do metody `get_entries(self, n_letters)`
#  zwracającą listę produktów spełniających kryterium wyszukiwania

class Server(ABC):
    n_max_returned_entries: int = 3

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

    @abstractmethod
    def get_entries(self, n_letters: int = 1) -> List[Product]:
        raise NotImplementedError


class ListServer(Server):

    def __init__(self, lst: List[Product]):
        super().__init__()
        lst = list(set(lst))
        self.products = lst

    def get_entries(self, n_letters: int = 1) -> List[Product]:
        if type(n_letters) != int or n_letters <= 0:
            raise ValueError
        form = "[a-zA-Z]" * n_letters + "\d{2,3}"
        to_return = []
        for i in self.products:
            if re.fullmatch(form, i.name) is not None:
                to_return.append(i)
            if len(to_return) > super().n_max_returned_entries:
                raise TooManyProductsFoundError("too many found")
        return sorted(to_return, key=lambda x: x.price)


class MapServer(Server):
    def __init__(self, lst: List[Product]):
        super().__init__()
        lst = list(set(lst))
        self.products = {i.name: [] for i in lst}
        for i in lst:
            self.products[i.name].append(i)
        super(MapServer, self).__init__()

    def get_entries(self, n_letters: int = 1):
        if type(n_letters) != int or n_letters <= 0:
            raise ValueError
        form = "[a-zA-Z]" * n_letters + "\d{2,3}"
        to_return = []
        for i in self.products.keys():
            if re.fullmatch(form, i) is not None:
                to_return.extend(self.products[i])
            if len(to_return) > super().n_max_returned_entries:
                raise TooManyProductsFoundError("too many found")
        return sorted(to_return, key=lambda x: x.price)


class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    def __init__(self, server_: Server):
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