# --- Day 7: Amplification Circuit ---
# Based on the navigational maps, you're going to need to send more power to your ship's thrusters to reach Santa in time. To do this, you'll need to configure a series of amplifiers already installed on the ship.

# There are five amplifiers connected in series; each one receives an input signal and produces an output signal. They are connected such that the first amplifier's output leads to the second amplifier's input, the second amplifier's output leads to the third amplifier's input, and so on. The first amplifier's input value is 0, and the last amplifier's output leads to your ship's thrusters.

#     O-------O  O-------O  O-------O  O-------O  O-------O
# 0 ->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-> (to thrusters)
#     O-------O  O-------O  O-------O  O-------O  O-------O
# The Elves have sent you some Amplifier Controller Software (your puzzle input), a program that should run on your existing Intcode computer. Each amplifier will need to run a copy of the program.

# When a copy of the program starts running on an amplifier, it will first use an input instruction to ask the amplifier for its current phase setting (an integer from 0 to 4). Each phase setting is used exactly once, but the Elves can't remember which amplifier needs which phase setting.

# The program will then call another input instruction to get the amplifier's input signal, compute the correct output signal, and supply it back to the amplifier with an output instruction. (If the amplifier has not yet received an input signal, it waits until one arrives.)

# Your job is to find the largest output signal that can be sent to the thrusters by trying every possible combination of phase settings on the amplifiers. Make sure that memory is not shared or reused between copies of the program.

# For example, suppose you want to try the phase setting sequence 3,1,2,4,0, which would mean setting amplifier A to phase setting 3, amplifier B to setting 1, C to 2, D to 4, and E to 0. Then, you could determine the output signal that gets sent from amplifier E to the thrusters with the following steps:

# Start the copy of the amplifier controller software that will run on amplifier A. At its first input instruction, provide it the amplifier's phase setting, 3. At its second input instruction, provide it the input signal, 0. After some calculations, it will use an output instruction to indicate the amplifier's output signal.
# Start the software for amplifier B. Provide it the phase setting (1) and then whatever output signal was produced from amplifier A. It will then produce a new output signal destined for amplifier C.
# Start the software for amplifier C, provide the phase setting (2) and the value from amplifier B, then collect its output signal.
# Run amplifier D's software, provide the phase setting (4) and input value, and collect its output signal.
# Run amplifier E's software, provide the phase setting (0) and input value, and collect its output signal.
# The final output signal from amplifier E would be sent to the thrusters. However, this phase setting sequence may not have been the best one; another sequence might have sent a higher signal to the thrusters.

# Here are some example programs:

# Max thruster signal 43210 (from phase setting sequence 4,3,2,1,0):

# 3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0
# Max thruster signal 54321 (from phase setting sequence 0,1,2,3,4):

# 3,23,3,24,1002,24,10,24,1002,23,-1,23,
# 101,5,23,23,1,24,23,23,4,23,99,0,0
# Max thruster signal 65210 (from phase setting sequence 1,0,4,3,2):

