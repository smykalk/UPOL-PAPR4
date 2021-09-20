import threading


# class Printer:
#     _mutex = threading.Semaphore(value=1)

#     @classmethod
#     def print_text(cls, text: str):
#         with cls._mutex:
#             print(text)


class Barbershop:
    def __init__(self, number_of_chairs):
        self.chair_count = number_of_chairs
        self._customers_inside = 0
        self._mutex = threading.Semaphore(1)

        self._customer = threading.Semaphore(0)
        self._barber = threading.Semaphore(0)
        self._customer_done = threading.Semaphore(0)
        self._barber_done = threading.Semaphore(0)

    # CUSTOMER THREADS:
    def customer_get_haircut(self, thread_id):
        self._mutex.acquire()
        # if the barbershop is full, do nothing
        if self._customers_inside == self.chair_count:
            # Printer.print_text(
            #     "Customer #{}: all chairs occupied, leaving".format(thread_id))
            self._mutex.release()
            return

        self._customers_inside += 1
        self._mutex.release()

        # if not full, signal arrival and wait for barber
        self._customer.release()
        self._barber.acquire()

        # WORK GOES HERE
        # Printer.print_text("Customer #{}: getting a haircut".format(thread_id))

        # after getting the haircut, signal being done and wait for (synchronize with) barber
        self._customer_done.release()
        self._barber_done.acquire()

        self._mutex.acquire()
        self._customers_inside -= 1
        self._mutex.release()

    # BARBER THREAD
    def barber_cut_hair(self):
        while True:
            # if ready to cut, signal to customers
            # no customers -> thread goes to sleep
            self._barber.release()
            self._customer.acquire()

            # WORK GOES HERE
            #Printer.print_text("Barber: cutting")

            # signal being done and synchronize with customer
            self._barber_done.release()
            self._customer_done.acquire()
