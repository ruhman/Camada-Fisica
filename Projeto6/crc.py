class CRC:
    # Returns XOR of 'a' and 'b'
    # (both of same length)
    def __init__(self):
        """ Initializes the TX class
        """
        self.key = "1101101011100110"
        
        
    def xor(self, a, b):
    
        # initialize result
        result = []
    
        # Traverse all bits, if bits are
        # same, then XOR is 0, else 1
        for i in range(1, len(b)):
            if a[i] == b[i]:
                result.append('0')
            else:
                result.append('1')
    
        return ''.join(result)

    # Performs Modulo-2 division
    def mod2div(self, divident, divisor):
    
        # Number of bits to be XORed at a time.
        pick = len(divisor)
    
        # Slicing the divident to appropriate
        # length for particular step
        tmp = divident[0 : pick]
    
        while pick < len(divident):
    
            if tmp[0] == '1':
    
                # replace the divident by the result
                # of XOR and pull 1 bit down
                tmp = self.xor(divisor, tmp) + divident[pick]
    
            else:   # If leftmost bit is '0'
                # If the leftmost bit of the dividend (or the
                # part used in each step) is 0, the step cannot
                # use the regular divisor; we need to use an
                # all-0s divisor.
                tmp = self.xor('0'*pick, tmp) + divident[pick]
    
            # increment pick to move further
            pick += 1
    
        # For the last n bits, we have to carry it out
        # normally as increased value of pick will cause
        # Index Out of Bounds.
        if tmp[0] == '1':
            tmp = self.xor(divisor, tmp)
        else:
            tmp = self.xor('0'*pick, tmp)
    
        checkword = tmp
        return checkword
    
    # Function used at the sender side to encode
    # data by appending remainder of modular divison
    # at the end of data.
    def encodeData(self, data):
        unidos = ""
        for b in data:
            b = bin(b)
            b = b[2:]
            unidos += b
        l_key = len(self.key)
    
        # Appends n-1 zeroes at end of data
        appended_data = unidos + '0'*(l_key-1)
        remainder = self.mod2div(appended_data, self.key)
    
        return remainder




        