# 3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
# 1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0
# Try every combination of phase settings on the amplifiers. What is the highest signal that can be sent to the thrusters?
"""
from collections import deque
import itertools


def int_code(codes, inputs):

    # int_code version modified for day 07

    output = deque()

    copy = codes[:]                 # deep copy

    idx = 0
    while idx < len(copy):
        if copy[idx] == 99:             # Exit
            break
        else:
            op_code = list(str(copy[idx]))

            while len(op_code) < 5:            # Adjust to correct length ABCDE of the instruction
                op_code.insert(0, '0')

            # convert instruction back to integers:
            op_code = [int(o) for o in op_code]

            if op_code[4] == 3:                     # Input
                copy[copy[idx+1]] = inputs.popleft()
                idx += 2
            elif op_code[4] == 4:                   # Output
                if op_code[2] == 1:                 # immediate mode
                    output.append(copy[idx+1])
                    # print("Output: ", copy[idx+1])
                else:                               # position mode
                    output.append(copy[copy[idx+1]])
                    # print("Output: ", copy[copy[idx+1]])
                idx += 2
            elif op_code[4] in [1, 2, 5, 6, 7, 8]:
                # Obtain operands according to mode
                a = copy[idx + 1] if op_code[2] == 1 else copy[copy[idx+1]]
                b = copy[idx + 2] if op_code[1] == 1 else copy[copy[idx+2]]

                if op_code[4] in [1, 2]:                                        # Add or multiply
                    copy[copy[idx+3]] = operate(op_code[4], a, b)
                    idx += 4
                elif op_code[4] in [5, 6]:
                    if (a != 0) and (op_code[4] == 5):
                        idx = b
                    elif (a == 0) and (op_code[4] == 6):
                        idx = b
                    else:
                        idx += 3            # No jump, next instruction
                elif op_code[4] in [7, 8]:
                    if (a < b) and op_code[4] == 7:
                        copy[copy[idx+3]] = 1
                    elif (a == b) and op_code[4] == 8:
                        copy[copy[idx+3]] = 1
                    else:
                        copy[copy[idx+3]] = 0
                    idx += 4
            else:
                print("Invalid code.")

    return output.popleft()


def operate(op_code, a=None, b=None):
    result = None
    if op_code == 1:
        result = a + b
    elif op_code == 2:
        result = a*b
    else:
        print("Invalid opcode, returning None")

    return result


test_data = [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23,
             101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0]            # max thurster signal 54321

test_data = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]                       # max thruster signal 65210

data = [3,8,1001,8,10,8,105,1,0,0,21,34,43,60,81,94,175,256,337,418,99999,3,9,101,2,9,9,102,4,9,9,4,9,99,3,9,102,2,9,9,4,9,99,3,9,102,4,9,9,1001,9,4,9,102,3,9,9,4,9,99,3,9,102,4,9,9,1001,9,2,9,1002,9,3,9,101,4,9,9,4,9,99,3,9,1001,9,4,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,99]

phase_sequences = list(itertools.permutations(range(0, 5), 5))

thruster_signal = []
for sequence in phase_sequences:
    print("Current phase sequence", sequence)

    input_signal = 0
    for s in sequence:
        input_code = deque([s, input_signal])            # first input
        output_signal = int_code(data, input_code)
        input_signal = output_signal

    thruster_signal.append(output_signal)

print("Max thurster signal is: ", max(thruster_signal))
"""
# ====================================================================================================================
# --- Part Two - --
# It's no good - in this configuration, the amplifiers can't generate a large enough output signal to produce the thrust you'll need. The Elves quickly talk you through rewiring the amplifiers into a feedback loop:

#       O-------O  O-------O  O-------O  O-------O  O-------O
# 0 - + -> | Amp A | -> | Amp B | -> | Amp C | -> | Amp D | -> | Amp E | -.
#    |  O-------O  O-------O  O-------O  O-------O  O-------O |
#    | |
#    '--------------------------------------------------------+
#                                                             |
#                                                             v
#                                                      (to thrusters)
# Most of the amplifiers are connected as they were before; amplifier A's output is connected to amplifier B's input, and so on. However, the output from amplifier E is now connected into amplifier A's input. This creates the feedback loop: the signal will be sent through the amplifiers many times.

# In feedback loop mode, the amplifiers need totally different phase settings: integers from 5 to 9, again each used exactly once. These settings will cause the Amplifier Controller Software to repeatedly take input and produce output many times before halting. Provide each amplifier its phase setting at its first input instruction; all further input/output instructions are for signals.

# Don't restart the Amplifier Controller Software on any amplifier during this process. Each one should continue receiving and sending signals until it halts.

# All signals sent or received in this process will be between pairs of amplifiers except the very first signal and the very last signal. To start the process, a 0 signal is sent to amplifier A's input exactly once.

# Eventually, the software on the amplifiers will halt after they have processed the final loop. When this happens, the last output signal from amplifier E is sent to the thrusters. Your job is to find the largest output signal that can be sent to the thrusters using the new phase settings and feedback loop arrangement.

# Here are some example programs:

# Max thruster signal 139629729 (from phase setting sequence 9,8,7,6,5):

# 3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
# 27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
# Max thruster signal 18216 (from phase setting sequence 9,7,8,5,6):

