import csv
from sqlalchemy.orm import Session
from crud.supplier_crud import get_all_suppliers


def export_suppliers_to_csv(session: Session, filepath: str = "exports/suppliers.csv"):

    suppliers = get_all_suppliers(session)

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # En-têtes
        writer.writerow(["id", "name", "email"])

        # Données
        for supplier in suppliers:
            writer.writerow([supplier.id, supplier.name, supplier.email])

    print(f"{len(suppliers)} fournisseurs exportés dans {filepath}")