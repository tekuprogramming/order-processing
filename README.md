# order-processing


# **Multithreaded Order Processing System**

This project implements a multithreaded order-processing pipeline using Python’s `threading` and `queue` modules. It demonstrates a full workflow for receiving orders, checking stock, generating invoices, and notifying customers, all executed concurrently and coordinated through thread-safe queues.

## **Overview**

The system consists of four dedicated threads, each responsible for a specific stage of the order-processing workflow:

1. **Order Receiver**
   Creates incoming orders and places them in the `order_queue`.

2. **Stock Checker**
   Reads orders from the queue, verifies stock availability, updates the inventory, and forwards the result to the `stock_queue`.

3. **Invoice Creator**
   Generates an invoice for any order confirmed to be in stock and sends the result to the `invoice_queue`.

4. **Notifier**
   Sends a message indicating whether an order has been confirmed or rejected.

All communication between stages is handled exclusively using thread-safe queues, ensuring clean separation and safe concurrent processing.

## **Features**

* **Thread-safe pipelines** using `queue.Queue`
* **Synchronized inventory updates** via a shared `Lock`
* **Independent, decoupled processing stages**
* **Daemon threads** for automatic cleanup when the program terminates
* **Structured console output** showing each processing step

## **How It Works**

### 1. Order Receiver

Receives or creates incoming orders:

```python
order_queue.put((order_id, item))
```

### 2. Stock Checker

Verifies availability and updates inventory safely:

```python
with lock:
    stock[item] -= 1
```

Pushes results forward:

```python
stock_queue.put((order_id, item, available))
```

### 3. Invoice Creator

Builds an invoice for orders that can be fulfilled:

```python
invoice_queue.put((order_id, item, invoice_or_none))
```

### 4. Notifier

Sends confirmation or rejection messages to the customer.

## **Running the Program**

Run the script normally:

```bash
python main.py
```

The program launches all worker threads and processes orders continuously.
The main thread sleeps for **20 seconds**, after which the process exits.

## **Example Output**

```
📝 Received order: 4 for table
❌ Order 4: table isn't in the stock
📧 Notification for the client: Order 4 table was not confirmed
```

## **Customization**

You can adjust the workflow easily:

* **Modify inventory:**
  Edit the `stock` dictionary.

* **Change order frequency:**
  Modify the `time.sleep(random.uniform(0.5, 1.5))` delay.

* **Change runtime:**
  Update `time.sleep(20)` at the bottom of the file.

## **Concepts Demonstrated**

This project covers:

* Multithreading with Python
* Queue-based inter-thread communication
* Coordinated shared-resource access
* Producer/consumer workflows
* Building multistage concurrent pipelines
