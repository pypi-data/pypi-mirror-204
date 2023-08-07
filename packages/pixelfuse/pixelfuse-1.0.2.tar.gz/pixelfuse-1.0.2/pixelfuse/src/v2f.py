import ffmpegio
import numpy as np
import hashlib
import pickle
from pixelfuse import decoder, compatible_encoders
from rich.console import Console

class ToFile:
    def __init__(self, filename, verbose, show_log):
        self.filename = filename
        self.verbose = verbose
        self.show_log = show_log
        self.console = Console()

    def read_video(self):
        self.print_verbose("Reading video...", 1)
        _, I = ffmpegio.video.read(self.filename, show_log=self.show_log)
        self.I = np.flip(I, axis=3)

    def load_meta(self):
        self.print_verbose("Loading meta...", 2)
        self.meta = pickle.loads(bytes(self.I[-1].flatten()))

        if self.meta["encoder"] not in compatible_encoders:
            self.print_verbose(f"[yellow bold]Endcoder {self.meta['encoder']} isn't compatible by {decoder}", 0)

    def preprocess_file_data(self):
        self.print_verbose("Preprocessing file data...", 2)
        data = self.I[:-1].flatten()
        data = data.reshape((-1, 3))
        while np.all(data[-1] == 0):
            data = data[:-1]
        data = data.flatten()
        self.data = data[:len(data)-self.meta["lastZeros"]]

    def write_file(self):
        self.print_verbose("Writing file data...", 1)
        with open(self.meta["filename"], "wb") as f:
            f.write(bytes(self.data))

    def verify(self):
        self.print_verbose("Verifing file data...", 2)
        if self.meta["checksum"] != hashlib.sha512(open(self.meta["filename"], 'rb').read()).hexdigest():
            self.print_verbose("[red bold]File checksum doesn't match!", np.NINF)

    def convert(self):
        with self.console.status("[green]Decoding video...") as s:
            self.read_video()
            self.load_meta()
            self.preprocess_file_data()
            self.write_file()
            self.verify()

    def print_verbose(self, text, verbose):
        if self.verbose >= verbose:
            self.console.print(text)