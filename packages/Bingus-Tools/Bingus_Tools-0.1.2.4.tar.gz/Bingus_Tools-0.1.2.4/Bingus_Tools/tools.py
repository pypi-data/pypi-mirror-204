class random:
    def number(start:int, end:int):
        import random
        return random.randint(start, end)
    def letter(case:str):
        if case == "lower-case" or case == "lowercase" or case == "lower case":
            import string
            import random
            return random.choice(string.ascii_lowercase)
        elif case == "upper-case" or case == "uppercase" or case == "upper case":
            import string
            import random
            return random.choice(string.ascii_uppercase)
    def string(length:int):
        import random
        import string
        return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation, k=length))
    def words(numberofwords:int):
        for i in range(numberofwords):
            import random
            words = open('words.txt').read().splitlines()
            return random.choice(words)
    def country():
        import pycountry
        import random
        return random.choice(list(pycountry.countries))

def qrcode(size:int, link:str, colour1:str, colour2:str, filename:str):
    import qrcode
    qr = qrcode.QRCode(
        version=size,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color=colour1, back_color=colour2)
    img.save(filename)
