import unittest
from collections import Counter
import main
from servers import ListServer, Product, Client, MapServer, Server,TooManyProductsFoundError

server_types = (ListServer, MapServer)


class ServerTest(unittest.TestCase):

    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))

    def test_get_entries_returns_proper_entries_empty(self):
        products = [Product('aPP12', 1), Product('PPPP234', 2), Product('PPP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            self.assertEqual([],server.get_entries(2))

    def test_get_entries_too_many_products(self):
        serv = ListServer([])
        products = []
        for i in range(serv.n_max_returned_entries+1):
            products.append(Product('PA12', i))
        for server_type in server_types:
            server = server_type(products)
            with self.assertRaises(TooManyProductsFoundError):
                p = server.get_entries(2)

    def test_dict_server_duplicated_names(self):
        products = [Product('PA12', 1), Product('PA12', 2), Product('PA12', 3),Product('PPP235', 13)]    
        server = MapServer(products)  
        self.assertEqual(len(server.get_entries(2)),3)
    
    def test_get_entries_with_invalid_n(self):
        products = [Product('aPP12', 1), Product('PPPP234', 2), Product('PPP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            with self.assertRaises(ValueError):
                p = server.get_entries(-2)

    
class ProductTest(unittest.TestCase):
    
    def test_invalid_name1(self):
        with self.assertRaises(ValueError):
            p = Product('23p',1)
    def test_invalid_name2(self):
        with self.assertRaises(ValueError):
            p = Product('P,12',1)
    def test_invalid_name3(self):
        with self.assertRaises(ValueError):
            p = Product('GG234\n',1)
    def test_no_name(self):
        with self.assertRaises(ValueError):
            p = Product('',1)
    def test_not_str_as_name(self):
        with self.assertRaises(ValueError):
            p = Product(123,1)
    def test_price_is_below_zero(self):
        with self.assertRaises(ValueError):
            p = Product("PP123",-1)

class ClientTest(unittest.TestCase):
    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))
    
    def test_total_price_empty(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(4))
    
    def test_too_many_products(self):
        serv = ListServer([])
        products = []
        for i in range(serv.n_max_returned_entries+1):
            products.append(Product('PA12', i))
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None,client.get_total_price(2))

    def test_empty_server(self):
        products = []
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(2))

    

if __name__ == '__main__':
    unittest.main()