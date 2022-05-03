class Metrics:

    @staticmethod
    def count(window):
        return window.count()

    @staticmethod
    def sum(window):
        return window.sum()

    @staticmethod
    def mean(window):
        return window.mean()
    
    @staticmethod
    def max(window):
        return window.max()