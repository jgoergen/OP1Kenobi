class Test():
    pad = 0
    measures = 0
    path = ""
    filename = ""
    bpm = 0

    def __init__(self, pad, measures, path, filename, bpm):
        self.pad = int(pad)
        self.measures = int(measures)
        self.path = path
        self.filename = filename
        self.bpm = int(bpm)