# Proces reklamacji

```mermaid


sequenceDiagram
    actor Klient
    participant Sklep as System sklepu
    participant Kurier
    participant Magazyn
    participant RMA as Dział RMA
    participant Serwis
    participant Ksiegowosc as Księgowość

    Klient->>Sklep: Złożenie reklamacji
    Sklep->>Klient: Potwierdzenie przyjęcia reklamacji

    Sklep->>Kurier: Zlecenie odbioru towaru
    Kurier->>Klient: Odbiór reklamowanego towaru
    Kurier->>Magazyn: Dostarczenie towaru

    Magazyn->>RMA: Przekazanie produktu do weryfikacji

    RMA->>RMA: Sprawdzenie towaru

    alt Zwrot środków

        RMA->>Klient: Ustalenie zwrotu środków

        RMA->>Ksiegowosc: Wystawienie FV korekty

        Ksiegowosc->>Klient: Zwrot środków na konto

    else Naprawa towaru

        RMA->>Klient: Ustalenie naprawy

        RMA->>Serwis: Przekazanie towaru do naprawy

        Serwis->>Serwis: Naprawa produktu

        Serwis->>Magazyn: Zwrot naprawionego towaru

        Magazyn->>Kurier: Nadanie przesyłki

        Kurier->>Klient: Dostarczenie naprawionego towaru

    end