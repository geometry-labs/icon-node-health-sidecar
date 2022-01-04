class PeerHeight:
    best = -1

    def setBest(self, best_height):
        self.best = best_height

    def getBest(self):
        return self.best


shared_height = PeerHeight()
