"""Configuration: paths, thresholds and activity mappings for the BPIC15_1 analysis."""
import os

# Path to the BPIC15_1 XES event log (override with env var PERMIT_LOG_PATH or the --log CLI flag)
LOG_PATH = os.environ.get("PERMIT_LOG_PATH", os.path.join("data", "BPIC15_1.xes"))

# Output folder for exported CSV files
OUTPUT_DIR = os.environ.get("PERMIT_OUTPUT_DIR", "output")

# Number of most common variants kept in the variant filter
NUMBER_OF_VARIANTS = 15

# Activities occurring fewer times than this are dropped
FREQUENCY_THRESHOLD = 300

# Time windows used for the yearly BPMN models (start, end)
TIME_WINDOWS = [
    ("2010-10-01 00:00:00", "2011-12-31 23:59:59"),
    ("2012-01-01 00:00:00", "2012-12-31 23:59:59"),
    ("2013-01-01 00:00:00", "2013-12-31 23:59:59"),
    ("2014-01-01 00:00:00", "2014-12-31 23:59:59"),
    ("2015-01-01 00:00:00", "2015-12-31 23:59:59"),
]

# Year excluded from the yearly trend plot of the manually filtered main process
EXCLUDED_YEAR = 2015

# Activity code -> readable name (event log B)
ACTIVITY_MAPPING = {
    '01_BB': 'Objections and complaints',
    '01_HOOFD': 'Main process',
    '02_DRZ': 'Stakeholder and Authority Notification',
    '03_GBH': 'Applicant is stakeholder',
    '03_VD': 'Create cover letter extend procedure term',
    '04_BPT': 'No permit, WABO, Phase',
    '05_EIND': 'Terminate on request',
    '06_VD': 'Extend procedure term',
    '07_OPS': 'Suspend term',
    '08_AWB45': 'Request complete, Requesting missing data, Permanent suspension',
    '09_AH': 'Article 34 WABO applies',
    '09_AWB45': 'Request complete',
    '10_UOV': 'Draft and Final Decision',
    '11_AH': 'Phase decision suspended',
    '12_AP': 'Phase updated plan requested',
    '13_CRD': 'Coordination of application',
    '14_VRIJ': 'No permit needed or only notification needed',
    '15_NGV': 'Request further information',
    '16_LGSV': 'Calculate provisional charges'
}

# Activity code -> "code: readable name" (event log C)
ACTIVITY_MAPPING_DETAILED = {
    '01_BB': '01_BB: Objections and complaints',
    '01_HOOFD': '01_HOOFD: Main process',
    '02_DRZ': '02_DRZ: Stakeholder and Authority Notification',
    '03_GBH': '03_GBH: Applicant is stakeholder',
    '03_VD': '03_VD: Create cover letter extend procedure term',
    '04_BPT': '04_BPT: No permit, WABO, Phase',
    '05_EIND': '05_EIND: Terminate on request',
    '06_VD': '06_VD: Extend procedure term',
    '07_OPS': '07_OPS: Suspend term',
    '08_AWB45': '08_AWB45: Request complete, Requesting missing data, Permanent suspension',
    '09_AH': '09_AH: Article 34 WABO applies',
    '09_AWB45': '09_AWB45: Request complete',
    '10_UOV': '10_UOV: Draft and Final Decision',
    '11_AH': '11_AH: Phase decision suspended',
    '12_AP': '12_AP: Phase updated plan requested',
    '13_CRD': '13_CRD: Coordination of application',
    '14_VRIJ': '14_VRIJ: No permit needed or only notification needed',
    '15_NGV': '15_NGV: Request further information',
    '16_LGSV': '16_LGSV: Calculate provisional charges'
}

