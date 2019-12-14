# Santa has become stranded at the edge of the Solar System while delivering presents to other planets! To accurately calculate his position in space, safely align his warp drive, and return to Earth in time to save Christmas, he needs you to bring him measurements from fifty stars.

# Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar
# the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

# The Elves quickly load you into a spacecraft and prepare to launch.

# At the first Go / No Go poll, every Elf is Go until the Fuel Counter-Upper. They haven't determined the amount of fuel required yet.

# Fuel required to launch a given module is based on its mass. Specifically, to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.

# For example:

# For a mass of 12, divide by 3 and round down to get 4, then subtract 2 to get 2.
# For a mass of 14, dividing by 3 and rounding down still yields 4, so the fuel required is also 2.
# For a mass of 1969, the fuel required is 654.
# For a mass of 100756, the fuel required is 33583.
# The Fuel Counter-Upper needs to know the total fuel requirement. To find it, individually calculate the fuel needed for the mass of each module(your puzzle input), then add together all the fuel values.

# What is the sum of the fuel requirements for all of the modules on your spacecraft?
import math
test_data = [12, 14, 1969, 100756]
test_result = [2, 2, 654, 33583]

data = [120183,
        105169,
        58942,
        105283,
        100729,
        57778,
        59601,
        86011,
        148930,
        76533,
        132625,
        79105,
        66334,
        87695,
        148836,
        129384,
        71225,
        96010,
        67221,
        139037,
        90010,
        72531,
        145543,
        137983,
        63687,
        131307,
        62602,
        129223,
        76717,
        98896,
        58484,
        127996,
        128840,
        60723,
        149932,
        141443,
        96997,
        96196,
        104670,
        104055,
        129552,
        54426,
        104507,
        80241,
        91570,
        140053,
        106108,
        119792,
        133703,
        66387,
        129594,
        144794,
        91962,
        134610,
        97937,
        111599,
        77667,
        133644,
        89207,
        121935,
        80434,
        147413,
        94091,
        110244,
        59255,
        53071,
        133121,
        55972,
        122369,
        95605,
        142303,
        120242,
        113412,
        107519,
        88325,
        85243,
        104752,
        85418,
        101515,
        145236,
        107302,
        142970,
        87763,
        112798,
        105469,
        88303,
        91668,
        129187,
        115297,
        56238,
        69358,
        109148,
        99943,
        96480,
        98344,
        77777,
        98973,
        138814,
        106194,
        128739]


def fuel_required(d):
    return math.floor(d/3)-2


for tr, td in zip(test_result, test_data):
    assert tr == fuel_required(td), "Test failed"

total_fuel = sum([fuel_required(d) for d in data])

# print("Total fuel is: ", total_fuel)


# --- Part Two - --
# During the second Go / No Go poll, the Elf in charge of the Rocket Equation Double-Checker stops the launch sequence. Apparently, you forgot to include additional fuel for the fuel you just added.

# Fuel itself requires fuel just like a module - take its mass, divide by three, round down, and subtract 2. However, that fuel also requires fuel, and that fuel requires fuel, and so on. Any mass that would require negative fuel should instead be treated as if it requires zero fuel; the remaining mass, if any, is instead handled by wishing really hard, which has no mass and is outside the scope of this calculation.

# So, for each module mass, calculate its fuel and add it to the total. Then, treat the fuel amount you just calculated as the input mass and repeat the process, continuing until a fuel requirement is zero or negative. For example:

# A module of mass 14 requires 2 fuel. This fuel requires no further fuel(2 divided by 3 and rounded down is 0, which would call for a negative fuel), so the total fuel required is still just 2.
# At first, a module of mass 1969 requires 654 fuel. Then, this fuel requires 216 more fuel(654 / 3 - 2). 216 then requires 70 more fuel, which requires 21 fuel, which requires 5 fuel, which requires no further fuel. So, the total fuel required for a module of mass 1969 is 654 + 216 + 70 + 21 + 5 = 966.
# The fuel required by a module of mass 100756 and its fuel is: 33583 + 11192 + 3728 + 1240 + 411 + 135 + 43 + 12 + 2 = 50346.
# What is the sum of the fuel requirements for all of the modules on your spacecraft when also taking into account the mass of the added fuel? (Calculate the fuel requirements for each module separately, then add them all up at the end.)

def fuel_required_corrected(data):
    flag = True
    total = 0
    while flag:
        data = [fuel_required(d) for d in data]
        data = [d for d in data if d > 0]
        total += sum(data)
        if len(data) == 0:
            flag = False

    return total


print("Total fuel is: ", fuel_required_corrected(data))
