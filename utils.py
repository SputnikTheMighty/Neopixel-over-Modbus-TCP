
class Words:
    ''' Immutable, iterable object containing 16 bit numbers '''

    def __init__(self, values):
        for i in values:
            assert i < 2**16
        self._buf = values

    def __getitem__(self, index) -> int:
        return self._buf[index]

    def __repr__(self) -> str:
        return " ".join(hex(x) for x in self._buf)

    def __len__(self) -> int:
        return len(self._buf)

    def to_int(self, endian: str):
        temp = 0

        if endian == 'big':
            n = len(self)
            for i in range(n):
                temp += self[n - i - 1] << (16 * i)
            return temp
        
        elif endian == 'little':
            for i in range(len(self)):
                temp += self[i] << (16 * i)
            return temp

        else:
            raise NotImplementedError

    @classmethod
    def from_int(cls, value: int, endian: str, length: int):
        ''' Get Words from int, result may be truncated if length is too short '''
        temp = [0] * length

        if endian == 'big':
            for i in range(length):
                temp[i] = ((0xFFFF << 16*(length - i - 1)) & value) >> 16*(length - i - 1)
            return Words(temp)
        
        elif endian == 'little':
            for i in range(length):
                temp[i] = ((0xFFFF << 16*i) & value) >> 16*i
            return Words(temp)
        
        else:
            raise NotImplementedError

    @classmethod
    def from_bytes(cls, bytes_src: bytes, endian: str):
        assert isinstance(bytes_src, bytes)
        
        if len(bytes_src) % 2 != 0:
            if endian == 'big':
                temp = bytearray(1)
                temp += bytes_src
            if endian == 'little':
                temp = bytearray(bytes_src)
                temp.append(0)
            bytes_src = temp
        
        temp = []
        if endian == 'big':
            for i in range(0, len(bytes_src), 2):
                temp.append((bytes_src[i] << 8) + bytes_src[i+1])
        
        elif endian == 'little':
            for i in range(0, len(bytes_src), 2):
                temp.append((bytes_src[i+1] << 8) + bytes_src[i])

        return Words(temp)

    def to_bytes(self, endian: str):
        temp = []
        if endian == 'big':
            for i in range(len(self)):
                temp.append((self[i] & 0xFF00) >> 8)
                temp.append((self[i] & 0x00FF) >> 0)

        elif endian == 'little':
            for i in range(len(self)):
                temp.append((self[i] & 0x00FF) >> 0)
                temp.append((self[i] & 0xFF00) >> 8)

        else:
            raise NotImplementedError

        return bytes(temp)

if __name__ == "__main__":

    words_from_sequence = Words((32, 39702, 4937, 102, 48271))
    print(words_from_sequence)

    words_from_bytes = Words.from_bytes(bytes((0xFF, 0x73, 0x22, 0xFE)), 'big')
    print(words_from_bytes)

    words_from_bytes = Words.from_bytes(bytes((0xFF, 0x73, 0x22, 0xFE)), 'little')
    print(words_from_bytes)

    words_to_bytes = words_from_bytes.to_bytes('big')
    print([hex(x) for x in words_to_bytes])
    
    words_to_bytes = words_from_bytes.to_bytes('little')
    print([hex(x) for x in words_to_bytes])

    words_from_odd_number_bytes = Words.from_bytes(bytes((0xFF, 0xDE, 0x55)), 'big')
    print(words_from_odd_number_bytes)

    words_from_int = Words.from_int(0xFF778899, endian='big', length=2)
    print(words_from_int)

    words_to_int = words_from_int.to_int(endian='big')
    print(hex(words_to_int))