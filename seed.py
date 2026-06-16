from db.database import Base, engine
from sqlalchemy.orm import sessionmaker

from crud.warehouse_crud import create_warehouse
from crud.supplier_crud import create_supplier
from crud.products_crud import create_product
from crud.receipt_crud import create_receipt
from crud.receiptline_crud import create_receipt_line
from crud.transfert_crud import create_transfert
from crud.transfertline_crud import create_transfert_line

from models.receipt import Status as ReceiptStatus
from models.transfert import Status as TransfertStatus

from services.receipt_services import validate_receipt
from services.transfert_services import validate_transfert

from datetime import datetime


def seed():

    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)

    with SessionLocal() as session:

        # ── 1. WAREHOUSES ────────────────────────────────────────────────
        print("Création des entrepôts...")
        wh1 = create_warehouse(session, name="Entrepôt Paris",     location="12 rue de la Logistique, Paris")
        wh2 = create_warehouse(session, name="Entrepôt Lyon",      location="8 avenue Industrielle, Lyon")
        wh3 = create_warehouse(session, name="Entrepôt Marseille", location="45 boulevard du Port, Marseille")
        wh4 = create_warehouse(session, name="Entrepôt Lille",     location="3 rue des Flandres, Lille")

        # ── 2. SUPPLIERS ─────────────────────────────────────────────────
        print("Création des fournisseurs...")
        sup1 = create_supplier(session, name="Acier Pro",         email="contact@acierpro.fr")
        sup2 = create_supplier(session, name="MetalTech",         email="commandes@metaltech.fr")
        sup3 = create_supplier(session, name="Visserie Dupont",   email="info@visserie-dupont.fr")
        sup4 = create_supplier(session, name="Industrie Leblanc", email="ventes@industrie-leblanc.fr")
        sup5 = create_supplier(session, name="Fournitures BCG",   email="bcg@fournitures.fr")

        # ── 3. PRODUCTS ──────────────────────────────────────────────────
        print("Création des produits...")
        p1  = create_product(session, name="Vis M6 x 20mm",          sku="VIS-M6-20")
        p2  = create_product(session, name="Vis M8 x 30mm",          sku="VIS-M8-30")
        p3  = create_product(session, name="Boulon M10",             sku="BOU-M10")
        p4  = create_product(session, name="Écrou M6",               sku="ECR-M6")
        p5  = create_product(session, name="Écrou M8",               sku="ECR-M8")
        p6  = create_product(session, name="Rondelle M6",            sku="RON-M6")
        p7  = create_product(session, name="Rondelle M10",           sku="RON-M10")
        p8  = create_product(session, name="Cheville 8mm",           sku="CHE-8MM")
        p9  = create_product(session, name="Cheville 10mm",          sku="CHE-10MM")
        p10 = create_product(session, name="Tige filetée M12",       sku="TIG-M12")
        p11 = create_product(session, name="Plaque acier 2mm",       sku="PLA-AC-2")
        p12 = create_product(session, name="Plaque acier 5mm",       sku="PLA-AC-5")
        p13 = create_product(session, name="Tube carré 20x20",       sku="TUB-CA-20")
        p14 = create_product(session, name="Tube rond 25mm",         sku="TUB-RO-25")
        p15 = create_product(session, name="Profilé en U 30mm",      sku="PRO-U-30")
        p16 = create_product(session, name="Ressort de compression",  sku="RES-COMP")
        p17 = create_product(session, name="Goupille 4mm",           sku="GOP-4MM")
        p18 = create_product(session, name="Clip de fixation",       sku="CLI-FIX")
        p19 = create_product(session, name="Joint torique 10mm",     sku="JOI-TO-10")
        p20 = create_product(session, name="Câble acier 3mm",        sku="CAB-AC-3")

        # ── 4. RECEIPTS + LINES ──────────────────────────────────────────
        print("Création des bons de réception...")

        # Receipt 1 — Acier Pro → Paris
        r1 = create_receipt(session,
            supplier_id=sup1.id,
            warehouse_id=wh1.id,
            status=ReceiptStatus.DRAFT
        )
        create_receipt_line(session, receipt_id=r1.id, product_id=p1.id, quantity=500)
        create_receipt_line(session, receipt_id=r1.id, product_id=p2.id, quantity=300)
        create_receipt_line(session, receipt_id=r1.id, product_id=p3.id, quantity=200)
        validate_receipt(session, r1.id)

        # Receipt 2 — MetalTech → Lyon
        r2 = create_receipt(session,
            supplier_id=sup2.id,
            warehouse_id=wh2.id,
            status=ReceiptStatus.DRAFT
        )
        create_receipt_line(session, receipt_id=r2.id, product_id=p11.id, quantity=100)
        create_receipt_line(session, receipt_id=r2.id, product_id=p12.id, quantity=80)
        create_receipt_line(session, receipt_id=r2.id, product_id=p13.id, quantity=60)
        validate_receipt(session, r2.id)

        # Receipt 3 — Visserie Dupont → Marseille
        r3 = create_receipt(session,
            supplier_id=sup3.id,
            warehouse_id=wh3.id,
            status=ReceiptStatus.DRAFT
        )
        create_receipt_line(session, receipt_id=r3.id, product_id=p4.id, quantity=400)
        create_receipt_line(session, receipt_id=r3.id, product_id=p5.id, quantity=400)
        create_receipt_line(session, receipt_id=r3.id, product_id=p6.id, quantity=600)
        create_receipt_line(session, receipt_id=r3.id, product_id=p7.id, quantity=600)
        validate_receipt(session, r3.id)

        # Receipt 4 — Industrie Leblanc → Lille
        r4 = create_receipt(session,
            supplier_id=sup4.id,
            warehouse_id=wh4.id,
            status=ReceiptStatus.DRAFT
        )
        create_receipt_line(session, receipt_id=r4.id, product_id=p14.id, quantity=50)
        create_receipt_line(session, receipt_id=r4.id, product_id=p15.id, quantity=50)
        create_receipt_line(session, receipt_id=r4.id, product_id=p16.id, quantity=200)
        validate_receipt(session, r4.id)

        # Receipt 5 — Fournitures BCG → Paris (laissé en DRAFT)
        r5 = create_receipt(session,
            supplier_id=sup5.id,
            warehouse_id=wh1.id,
            status=ReceiptStatus.DRAFT
        )
        create_receipt_line(session, receipt_id=r5.id, product_id=p17.id, quantity=300)
        create_receipt_line(session, receipt_id=r5.id, product_id=p18.id, quantity=300)
        create_receipt_line(session, receipt_id=r5.id, product_id=p19.id, quantity=150)
        create_receipt_line(session, receipt_id=r5.id, product_id=p20.id, quantity=100)

        # ── 5. TRANSFERTS + LINES ────────────────────────────────────────
        print("Création des transferts...")

        # Transfert 1 — Paris → Lyon (vis et boulons)
        t1 = create_transfert(session,
            source_warehouse_id=wh1.id,
            destination_warehouse_id=wh2.id,
            status=TransfertStatus.DRAFT
        )
        create_transfert_line(session, transfer_id=t1.id, product_id=p1.id, quantity=100)
        create_transfert_line(session, transfer_id=t1.id, product_id=p2.id, quantity=50)
        validate_transfert(session, t1.id)

        # Transfert 2 — Lyon → Marseille (plaques acier)
        t2 = create_transfert(session,
            source_warehouse_id=wh2.id,
            destination_warehouse_id=wh3.id,
            status=TransfertStatus.DRAFT
        )
        create_transfert_line(session, transfer_id=t2.id, product_id=p11.id, quantity=30)
        create_transfert_line(session, transfer_id=t2.id, product_id=p12.id, quantity=20)
        validate_transfert(session, t2.id)

        # Transfert 3 — Marseille → Lille (écrous et rondelles)
        t3 = create_transfert(session,
            source_warehouse_id=wh3.id,
            destination_warehouse_id=wh4.id,
            status=TransfertStatus.DRAFT
        )
        create_transfert_line(session, transfer_id=t3.id, product_id=p4.id, quantity=100)
        create_transfert_line(session, transfer_id=t3.id, product_id=p6.id, quantity=150)
        validate_transfert(session, t3.id)

        # Transfert 4 — Paris → Lille (laissé en DRAFT)
        t4 = create_transfert(session,
            source_warehouse_id=wh1.id,
            destination_warehouse_id=wh4.id,
            status=TransfertStatus.DRAFT
        )
        create_transfert_line(session, transfer_id=t4.id, product_id=p3.id, quantity=50)
        create_transfert_line(session, transfer_id=t4.id, product_id=p8.id, quantity=80)

        print("Seed terminé avec succès !")


if __name__ == "__main__":
    seed()