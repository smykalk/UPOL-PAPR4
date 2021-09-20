from random import randint
import threading
import types
import time


class SyncVector:
    def __init__(self, size, initial_value = 0):
        self.size = size

        # Create a lock for each element of the vector
        self.locks = [threading.Lock() for _ in range(size)]

        if type(initial_value) is types.LambdaType:
            self.elements = [initial_value() for _ in range(size)]

        else:
            self.elements = [initial_value for _ in range(size)]


    def get(self, index):
        with self.locks[index]:
            value = self.elements[index]
       
        return value;


    def set(self, index, value):
        with self.locks[index]:
            self.elements[index] = value     



VECTOR_SIZE = 10

# Vytvoří nulový vektor délky 10
vector = SyncVector(VECTOR_SIZE)

# Vytvoří vektor délky 10, kde všechny složky mají hodnotu 1
vector = SyncVector(VECTOR_SIZE, initial_value=1)

# Vytvoří náhodný vektor délky 10
random_vector = SyncVector(VECTOR_SIZE, lambda: randint(0, 100))

# Získání i-té složky vektoru
#vector.get(index)

# Nastavení i-té složky vektoru
# vector.set(value, index)


def nmapv(func, sync_vector:SyncVector, thread_count = 2):
    # We don't need more threads than elements in the vector,
    if thread_count > sync_vector.size:
        thread_count = sync_vector.size

    ranges = split_range(sync_vector.size, thread_count)

    threads = []

    # Get the required range from the list of ranges and assign it 
    # to a concrete thread which uses the map_from_to function
    for thread_num in range(thread_count):
        from_element = ranges[thread_num][0]
        to_element = ranges[thread_num][1]

        threads.append(threading.Thread(target=map_from_to, args=(func, sync_vector, from_element, to_element,)))
        
    for t in threads:
        t.start()

    for t in threads:
        t.join()


# Splits a range of 'N' into 'nb' (roughly) equal parts
def split_range(N, nb):
    step = N / nb

    result = [[round(step*i), round(step*(i+1))] for i in range(nb)]

    return result


# Maps elements in a SyncVector using given function only in a specified range
def map_from_to(map_function, sync_vector:SyncVector, from_element, to_element):
    for index in range(from_element,to_element):
        value = map_function(sync_vector.get(index))
        sync_vector.set(index,value)



def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)



vector = SyncVector(100, lambda: randint(0, 100))


print(vector.elements)
# Mapujeme 2. mocninu na vector a použijeme 10 vláken.
nmapv(lambda e: e * e, vector, 10)
print(vector.elements)


vector_1 = SyncVector(100, 15)
vector_2 = SyncVector(100, 15)


tic = time.perf_counter()
nmapv(factorial,vector_1, 1)
toc = time.perf_counter()


print(f"Time with 1 thread: {toc - tic:0.4f} seconds")

tic = time.perf_counter()
nmapv(factorial,vector_2, 100)
toc = time.perf_counter()


print(f"Time with 100 threads: {toc - tic:0.4f} seconds")





    
    

