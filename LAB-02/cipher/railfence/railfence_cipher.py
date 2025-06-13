class RailFenceCipher:
    def __init__(self):
        pass
    
    def encrypt(self, text, num):
        rails = [[] for _ in range(num)]
        rail_index = 0
        direction = 1
        for char in text:
            rails[rail_index].append(char)
            rail_index == 0
            if rail_index ==0:
                direction = 1
            elif rail_index == num -1:
                direction = -1
            rail_index += direction
        encrypted_text = "".join(''.join(rail) for rail in rails)
        return encrypted_text
    
    def decrypt(self, text, num):
        rails_length = [0] * num
        rail_index = 0
        direction = 1

        for _ in range(len(text)):
            rails_length[rail_index] += 1
            if rail_index == 0:
                direction = 1
            elif rail_index == num - 1:
                direction = -1
            rail_index += direction
        rails = []
        start = 0
        for length in rails_length:
            rails.append(text[start:start+length])
            start += length
        plain_text = ""
        rail_index = 0
        direction = 1

        for _ in range(len(text)):
            plain_text += rails[rail_index][0]
            rails[rail_index] = rails[rail_index][1:]
            if rail_index == 0:
                direction = 1
            elif rail_index == num - 1:
                direction = -1
            rail_index += direction 

        return plain_text