from credits import ClassCredits


def test_empty_state():
    class_credits = ClassCredits()
    assert class_credits.get_balance_at(timestamp=0) == 0


def test_get_balance():
    class_credits = ClassCredits()

    # We add one set of credits
    class_credits.add_credits(amount=11, effective_at=0, expires_at=5)

    # We deduct some credits
    class_credits.deduct_credits(amount=5, effective_at=1)

    assert class_credits.get_balance_at(timestamp=2) == 6


def test_add_then_deduct():
    class_credits = ClassCredits()

    # We add one set of credits
    class_credits.add_credits(amount=5, effective_at=0, expires_at=10)

    # We deduct some credits
    class_credits.deduct_credits(amount=1, effective_at=5)

    # Check the balance at a few different times
    assert class_credits.get_balance_at(timestamp=7) == 4
    assert class_credits.get_balance_at(timestamp=8) == 4
    assert class_credits.get_balance_at(timestamp=3) == 5


def test_readme_example():
    class_credits = ClassCredits()

    # Add a set of credits and a deduction
    class_credits.add_credits(amount=5, effective_at=15, expires_at=23)
    class_credits.deduct_credits(amount=4, effective_at=17)

    # Balance should be straightforward
    assert class_credits.get_balance_at(timestamp=20) == 1

    # Add a new set of credits in the _past_ that should be used instead
    class_credits.add_credits(amount=8, effective_at=3, expires_at=19)

    # Balance should change
    assert class_credits.get_balance_at(timestamp=20) == 5


def test_multiple_blocks():
    class_credits = ClassCredits()

    # We add two sets of credits:
    # 1. Five credits active from (0, 10)
    # 2. Six credits active from (1, 5)
    class_credits.add_credits(amount=5, effective_at=0, expires_at=10)
    class_credits.add_credits(amount=6, effective_at=1, expires_at=5)

    assert class_credits.get_balance_at(timestamp=2) == 11

    # Deduct four credits at time 3
    class_credits.deduct_credits(amount=4, effective_at=3)

    # At time 4, we should have seven credits remaining
    # since both of our blocks are active.
    assert class_credits.get_balance_at(timestamp=4) == 7

    # At time 6, we should have five credits remaining
    # since one of the blocks expired
    assert class_credits.get_balance_at(timestamp=6) == 5


def test_old_and_new():
    class_credits = ClassCredits()

    # We add two sets of credits:
    # 1. Five credits active from (0, 10)
    # 2. Nine credits active from (15, 20)
    class_credits.add_credits(amount=5, effective_at=0, expires_at=10)
    class_credits.add_credits(amount=9, effective_at=15, expires_at=20)

    assert class_credits.get_balance_at(timestamp=2) == 5

    # Deduct some credits
    class_credits.deduct_credits(amount=5, effective_at=3)
    assert class_credits.get_balance_at(timestamp=4) == 0

    # Deduct some more credits
    class_credits.deduct_credits(amount=4, effective_at=16)
    assert class_credits.get_balance_at(timestamp=17) == 5


def test_multiple_deductions():
    class_credits = ClassCredits()

    # We add two sets of credits:
    # 1. Eight credits active from (0, 10)
    # 2. Six credits active from (5, 15)
    class_credits.add_credits(amount=8, effective_at=0, expires_at=10)
    class_credits.add_credits(amount=6, effective_at=5, expires_at=15)

    assert class_credits.get_balance_at(timestamp=2) == 8

    # Deduct some credits
    class_credits.deduct_credits(amount=5, effective_at=7)
    assert class_credits.get_balance_at(timestamp=8) == 9

    # Deduct some more credits in the past
    class_credits.deduct_credits(amount=4, effective_at=3)
    assert class_credits.get_balance_at(timestamp=13) == 5


def test_block_expiry():
    class_credits = ClassCredits()

    # Add two blocks with different expiration times
    # 1. Eight credits active from (2, 10)
    # 2. Twelve credits active from (1, 20)
    class_credits.add_credits(amount=8, effective_at=2, expires_at=10)
    class_credits.add_credits(amount=12, effective_at=1, expires_at=20)

    assert class_credits.get_balance_at(timestamp=5) == 20

    # Deduct some credits
    class_credits.deduct_credits(amount=5, effective_at=6)
    assert class_credits.get_balance_at(timestamp=7) == 15

    # Deduct some more credits
    class_credits.deduct_credits(amount=5, effective_at=15)
    assert class_credits.get_balance_at(timestamp=17) == 7

    # All blocks expired
    assert class_credits.get_balance_at(timestamp=25) == 0


# Optional way to run tests if pytest isn't working - python test_credits.py
if __name__ == "__main__":
    test_empty_state()
    test_get_balance()
    test_add_then_deduct()
    test_readme_example()
    test_multiple_blocks()
    test_old_and_new()
    test_multiple_deductions()
    test_block_expiry()
