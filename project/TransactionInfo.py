import collections
import ChtToDigit

class Info:
    def __init__(self, products) -> None:
        self.products = products
        self.cart = collections.defaultdict(int)

    def reset(self):
        self.cart = collections.defaultdict(int)

    def print_cart(self):
        cart = "購物車:\n{:<3}{:4s}品項\n".format("數量","金額")
        for name, num in self.cart.items():
            cart += "{:<5d}{:<6d}{:s}\n".format(num, num*self.products[name], name)
        return cart+"\n"
    
    def parse_shopping_list(self, sentence, default=1):
        cart = {}
        idx = [-1]*len(self.products)
        name = [k for k  in self.products.keys()]
        for i, product in enumerate(name):
            idx[i] = sentence.find(product)
        for i in range(len(name)):
            if idx[i] == -1:
                continue
            elif idx[i]==0:
                cart[name[i]] = default
            if(i==0):
                pre = 0
                pre_len = 0
            else:
                pre = idx[i-1]
                pre_len = len(name[i-1])
            if pre+pre_len>idx[i]-1:
                cart[name[i]] = 1
            else:    
                cart[name[i]] = ChtToDigit.trans(sentence[pre+pre_len:idx[i]], default)
        return cart
    
    def cart_add(self, cart_in):
        for name, num in cart_in.items():
            self.cart[name] += num

    def cart_remove(self, cart_in):
        for name, num in cart_in.items():
            self.cart[name] -= num
            if(self.cart[name] <= 0):
                del self.cart[name]
        


