import threading
import queue
import time
import random

order_queue = queue.Queue() # new orders
stock_queue = queue.Queue() # results of checking the stock
invoice_queue = queue.Queue() # invoice for sending notifications

stock = {"bed": 20, "closet": 10, "table": 15, "armchair": 5}
lock = threading.Lock() # blocking for synchronization of access to the warehouse (so 2 threads don't change the leftovers at the same time)

def order_receiver(): # receiving an order
    order_id = 0 # order id
    items = list(stock.keys()) # all items from stock
    while True:
        order_id += 1 # raises the id
        item = random.choice(items) # random element from stock
        print(f" 📝 Received order: {order_id} for {item}")
        order_queue.put((order_id, item)) # putting an order in a queue
        time.sleep(random.uniform(0.5, 1.5)) # pause from 0.5 to 1.5 seconds

def stock_checker():
    while True:
        order_id, item = order_queue.get() # unboxes the order of variable order_id and item
        with lock: # entering the blocking so the other threads don't interfere
            if stock[item] > 0: # if the order exists in the stock
                stock[item]-= 1 # removing the order from the stock
                print(f" ✅ Order {order_id}: {item} exists in stock (in stock there are {stock[item]} more)")
                stock_queue.put((order_id, item, True)) # putting results in queue stock_queue, True = item is available
            else:
                print(f" ❌ Order {order_id}: {item} isn't in the stock")
                stock_queue.put((order_id, item, False))
        order_queue.task_done() # informing the thread that the task is done

def invoice_creator():
    while True:
        order_id, item, available = stock_queue.get() # unboxes the result of checking the stock
        if available:
            invoice = f"Invoice of order {order_id}: {item}"
            print(f" 📄 The invoice was created: {invoice}")
            invoice_queue.put((order_id, item, invoice)) # putting the order together with the input in the queue
        else:
            invoice_queue.put((order_id, item, None)) # putting the order in the queue without the invoice
        stock_queue.task_done() # informing the thread that the task is done

def notifier():
    while True:
        order_id, item, invoice = invoice_queue.get() # unboxes the result of checking the stock
        if invoice:
            print(f" 📧 Notification for the client: Order {order_id} {item} was confirmed")
        else:
            print(f" 📧 Notification for the client: Order {order_id} {item} was not confirmed")
        invoice_queue.task_done()

threads = [
    threading.Thread(target=order_receiver, daemon=True), # thread does order_receiver, daemon=True - the thread ends with the program
    threading.Thread(target=stock_checker, daemon=True), # thread does order_receiver, daemon=True - the thread ends with the program
    threading.Thread(target=invoice_creator, daemon=True), # thread does order_receiver, daemon=True - the thread ends with the program
    threading.Thread(target=notifier, daemon=True) # thread does order_receiver, daemon=True - the thread ends with the program
]

for t in threads:
    t.start()

time.sleep(20)
