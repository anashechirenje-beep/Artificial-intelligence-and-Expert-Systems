from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")


# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Biconditional(AKnight, And(AKnight, AKnave))
)



# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    Biconditional(
        AKnight,
        And(AKnave, BKnave)
    )
)



# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    Biconditional(
        AKnight,
        Or(
            And(AKnight, BKnight),
            And(AKnave, BKnave)
        )
    ),

    Biconditional(
        BKnight,
        Or(
            And(AKnight, BKnave),
            And(AKnave, BKnight)
        )
    )
)




# Puzzle 3

# Represent the two possible statements A could have made
a_said_knight = And(
    Implication(AKnight, AKnight),
    Implication(AKnave, Not(AKnight))
)

a_said_knave = And(
    Implication(AKnight, AKnave),
    Implication(AKnave, Not(AKnave))
)

knowledge3 = And(

    # Each person must be either a knight or a knave
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    # A said either "I am a knight" or "I am a knave"
    Or(a_said_knight, a_said_knave),

    # B says A said "I am a knave"
    Biconditional(BKnight, a_said_knave),

    # B also says C is a knave
    Biconditional(BKnight, CKnave),

    # C says A is a knight
    Biconditional(CKnight, AKnight)
)





def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
