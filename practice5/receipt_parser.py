import re
import json
import os
from decimal import Decimal, InvalidOperation


def money_to_decimal(value: str) -> Decimal:
    """
    Convert a money string from the receipt into a Decimal.

    Examples:
      "154,00"   -> 154.00
      "1 200,00" -> 1200.00
    """
    value = value.strip()
    value = value.replace("\u00A0", " ").replace(" ", "")  # remove spaces & NBSP
    value = value.replace(",", ".")  # comma -> dot

    try:
        return Decimal(value)
    except InvalidOperation:
        return Decimal("0")


def parse_receipt(text: str) -> dict:
    # -------------------------
    # Extract date and time
    # -------------------------
    dt_match = re.search(
        r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})",
        text
    )
    date_str = dt_match.group(1) if dt_match else None
    time_str = dt_match.group(2) if dt_match else None

    # -------------------------
    # Extract payment method and paid amount
    # -------------------------
    pay_match = re.search(
        r"(Банковская карта|Наличные)\s*:\s*\n\s*([\d\s]+,\d{2})",
        text
    )
    payment_method = pay_match.group(1) if pay_match else None
    paid_amount = money_to_decimal(pay_match.group(2)) if pay_match else None

    # -------------------------
    # Extract total amount
    # -------------------------
    total_match = re.search(
        r"ИТОГО\s*:\s*\n\s*([\d\s]+,\d{2})",
        text,
        flags=re.IGNORECASE
    )
    total_amount = money_to_decimal(total_match.group(1)) if total_match else None

    # -------------------------
    # Extract ALL prices (format-only)
    # -------------------------
    all_prices_str = re.findall(r"\b\d[\d\s]*,\d{2}\b", text)
    all_prices = [float(money_to_decimal(x)) for x in all_prices_str]

    # -------------------------
    # Extract items (products)
    # -------------------------
    item_pattern = re.compile(
        r"(?m)^\s*(\d+)\.\s*\n"                    # item number line "1."
        r"(.+?)\n"                                # product name (next line)
        r"(\d+,\d{3})\s*x\s*([\d\s]+,\d{2})\s*\n"  # quantity and unit price
        r"([\d\s]+,\d{2})\s*$"                    # line total
    )

    items = []
    product_names = []

    for m in item_pattern.finditer(text):
        item_no = int(m.group(1))
        name = m.group(2).strip()

        qty = Decimal(m.group(3).replace(",", "."))  # "2,000" -> 2.000
        unit_price = money_to_decimal(m.group(4))
        line_total = money_to_decimal(m.group(5))

        product_names.append(name)
        items.append({
            "no": item_no,
            "name": name,
            "qty": float(qty),
            "unit_price": float(unit_price),
            "line_total": float(line_total),
        })

    # -------------------------
    # Calculate sum of items
    # -------------------------
    items_sum = sum(Decimal(str(it["line_total"])) for it in items) if items else Decimal("0")

    # -------------------------
    # Optional header data
    # -------------------------
    branch_match = re.search(r"Филиал\s+(.+)", text)
    bin_match = re.search(r"\bБИН\s+(\d+)\b", text)
    receipt_no_match = re.search(r"Чек\s*№\s*(\d+)", text)

    branch = branch_match.group(1).strip() if branch_match else None
    bin_number = bin_match.group(1) if bin_match else None
    receipt_no = receipt_no_match.group(1) if receipt_no_match else None

    # -------------------------
    # Build result dictionary
    # -------------------------
    result = {
        "branch": branch,
        "bin": bin_number,
        "receipt_no": receipt_no,

        "date": date_str,
        "time": time_str,

        "payment_method": payment_method,
        "paid_amount": float(paid_amount) if paid_amount is not None else None,

        "total_amount": float(total_amount) if total_amount is not None else None,
        "items_sum_calculated": float(items_sum),

        "product_names": product_names,
        "items": items,

        "all_prices": all_prices,
    }

    # Consistency check: does items_sum equal printed total?
    if total_amount is not None:
        result["total_matches_items_sum"] = (items_sum == total_amount)

    return result


def main():
    """
    Entry point:
    - Read raw.txt
    - Parse it
    - Print JSON
    """

    # IMPORTANT FIX:
    # Read raw.txt relative to the script file, not the current working directory.
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "raw.txt")

    with open(file_path, "r", encoding="utf-8") as f:
        receipt_text = f.read()

    parsed = parse_receipt(receipt_text)
    print(json.dumps(parsed, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()