# Full list of 01_HOOFD (main process) activities (event log D)
MAIN_PROCESS_ACTIVITIES = [
    "01_HOOFD_010", "01_HOOFD_011", "01_HOOFD_015", "01_HOOFD_020", 
    "01_HOOFD_030_1", "01_HOOFD_030_2", "01_HOOFD_040", "01_HOOFD_050", 
    "01_HOOFD_055", "01_HOOFD_060", "01_HOOFD_061", "01_HOOFD_065_0", 
    "01_HOOFD_065_1", "01_HOOFD_065_2", "01_HOOFD_080", "01_HOOFD_090", 
    "01_HOOFD_099", "01_HOOFD_100", "01_HOOFD_100_0", "01_HOOFD_101", 
    "01_HOOFD_101b", "01_HOOFD_110", "01_HOOFD_110_0", "01_HOOFD_110_1", 
    "01_HOOFD_110_2", "01_HOOFD_120", "01_HOOFD_130", "01_HOOFD_140", 
    "01_HOOFD_150", "01_HOOFD_160", "01_HOOFD_180", "01_HOOFD_181", 
    "01_HOOFD_190", "01_HOOFD_190_1", "01_HOOFD_190_2", "01_HOOFD_191", 
    "01_HOOFD_192", "01_HOOFD_193", "01_HOOFD_195", "01_HOOFD_195_1", 
    "01_HOOFD_195_2", "01_HOOFD_196", "01_HOOFD_197", "01_HOOFD_200", 
    "01_HOOFD_205", "01_HOOFD_210_0", "01_HOOFD_210_1", "01_HOOFD_210_2", 
    "01_HOOFD_250", "01_HOOFD_250_0", "01_HOOFD_250_1", "01_HOOFD_250_2", 
    "01_HOOFD_260", "01_HOOFD_270", "01_HOOFD_280_1", "01_HOOFD_280_2", 
    "01_HOOFD_330", "01_HOOFD_331", "01_HOOFD_332", "01_HOOFD_350_0", 
    "01_HOOFD_350_1", "01_HOOFD_350_2", "01_HOOFD_370", "01_HOOFD_375", 
    "01_HOOFD_380", "01_HOOFD_390", "01_HOOFD_400", "01_HOOFD_410_0", 
    "01_HOOFD_410_1", "01_HOOFD_410_2", "01_HOOFD_420", "01_HOOFD_430", 
    "01_HOOFD_440_1", "01_HOOFD_440_1a", "01_HOOFD_440_2", "01_HOOFD_445", 
    "01_HOOFD_446", "01_HOOFD_446_0", "01_HOOFD_446_1", "01_HOOFD_446_2", 
    "01_HOOFD_447", "01_HOOFD_450", "01_HOOFD_451", "01_HOOFD_455", 
    "01_HOOFD_456", "01_HOOFD_459", "01_HOOFD_460", "01_HOOFD_460a", 
    "01_HOOFD_465", "01_HOOFD_470", "01_HOOFD_480", "01_HOOFD_490_1", 
    "01_HOOFD_490_1a", "01_HOOFD_490_2", "01_HOOFD_490_3", "01_HOOFD_490_3a", 
    "01_HOOFD_490_4", "01_HOOFD_490_5", "01_HOOFD_490_5a", "01_HOOFD_491", 
    "01_HOOFD_491a", "01_HOOFD_492_0", "01_HOOFD_492_1", "01_HOOFD_492_2", 
    "01_HOOFD_493", "01_HOOFD_494a", "01_HOOFD_495", "01_HOOFD_496_1", 
    "01_HOOFD_496_2", "01_HOOFD_498", "01_HOOFD_500", "01_HOOFD_505", 
    "01_HOOFD_510_0", "01_HOOFD_510_1", "01_HOOFD_510_2", "01_HOOFD_510_2a", 
    "01_HOOFD_510_3", "01_HOOFD_510_4", "01_HOOFD_515", "01_HOOFD_516", 
    "01_HOOFD_516a", "01_HOOFD_519", "01_HOOFD_520", "01_HOOFD_530", 
    "01_HOOFD_530a", "01_HOOFD_530b", "01_HOOFD_532", "01_HOOFD_540", 
    "01_HOOFD_550", "01_HOOFD_570", "01_HOOFD_580_1", "01_HOOFD_580_2", 
    "01_HOOFD_590", "01_HOOFD_600_1", "01_HOOFD_600_2", "01_HOOFD_790", 
    "01_HOOFD_800", "01_HOOFD_805", "01_HOOFD_809", "01_HOOFD_809b", 
    "01_HOOFD_809c", "01_HOOFD_810", "01_HOOFD_811", "01_HOOFD_814", 
    "01_HOOFD_815", "01_HOOFD_820"
]

