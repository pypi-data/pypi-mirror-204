import random
from typing import List

class AIJokeGenerator:
    """
    A class used to generate AI-themed jokes.

    ...

    Attributes
    ----------
    jokes : List[str]
        a list of AI-themed jokes

    Methods
    -------
    get_joke() -> str:
        Returns a randomly selected joke from the jokes list.
    """

    def __init__(self):
        self.jokes: List[str] = [
            "Why did the AI go to school? Because it wanted to be a neural scholar!",
            "Why don't AI agents tell secrets? Because they can't keep anything private!",
            "What do you call a machine learning model that plays the drums? A beat-learning algorithm!",
            "Why was the AI so bad at tennis? It couldn't find the optimal serve!",
            "Why was the AI programmer always broke? They kept losing their cache!",
            "Why did the AI refuse to play cards? It was afraid of the high stakes in poker!",
            "How did the computer scientist cure their insomnia? With neural REST!",
            "Why did the neural network go to the doctor? It had a bad case of overfitting!",
            "Why do AI agents make terrible comedians? They always forget the punch line!",
            "Why did the AI cross the road? To get to the other side of the data set!",
        ]

    def get_joke(self) -> str:
        """
        Randomly selects and returns a joke from the jokes list.

        Returns
        -------
        str
            A randomly selected AI-themed joke.
        """

        return random.choice(self.jokes)
