import copy
from dataclasses import dataclass



@dataclass
class CreditBlock:
    amount: int
    effective_at: int
    expires_at: int


@dataclass
class Deduction:
    amount: int
    effective_at: int


class ClassCredits:
    """
    ClassCredits manages a user's credit balance over time.

    This class is designed to handle credit additions and deductions where
    operations can be recorded out of order. It calculates the credit
    balance at any given point in time.
    """

    def __init__(self) -> None:
        """Initializes the ClassCredits system."""
        self._credit_blocks: list[CreditBlock] = []
        self._deductions: list[Deduction] = []

    def add_credits(self, amount: int, effective_at: int, expires_at: int) -> None:
        """
        Adds a block of credits to the system.

        Args:
            amount: The number of credits to add.
            effective_at: The timestamp when these credits become valid.
            expires_at: The timestamp when these credits expire.
        """
        self._credit_blocks.append(CreditBlock(amount, effective_at, expires_at))

    def deduct_credits(self, amount: int, effective_at: int) -> None:
        """
        Records a deduction of credits for a class.

        Args:
            amount: The number of credits to deduct.
            effective_at: The timestamp of the class/deduction.
        """
        self._deductions.append(Deduction(amount, effective_at))

    def print_state(self) -> None:
        """
        Print the underlying state inside the class to help aid in debugging.
        """

        print("Credit blocks")
        for block in self._credit_blocks:
            print(
                f"\tAmount: {block.amount}, Effective At: {block.effective_at}, Expires At: {block.expires_at}"
            )

        print("Deductions")
        for deduction in self._deductions:
            print(
                f"\tAmount: {deduction.amount}, Effective At: {deduction.effective_at}"
            )

    def get_balance_at(self, timestamp: int) -> int:
        """
        Calculates the total available credit balance at a specific timestamp.

        This method accounts for all credit blocks and deductions that have
        occurred up to the given timestamp. It is designed to deduct credits
        from the soonest expiring blocks first.

        Args:
            timestamp: The point in time to calculate the balance for.

        Returns:
            The total credit balance available at the given timestamp.


        add_credits(amount=5, effective_at=15, expires_at=23) # Credit Block A
        deduct_credits(amount=4, effective_at=17)
        get_balance_at(timestamp=20) # Returns: 1
        """

        # Ensure our list of `activeBlocks` is _mutable_ so that we can track
        # changes to it below to calculate the credit balance.
        active_blocks: list[CreditBlock] = []
        for block in self._credit_blocks:
            block_copy = copy.copy(block)
            
            active_blocks.append(block_copy)

        print("active blocks before sort:", active_blocks)        
        active_blocks = sorted(active_blocks, key=lambda block: block.expires_at)
        print("active blocks after sort:", active_blocks)

        # Filter for deductions that are active at the given timestamp
        effective_deductions: list[Deduction] = []
        for deduction in self._deductions:
            if deduction.effective_at < timestamp:
                effective_deductions.append(deduction)

        print("effective_deductions", effective_deductions)
        # Process deductions that occurred up to the given timestamp.
        for deduction in effective_deductions:
            # Track the amount deducted thus far. Since we may deduct across
            # multiple credit blocks, we need to track the cumulative amount.
            deducted_so_far = 0
            print("active deduction:", deduction)
            # Find the first available block to deduct from.
            for block in active_blocks:

                if deduction.effective_at < block.effective_at and \
                deduction.effective_at > block.expires_at:
                    continue
                    

                # Skip used blocks
                if block.amount <= 0:
                    continue

                to_deduct = deduction.amount - deducted_so_far
                amount_to_take = min(block.amount, to_deduct)


                self.print_state()
                block.amount -= amount_to_take # TODO check this calc.
                deducted_so_far += amount_to_take

                # If we've deducted everything, we can skip
                if deducted_so_far == deduction.amount:
                    break

            if deducted_so_far == deduction.amount:
                continue

        # Calculate the final balance from the modified blocks.
        total_balance = 0
        for block in active_blocks:
            if block.effective_at <= timestamp and timestamp < block.expires_at:
                total_balance += block.amount

        return total_balance
