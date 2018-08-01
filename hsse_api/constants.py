"""PROJECT CONSTANTS
"""

class Constants():
    CONTRIBUTING_ACTIONS = (
        ("ONT", "Operating w/o necessary training"),
        ("FMS", "Failure to make secure"),
        ("OUS", "Operating at unsafe speed"),
        ("IWS", "Inadequate warning/signal"),
        ("NSD", "Nullified safety device"),
        ("UDE", "Used defective equipment"),
        ("UEU", "Used equipment unsafely"),
        ("UWE", "Used wrong tool/equipment"),
        ("IGD", "Inadequate guard/safety device"),
        ("HA", "Hazardous attire"),
        ("FEH", "Fire or explosion hazard"),
        ("UAM", "Unsecured against movement"),
        ("PH", "Poor housekeeping"),
        ("POH", "Protruding object hazard")
    )
    CONTRIBUTING_CONDITIONS = (
        ("IGD", "Inadequate guard/safety device"),
        ("HA", "Hazardous attire"),
        ("IWS", "Inadequate warning/signal"),
        ("UAM", "Unsecured against movement"),
        ("PH", "Poor housekeeping"),
        ("POH", "Protruding object hazard"),
        ("CCC", "Close clearance/congestion"),
        ("HAS", "Hazardous arrangement/storage"),
        ("DTE", "Defective tools/equipment"),
        ("AC", "Atmospheric condition"),
        ("INH", "Illumination/noise hazard"),
        ("OUC", "Other unsafe condition"),
        ("NUC", "No Unsafe condition")
    )
    INFLUENCE_CONTRIBUTING_ACTIONS = (
        ("UJH", "Unaware of job hazards"),
        ("ITH", "Inattention to hazard"),
        ("USM", "Unaware of safe method"),
        ("LLJS", "Low level job skill"),
        ("TGST", "Tried to gain or save time"),
        ("TAEF", "Tried to avoid extra effort"),
        ("TAD", "Tried to avoid discomfort"),
        ("CBE", "Caused by employee"),
        ("CAE", "Caused by another employee"),
        ("DNU", "Defective from normal use"),
        ("ISI", "Inadequate safety inspection"),
        ("IHC", "Inadequate housekeeping/clean-up"),
        ("FDC", "Faulty desing/construction")
    )
    INFLUENCE_CONTRIBUTING_CONDITIONS = (
        ("CBE", "Caused by employee"),
        ("CAE", "Caused by another employee"),
        ("DNU", "Defective from normal use"),
        ("DAM", "Defective via abuse/misuse"),
        ("ISI", "Inadequate safety inspection"),
        ("IHC", "Inadequate housekeeping/clean-up"),
        ("FDC", "Faulty desing/construction"),
        ("OC", "Outside contractor"),
        ("IPM", "Inadequate preventive maintenance"),
        ("PP", "Purchasing practice"),
        ("DE", "Deteriorating exposure"),
        ("MA", "Management acceptance"),
        ("OSC", "Other source case"),
        ("USC", "Unkwon source cause")
    )
    GENDERS_CHOICES = (
        ("F", "Female"),
        ("M", "Male")
    )
    COMMON_CHOICES = (
        ("Y", "Yes"),
        ("N", "No"),
        ("N/A", "No Answer")
    )
    CASE_TYPES = (
        ("FA", "First Aids"),
        ("MT", "Medical Treatment"),
        ("RA", "Restricted Activity"),
        ("LD", "Lost Days"),
        ("IFE", "Injury Free Event")
    )
    ACCIDENT_TYPES = (
        ("AE", "Automatic Equipment"),
        ("RE", "Robotic Equipment"),
        ("TI", "Trapped in"),
        ("FDL", "Falling from Different Level"),
        ("SLF", "Same level fall"),
        ("ER", "Electric risk"),
        ("HEC", "Hazardous Energy Control (LOTO)"),
        ("CS", "Confined Space"),
        ("PV", "Pressure Vessels"),
        ("ME", "Mobile Equipment"),
        ("CHS", "Cranes/Hoists/Slings"),
        ("F", "Fire")
    )
    OTHER_RESULTS = (
        ("LC", "Lost of Consciousness"),
        ("TT", "Temporal Transfer"),
        ("PT", "Permanent Transfer"),
        ("ET", "Employee Termination"),
        ("PR", "Permanent Restriction"),
        ("TD", "Total Disability")
    )
    INJURY_MECHANISMS = (
        ("SB", "Struck by"),
        ("SA", "Struck against"),
        ("CW", "Contact With"),
        ("CB", "Contacted By"),
        ("TI", "Trapped In"),
        ("TO", "Trapped On"),
        ("TB", "Trapped between"),
        ("SLF", "Same Level Fall"),
        ("DLF", "Different Level Fall"),
        ("SS", "Sprain/Strain"),
        ("E", "Exposure")
    )
    FATALITY_POTENTIAL = (
        ("H", "High"),
        ("M", "Medium"),
        ("L", "Low")
    )
    STATUS_CHOICES = (
        ("OV", "Overdue"),
        ("CL", "Closed"),
        ("IP", "In progress"),
        ("O", "Open")
    )
