from dataclasses import dataclass, field


@dataclass
class LockFile():
    lockstr: str
    name: str = field(init=False)
    pid: str = field(init=False)
    port: int = field(init=False)
    password: str = field(init=False)
    protocol: str = field(init=False)

    def __post_init__(self):
        split = self.lockstr.split(":")
        self.name = split[0]
        self.pid = split[1]
        self.port = int(split[2])
        self.password = split[3]
        self.protocol = split[4]
