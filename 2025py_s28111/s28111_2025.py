# CEL PROGRAMU:
# Program generuje losową sekwencję DNA w formacie FASTA.
# Pobiera dane od użytkownika, dodaje imię do sekwencji (nie wpływając na statystyki),
# zapisuje dane do pliku .fasta i wyświetla statystyki nukleotydów.

import random  # Import modułu do generowania liczb losowych

# Funkcja generująca losową sekwencję DNA
def generate_dna_sequence(length):
    # Zwraca łańcuch długości 'length' składający się z losowych liter A, C, G, T
    return ''.join(random.choices('ACGT', k=length))

# Funkcja wstawiająca imię w losowym miejscu sekwencji
# Imię nie wpływa na statystyki i nie jest liczone do długości sekwencji
def insert_name(sequence, name):
    position = random.randint(0, len(sequence))  # Losowa pozycja wstawienia imienia
    return sequence[:position] + name + sequence[position:]  # Zwraca nową sekwencję

# Funkcja licząca statystyki sekwencji DNA
def calculate_stats(sequence):
    counts = {nuc: sequence.count(nuc) for nuc in 'ACGT'}  # Zlicza wystąpienia nukleotydów
    total = sum(counts.values())  # Całkowita liczba nukleotydów (powinna równać się długości)
    percentages = {nuc: round((counts[nuc] / total) * 100, 1) for nuc in counts}  # Procentowa zawartość
    cg = counts['C'] + counts['G']  # Liczba C i G
    at = counts['A'] + counts['T']  # Liczba A i T
    cg_at_ratio = round((cg / at) * 100, 1) if at != 0 else 0  # Stosunek CG do AT
    return percentages, cg_at_ratio

# ==========================
# POBIERANIE DANYCH OD UŻYTKOWNIKA Z WALIDACJĄ

# ORIGINAL:
# length = int(input("Podaj długość sekwencji: "))

# MODIFIED (dodanie walidacji długości – użytkownik musi podać dodatnią liczbę całkowitą):
while True:
    try:
        length = int(input("Podaj długość sekwencji: "))
        if length > 0:
            break
        else:
            print("Długość musi być większa od zera.")
    except ValueError:
        print("Podaj poprawną liczbę całkowitą.")

seq_id = input("Podaj ID sekwencji: ")  # ID sekwencji do użycia w pliku i nagłówku FASTA
description = input("Podaj opis sekwencji: ")  # Opis do nagłówka FASTA
name = input("Podaj imię: ")  # Imię użytkownika do wstawienia w sekwencji

# ==========================
# GENEROWANIE SEKWENCJI I STATYSTYK

dna_sequence = generate_dna_sequence(length)  # Generowanie sekwencji bez imienia
dna_with_name = insert_name(dna_sequence, name)  # Dodanie imienia w losowym miejscu
stats, cg_at_ratio = calculate_stats(dna_sequence)  # Obliczanie statystyk dla oryginalnej sekwencji

# ==========================
# ZAPIS DO PLIKU FASTA

filename = f"{seq_id}.fasta"  # Nazwa pliku na podstawie ID

with open(filename, 'w') as f:
    f.write(f">{seq_id} {description}\n")  # Nagłówek FASTA

    # ORIGINAL:
    # f.write(dna_with_name + "\n")

    # MODIFIED (złamanie sekwencji co 60 znaków dla zgodności z FASTA):
    for i in range(0, len(dna_with_name), 60):
        f.write(dna_with_name[i:i+60] + "\n")

    # MODIFIED (zapis statystyk jako komentarze FASTA z prefiksem ;)
    f.write(f"; A: {stats['A']}%\n")
    f.write(f"; C: {stats['C']}%\n")
    f.write(f"; G: {stats['G']}%\n")
    f.write(f"; T: {stats['T']}%\n")
    f.write(f"; %CG: {cg_at_ratio}\n")

# ==========================
# WYŚWIETLENIE STATYSTYK NA EKRANIE

print(f"Sekwencja została zapisana do pliku {filename}")
print("Statystyki sekwencji:")
for nuc in 'ACGT':
    print(f"{nuc}: {stats[nuc]}%")
print(f"%CG: {cg_at_ratio}")
