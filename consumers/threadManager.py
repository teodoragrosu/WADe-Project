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
                print("Data left: " + str(len(self.resources) - 1))
                return self.resources.pop(0)
            return None

    def addResource(self, resource):
        with self.lock:
            self.resources.append(resource)


def threadWrapperFunction(parent, threadIndex, innerFunction):
    while True:
        resource = parent.getResource()
        if resource == None:
            time.sleep(1)
        else:
            tries = 0
            innerFunction(resource)
            #while tries <= 10:
            #   try:
            #        innerFunction(resource)
            #    except:
            #       tries += 1
            #       time.sleep(5)
            #       continue
            #   break
            time.sleep(1)