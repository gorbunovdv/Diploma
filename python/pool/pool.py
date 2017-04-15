import pathos.multiprocessing
import multiprocessing

lock = multiprocessing.Lock()
pool = pathos.multiprocessing.Pool(processes=multiprocessing.cpu_count())
