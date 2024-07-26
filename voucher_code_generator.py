#Author: Visahl Samson David Selvam

import secrets
import string
import csv
import pandas as pd

def generate_voucher_code(start_letters, num_vouchers):
    voucher_chars = string.ascii_uppercase.replace('I', '').replace('J', '').replace('O', '')  # Remove 'I' and 'J' from the characters set
    vouchers = []
    for _ in range(num_vouchers):
        random_chars = ''.join(secrets.choice(voucher_chars) for _ in range(len(start_letters)))
        random_nums = ''.join(secrets.choice(string.digits) for _ in range(2))
        random_symbols = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(2))
        code = f"VS10{start_letters}{random_symbols}{random_nums}{random_chars}{random_chars}{random_nums}" #feel free to modify VS10 to your desired characters
        vouchers.append(code)
    return vouchers

def save_voucher_codes_to_csv(filename, vouchers, max_per_sheet=1000):
    num_sheets = (len(vouchers) - 1) // max_per_sheet + 1
    df_list = [vouchers[i:i+max_per_sheet] for i in range(0, len(vouchers), max_per_sheet)]

    with pd.ExcelWriter(filename, engine='openpyxl') as writer:

        for i, df in enumerate(df_list):
            df = pd.DataFrame(df, columns=['Voucher Code'])
            sheet_name = f'Sheet{i + 1}'
            df.to_excel(writer, sheet_name=sheet_name, index=False)

if __name__ == "__main__":
    try:
        num_vouchers = int(input("Enter the number of voucher codes to generate: "))
        start_letters = input("Enter the start letters (up to triple alphabetical): ").upper()

        if not start_letters.isalpha() or len(start_letters) > 5:
            print("Start letters must be up to triple alphabetical.")
        elif num_vouchers <= 0:
            print("Number of vouchers should be a positive integer.")
        else:
            vouchers = generate_voucher_code(start_letters, num_vouchers)
            for voucher in vouchers:
                print(voucher)

            save_to_csv = input("Do you want to save the generated codes to a CSV file? (y/n): ").lower()
            if save_to_csv == 'y':
                file_name = input("Enter the filename to save (e.g., vouchers.xlsx): ")
                save_voucher_codes_to_csv(file_name, vouchers)
                print(f"Voucher codes saved to {file_name}")

    except ValueError:
        print("Invalid input. Please enter valid start letters and a number of vouchers.")
