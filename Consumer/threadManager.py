import time
import threading

class ThreadManager:
    def __init__(self, poolSize, function):
        self.threads = []
        self.resources = []
        self.lock = threading.Lock()

        for index in range(poolSize):
            self.threads.append(threading.Thread(target=threadWrapperFunction, args=(self,index, function)))

        for thread in self.threads:
            thread.start()

    def getResource(self):
        with self.lock:
            if len(self.resources) > 0:
                return self.resources.pop(0)
            return None

    def addResource(self, resource):
        with self.lock:
            self.resources.append(resource)


def threadWrapperFunction(parent, threadIndex, innerFunction):
    while True:
        resource = parent.getResource()
        if resource == None:
            print(threadIndex, "Wait")
            time.sleep(1)
        else:
            print(threadIndex, "Work")
            tries = 0
            while tries <= 10:      
                try:
                    innerFunction(resource)
                except:
                    print(threadIndex, "Error")
                    tries += 1
                    time.sleep(5)
                    continue
                break
            time.sleep(1)