# 3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
# -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
# 53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10
# Try every combination of the new phase settings on the amplifier feedback loop. What is the highest signal that can be sent to the thrusters?


from collections import deque
import itertools
from copy import deepcopy


class Amp:
    def __init__(self, codes):
        self.codes = codes[:]           # deep copy for each object
        self.idx = 0                    # index in codes
        self.output = 0
        self.halt = False               # program is halting or not
        self.input_counter = 0


def run_amp(inputs, amp):

    inputs_copy = deepcopy(inputs)

    while amp.codes[amp.idx] != 99:
        op_code = list(str(amp.codes[amp.idx]))

        while len(op_code) < 5:            # Adjust to correct length ABCDE of the instruction
            op_code.insert(0, '0')

        # convert instruction back to integers:
        op_code = [int(o) for o in op_code]

        if op_code[4] == 3:
            if not amp.input_counter:               # input
                amp.codes[amp.codes[amp.idx+1]] = inputs.popleft()
            else:
                amp.codes[amp.codes[amp.idx+1]] = inputs.pop()
            
            amp.idx += 2
            amp.input_counter += 1

        elif op_code[4] == 4:                   # Output
            if op_code[2] == 1:                 # immediate mode
                amp.output = amp.codes[amp.idx+1]
                amp.idx += 2
                return amp
            else:                               # position mode
                amp.output = amp.codes[amp.codes[amp.idx+1]]
                amp.idx += 2
                return amp
        elif op_code[4] in [1, 2, 5, 6, 7, 8]:
            # Obtain operands according to mode
            a = amp.codes[amp.idx +
                          1] if op_code[2] == 1 else amp.codes[amp.codes[amp.idx+1]]
            b = amp.codes[amp.idx +
                          2] if op_code[1] == 1 else amp.codes[amp.codes[amp.idx+2]]

            if op_code[4] in [1, 2]:                                        # Add or multiply
                amp.codes[amp.codes[amp.idx+3]] = operate(op_code[4], a, b)
                amp.idx += 4
            elif op_code[4] in [5, 6]:
                if (a != 0) and (op_code[4] == 5):
                    amp.idx = b
                elif (a == 0) and (op_code[4] == 6):
                    amp.idx = b
                else:
                    amp.idx += 3            # No jump, next instruction
            elif op_code[4] in [7, 8]:
                if (a < b) and op_code[4] == 7:
                    amp.codes[amp.codes[amp.idx+3]] = 1
                elif (a == b) and op_code[4] == 8:
                    amp.codes[amp.codes[amp.idx+3]] = 1
                else:
                    amp.codes[amp.codes[amp.idx+3]] = 0
                amp.idx += 4
        else:
            print("Invalid code.")
    
    amp.halt = True

    return amp


def operate(op_code, a=None, b=None):
    result = None
    if op_code == 1:
        result = a + b
    elif op_code == 2:
        result = a*b
    else:
        print("Invalid opcode, returning None")

    return result

data = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]

data = [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54,
        -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4,
        53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10]

data = [3,8,1001,8,10,8,105,1,0,0,21,34,43,60,81,94,175,256,337,418,99999,3,9,101,2,9,9,102,4,9,9,4,9,99,3,9,102,2,9,9,4,9,99,3,9,102,4,9,9,1001,9,4,9,102,3,9,9,4,9,99,3,9,102,4,9,9,1001,9,2,9,1002,9,3,9,101,4,9,9,4,9,99,3,9,1001,9,4,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,99]

phase_sequences = list(itertools.permutations(range(5, 9+1), 5))

thruster_signal = []
for sequence in phase_sequences:
    amps = [Amp(data) for _ in range(5)]

    input_signal = 0
    active = 0
    counter = 0
    while not amps[4].halt:
        input_code = deque([sequence[active], input_signal])            # first input
        amps[active] = run_amp(input_code, amps[active])
        input_signal = amps[active].output
        counter += 1
        active = (active + 1) % 5                                   # Create repeating counter

    thruster_signal.append(amps[4].output)

print("Max thurster signal is: ", max(thruster_signal))
