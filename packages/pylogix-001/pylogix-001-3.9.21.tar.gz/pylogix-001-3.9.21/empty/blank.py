from random import randrange
from .empty import empty

class GuessMyNumber(empty):

    

    def __init__(self, number=0):

        Guesser.__init__(self,number)
        self.magicNumber = 2


    def play(self):
        '''Function to play GuessMyNumber
        Args:
            None
        Returns:
            None
        '''
        self.giveInstructions()
        self.numberinMind = self.guessingNumber()
        print('...')
        print('Your result is {}'.format(int(self.numberinMind)))



    def giveInstructions(self):
        '''Function to display directions to play
        Args:
            None

        Returns:
            None
        '''

        self.magicNumber = self.generateMagicNumber()
        print('Follow these steps and I will guess your result')
        input("Press Enter to continue...")
        print('Let''s play!')
        print('Think a number greater than 0, do not tell me')
        input("Press Enter to continue...")
        print('Multiple your number times 2')
        input("Press Enter to continue...")
        print('Add {}'.format(self.magicNumber))
        input("Press Enter to continue...")
        print('Divide your result by 2')
        input("Press Enter to continue...")
        print('Last step, subtract to your result the number you initially though')
        input("Press Enter to continue...")
        print('...')
        print('Guessing your result...')


    def generateMagicNumber(self):
        '''Function to generate an even random number between 4 and 24
        Args:
            None

        Returns:
            Integer: An even number between 4 and 24
        '''
        n = randrange(4, 24, 2)
        return int(n)


    def guessingNumber(self):
        '''Function to 'guess' the result of arithmetic operations calculated during the GuessMyNumber
           game.
        Args:
            None

        Returns:
            Integer: the result of arithmetic operations
        '''

        return self.magicNumber / 2
