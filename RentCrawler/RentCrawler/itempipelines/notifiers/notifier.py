from abc import ABCMeta, abstractmethod

class BaseNotifier:
    __metaclass__ = ABCMeta

    @abstractmethod
    def notify_new(self, rentitem):
        pass

    @abstractmethod
    def notify_lowerprice(self, old_rentitem, rentitem):
        pass

    @abstractmethod
    def notify(self, rentitem, title, msg):
        pass
