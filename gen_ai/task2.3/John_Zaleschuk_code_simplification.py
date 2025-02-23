from math import gcd

def degrees_to_radians():
    for degrees in range(361):
        num, denom = degrees, 180
        common_divisor = gcd(num, denom)
        num //= common_divisor
        denom //= common_divisor
        
        if num == 0:
            print(f"{degrees} Degrees = 0 Radians")
        elif denom == 1:
            print(f"{degrees} Degrees = {num}π Radians")
        else:
            print(f"{degrees} Degrees = {num}π/{denom} Radians")

degrees_to_radians()
