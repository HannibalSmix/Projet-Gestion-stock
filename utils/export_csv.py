import csv
from sqlalchemy.orm import Session
from crud.products_crud import get_all_products, get_product
from crud.warehouse_crud import get_all_warehouses, get_warehouse
from crud.receipt_crud import get_all_receipts, get_receipt
from crud.supplier_crud import get_all_suppliers, get_supplier
from crud.receiptline_crud import get_all_receiptlines
from crud.stockmove_crud import get_all_stock_moves
from crud.transfert_crud import get_all_transferts, get_transfert
from crud.transfertline_crud import get_all_transfert_line


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


def export_products_to_csv(session: Session, filepath: str = "exports/products.csv"):

    products = get_all_products(session)

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # En-têtes
        writer.writerow(["id", "name", "sku", "active"])

        # Données
        for product in products:
            writer.writerow([product.id, product.name, product.sku, product.active])

    print(f"{len(products)} produits exportés dans {filepath}")


def export_warehouse_to_csv(session: Session, filepath: str = "exports/warehouses.csv"):

    warehouses = get_all_warehouses(session)

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # En-têtes
        writer.writerow(["id", "name", "location"])

        # Données
        for warehouse in warehouses:
            writer.writerow([warehouse.id, warehouse.name, warehouse.location])

    print(f"{len(warehouses)} warehouse exportés dans {filepath}")


def export_receipt_to_csv(session: Session, filepath: str = "exports/receipts.csv"):

    receipts = get_all_receipts(session)

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # En-têtes
        writer.writerow(["id", "supplier", "warehouse", "status", "created_at"])

        # Données
        for receipt in receipts:
            supplier = get_supplier(session, receipt.supplier_id)
            warehouse = get_warehouse(session, receipt.warehouse_id)
            writer.writerow([receipt.id, supplier.name, warehouse.name, receipt.status, receipt.created_at.strftime("%d/%m/%Y %H:%M:%S")])
# get_lines_by_receipt
    print(f"{len(receipts)} receipt exportés dans {filepath}")


def export_receiptline_to_csv(session: Session, filepath: str = "exports/receiptlines.csv"):

    receiptlines = get_all_receiptlines(session)

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # En-têtes
        writer.writerow(["id", "receipt supplier", "receipt warehouse", "product", "quantity"])

        # Données
        for receiptline in receiptlines:
            receipt = get_receipt(session, receiptline.receipt_id)
            supplier = get_supplier(session, receipt.supplier_id)
            warehouse = get_warehouse(session, receipt.warehouse_id)
            product = get_product(session, receiptline.product_id)
            writer.writerow([receiptline.id, supplier.name, warehouse.name, product.name, receiptline.quantity])

    print(f"{len(receiptlines)} receiptlines exportés dans {filepath}")


def export_stockmove_to_csv(session: Session, filepath: str = "exports/stockmoves.csv"):

    stockmoves = get_all_stock_moves(session)

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # En-têtes
        writer.writerow(["id", "product", "warehouse source", "warehouse destination", "type", "status", "created_at"])

        # Données
        for stockmove in stockmoves:
            product = get_product(session, stockmove.product_id)
            warehouse_source = get_warehouse(session, stockmove.source_warehouse_id)
            warehouse_dest = get_warehouse(session, stockmove.source_warehouse_id)

            writer.writerow([stockmove.id, product.name, warehouse_source.name, warehouse_dest.name, stockmove.type, stockmove.status, stockmove.created_at.strftime("%d/%m/%Y %H:%M:%S")])

    print(f"{len(stockmoves)} stock moves exportés dans {filepath}")


def export_transfert_to_csv(session: Session, filepath: str = "exports/transferts.csv"):

    transferts = get_all_transferts(session)

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # En-têtes
        writer.writerow(["id", "warehouse source", "warehouse destination", "status", "created_at"])

        # Données
        for transfert in transferts:
            warehouse_s = get_warehouse(session, transfert.source_warehouse_id)
            warehouse_d = get_warehouse(session, transfert.destination_warehouse_id)
            writer.writerow([transfert.id, warehouse_s.name, warehouse_d.name, transfert.status, transfert.created_at.strftime("%d/%m/%Y %H:%M:%S")])
# get_lines_by_receipt
    print(f"{len(transferts)} transferts exportés dans {filepath}")


def export_transfertline_to_csv(session: Session, filepath: str = "exports/transfertlines.csv"):

    transfert_lines = get_all_transfert_line(session)

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # En-têtes
        writer.writerow(["id", "transfert id", "product", "quantity", "Warehouse source", "Warehouse destination"])

        # Données
        for transfert_line in transfert_lines:
            transfert = get_transfert(session, transfert_line.transfer_id)
            warehouse_s = get_warehouse(session, transfert.source_warehouse_id)
            warehouse_d = get_warehouse(session, transfert.destination_warehouse_id)
            product = get_product(session, transfert_line.product_id)
            writer.writerow([transfert_line.id, transfert.id, product.name, transfert_line.quantity, warehouse_s.name, warehouse_d.name])

    print(f"{len(transfert_lines)} transfert lines exportés dans {filepath}")

