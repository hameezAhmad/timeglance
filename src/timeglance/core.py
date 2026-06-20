import time
import tracemalloc
import warnings

def glance(iterable, sample_size=10, max_ram_mb=None, max_time_sec=None):
    """Predicts execution time and memory growth of an iterable early in its execution."""
    tracemalloc.start()
    start_time = time.time()
    start_mem, _ = tracemalloc.get_traced_memory()

    try:
        total_items = len(iterable)
    except TypeError:
        total_items = None 

    iterator = iter(iterable)
    
    for i, item in enumerate(iterator):
        yield item
        
        if i + 1 == sample_size:
            elapsed_time = time.time() - start_time
            current_mem, _ = tracemalloc.get_traced_memory()
            
            mem_growth_mb = (current_mem - start_mem) / (1024 * 1024)
            time_per_iter = elapsed_time / sample_size
            
            if total_items:
                est_total_time = time_per_iter * total_items
                est_total_mem_mb = (mem_growth_mb / sample_size) * total_items
                
                print(f"[TimeGlance] ETA: {est_total_time:.2f}s | Est. Mem Growth: {est_total_mem_mb:.2f}MB")

                if max_time_sec and est_total_time > max_time_sec:
                    warnings.warn(f"Time limit predicted to be exceeded: {est_total_time:.2f}s > {max_time_sec}s")
                if max_ram_mb and est_total_mem_mb > max_ram_mb:
                    warnings.warn(f"Memory limit predicted to be exceeded: {est_total_mem_mb:.2f}MB > {max_ram_mb}MB")
            else:
                print(f"[TimeGlance] Rate: {time_per_iter:.4f}s/iter | {mem_growth_mb/sample_size:.4f}MB/iter (Unknown total length)")
            
            # Stop tracking to eliminate overhead for the remaining iterations
            tracemalloc.stop()