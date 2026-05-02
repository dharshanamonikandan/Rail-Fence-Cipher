"""
Rail Fence Cipher - Encryption and Decryption
Network Security Assignment

The Rail Fence cipher is a transposition cipher that writes the plaintext
in a zigzag pattern across 'n' rails, then reads off each row.

Example: "HELLOWORLD" with 3 rails:

  H . . . O . . . D
  . E . L . W . L .
  . . L . . . O . .

Ciphertext: HOD + ELWL + LO => "HODELWLLO"
"""


# ──────────────────────────────────────────────
# ENCRYPTION
# ──────────────────────────────────────────────
def encrypt(text, rails):
    # Create a 2D rail grid filled with empty strings
    rail = [[''] * len(text) for _ in range(rails)]

    row, direction = 0, -1

    for i, ch in enumerate(text):
        rail[row][i] = ch
        # Change direction at top or bottom rail
        if row == 0 or row == rails - 1:
            direction = -direction
        row += direction

    # Read off row by row to form ciphertext
    cipher = ''.join(ch for r in rail for ch in r if ch != '')
    return cipher


# ──────────────────────────────────────────────
# DECRYPTION
# ──────────────────────────────────────────────
def decrypt(cipher, rails):
    n = len(cipher)

    # Mark zigzag positions with '*'
    rail = [[''] * n for _ in range(rails)]
    row, direction = 0, -1

    for i in range(n):
        rail[row][i] = '*'
        if row == 0 or row == rails - 1:
            direction = -direction
        row += direction

    # Fill marked positions with cipher characters row by row
    idx = 0
    for r in range(rails):
        for c in range(n):
            if rail[r][c] == '*':
                rail[r][c] = cipher[idx]
                idx += 1

    # Read back in zigzag order to recover plaintext
    plaintext = []
    row, direction = 0, -1

    for i in range(n):
        plaintext.append(rail[row][i])
        if row == 0 or row == rails - 1:
            direction = -direction
        row += direction

    return ''.join(plaintext)


# ──────────────────────────────────────────────
# VISUALISE THE ZIGZAG PATTERN
# ──────────────────────────────────────────────
def visualize(text, rails):
    rail = [['.' ] * len(text) for _ in range(rails)]

    row, direction = 0, -1

    for i, ch in enumerate(text):
        rail[row][i] = ch
        if row == 0 or row == rails - 1:
            direction = -direction
        row += direction

    print(f"\n  Zigzag Pattern ({rails} rails):\n")
    for r in range(rails):
        print(f"  Rail {r + 1}: {' '.join(rail[r])}")
    print()


# ──────────────────────────────────────────────
# HELPER: Read a valid number of rails
# ──────────────────────────────────────────────
def get_rails(text_len):
    while True:
        try:
            rails = int(input("  Enter number of rails : "))
            if rails < 2:
                print("  [!] Rails must be >= 2. Try again.")
            elif rails >= text_len:
                print(f"  [!] Rails must be less than text length ({text_len}). Try again.")
            else:
                return rails
        except ValueError:
            print("  [!] Please enter a valid integer.")


# ──────────────────────────────────────────────
# HELPER: Yes / No prompt
# ──────────────────────────────────────────────
def ask_yes_no(question):
    while True:
        ans = input(f"{question} (y/n): ").strip().lower()
        if ans == 'y':
            return True
        if ans == 'n':
            return False
        print("  [!] Please enter 'y' or 'n'.")


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────
def main():
    print("╔══════════════════════════════════════╗")
    print("║      Rail Fence Cipher (Python)      ║")
    print("║      Network Security Assignment     ║")
    print("╚══════════════════════════════════════╝")

    # ═══════════════════════════════════════════
    # OUTER LOOP — repeat for new text
    # ═══════════════════════════════════════════
    while True:
        # ── Step 1: Choose operation ──
        print("\n  ┌─────────────────────────────┐")
        print("  │   Choose Operation          │")
        print("  │   1. Encryption             │")
        print("  │   2. Decryption             │")
        print("  └─────────────────────────────┘")

        choice = input("  Enter choice (1 or 2): ").strip()

        if choice not in ('1', '2'):
            print("  [!] Invalid choice. Please enter 1 or 2.")
            continue

        # ─────────────────────────────────────
        # ENCRYPTION PATH
        # ─────────────────────────────────────
        if choice == '1':
            print("\n  --- ENCRYPTION ---")

            # Step 2a: Get plaintext
            plaintext = input("  Enter plaintext (no spaces): ").strip()
            if not plaintext:
                print("  [!] Plaintext cannot be empty.")
                continue

            # Step 3: Get rails
            rails = get_rails(len(plaintext))

            # Step 4: Visualize zigzag
            visualize(plaintext, rails)

            # Step 5: Encrypt and show result
            ciphertext = encrypt(plaintext, rails)
            print(f"  Plaintext  : {plaintext}")
            print(f"  Ciphertext : {ciphertext}")

            # Step 6: Ask if also want to decrypt
            print()
            if ask_yes_no("  Do you also want to decrypt the ciphertext?"):
                print("\n  --- DECRYPTION ---")
                decrypted = decrypt(ciphertext, rails)
                print(f"  Ciphertext : {ciphertext}")
                print(f"  Decrypted  : {decrypted}")

                if plaintext == decrypted:
                    print("  [✓] Decryption successful — matches original plaintext.")
                else:
                    print("  [✗] Decryption FAILED.")

        # ─────────────────────────────────────
        # DECRYPTION PATH
        # ─────────────────────────────────────
        else:
            print("\n  --- DECRYPTION ---")

            # Step 2b: Get ciphertext
            ciphertext = input("  Enter ciphertext (no spaces): ").strip()
            if not ciphertext:
                print("  [!] Ciphertext cannot be empty.")
                continue

            # Step 3: Get rails
            rails = get_rails(len(ciphertext))

            # Step 4: Decrypt and show result
            decrypted = decrypt(ciphertext, rails)
            print(f"  Ciphertext : {ciphertext}")
            print(f"  Decrypted  : {decrypted}")

        print()

        # Step 7: Ask to process another text
        if not ask_yes_no("  Do you want to process another text?"):
            break

    print("\n  Thank you! Exiting Rail Fence Cipher.\n")


if __name__ == "__main__":
    main()