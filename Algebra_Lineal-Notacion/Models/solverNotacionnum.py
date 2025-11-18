
def decompose_base10(num_str):
    """
    Descompone un número en base 10 usando potencias de 10,
    mostrando multiplicación de cada cifra y suma final.
    """
    try:
        num = int(num_str)
        if num < 0:
            raise ValueError("Número debe ser positivo.")
    except ValueError:
        raise ValueError("Ingresa un número entero positivo válido.")
    
    digits = [int(d) for d in str(num)]
    n = len(digits)

    # Construir términos de la forma: "8 × 10^4"
    terms = []
    for i, digit in enumerate(digits):
        power = n - 1 - i
        terms.append(f"{digit} × 10^{power}")
    
    decomposition = " + ".join(terms)

    # Suma final mostrando el número original
    sum_final = " + ".join([f"{digit * (10**(n - 1 - i))}" for i, digit in enumerate(digits)])

    # Concatenar todo en el formato pedido
    result_text = f"{num} = {decomposition}\n\nSuma final: {sum_final} = {num}"
    return result_text


def decompose_base2(binary_str):
    """
    Descompone un número binario usando potencias de 2,
    mostrando multiplicación de cada dígito y suma final en base 10.
    """
    try:
        binary = binary_str.strip()
        if not all(c in '01' for c in binary) or not binary:
            raise ValueError("Debe ser un número binario válido (solo 0s y 1s).")
        num_decimal = int(binary, 2)
    except ValueError as e:
        raise ValueError(str(e))
    
    digits = [int(d) for d in binary]
    n = len(digits)

    # Construir términos: "1 × 2^4"
    terms = []
    for i, digit in enumerate(digits):
        power = n - 1 - i
        terms.append(f"{digit} × 2^{power}")

    decomposition = " + ".join(terms)

    # Suma final: multiplicando cada término
    sum_final_terms = [str(digit * (2**(n - 1 - i))) for i, digit in enumerate(digits)]
    sum_final_str = " + ".join(sum_final_terms)

    result_text = f"{binary} = {decomposition}\n\nSuma final: {sum_final_str} = {num_decimal} "
    return result_text
