# from db.database import Base, engine
# from sqlalchemy.orm import sessionmaker

# # Base.metadata.create_all(engine)

# SessionLocal = sessionmaker(bind=engine)

# with SessionLocal() as session:
#     print('hello')

from db.database import engine
from sqlalchemy.orm import sessionmaker

from crud.warehouse_crud import get_all_warehouses
from crud.supplier_crud import get_all_suppliers
from crud.products_crud import get_all_products, create_product
from crud.receipt_crud import create_receipt, get_all_receipts
from crud.receiptline_crud import create_receipt_line, get_lines_by_receipt
from crud.transfert_crud import create_transfert, get_all_transferts
from crud.transfertline_crud import create_transfert_line, get_lines_by_transfert
from crud.stocklevel_crud import get_stock_by_warehouse

from models.receipt import Status as ReceiptStatus
from models.transfert import Status as TransfertStatus

from services.receipt_services import validate_receipt
from services.transfert_services import validate_transfert

SessionLocal = sessionmaker(bind=engine)


def afficher_titre(titre: str):
    print()
    print("=" * 60)
    print(titre)
    print("=" * 60)


def demander_int(message: str) -> int:
    while True:
        valeur = input(message)
        if valeur.isdigit():
            return int(valeur)
        print("Merci d'entrer un nombre entier valide.")


# ── ACTIONS DU MENU ──────────────────────────────────────────────────────

def action_lister_entrepots(session):
    afficher_titre("ENTREPÔTS")
    for wh in get_all_warehouses(session):
        print(f"  [{wh.id}] {wh.name} — {wh.location}")


def action_lister_produits(session):
    afficher_titre("PRODUITS")
    for p in get_all_products(session):
        statut = "actif" if p.active else "inactif"
        print(f"  [{p.id}] {p.name} (SKU: {p.sku}) — {statut}")


def action_ajouter_produit(session):
    afficher_titre("AJOUTER UN PRODUIT")
    name = input("Nom du produit : ")
    sku = input("SKU du produit : ")
    product = create_product(session, name=name, sku=sku)
    print(f"\nProduit créé : [{product.id}] {product.name} (SKU: {product.sku})")


def action_voir_stock(session):
    afficher_titre("NIVEAUX DE STOCK PAR ENTREPÔT")
    warehouses = get_all_warehouses(session)
    for wh in warehouses:
        print(f"\n  {wh.name} :")
        stock_levels = get_stock_by_warehouse(session, wh.id)
        if not stock_levels:
            print("      (aucun stock)")
        for sl in stock_levels:
            print(f"      • produit {sl.product_id} — quantité: {sl.quantity}")


def action_nouvelle_reception(session):
    afficher_titre("NOUVELLE RÉCEPTION")

    action_lister_entrepots(session)
    warehouse_id = demander_int("\nID de l'entrepôt de réception : ")

    print("\nFournisseurs disponibles :")
    for sup in get_all_suppliers(session):
        print(f"  [{sup.id}] {sup.name}")
    supplier_id = demander_int("\nID du fournisseur : ")

    receipt = create_receipt(
        session,
        supplier_id=supplier_id,
        warehouse_id=warehouse_id,
        status=ReceiptStatus.DRAFT
    )
    print(f"\nReceipt #{receipt.id} créé en DRAFT.")

    while True:
        action_lister_produits(session)
        product_id = demander_int("\nID du produit à ajouter (0 pour terminer) : ")
        if product_id == 0:
            break
        quantity = demander_int("Quantité reçue : ")
        create_receipt_line(session, receipt_id=receipt.id, product_id=product_id, quantity=quantity)
        print("Ligne ajoutée.")

    confirmer = input("\nValider la réception maintenant ? (o/n) : ")
    if confirmer.lower() == "o":
        validate_receipt(session, receipt.id)
    else:
        print("Réception laissée en DRAFT.")


def action_nouveau_transfert(session):
    afficher_titre("NOUVEAU TRANSFERT")

    action_lister_entrepots(session)
    source_id = demander_int("\nID de l'entrepôt source : ")
    destination_id = demander_int("ID de l'entrepôt destination : ")

    transfert = create_transfert(
        session,
        source_warehouse_id=source_id,
        destination_warehouse_id=destination_id,
        status=TransfertStatus.DRAFT
    )
    print(f"\nTransfert #{transfert.id} créé en DRAFT.")

    while True:
        action_lister_produits(session)
        product_id = demander_int("\nID du produit à transférer (0 pour terminer) : ")
        if product_id == 0:
            break
        quantity = demander_int("Quantité à transférer : ")
        create_transfert_line(session, transfer_id=transfert.id, product_id=product_id, quantity=quantity)
        print("Ligne ajoutée.")

    confirmer = input("\nValider le transfert maintenant ? (o/n) : ")
    if confirmer.lower() == "o":
        validate_transfert(session, transfert.id)
    else:
        print("Transfert laissé en DRAFT.")


def action_historique_receptions(session):
    afficher_titre("HISTORIQUE DES RÉCEPTIONS")
    for r in get_all_receipts(session):
        print(f"\n  Receipt #{r.id} — statut: {r.status.name} "
              f"— fournisseur: {r.supplier_id} — entrepôt: {r.warehouse_id}")
        for line in get_lines_by_receipt(session, r.id):
            print(f"      • produit {line.product_id} — quantité: {line.quantity}")


def action_historique_transferts(session):
    afficher_titre("HISTORIQUE DES TRANSFERTS")
    for t in get_all_transferts(session):
        print(f"\n  Transfert #{t.id} — statut: {t.status.name} "
              f"— source: {t.source_warehouse_id} → destination: {t.destination_warehouse_id}")
        for line in get_lines_by_transfert(session, t.id):
            print(f"      • produit {line.product_id} — quantité: {line.quantity}")


# ── MENU PRINCIPAL ───────────────────────────────────────────────────────

MENU = """
─────────────────────────────────────────
   GESTION DE STOCK — MENU PRINCIPAL
─────────────────────────────────────────
 1. Lister les entrepôts
 2. Lister les produits
 3. Ajouter un produit
 4. Voir les niveaux de stock
 5. Créer une réception
 6. Créer un transfert
 7. Historique des réceptions
 8. Historique des transferts
 0. Quitter
─────────────────────────────────────────
"""


def main():
    with SessionLocal() as session:
        while True:
            print(MENU)
            choix = input("Choix : ")

            if choix == "1":
                action_lister_entrepots(session)
            elif choix == "2":
                action_lister_produits(session)
            elif choix == "3":
                action_ajouter_produit(session)
            elif choix == "4":
                action_voir_stock(session)
            elif choix == "5":
                action_nouvelle_reception(session)
            elif choix == "6":
                action_nouveau_transfert(session)
            elif choix == "7":
                action_historique_receptions(session)
            elif choix == "8":
                action_historique_transferts(session)
            elif choix == "0":
                print("\nAu revoir !")
                break
            else:
                print("\nChoix invalide, réessaie.")


if __name__ == "__main__":
    main()    