# Function adapted from dlink_pingen.py
def wps_pin_checksum(pin: int) -> int:
    accum = 0

    while pin:
        accum += 3 * (pin % 10)
        pin = int(pin / 10)
        accum += (pin % 10)
        pin = int(pin / 10)

    return int((10 - accum % 10) % 10)


def validate(pin: int) -> bool:
    return wps_pin_checksum(pin) == (pin % 10)


def calc_pin(partial_pin: int, num: int = 0) -> str:
    num_sum = int(partial_pin + num)
    return '{0:0>8}'.format(str(num_sum * 10 + wps_pin_checksum(num_sum)))
