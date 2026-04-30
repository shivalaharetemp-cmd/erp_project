# seed_data.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp.settings')
django.setup()

from company.models import Company
from masters.models import MasterType, Master
from accounts.models import MasterGroup, Ledger
from logistics.models import Vehicle

def seed():
    # Companies
    c1 = Company.objects.create(name='PARIJAT MINERALS PRIVATE LIMITED', gst_number='22AAMCP8719N1ZS', address='2nd Floor, Office No 3 Shrishti Palazo, Avanti Vihar Road Raipur 492001')
    c2 = Company.objects.create(name='BHARAT TRADES', gst_number='27AAIFB2896F1Z9', address='A-3/42 VRINDAVAN APARTMENTS CIVIL LINES NAGPUR')
    c3 = Company.objects.create(name='BHARAT TRADES', gst_number='22AAIFB2896F2ZI', address='128 129 130 BIRKONI INDUSTRIAL AREA DIST MAHASAMUND BIRKONI')

    # Master Types
    supply_type = MasterType.objects.create(name='Supply Type', code='SUPPLY_TYPE')
    sub_supply_type = MasterType.objects.create(name='Sub Supply Type', code='SUB_SUPPLY_TYPE')
    doc_type = MasterType.objects.create(name='Document Type', code='DOCUMENT_TYPE')
    trans_mode = MasterType.objects.create(name='Transportation Mode', code='TRANSPORTATION_MODE')
    consignment_status = MasterType.objects.create(name='Consignment Status', code='CONSIGNMENT_STATUS')
    vehicle_type = MasterType.objects.create(name='Vehicle Type', code='VEHICLE_TYPE')
    transaction_type = MasterType.objects.create(name='Transaction Type', code='TRANSACTION_TYPE')
    unit_type = MasterType.objects.create(name='Unit', code='UNIT')

    # Masters
    Master.objects.create(type=supply_type, code='SUP_GOODS', name='Supply of Goods')
    Master.objects.create(type=supply_type, code='SUP_SERVICES', name='Supply of Services')
    Master.objects.create(type=sub_supply_type, code='SUB_SUP_MAIN', name='Main Supply')
    Master.objects.create(type=doc_type, code='DOC_INVOICE', name='Tax Invoice')
    Master.objects.create(type=doc_type, code='DOC_BILL', name='Bill of Supply')
    Master.objects.create(type=trans_mode, code='TRANS_ROAD', name='Road')
    Master.objects.create(type=trans_mode, code='TRANS_RAIL', name='Rail')
    Master.objects.create(type=consignment_status, code='CONS_IN_TRANSIT', name='In Transit')
    Master.objects.create(type=consignment_status, code='CONS_DELIVERED', name='Delivered')
    Master.objects.create(type=vehicle_type, code='VEH_TRUCK', name='Truck')
    Master.objects.create(type=vehicle_type, code='VEH_TRAILER', name='Trailer')
    Master.objects.create(type=transaction_type, code='TXN_SALE', name='Sale')
    Master.objects.create(type=transaction_type, code='TXN_PURCHASE', name='Purchase')
    Master.objects.create(type=unit_type, code='UNIT_PCS', name='Pieces')
    Master.objects.create(type=unit_type, code='UNIT_KG', name='Kilograms')

    # Master Groups
    assets = MasterGroup.objects.create(name='Assets', type='ASSET')
    liabilities = MasterGroup.objects.create(name='Liabilities', type='LIABILITY')
    income = MasterGroup.objects.create(name='Income', type='INCOME')
    expenses = MasterGroup.objects.create(name='Expenses', type='EXPENSE')

    MasterGroup.objects.create(name='Current Assets', parent=assets, type='ASSET')
    MasterGroup.objects.create(name='Fixed Assets', parent=assets, type='ASSET')
    MasterGroup.objects.create(name='Current Liabilities', parent=liabilities, type='LIABILITY')
    MasterGroup.objects.create(name='Direct Income', parent=income, type='INCOME')
    MasterGroup.objects.create(name='Direct Expenses', parent=expenses, type='EXPENSE')

    # Ledgers
    sales_ledger = Ledger.objects.create(company=c1, name='Sales', group=MasterGroup.objects.get(name='Direct Income'))
    purchase_ledger = Ledger.objects.create(company=c1, name='Purchases', group=MasterGroup.objects.get(name='Direct Expenses'))
    cash_ledger = Ledger.objects.create(company=c1, name='Cash', group=MasterGroup.objects.get(name='Current Assets'))

    Ledger.objects.create(company=c2, name='Sales', group=MasterGroup.objects.get(name='Direct Income'))
    Ledger.objects.create(company=c2, name='Purchases', group=MasterGroup.objects.get(name='Direct Expenses'))

    # Vehicles
    Vehicle.objects.create(vehicle_number='MH12AB1234', vehicle_type=Master.objects.get(code='VEH_TRUCK'))
    Vehicle.objects.create(vehicle_number='KA05CD5678', vehicle_type=Master.objects.get(code='VEH_TRAILER'))

    print("Seed data created successfully!")

if __name__ == '__main__':
    seed()