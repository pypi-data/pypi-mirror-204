"In this script you can find additional functions to reduce the code written."
class Numbers:

    def isOdd(args):
        "Check if one or more numbers, entered in input, are odd."

        if isinstance(args, int):
            if args % 2 == 1:
                return True
            
            return False

        for arg in args:
            if not isinstance(arg, int) and not isinstance(arg, float):
                return None

            if arg % 2 == 1:
                continue
            else:
                return False
            
        return True


    def isEven(args):
        "Check if one or more numbers, entered in input, are even."

        if isinstance(args, int):
            if args % 2 == 0:
                return True
            
            return False

        for arg in args:

            if not isinstance(arg, int) and not isinstance(arg, float):
                return None

            if arg % 2 == 0:
                continue
            else:
                return False
            
        return True

    def listMultiplication(arg: list):
        "From a given list or tuple in input, calculate the multiplication of the numbers inside it. \n\nNote: Non-numerical values will be skipped."

        if isinstance(arg, int) or isinstance(arg, float):
            return arg

        result = 1

        for i in arg:

            try:
                result *= int(i)
            
            except ValueError:
                continue

        return result

    def listSum(arg: list):
        "From a given list or tuple in input, calculate the addition of the numbers inside it. \n\nNote: Non-numerical values will be skipped."

        
        if isinstance(arg, int) or isinstance(arg, float):
            return arg
        

        result = 0

        for i in arg:

            try:
                result += int(i)

            except ValueError:
                continue

        return result
    

class stopwatch:
    "Create as many stopwatch as you need."
    def start():
        "Start a stopwatch. \nNote: The stopwatch needs to be saved into a variable."
        import time
        return time.time()

    def stop(stopwatch):
        "Stop a given stopwatch, and prints out the execution time."
        import time
        elapsed = time.time() - stopwatch
        return elapsed
    

class UnicodeConversion:
    "Here you can convert your text to integer and reconvert it to text, using Unicode."

    def TextToInt(text: str) -> int:
        "Given a string in input convert it into a integer number using Unicode."
        unicode_text = text.encode('utf-8')
        int_value = int.from_bytes(unicode_text, byteorder='big')

        return int_value
    
    def IntToText(text_integer: int) -> str:
        "Given an integer in input convert it to text using Unicode.\n\nWarning: If the integer that has to be converted to text wasn't, before, converted to int using the TextToInt function it won't work."
        byte_sequence = text_integer.to_bytes((text_integer.bit_length() + 7) // 8, byteorder='big')
        unicode_text = byte_sequence.decode('utf-8')

        return unicode_text