# Manual grouping of main-process activities (event log E)
ACTIVITY_CLASSIFICATION = {
    # Registration and Reception
    "01_HOOFD_010": "Registration and Reception",
    "01_HOOFD_011": "Registration and Reception",
    "01_HOOFD_015": "Registration and Reception",
    "01_HOOFD_020": "Registration and Reception",
    "01_HOOFD_030_1": "Registration and Reception",
    "01_HOOFD_030_2": "Registration and Reception",
    "01_HOOFD_060": "Registration and Reception",
    
    # Confirmation and Communication
    "01_HOOFD_040": "Confirmation and Communication",
    "01_HOOFD_050": "Confirmation and Communication",
    "01_HOOFD_430": "Communication",
    "01_HOOFD_510_1": "Communication",

    # Investigate
    "01_HOOFD_055": "Investigate",
    
    # WABO Procedures
    "01_HOOFD_061": "WABO Procedures",
    "01_HOOFD_181": "WABO Procedures",
    "01_HOOFD_197": "WABO Procedures",
    "01_HOOFD_331": "WABO Procedures",
    "01_HOOFD_332": "WABO Procedures",

    # Confirmation Procedures
    "01_HOOFD_065_0": "Confirmation procedure",
    "01_HOOFD_065_1": "Confirmation procedure",
    "01_HOOFD_065_2": "Confirmation procedure",
    "01_HOOFD_190_2": "Confirmation",
    "01_HOOFD_195_2": "Confirmation",
    "01_HOOFD_210_0": "Confirmation",
    "01_HOOFD_210_1": "Confirmation",
    "01_HOOFD_210_2": "Confirmation",
    "01_HOOFD_350_0": "Confirmation",
    "01_HOOFD_350_1": "Confirmation",
    "01_HOOFD_350_2": "Confirmation",

    # Inspection and Review
    "01_HOOFD_080": "Inspection and Review",
    "01_HOOFD_375": "Inspection and Review",
    "01_HOOFD_380": "Inspection and Review",
    "01_HOOFD_390": "Inspection and Review",
    "01_HOOFD_532": "Inspection and Review",

    # Subcase Review and Processing
    "01_HOOFD_110": "Subcase Review and Processing",
    "01_HOOFD_110_0": "Subcase Review and Processing",
    "01_HOOFD_110_1": "Subcase Review and Processing",
    "01_HOOFD_110_2": "Subcase Review and Processing",
    "01_HOOFD_120": "Subcase Review and Processing",
    "01_HOOFD_196": "Subcase Review and Processing",
    "01_HOOFD_250": "Subcase Review and Processing",
    "01_HOOFD_250_0": "Subcase Review and Processing",
    "01_HOOFD_250_1": "Subcase Review and Processing",
    "01_HOOFD_250_2": "Subcase Review and Processing",
    "01_HOOFD_260": "Subcase Review and Processing",

    # Complete
    "01_HOOFD_190": "Complete",
    "01_HOOFD_200": "Complete",
    "01_HOOFD_370": "Complete",

    # Processing
    "01_HOOFD_195": "Processing",
    "01_HOOFD_205": "Processing",
    "01_HOOFD_330": "Processing",
    "01_HOOFD_410_1": "Processing",
    "01_HOOFD_410_2": "Processing",
    "01_HOOFD_420": "Processing",

    # Decision Making
    "01_HOOFD_180": "Decision Making",
    "01_HOOFD_440_1": "Decision Making",
    "01_HOOFD_440_1a": "Decision Making",
    "01_HOOFD_440_2": "Decision Making",
    "01_HOOFD_445": "Decision Making",
    "01_HOOFD_450": "Decision Making",
    "01_HOOFD_451": "Decision Making",
    "01_HOOFD_490_1": "Decision Making",
    "01_HOOFD_490_1a": "Decision Making",
    "01_HOOFD_490_2": "Decision Making",
    "01_HOOFD_490_3": "Decision Making",
    "01_HOOFD_490_4": "Decision Making",
    "01_HOOFD_490_5": "Decision Making",
    "01_HOOFD_490_5a": "Decision Making",
    "01_HOOFD_491": "Decision Making",
    "01_HOOFD_494a": "Decision Making",
    "01_HOOFD_495": "Decision Making",
    "01_HOOFD_510_0": "Decision Making",
    "01_HOOFD_510_2": "Decision Making",
    "01_HOOFD_510_2a": "Decision Making",
    "01_HOOFD_510_3": "Decision Making",
    "01_HOOFD_510_4": "Decision Making",
    "01_HOOFD_515": "Decision Making",

    # Suspension Procedures
    "01_HOOFD_160": "Suspension Procedures",
    "01_HOOFD_470": "Suspension Procedures",
    "01_HOOFD_540": "Suspension Procedures",
    "01_HOOFD_550": "Suspension Procedures",
    "01_HOOFD_570": "Suspension Procedures",

    # Continuation Procedures
    "01_HOOFD_498": "Continuation Procedures",
    "01_HOOFD_505": "Continuation Procedures",
    "01_HOOFD_590": "Continuation Procedures",
    "01_HOOFD_600_1": "Continuation Procedures",
    "01_HOOFD_600_2": "Continuation Procedures",

    # Publication
    "01_HOOFD_090": "Publication",
    "01_HOOFD_099": "Publication",
    "01_HOOFD_100": "Publication",
    "01_HOOFD_100_0": "Publication",
    "01_HOOFD_101": "Publication",
    "01_HOOFD_519": "Publication",
    "01_HOOFD_520": "Publication",
    "01_HOOFD_530": "Publication",

    # Case Closure
    "01_HOOFD_446": "Case Closure",
    "01_HOOFD_790": "Case Closure",
    "01_HOOFD_800": "Case Closure",
    "01_HOOFD_805": "Case Closure",
    "01_HOOFD_814": "Case Closure",
    "01_HOOFD_815": "Case Closure",
    "01_HOOFD_820": "Case Closure",

    # Appeal
    "01_HOOFD_500": "Appeal",

    # By Law
    "01_HOOFD_480": "By law",
    
    # General
    '01_BB': '01.BB: Objections and complaints',
    '02_DRZ': '02.DRZ: Stakeholder and Authority Notification',
    '03_GBH': '03.GBH: Applicant is stakeholder',
    '03_VD': '03.VD: Create cover letter extend procedure term',
    '04_BPT': '04.BPT: No permit, WABO, Phase',
    '05_EIND': '05.EIND: Terminate on request',
    '06_VD': '06.VD: Extend procedure term',
    '07_OPS': '07.OPS: Suspend term',
    '08_AWB45': '08.AWB45: Request complete, Missing data, Suspension',
    '09_AH': '09.AH: WABO applies',
    '09_AWB45': '09.AW: Request complete',
    '10_UOV': '10.UOV: Draft and Final Decision',
    '11_AH': '11.AH: Phase decision suspended',
    '12_AP': '12.AP: Phase updated plan requested',
    '13_CRD': '13.CRD: Coordination of application',
    '14_VRIJ': '14.VRIJ: No permit needed or only notification needed',
    '15_NGV': '15.NGV: Request further information',
    '16_LGSV': '16.LGSV: Calculate provisional charges'
}
