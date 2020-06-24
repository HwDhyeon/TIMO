import time

def timer(original_func):
    """
    The execution time of the function is measured and the result is displayed on the screen  
    Use it as a decorator
    """
    def wrapper_func(*args, **kwargs):
        start_time: float = time.time()
        result = original_func(*args, **kwargs)
        end_time: float = time.time()
        print('Time spending: {:.2f} seconds'.format(end_time - start_time), end='\n\n')
        return result
    return wrapper_func
