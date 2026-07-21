# expense_tracker.py
# Project 2 — Accumulator Pattern + Defensive Coding
#
# This script is intentionally more than "just sum some numbers".
# The point is to show: running state, sentinel exit, type-safe conversion,
# and a clean separation between input-handling, math, and display.


SENTINEL_VALUES = {"quit", "done", "q"}  # any of these exits the loop cleanly


def get_expense_input() -> float | None:
    """
    Prompts the user for a single expense entry.

    Returns:
        float  — the validated expense amount
        None   — signals the caller that the user wants to quit

    Design choice: negative numbers are REJECTED here with a message.
    Rationale: an expense tracker should log money going OUT; if you want
    to handle refunds, a dedicated 'refund' command is cleaner than letting
    negatives silently reduce the total in unexpected ways.
    """
    raw = input("Enter expense amount (or 'quit' to finish): ").strip().lower()

    # Sentinel check — user typed quit/done/q, signal the loop to stop
    if raw in SENTINEL_VALUES:
        return None

    # Type-safety lesson: '100' + '50' = '10050' (string concat — wrong!)
    # float('100') + float('50') = 150.0 (arithmetic — correct!)
    # This is exactly why we convert, not assume.
    try:
        amount = float(raw)
    except ValueError:
        # Non-numeric input like "ten", "abc", "$50" — don't crash, re-prompt
        print("  ✗ Invalid input — please enter a number (e.g. 12.50).\n")
        return get_expense_input()  # recurse to re-prompt cleanly

    # Reject negatives explicitly — see design choice comment above
    if amount < 0:
        print("  ✗ Negative amounts aren't accepted. Log expenses as positive values.\n")
        return get_expense_input()  # re-prompt

    if amount == 0:
        print("  ⚠  Zero entered — skipping (nothing to log).\n")
        return get_expense_input()  # re-prompt

    return amount


def collect_expenses() -> tuple[list[float], float]:
    """
    Core loop: runs until the user signals exit via a sentinel value.

    The accumulator pattern lives here:
        total starts at 0 BEFORE the loop (outside any iteration)
        each valid entry updates total via +=
        expense_log captures every entry so we have a breakdown, not just a sum

    Returns:
        (expense_log, total) — the list of entries and the final running total
    """
    expense_log: list[float] = []  # storage — bridges Project 1's list skill
    total: float = 0.0             # accumulator — initialized ONCE, outside the loop

    print("\n── Expense Tracker ─────────────────────────────────")
    print("  Enter each expense one at a time.")
    print("  Type 'quit' (or 'done') when you're finished.\n")

    while True:
        amount = get_expense_input()

        if amount is None:
            # Sentinel received — user is done, break cleanly
            break

        # Update running state — this is the accumulator pattern in action
        total += amount          # NOT total = total + str(amount) — always arithmetic
        expense_log.append(amount)

        # Show a live running total after each entry — useful UX, and it
        # demonstrates that 'total' genuinely persists between iterations
        print(f"  ✓ Added ${amount:.2f} | Running total: ${total:.2f}\n")

    return expense_log, total


def display_summary(expense_log: list[float], total: float) -> None:
    """
    Prints the final summary: count of entries + formatted total.
    Kept separate from logic so output format can change without touching math.
    """
    count = len(expense_log)

    print("\n── Summary ─────────────────────────────────────────")

    if count == 0:
        print("  No expenses were logged.")
        return

    # Breakdown — each entry with its index (1-based for readability)
    for i, amount in enumerate(expense_log, start=1):
        print(f"  {i:>3}. ${amount:.2f}")

    print("  " + "─" * 30)
    print(f"  Total expenses logged : {count}")
    print(f"  Final Total           : ${total:.2f}")
    print("────────────────────────────────────────────────────\n")


def main() -> None:
    """
    Entry point — owns the mutable state (expense_log, total) and passes
    it between functions. No global mutable state anywhere in this file.
    """
    expense_log, total = collect_expenses()
    display_summary(expense_log, total)


if __name__ == "__main__":
    # Standard Python guard — ensures main() only runs when this file is
    # executed directly, not when it's imported as a module elsewhere.
    main()
