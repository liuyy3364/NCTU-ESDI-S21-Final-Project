import collections
import ChtToDigit

class Info:
    def __init__(self, products) -> None:
        self.products = products
        self.cart = collections.defaultdict(int)

    def reset(self):
        print("clear")
        self.cart = collections.defaultdict(int)

    def print_cart(self):
        cart = "購物車:\n{:<3}{:4s}品項\n".format("數量","金額")
        for name, num in self.cart.items():
            cart += "{:<5d}{:<6d}{:s}\n".format(num, num*self.products[name], name)
        return cart+"\n"

    def print_cart_with_total(self):
        cart = "購物車:\n{:<3}{:4s}品項\n".format("數量","金額")
        total = 0
        for name, num in self.cart.items():
            cart += "{:<5d}{:<6d}{:s}\n".format(num, num*self.products[name], name)
            total += num*self.products[name]
        cart+="共 " + str(total) + "元"
        return cart+"\n"
    
    def parse_shopping_list(self, sentence, default=1):
        cart = {}
        idx = []
        name = [k for k  in self.products.keys()]
        for i, product in enumerate(name):
            idx_t = sentence.find(product)
            if(idx_t!=-1):
                idx.append((product,idx_t))
        idx.sort(key= lambda x:x[1])
        for i in range(len(idx)):
            if idx[i]==0:
                cart[idx[i][0]] = default
            if(i==0):
                pre = 0
                pre_len = 0
            else:
                pre = idx[i-1][1]
                pre_len = len(idx[i-1][0])
            if pre+pre_len>=idx[i][1]:
                cart[idx[i][0]] = 1
            else:    
                cart[idx[i][0]] = ChtToDigit.trans(sentence[pre+pre_len:idx[i][1]], default)
        return cart
    # def parse_shopping_list(self, sentence, default=1):
    #     cart = {}
    #     idx = [-1]*len(self.products)
    #     name = [k for k  in self.products.keys()]
    #     for i, product in enumerate(name):
    #         idx[i] = sentence.find(product)
    #     for i in range(len(name)):
    #         if idx[i] == -1:
    #             continue
    #         elif idx[i]==0:
    #             cart[name[i]] = default
    #         if(i==0):
    #             pre = 0
    #             pre_len = 0
    #         else:
    #             pre = idx[i-1]
    #             pre_len = len(name[i-1])
    #         if pre+pre_len>idx[i]-1:
    #             cart[name[i]] = 1
    #         else:    
    #             cart[name[i]] = ChtToDigit.trans(sentence[pre+pre_len:idx[i]], default)
    #     return cart
    
    def cart_add(self, cart_in):
        for name, num in cart_in.items():
            self.cart[name] += num

    def cart_remove(self, cart_in):
        for name, num in cart_in.items():
            self.cart[name] -= num
            if(self.cart[name] <= 0):
                del self.cart[name]
        


