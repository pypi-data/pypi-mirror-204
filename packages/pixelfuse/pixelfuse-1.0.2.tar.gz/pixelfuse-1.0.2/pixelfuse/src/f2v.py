import struct
import cv2
import numpy as np
import pickle
import hashlib
import os
from rich.progress import track
from rich import print
from pixelfuse import encoder

class ToVideo(object):
    def __init__(self, filename, fps=1., width=640, height=480, fourcc="HFYU", output="output.avi", verbose=2):
        self.filename = filename
        self.fps = fps
        self.width = width
        self.height = height
        self.fourcc = cv2.VideoWriter_fourcc(*fourcc)
        self.output = output
        self.checksum = hashlib.sha512(open(self.filename, 'rb').read()).hexdigest()
        self.verbose = verbose

        self.bytesInFile = os.stat(self.filename).st_size
        self.pixelsInFile = (self.bytesInFile//3)+1

    def convert(self):
        out = cv2.VideoWriter(self.output, self.fourcc, self.fps, (self.width, self.height))

        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.print_verbose("Opening the file...", 1)
        with open(self.filename, 'rb') as f:
            y = 0
            x = 0
            self.print_verbose("Creating meta data...", 2)
            meta = {
                "checksum": self.checksum,
                "filename": self.filename.split("/")[-1],
                "encoder": encoder,
                "lastZeros": 0
            }
            self.print_verbose("Starting video writing...", 1)
            for i in track(range(self.pixelsInFile), transient=True):
                b = f.read(3)
                if not b:
                    self.print_verbose("File end", 3)
                    break
                if len(b) < 3:
                    meta["lastZeros"] = 3-len(b)
                    self.print_verbose(f"File end with {meta['lastZeros']} left zeros", 3)
                    b = b.ljust(3, b'\x00')

                frame[y, x] = struct.unpack('<BBB', b)
                x += 1
                if x >= self.width:
                    x = 0
                    y += 1
                if y >= self.height:
                    self.print_verbose(f"Done {frame[0, 0]} frame", 2)
                    out.write(frame)
                    y = 0
                    frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)

            if np.any(frame):
                self.print_verbose(f"Writing not full {frame[0, 0]} frame", 2)
                out.write(frame)

            self.print_verbose(f"Creating meta data frame...", 3)
            pickle_bytes = pickle.dumps(meta)
            frame = np.frombuffer(pickle_bytes, dtype=np.uint8).copy()
            frame.resize((self.height, self.width, 3))

            self.print_verbose(f"Writing meta data {frame[0, 0]} frame", 2)
            out.write(frame)

        self.print_verbose(f"Writing video...", 1)
        out.release()

    def print_verbose(self, text, verbose):
        if self.verbose >= verbose:
            print(text)