from pymem import Pymem


class OFFSETS:
    LOCAL_PLAYER_PTR = 0x18AC00
    ENTITY_LIST_PTR = 0x18AC04
    PLAYER_COUNT = 0x18AC0C
    MAP_NAME = 0x16F58C

    class Player:
        HEALTH = 0xEC
        NAME = 0x205
        POSITION = 0x28
        TEAM = 0x30C


class Position:
    def __init__(self, pm: Pymem, address):
        self._pm = pm
        self._address = address

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    @property
    def x(self):
        return self._pm.read_float(self._address)

    @x.setter
    def x(self, value):
        self._pm.write_float(self._address, float(value))

    @property
    def y(self):
        return self._pm.read_float(self._address + 0x8)

    @y.setter
    def y(self, value):
        self._pm.write_float(self._address + 0x8, float(value))

    @property
    def z(self):
        return self._pm.read_float(self._address + 0x4)

    @z.setter
    def z(self, value):
        self._pm.write_float(self._address + 0x4, float(value))

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"


class Player:
    def __init__(self, pm: Pymem, address):
        self._pm = pm
        self._address = address
        self._position = Position(self._pm, address + OFFSETS.Player.POSITION)

    @property
    def health(self):
        return self._pm.read_int(self._address + OFFSETS.Player.HEALTH)

    @health.setter
    def health(self, value):
        self._pm.write_int(self._address + OFFSETS.Player.HEALTH, value)

    @property
    def name(self):
        return self._pm.read_string(self._address + OFFSETS.Player.NAME)

    @name.setter
    def name(self, value):
        self._pm.write_string(self._address + OFFSETS.Player.NAME, value)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        x, y, z = value
        self._position.x = x
        self._position.y = y
        self._position.z = z

    @property
    def team(self):
        return self._pm.read_int(self._address + OFFSETS.Player.TEAM) # 1 - Blue, 0 - red

    def __str__(self):
        return f"{self.name} - Health: {self.health}; Position: {self.position}, Team: {self.team}"


class EntityList:
    def __init__(self, pm: Pymem):
        self._pm = pm
        self._address = self._pm.read_int(pm.base_address + OFFSETS.ENTITY_LIST_PTR)

    @property
    def player_count(self):
        return self._pm.read_int(self._pm.base_address + OFFSETS.PLAYER_COUNT)

    def __iter__(self):
        for i in range(1, self.player_count):
            yield Player(self._pm, self._pm.read_int(self._address + 0x4 * i))


class AssaultCube:
    def __init__(self):
        self._pm = Pymem("ac_client.exe")
        self.entity_list = EntityList(self._pm)
        self.local_player = Player(self._pm, self._pm.read_int(self._pm.base_address + OFFSETS.LOCAL_PLAYER_PTR))

    @property
    def map(self):
        return self._pm.read_string(self._pm.base_address + OFFSETS.MAP_NAME)