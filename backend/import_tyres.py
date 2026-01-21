import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Sample tyre data from the Excel file
TYRE_DATA = [
    # MRF Tyres
    {"brand": "MRF", "size": "400*8", "type": "TY", "pattern": "AUTOMILER84 6 PLY", "stock": 0, "price": 1230},
    {"brand": "MRF", "size": "400*8", "type": "TY", "pattern": "TRIPEL PLUS 4 PLY", "stock": 0, "price": 1090},
    {"brand": "MRF", "size": "450*10", "type": "TT", "pattern": "SHAVARI", "stock": 0, "price": 2380},
    {"brand": "MRF", "size": "155D*12", "type": "TT", "pattern": "SHAVARI", "stock": 0, "price": 2900},
    {"brand": "MRF", "size": "155D*12", "type": "TT", "pattern": "SHAVARI LUG", "stock": 0, "price": 3150},
    {"brand": "MRF", "size": "165D*13", "type": "TT", "pattern": "SHAVARI", "stock": 0, "price": 3620},
    {"brand": "MRF", "size": "165D*13", "type": "TT", "pattern": "SHAVARI LUG", "stock": 0, "price": 3820},
    {"brand": "MRF", "size": "400*8", "type": "TL", "pattern": "AUTOMILER84 6 PLY", "stock": 0, "price": 1550},
    {"brand": "MRF", "size": "400*10", "type": "TT", "pattern": "AUTO MILER", "stock": 0, "price": 1700},
    {"brand": "MRF", "size": "400*10", "type": "TL", "pattern": "AUTO MILER 99", "stock": 0, "price": 1650},
    {"brand": "MRF", "size": "275*18", "type": "TT", "pattern": "ZAPPER FS FRONT", "stock": 0, "price": 1420},
    {"brand": "MRF", "size": "275*18", "type": "TT", "pattern": "RIB FRONT", "stock": 0, "price": 1380},
    {"brand": "MRF", "size": "275*18", "type": "TT", "pattern": "NYLOGRIP PLUS", "stock": 0, "price": 1470},
    {"brand": "MRF", "size": "275*18", "type": "TL", "pattern": "NAYLOGRIP PLUS", "stock": 0, "price": 1400},
    {"brand": "MRF", "size": "300*18", "type": "TT", "pattern": "NYLOGRIP PLUS", "stock": 0, "price": 1590},
    {"brand": "MRF", "size": "275*17", "type": "TT", "pattern": "ZAPPER FS FRONT", "stock": 0, "price": 1320},
    {"brand": "MRF", "size": "300*17", "type": "TT", "pattern": "NAYLOGRIP PLUS", "stock": 0, "price": 1480},
    {"brand": "MRF", "size": "80/100*18", "type": "TL", "pattern": "ZAPPER FS FRONT", "stock": 0, "price": 1500},
    {"brand": "MRF", "size": "80/100*18", "type": "TL", "pattern": "METEOR-M+", "stock": 0, "price": 1670},
    {"brand": "MRF", "size": "80/100*18", "type": "TL", "pattern": "ZAPPER-Y", "stock": 0, "price": 1550},
    {"brand": "MRF", "size": "80/100*18", "type": "TL", "pattern": "NAYLOGRIP PLUS", "stock": 0, "price": 1530},
    {"brand": "MRF", "size": "90/100*10", "type": "TY", "pattern": "NAYLOGRIP FE", "stock": 0, "price": 900},
    {"brand": "MRF", "size": "90/100*10", "type": "TL", "pattern": "ZAPPER C-1", "stock": 0, "price": 1140},
    {"brand": "MRF", "size": "90/100*10", "type": "TL", "pattern": "ZAPPER", "stock": 0, "price": 1120},
    {"brand": "MRF", "size": "90/100*10", "type": "TL", "pattern": "NAYLOGRIP FE", "stock": 0, "price": 940},
    {"brand": "MRF", "size": "100/90*18", "type": "TL", "pattern": "ZAPPER-Y", "stock": 0, "price": 1810},
    {"brand": "MRF", "size": "100/90*18", "type": "TT", "pattern": "ZAPPER-Y", "stock": 0, "price": 1870},
    {"brand": "MRF", "size": "100/90*17", "type": "TL", "pattern": "ZAPPER-Y", "stock": 0, "price": 1760},
    {"brand": "MRF", "size": "100/90*17", "type": "TT", "pattern": "ZAPPER-Y", "stock": 0, "price": 1860},
    {"brand": "MRF", "size": "90/90*17", "type": "TL", "pattern": "ZAPPER FS FRONT", "stock": 0, "price": 1560},
    {"brand": "MRF", "size": "140/60*17", "type": "TL", "pattern": "ZAPPER", "stock": 0, "price": 2950},
    {"brand": "MRF", "size": "100/80*17", "type": "TL", "pattern": "ZAPPER FRONT", "stock": 0, "price": 1680},
    {"brand": "MRF", "size": "80/100*17", "type": "TL", "pattern": "ZAPPER FS FRONT", "stock": 0, "price": 1430},
    {"brand": "MRF", "size": "90/90*12", "type": "TL", "pattern": "ZAPPER FG", "stock": 0, "price": 1120},
    {"brand": "MRF", "size": "110/70*12", "type": "TL", "pattern": "ZAPPER-N", "stock": 0, "price": 1550},
    {"brand": "MRF", "size": "110/70*11", "type": "TL", "pattern": "ZAPPER FG", "stock": 0, "price": 1300},
    {"brand": "MRF", "size": "120/70*10", "type": "TL", "pattern": "ZAPPER FG", "stock": 0, "price": 1450},
    {"brand": "MRF", "size": "110/90*18", "type": "TT", "pattern": "ZAPPER-Q", "stock": 0, "price": 2150},
    {"brand": "MRF", "size": "90/90*19", "type": "TL", "pattern": "ZFM FRONT", "stock": 0, "price": 1830},
    {"brand": "MRF", "size": "90/90*19", "type": "TT", "pattern": "ZFM FRONT", "stock": 0, "price": 1860},
    {"brand": "MRF", "size": "130/90*15", "type": "TL", "pattern": "ZAPPER-Y", "stock": 0, "price": 2170},
    {"brand": "MRF", "size": "300*10", "type": "TL", "pattern": "NGP (E/F+150)", "stock": 0, "price": 980},
    
    # TVS Tyres
    {"brand": "TVS", "size": "400*8", "type": "TY", "pattern": "STREET KING", "stock": 0, "price": 1060},
    {"brand": "TVS", "size": "275*18", "type": "TY", "pattern": "ATT-525 FRONT", "stock": 0, "price": 950},
    {"brand": "TVS", "size": "275*18", "type": "TY", "pattern": "RIB SC36 FRONT", "stock": 0, "price": 943},
    {"brand": "TVS", "size": "250*18", "type": "TY", "pattern": "RIB", "stock": 0, "price": 1002},
    {"brand": "TVS", "size": "275*18", "type": "TT", "pattern": "DURA PRO", "stock": 0, "price": 1270},
    {"brand": "TVS", "size": "275*18", "type": "TT", "pattern": "JUMBO", "stock": 0, "price": 1270},
    {"brand": "TVS", "size": "275*18", "type": "TY", "pattern": "ATT 250 (CHOKLET)", "stock": 0, "price": 1050},
    {"brand": "TVS", "size": "275*18", "type": "TY", "pattern": "CHNDRIKA", "stock": 0, "price": 1050},
    {"brand": "TVS", "size": "300*18", "type": "TT", "pattern": "DURA PRO", "stock": 0, "price": 1340},
    {"brand": "TVS", "size": "300*18", "type": "TT", "pattern": "JUMBO", "stock": 0, "price": 1399},
    {"brand": "TVS", "size": "275*17", "type": "TY", "pattern": "ATT525 FRONT", "stock": 0, "price": 983},
    {"brand": "TVS", "size": "275*17", "type": "TY", "pattern": "RIB FRONT", "stock": 0, "price": 949},
    {"brand": "TVS", "size": "300*17", "type": "TT", "pattern": "DURA PRO", "stock": 0, "price": 1352},
    {"brand": "TVS", "size": "300*17", "type": "TT", "pattern": "JUMBO", "stock": 0, "price": 1352},
    {"brand": "TVS", "size": "80/100*18", "type": "TL", "pattern": "ATT625 FRONT", "stock": 0, "price": 1218},
    {"brand": "TVS", "size": "275*18", "type": "TL", "pattern": "ATT 450 FRONT", "stock": 0, "price": 1083},
    {"brand": "TVS", "size": "80/100*18", "type": "TL", "pattern": "DURA PRO", "stock": 0, "price": 1399},
    {"brand": "TVS", "size": "80/100*18", "type": "TL", "pattern": "JUMBO GT", "stock": 0, "price": 1422},
    {"brand": "TVS", "size": "275*18", "type": "TL", "pattern": "DURA PRO", "stock": 0, "price": 1245},
    {"brand": "TVS", "size": "350*10", "type": "TY", "pattern": "CONTA", "stock": 0, "price": 871},
    {"brand": "TVS", "size": "90/100*10", "type": "TL", "pattern": "DURA PRO", "stock": 0, "price": 902},
    {"brand": "TVS", "size": "90/100*10", "type": "TL", "pattern": "CONTA 350", "stock": 0, "price": 909},
    {"brand": "TVS", "size": "90/100*10", "type": "TL", "pattern": "PANCER", "stock": 0, "price": 951},
    {"brand": "TVS", "size": "100/90*18", "type": "TL", "pattern": "REMORA /ATT455R", "stock": 0, "price": 1704},
    {"brand": "TVS", "size": "100/90*18", "type": "TT", "pattern": "JUMBO", "stock": 0, "price": 1811},
    {"brand": "TVS", "size": "100/90*17", "type": "TL", "pattern": "BEAMER VS", "stock": 0, "price": 1613},
    {"brand": "TVS", "size": "140/60*17", "type": "TL", "pattern": "MC63", "stock": 0, "price": 2769},
    {"brand": "TVS", "size": "80/100*17", "type": "TL", "pattern": "JUMBO GT", "stock": 0, "price": 1165},
    {"brand": "TVS", "size": "80/100*17", "type": "TL", "pattern": "ATT 525 FRONT", "stock": 0, "price": 1281},
    {"brand": "TVS", "size": "275*17", "type": "TL", "pattern": "ATT450 FORTUNA", "stock": 0, "price": 1092},
    {"brand": "TVS", "size": "90/90*12", "type": "TL", "pattern": "DURA PRO", "stock": 0, "price": 1037},
    {"brand": "TVS", "size": "90/90*12", "type": "TL", "pattern": "CONTA 775F", "stock": 0, "price": 909},
    {"brand": "TVS", "size": "120/80*16", "type": "TL", "pattern": "JUMBO PLOY-X", "stock": 0, "price": 2103},
    {"brand": "TVS", "size": "275*16", "type": "TL", "pattern": "JUMBO PT", "stock": 0, "price": 1142},
    {"brand": "TVS", "size": "250*16", "type": "TY", "pattern": "SIMHA RIB", "stock": 0, "price": 559},
    {"brand": "TVS", "size": "250*16", "type": "TY", "pattern": "JUMBO", "stock": 0, "price": 707},
    {"brand": "TVS", "size": "300*10", "type": "TL", "pattern": "CONTA (E/F+150)", "stock": 0, "price": 828},
    {"brand": "TVS", "size": "350*8", "type": "TY", "pattern": "RACHA", "stock": 0, "price": 729},
    
    # BEDROCK Tyres
    {"brand": "BEDROCK", "size": "400*8", "type": "TY", "pattern": "M-3 6 PLY", "stock": 0, "price": 1050},
    {"brand": "BEDROCK", "size": "400*8", "type": "TY", "pattern": "MEGIC 6 PLY", "stock": 0, "price": 1100},
    {"brand": "BEDROCK", "size": "450*10", "type": "TY", "pattern": "SUPER LOADER", "stock": 0, "price": 1950},
    {"brand": "BEDROCK", "size": "500*12", "type": "E-TY", "pattern": "SUPRE LUG", "stock": 0, "price": 2000},
    {"brand": "BEDROCK", "size": "450*12", "type": "E-TY", "pattern": "SU.LOADER R2", "stock": 0, "price": 1900},
    {"brand": "BEDROCK", "size": "400*12", "type": "E-TY", "pattern": "SUPRE LUG", "stock": 0, "price": 1500},
    {"brand": "BEDROCK", "size": "400*12", "type": "E-TY", "pattern": "SU.LOADER 8PLY", "stock": 0, "price": 1450},
    {"brand": "BEDROCK", "size": "400*12", "type": "E-TY", "pattern": "SU. LOADER 4PLY", "stock": 0, "price": 1350},
    {"brand": "BEDROCK", "size": "375*12", "type": "E-TY", "pattern": "SUPER LOADER", "stock": 0, "price": 1200},
    {"brand": "BEDROCK", "size": "375*12", "type": "E-TY", "pattern": "SUPREME", "stock": 0, "price": 1200},
    {"brand": "BEDROCK", "size": "400*8", "type": "TL", "pattern": "JAYA 6PLY", "stock": 0, "price": 1113},
    {"brand": "BEDROCK", "size": "275*18", "type": "TY", "pattern": "RACER FS FRONT", "stock": 0, "price": 1150},
    {"brand": "BEDROCK", "size": "275*18", "type": "TY", "pattern": "RIB FRONT", "stock": 0, "price": 1100},
    {"brand": "BEDROCK", "size": "250*18", "type": "TY", "pattern": "RIB", "stock": 0, "price": 1100},
    {"brand": "BEDROCK", "size": "275*18", "type": "TY", "pattern": "DURAMAX", "stock": 0, "price": 1250},
    {"brand": "BEDROCK", "size": "275*18", "type": "TY", "pattern": "SUPER SHAKTI", "stock": 0, "price": 1250},
    {"brand": "BEDROCK", "size": "275*18", "type": "TY", "pattern": "MG", "stock": 0, "price": 1200},
    {"brand": "BEDROCK", "size": "300*18", "type": "TY", "pattern": "DURAMAX", "stock": 0, "price": 1400},
    {"brand": "BEDROCK", "size": "300*18", "type": "TY", "pattern": "SUPER SHAKTI", "stock": 0, "price": 1400},
    {"brand": "BEDROCK", "size": "275*17", "type": "TY", "pattern": "RACER FS FRONT", "stock": 0, "price": 1150},
    {"brand": "BEDROCK", "size": "275*17", "type": "TY", "pattern": "RIB FRONT", "stock": 0, "price": 1100},
    {"brand": "BEDROCK", "size": "300*17", "type": "TY", "pattern": "SUPER SHAKTI", "stock": 0, "price": 1400},
    {"brand": "BEDROCK", "size": "300*17", "type": "TY", "pattern": "MG", "stock": 0, "price": 1350},
    {"brand": "BEDROCK", "size": "80/100*18", "type": "TL", "pattern": "RACER FS FRONT", "stock": 0, "price": 1400},
    {"brand": "BEDROCK", "size": "80/100*18", "type": "TL", "pattern": "SUPREME", "stock": 0, "price": 1600},
    {"brand": "BEDROCK", "size": "80/100*18", "type": "TL", "pattern": "CRUZER", "stock": 0, "price": 1600},
    {"brand": "BEDROCK", "size": "300*18", "type": "TL", "pattern": "SUPREME", "stock": 0, "price": 1650},
    {"brand": "BEDROCK", "size": "275*18", "type": "TL", "pattern": "SUPREME", "stock": 0, "price": 1450},
    {"brand": "BEDROCK", "size": "350*10", "type": "TY", "pattern": "ROYAL", "stock": 0, "price": 1050},
    {"brand": "BEDROCK", "size": "90/100*10", "type": "TL", "pattern": "RACER FS", "stock": 0, "price": 1250},
    {"brand": "BEDROCK", "size": "90/100*10", "type": "TL", "pattern": "SUPREME", "stock": 0, "price": 1250},
    {"brand": "BEDROCK", "size": "90/100*10", "type": "TL", "pattern": "DURAMAX", "stock": 0, "price": 1250},
    {"brand": "BEDROCK", "size": "90/100*10", "type": "TL", "pattern": "ROYAL", "stock": 0, "price": 1250},
    {"brand": "BEDROCK", "size": "90/100*10", "type": "TL", "pattern": "MAGNETO", "stock": 0, "price": 1250},
    {"brand": "BEDROCK", "size": "90/100*10", "type": "TL", "pattern": "RACER RS", "stock": 0, "price": 1250},
    {"brand": "BEDROCK", "size": "100/90*18", "type": "TL", "pattern": "DURAMAX", "stock": 0, "price": 2000},
    {"brand": "BEDROCK", "size": "100/90*17", "type": "TL", "pattern": "SUPREME", "stock": 0, "price": 1900},
    {"brand": "BEDROCK", "size": "120/80*17", "type": "TL", "pattern": "MAGNETO", "stock": 0, "price": 2200},
    {"brand": "BEDROCK", "size": "90/90*17", "type": "TL", "pattern": "RACER FS FRONT", "stock": 0, "price": 1600},
    {"brand": "BEDROCK", "size": "130/70*17", "type": "TL", "pattern": "MAGNETO", "stock": 0, "price": 2600},
    {"brand": "BEDROCK", "size": "140/60*17", "type": "TL", "pattern": "MAGNETO", "stock": 0, "price": 2700},
    {"brand": "BEDROCK", "size": "140/70*17", "type": "TL", "pattern": "MAGNETO", "stock": 0, "price": 2700},
    {"brand": "BEDROCK", "size": "100/80*17", "type": "TL", "pattern": "RACER FS FRONT", "stock": 0, "price": 1750},
    {"brand": "BEDROCK", "size": "80/100*17", "type": "TL", "pattern": "MAGNETO", "stock": 0, "price": 1500},
    {"brand": "BEDROCK", "size": "80/100*17", "type": "TL", "pattern": "RACER FS FRONT", "stock": 0, "price": 1400},
    {"brand": "BEDROCK", "size": "90/90*12", "type": "TL", "pattern": "SUPREME R2", "stock": 0, "price": 1350},
    {"brand": "BEDROCK", "size": "90/90*12", "type": "TL", "pattern": "GLIDER", "stock": 0, "price": 1250},
    {"brand": "BEDROCK", "size": "100/80*12", "type": "TL", "pattern": "RACER FS", "stock": 0, "price": 1600},
    {"brand": "BEDROCK", "size": "110/80*12", "type": "TL", "pattern": "MAGNETO", "stock": 0, "price": 1700},
    {"brand": "BEDROCK", "size": "250*16", "type": "TY", "pattern": "SUPER SHAKTI", "stock": 0, "price": 850},
    {"brand": "BEDROCK", "size": "250*16", "type": "TY", "pattern": "RIB", "stock": 0, "price": 750},
    {"brand": "BEDROCK", "size": "300*10", "type": "TL", "pattern": "RACER FS(E/F+150)", "stock": 0, "price": 1100},
    {"brand": "BEDROCK", "size": "300*10", "type": "TL", "pattern": "ROYAL (E/F +150)", "stock": 0, "price": 1100},
    
    # CEAT Tyres
    {"brand": "CEAT", "size": "450*10", "type": "TT", "pattern": "MILE XL (LUG)", "stock": 0, "price": 2500},
    {"brand": "CEAT", "size": "450*10", "type": "TT", "pattern": "ANMOL RIB HD", "stock": 0, "price": 2400},
    {"brand": "CEAT", "size": "400*8", "type": "TL", "pattern": "BULAND X3 6PLY", "stock": 0, "price": 1350},
    {"brand": "CEAT", "size": "275*18", "type": "TT", "pattern": "SEC.ZOOM FRONT", "stock": 0, "price": 1500},
    {"brand": "CEAT", "size": "275*18", "type": "TT", "pattern": "F-85 RIB FRONT", "stock": 0, "price": 1500},
    {"brand": "CEAT", "size": "275*18", "type": "TT", "pattern": "SecuraLYFE", "stock": 0, "price": 1650},
    {"brand": "CEAT", "size": "275*18", "type": "TT", "pattern": "MILAZE", "stock": 0, "price": 1550},
    {"brand": "CEAT", "size": "300*18", "type": "TT", "pattern": "MILAZE", "stock": 0, "price": 1700},
    {"brand": "CEAT", "size": "275*17", "type": "TT", "pattern": "SEC ZOOM FRONT", "stock": 0, "price": 1550},
    {"brand": "CEAT", "size": "275*17", "type": "TT", "pattern": "F85 FRONT", "stock": 0, "price": 1550},
    {"brand": "CEAT", "size": "300*17", "type": "TT", "pattern": "MILAZE", "stock": 0, "price": 1750},
    {"brand": "CEAT", "size": "80/100*18", "type": "TL", "pattern": "SEC ZOOM FRONT", "stock": 0, "price": 1550},
    {"brand": "CEAT", "size": "275*18", "type": "TL", "pattern": "SEC ZOOM FRONT", "stock": 0, "price": 1450},
    {"brand": "CEAT", "size": "80/100*18", "type": "TL", "pattern": "SECURALYFE", "stock": 0, "price": 1800},
    {"brand": "CEAT", "size": "80/100*18", "type": "TL", "pattern": "SEC ZOOM +", "stock": 0, "price": 1700},
    {"brand": "CEAT", "size": "80/100*18", "type": "TL", "pattern": "MILAZE", "stock": 0, "price": 1700},
    {"brand": "CEAT", "size": "275*18", "type": "TL", "pattern": "SEURALYEF", "stock": 0, "price": 1600},
    {"brand": "CEAT", "size": "275*18", "type": "TL", "pattern": "MILAZE", "stock": 0, "price": 1500},
    {"brand": "CEAT", "size": "90/100*10", "type": "TY", "pattern": "MILAZE", "stock": 0, "price": 1150},
    {"brand": "CEAT", "size": "90/100*10", "type": "TL", "pattern": "ZOOM X3", "stock": 0, "price": 1300},
    {"brand": "CEAT", "size": "90/100*10", "type": "TL", "pattern": "GRIP X3", "stock": 0, "price": 1350},
    {"brand": "CEAT", "size": "90/100*10", "type": "TL", "pattern": "MILAZE X5", "stock": 0, "price": 1250},
    {"brand": "CEAT", "size": "120/80*17", "type": "TL", "pattern": "ZOOM X3", "stock": 0, "price": 2550},
    {"brand": "CEAT", "size": "90/90*17", "type": "TL", "pattern": "SEC ZOOM FRONT", "stock": 0, "price": 1800},
    {"brand": "CEAT", "size": "130/70*17", "type": "TL", "pattern": "ZOOM XL", "stock": 0, "price": 2850},
    {"brand": "CEAT", "size": "140/60*17", "type": "TL", "pattern": "CROSS RAD", "stock": 0, "price": 3300},
    {"brand": "CEAT", "size": "140/60*17", "type": "TL", "pattern": "ZOOM RAD X3", "stock": 0, "price": 3100},
    {"brand": "CEAT", "size": "100/80*17", "type": "TL", "pattern": "ZOOM FRONT", "stock": 0, "price": 2000},
    {"brand": "CEAT", "size": "300*17", "type": "TL", "pattern": "MILAZE", "stock": 0, "price": 1700},
    {"brand": "CEAT", "size": "80/100*17", "type": "TL", "pattern": "ZOOM XL FRONT", "stock": 0, "price": 1650},
    {"brand": "CEAT", "size": "275*17", "type": "TL", "pattern": "SEC ZOOM FRONT", "stock": 0, "price": 1450},
    {"brand": "CEAT", "size": "90/90*12", "type": "TL", "pattern": "ZOOM D/X3", "stock": 0, "price": 1350},
    {"brand": "CEAT", "size": "90/90*12", "type": "TL", "pattern": "MILAZE X5", "stock": 0, "price": 1350},
    {"brand": "CEAT", "size": "110/70*12", "type": "TL", "pattern": "ENERGY RIDE EV", "stock": 0, "price": 1600},
    {"brand": "CEAT", "size": "120/80*18", "type": "TT", "pattern": "ZC", "stock": 0, "price": 2250},
    {"brand": "CEAT", "size": "110/90*18", "type": "TL", "pattern": "ZAPPER Y", "stock": 0, "price": 1895},
    {"brand": "CEAT", "size": "130/90*15", "type": "TL", "pattern": "ZOOM X3", "stock": 0, "price": 2650},
    {"brand": "CEAT", "size": "300*10", "type": "TL", "pattern": "ER/EV (E/F+150)", "stock": 0, "price": 1200},
]

async def import_data():
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    # Clear existing data
    await db.tyres.delete_many({})
    print("Cleared existing tyre data")
    
    # Insert new data
    result = await db.tyres.insert_many(TYRE_DATA)
    print(f"Imported {len(result.inserted_ids)} tyres successfully!")
    
    # Show summary
    pipeline = [
        {"$group": {"_id": "$brand", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    summary = await db.tyres.aggregate(pipeline).to_list(100)
    
    print("\nImport Summary:")
    for item in summary:
        print(f"  {item['_id']}: {item['count']} items")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(import_data())
