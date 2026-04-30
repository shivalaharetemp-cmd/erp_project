# seed_data.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp.settings')
django.setup()

from company.models import Company
from masters.models import MasterType, Master
from accounts.models import MasterGroup

def seed():
    # ============================================
    # COMPANIES
    # ============================================
    c1 = Company.objects.create(name='PARIJAT MINERALS PRIVATE LIMITED', gst_number='22AAMCP8719N1ZS', address='2nd Floor, Office No 3 Shrishti Palazo, Avanti Vihar Road Raipur 492001')
    c2 = Company.objects.create(name='BHARAT TRADES MH', gst_number='27AAIFB2896F1Z9', address='A-3/42 VRINDAVAN APARTMENTS CIVIL LINES NAGPUR')
    c3 = Company.objects.create(name='BHARAT TRADES CG', gst_number='22AAIFB2896F2ZI', address='128 129 130 BIRKONI INDUSTRIAL AREA DIST MAHASAMUND BIRKONI')

    # ============================================
    # MASTER TYPES - Initial Setup Masters
    # ============================================

    # Supply Related
    supply_type = MasterType.objects.create(name='Supply Type', code='SUPPLY_TYPE')
    sub_supply_type = MasterType.objects.create(name='Sub Supply Type', code='SUB_SUPPLY_TYPE')
    doc_type = MasterType.objects.create(name='Document Type', code='DOCUMENT_TYPE')

    # Transaction & Units
    transaction_type = MasterType.objects.create(name='Transaction Type', code='TRANSACTION_TYPE')
    unit_type = MasterType.objects.create(name='Unit', code='UNIT')

    # Transportation
    trans_mode = MasterType.objects.create(name='Transportation Mode', code='TRANSPORTATION_MODE')
    consignment_status = MasterType.objects.create(name='Consignment Status', code='CONSIGNMENT_STATUS')
    vehicle_type = MasterType.objects.create(name='Vehicle Type', code='VEHICLE_TYPE')

    # ============================================
    # MASTERS - Supply & Transaction Related
    # ============================================

    # Supply Types (GST e-way bill compatible)
    Master.objects.create(type=supply_type, code='B2B', name='Business to Business')
    Master.objects.create(type=supply_type, code='B2C', name='Business to Consumer')
    Master.objects.create(type=supply_type, code='SEZWP', name='SEZ with Payment')
    Master.objects.create(type=supply_type, code='SEZWOP', name='SEZ without Payment')
    Master.objects.create(type=supply_type, code='EXPWP', name='Export with Payment')
    Master.objects.create(type=supply_type, code='EXPWOP', name='Export without Payment')
    Master.objects.create(type=supply_type, code='DEXP', name='Deemed Export')

    # Sub Supply Types
    Master.objects.create(type=sub_supply_type, code='SUPPLY', name='Supply')
    Master.objects.create(type=sub_supply_type, code='IMPORT', name='Import')
    Master.objects.create(type=sub_supply_type, code='EXPORT', name='Export')
    Master.objects.create(type=sub_supply_type, code='JOB_WORK', name='Job Work')
    Master.objects.create(type=sub_supply_type, code='SKD_CKD', name='SKD/CKD')
    Master.objects.create(type=sub_supply_type, code='REPAIR', name='Repair/Maintenance')

    # Document Types
    Master.objects.create(type=doc_type, code='INV', name='Tax Invoice')
    Master.objects.create(type=doc_type, code='BOS', name='Bill of Supply')
    Master.objects.create(type=doc_type, code='BOE', name='Bill of Entry')
    Master.objects.create(type=doc_type, code='CHL', name='Delivery Challan')
    Master.objects.create(type=doc_type, code='CRN', name='Credit Note')
    Master.objects.create(type=doc_type, code='DBN', name='Debit Note')

    # Transaction Types
    Master.objects.create(type=transaction_type, code='SALE', name='Sale')
    Master.objects.create(type=transaction_type, code='PURCHASE', name='Purchase')
    Master.objects.create(type=transaction_type, code='SALE_RET', name='Sales Return')
    Master.objects.create(type=transaction_type, code='PUR_RET', name='Purchase Return')
    Master.objects.create(type=transaction_type, code='TRANSFER', name='Stock Transfer')
    Master.objects.create(type=transaction_type, code='JOB_WORK', name='Job Work')

    # ============================================
    # UNITS - GST e-way bill system compliant
    # ============================================
    # Common units as per GST e-way bill system

    Master.objects.create(type=unit_type, code='NOS', name='Numbers')          # Pieces/Numbers
    Master.objects.create(type=unit_type, code='KGS', name='Kilograms')        # Weight
    Master.objects.create(type=unit_type, code='MTS', name='Metric Tons')      # Weight
    Master.objects.create(type=unit_type, code='GMS', name='Grams')          # Weight
    Master.objects.create(type=unit_type, code='MTR', name='Meters')         # Length
    Master.objects.create(type=unit_type, code='KMS', name='Kilometers')      # Distance
    Master.objects.create(type=unit_type, code='CMS', name='Centimeters')      # Length
    Master.objects.create(type=unit_type, code='LTR', name='Litres')          # Volume
    Master.objects.create(type=unit_type, code='MLT', name='Millilitres')     # Volume
    Master.objects.create(type=unit_type, code='SET', name='Sets')            # Sets
    Master.objects.create(type=unit_type, code='BOX', name='Boxes')           # Packaging
    Master.objects.create(type=unit_type, code='BGS', name='Bags')            # Packaging
    Master.objects.create(type=unit_type, code='BDL', name='Bundles')         # Packaging
    Master.objects.create(type=unit_type, code='CTN', name='Cartons')         # Packaging
    Master.objects.create(type=unit_type, code='ROL', name='Rolls')           # Packaging
    Master.objects.create(type=unit_type, code='DRM', name='Drums')           # Packaging
    Master.objects.create(type=unit_type, code='SQM', name='Square Meters')  # Area
    Master.objects.create(type=unit_type, code='CUB', name='Cubic Meters')    # Volume
    Master.objects.create(type=unit_type, code='TON', name='Tons')           # Weight
    Master.objects.create(type=unit_type, code='UNT', name='Units')           # General

    # ============================================
    # TRANSPORTATION MODES
    # ============================================
    Master.objects.create(type=trans_mode, code='ROAD', name='Road')
    Master.objects.create(type=trans_mode, code='RAIL', name='Rail')
    Master.objects.create(type=trans_mode, code='AIR', name='Air')
    Master.objects.create(type=trans_mode, code='SHIP', name='Ship/Sea')

    # Consignment Status
    Master.objects.create(type=consignment_status, code='IN_TRANSIT', name='In Transit')
    Master.objects.create(type=consignment_status, code='DELIVERED', name='Delivered')
    Master.objects.create(type=consignment_status, code='PENDING', name='Pending')
    Master.objects.create(type=consignment_status, code='CANCELLED', name='Cancelled')

    # ============================================
    # VEHICLE TYPES
    # ============================================
    Master.objects.create(type=vehicle_type, code='TRUCK', name='Truck')
    Master.objects.create(type=vehicle_type, code='TRAILER', name='Trailer')
    Master.objects.create(type=vehicle_type, code='TANKER', name='Tanker')
    Master.objects.create(type=vehicle_type, code='CONTAINER', name='Container')
    Master.objects.create(type=vehicle_type, code='TEMPER', name='Tempo')
    Master.objects.create(type=vehicle_type, code='PICKUP', name='Pickup')

    # ============================================
    # MASTER GROUPS - Account Group Structure
    # ============================================
    # Main Groups
    assets = MasterGroup.objects.create(name='Assets', type='ASSET')
    liabilities = MasterGroup.objects.create(name='Liabilities', type='LIABILITY')
    income = MasterGroup.objects.create(name='Income', type='INCOME')
    expenses = MasterGroup.objects.create(name='Expenses', type='EXPENSE')

    # Sub Groups - Assets
    MasterGroup.objects.create(name='Current Assets', parent=assets, type='ASSET')
    MasterGroup.objects.create(name='Fixed Assets', parent=assets, type='ASSET')
    MasterGroup.objects.create(name='Bank Accounts', parent=assets, type='ASSET')
    MasterGroup.objects.create(name='Cash-in-Hand', parent=assets, type='ASSET')
    MasterGroup.objects.create(name='Loans & Advances', parent=assets, type='ASSET')
    MasterGroup.objects.create(name='Sundry Debtors', parent=assets, type='ASSET')

    # Sub Groups - Liabilities
    MasterGroup.objects.create(name='Current Liabilities', parent=liabilities, type='LIABILITY')
    MasterGroup.objects.create(name='Loans Liability', parent=liabilities, type='LIABILITY')
    MasterGroup.objects.create(name='Bank OD Account', parent=liabilities, type='LIABILITY')
    MasterGroup.objects.create(name='Sundry Creditors', parent=liabilities, type='LIABILITY')
    MasterGroup.objects.create(name='Provisions', parent=liabilities, type='LIABILITY')

    # Sub Groups - Income
    MasterGroup.objects.create(name='Direct Income', parent=income, type='INCOME')
    MasterGroup.objects.create(name='Indirect Income', parent=income, type='INCOME')
    MasterGroup.objects.create(name='Sales Account', parent=income, type='INCOME')
    MasterGroup.objects.create(name='Service Income', parent=income, type='INCOME')

    # Sub Groups - Expenses
    MasterGroup.objects.create(name='Direct Expenses', parent=expenses, type='EXPENSE')
    MasterGroup.objects.create(name='Indirect Expenses', parent=expenses, type='EXPENSE')
    MasterGroup.objects.create(name='Purchase Account', parent=expenses, type='EXPENSE')
    MasterGroup.objects.create(name='Freight & Cartage', parent=expenses, type='EXPENSE')
    MasterGroup.objects.create(name='Rent', parent=expenses, type='EXPENSE')
    MasterGroup.objects.create(name='Salaries & Wages', parent=expenses, type='EXPENSE')

    print("Initial masters created successfully!")
    print("- Supply Types (B2B, B2C, Export, etc.)")
    print("- Transaction Types (Sale, Purchase, Returns, etc.)")
    print("- Units (NOS, KGS, MTR, LTR, etc.)")
    print("- Document Types (Invoice, Challan, etc.)")
    print("- Transport Modes (Road, Rail, Air, Ship)")
    print("- Vehicle Types (Truck, Trailer, Tanker, etc.)")
    print("- Account Groups (Assets, Liabilities, Income, Expenses)")

if __name__ == '__main__':
    seed()