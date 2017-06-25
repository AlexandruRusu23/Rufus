"""
Animation Manager module
"""
import threading
import time
import Queue
import AnimationExecutor
import ResourceProvider

RESOURCE_PROVIDER = ResourceProvider.ResourceProvider()

class AnimationManager(object):
    """
    Animation Manager class
    - read from an extern queue and send the commands to
    Animation Executor
    """
    def __init__(self):
        self.__animation_executor = 0

    def animates(self, animations_queue):
        """
        read from the queue and send to Animation Executor
        """
        current_thread = threading.currentThread()
        self.__animation_executor = AnimationExecutor.AnimationExecutor()
        __thread_timer = time.time()
        while getattr(current_thread, 'is_running', True):
            if time.time() - __thread_timer > 100.0 / 1000.0:
                try:
                    animation = animations_queue.get(False)
                except Queue.Empty:
                    continue

                while getattr(current_thread, 'is_running', True):
                    if bool(self.__animation_executor.execute(str(animation))) is True:
                        break
                    time.sleep(0.05)
                animations_queue.task_done()
                __thread_timer = time.time()
