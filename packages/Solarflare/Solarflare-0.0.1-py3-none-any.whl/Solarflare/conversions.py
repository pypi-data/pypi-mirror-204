import math

def kg_to_lb(kg):
    """Convert kilograms to pounds."""
    return kg * 2.20462

def lb_to_kg(lb):
    """Convert pounds to kilograms."""
    return lb / 2.20462

def kg_to_g(kg):
    """Convert kilograms to grams."""
    return kg * 1000

def g_to_kg(g):
    """Convert grams to kilograms."""
    return g / 1000

def lb_to_oz(lb):
    """Convert pounds to ounces."""
    return lb * 16

def oz_to_lb(oz):
    """Convert ounces to pounds."""
    return oz / 16

def lb_to_st(lb):
    """Convert pounds to stones."""
    return lb / 14

def st_to_lb(st):
    """Convert stones to pounds."""
    return st * 14

def oz_to_g(oz):
    """Convert ounces to grams."""
    return oz * 28.3495

def g_to_oz(g):
    """Convert grams to ounces."""
    return g / 28.3495

def g_to_mg(g):
    """Convert grams to milligrams."""
    return g * 1000

def mg_to_g(mg):
    """Convert milligrams to grams."""
    return mg / 1000

def g_to_mcg(g):
    """Convert grams to micrograms."""
    return g * 1000000

def mcg_to_g(mcg):
    """Convert micrograms to grams."""
    return mcg / 1000000

def t_to_kg(t):
    """Convert tonnes to kilograms."""
    return t * 1000

def kg_to_t(kg):
    """Convert kilograms to tonnes."""
    return kg / 1000

def mt_to_kg(mt):
    """Convert metric tonnes to kilograms."""
    return mt * 1000

def kg_to_mt(kg):
    """Convert kilograms to metric tonnes."""
    return kg / 1000

def sht_to_lb(st):
    """Convert short tons to pounds."""
    return st * 2000

def lb_to_sht(lb):
    """Convert pounds to short tons."""
    return lb / 2000

def lt_to_lb(lt):
    """Convert long tons to pounds."""
    return lt * 2240

def lb_to_lt(lb):
    """Convert pounds to long tons."""
    return lb / 2240

def ct_to_g(ct):
    """Convert carats to grams."""
    return ct / 5

def g_to_ct(g):
    """Convert grams to carats."""
    return g * 5

def amu_to_kg(amu):
    """Convert atomic mass units to kilograms."""
    return amu * 1.66054e-27

def kg_to_amu(kg):
    """Convert kilograms to atomic mass units."""
    return kg / 1.66054e-27

def ozt_to_g(ozt):
    """Convert troy ounces to grams."""
    return ozt * 31.1035

def g_to_ozt(g):
    """Convert grams to troy ounces."""
    return g / 31.1035

def amu_to_ev(amu):
    """Convert atomic mass units to electronvolts."""
    return amu * 931.5e6

def ev_to_amu(ev):
    """Convert electronvolts to atomic mass units."""
    return ev / 931.5e6

def amu_to_joules(amu):
    """Convert atomic mass units to joules."""
    return amu_to_ev(amu) * 1.60218e-19

def joules_to_amu(joules):
    """Convert joules to atomic mass units."""
    return ev_to_amu(joules / 1.60218e-19)


"""
VELOCITY
"""

def mph_to_kph(mph):
    """Convert miles per hour to kilometers per hour."""
    return mph * 1.60934

def kph_to_mph(kph):
    """Convert kilometers per hour to miles per hour."""
    return kph / 1.60934

def fps_to_mps(fps):
    """Convert feet per second to meters per second."""
    return fps * 0.3048

def mps_to_fps(mps):
    """Convert meters per second to feet per second."""
    return mps / 0.3048

def knots_to_mph(knots):
    """Convert knots to miles per hour."""
    return knots * 1.15078

def mph_to_knots(mph):
    """Convert miles per hour to knots."""
    return mph / 1.15078

def knots_to_kph(knots):
    """Convert knots to kilometers per hour."""
    return knots * 1.852

def kph_to_knots(kph):
    """Convert kilometers per hour to knots."""
    return kph / 1.852

def mach_to_mps(mach, temperature=15):
    """Convert Mach number to meters per second."""
    speed_of_sound = 331.3 + 0.606 * temperature
    return mach * speed_of_sound

def mps_to_mach(mps, temperature=15):
    """Convert meters per second to Mach number."""
    speed_of_sound = 331.3 + 0.606 * temperature
    return mps / speed_of_sound

def mph_to_fps(mph):
    """Convert miles per hour to feet per second."""
    return mph * 1.46667

def fps_to_mph(fps):
    """Convert feet per second to miles per hour."""
    return fps / 1.46667

def kph_to_fps(kph):
    """Convert kilometers per hour to feet per second."""
    return kph / 1.09728

def fps_to_kph(fps):
    """Convert feet per second to kilometers per hour."""
    return fps * 1.09728

def mach_to_knots(mach, temperature=15):
    """Convert Mach number to knots."""
    mps = mach_to_mps(mach, temperature)
    return mps_to_knots(mps)

def knots_to_mach(knots, temperature=15):
    """Convert knots to Mach number."""
    mps = knots_to_mps(knots)
    return mps_to_mach(mps, temperature)

def kph_to_mach(kph, temperature=15):
    """Convert kilometers per hour to Mach number."""
    mps = kph_to_mps(kph)
    return mps_to_mach(mps, temperature)

def mach_to_kph(mach, temperature=15):
    """Convert Mach number to kilometers per hour."""
    mps = mach_to_mps(mach, temperature)
    return mps_to_kph(mps)

def kph_to_mps(kph):
    """Convert kilometers per hour to meters per second."""
    return kph / 3.6

def mps_to_kph(mps):
    """Convert meters per second to kilometers per hour."""
    return mps * 3.6

def mps_to_knots(mps):
    """Convert meters per second to knots."""
    return mps * 1.94384449

def knots_to_mps(knots):
    """Convert knots to meters per second."""
    return knots / 1.94384449


"""
BRIGHTNESS
"""

def mag_to_flux(mag):
    """Convert apparent magnitude to flux density."""
    return 10**(-0.4 * (mag - 23.9))

def flux_to_mag(flux):
    """Convert flux density to apparent magnitude."""
    return -2.5 * math.log10(flux) + 23.9

def mag_to_luminosity(mag, distance):
    """Convert apparent magnitude to luminosity."""
    flux_density = mag_to_flux(mag)
    luminosity = 4 * math.pi * (distance * pc_to_cm)**2 * flux_density
    return luminosity

def luminosity_to_mag(luminosity, distance):
    """Convert luminosity to apparent magnitude."""
    flux_density = luminosity / (4 * math.pi * (distance * pc_to_cm)**2)
    mag = flux_to_mag(flux_density)
    return mag

def abs_mag_to_app_mag(abs_mag, distance):
    """Convert absolute magnitude to apparent magnitude."""
    app_mag = abs_mag + 5 * math.log10(distance / 10)
    return app_mag

def app_mag_to_abs_mag(app_mag, distance):
    """Convert apparent magnitude to absolute magnitude."""
    abs_mag = app_mag - 5 * math.log10(distance / 10)
    return abs_mag

def flux_to_luminosity(flux, distance):
    """Convert flux density to luminosity."""
    luminosity = 4 * math.pi * (distance * pc_to_cm)**2 * flux
    return luminosity

def luminosity_to_flux(luminosity, distance):
    """Convert luminosity to flux density."""
    flux = luminosity / (4 * math.pi * (distance * pc_to_cm)**2)
    return flux

def pc_to_cm(pc):
    """Convert parsecs to centimeters."""
    return pc * 3.086e18


"""
DISTANCE
"""

def au_to_km(au):
    """Convert astronomical units to kilometers."""
    return au * 149597870.7

def km_to_au(km):
    """Convert kilometers to astronomical units."""
    return km / 149597870.7

def ly_to_km(ly):
    """Convert light years to kilometers."""
    return ly * 9.461e12

def km_to_ly(km):
    """Convert kilometers to light years."""
    return km / 9.461e12

def pc_to_km(pc):
    """Convert parsecs to kilometers."""
    return pc * 3.086e13

def km_to_pc(km):
    """Convert kilometers to parsecs."""
    return km / 3.086e13

def mpc_to_km(mpc):
    """Convert megaparsecs to kilometers."""
    return mpc * 3.086e19

def km_to_mpc(km):
    """Convert kilometers to megaparsecs."""
    return km / 3.086e19

def gpc_to_km(gpc):
    """Convert gigaparsecs to kilometers."""
    return gpc * 3.086e22

def km_to_gpc(km):
    """Convert kilometers to gigaparsecs."""
    return km / 3.086e22

def au_to_miles(au):
    """Convert astronomical units to miles."""
    return au * 92955807.267

def miles_to_au(miles):
    """Convert miles to astronomical units."""
    return miles / 92955807.267

def ly_to_au(ly):
    """Convert light years to astronomical units."""
    return ly * 63241.1

def au_to_ly(au):
    """Convert astronomical units to light years."""
    return au / 63241.1

def km_to_miles(km):
    """Convert kilometers to miles."""
    return km * 0.621371

def miles_to_km(miles):
    """Convert miles to kilometers."""
    return miles / 0.621371

def pc_to_ly(pc):
    """Convert parsecs to light years."""
    return pc * 3.26156

def ly_to_pc(ly):
    """Convert light years to parsecs."""
    return ly / 3.26156

"""
TEMPERATURE
"""
# Celsius to Fahrenheit and Kelvin
def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return (celsius * 1.8) + 32

def celsius_to_kelvin(celsius):
    """Convert Celsius to Kelvin."""
    return celsius + 273.15

# Fahrenheit to Celsius and Kelvin
def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) / 1.8

def fahrenheit_to_kelvin(fahrenheit):
    """Convert Fahrenheit to Kelvin."""
    return (fahrenheit + 459.67) * 5/9

# Kelvin to Celsius and Fahrenheit
def kelvin_to_celsius(kelvin):
    """Convert Kelvin to Celsius."""
    return kelvin - 273.15

def kelvin_to_fahrenheit(kelvin):
    """Convert Kelvin to Fahrenheit."""
    return (kelvin * 9/5) - 459.67

"""
TIME
"""

# seconds to minutes, hours, and days
def seconds_to_minutes(seconds):
    """Convert seconds to minutes."""
    return seconds / 60

def seconds_to_hours(seconds):
    """Convert seconds to hours."""
    return seconds / 3600

def seconds_to_days(seconds):
    """Convert seconds to days."""
    return seconds / 86400

# minutes to seconds, hours, and days
def minutes_to_seconds(minutes):
    """Convert minutes to seconds."""
    return minutes * 60

def minutes_to_hours(minutes):
    """Convert minutes to hours."""
    return minutes / 60

def minutes_to_days(minutes):
    """Convert minutes to days."""
    return minutes / 1440

# hours to seconds, minutes, and days
def hours_to_seconds(hours):
    """Convert hours to seconds."""
    return hours * 3600

def hours_to_minutes(hours):
    """Convert hours to minutes."""
    return hours * 60

def hours_to_days(hours):
    """Convert hours to days."""
    return hours / 24

# days to seconds, minutes, and hours
def days_to_seconds(days):
    """Convert days to seconds."""
    return days * 86400

def days_to_minutes(days):
    """Convert days to minutes."""
    return days * 1440

def days_to_hours(days):
    """Convert days to hours."""
    return days * 24

"""
ANGULAR MEASUREMENT
"""

# degrees to radians and arcminutes
def degrees_to_radians(degrees):
    """Convert degrees to radians."""
    return degrees * (math.pi / 180)

def degrees_to_arcminutes(degrees):
    """Convert degrees to arcminutes."""
    return degrees * 60

# radians to degrees and arcminutes
def radians_to_degrees(radians):
    """Convert radians to degrees."""
    return radians * (180 / math.pi)

def radians_to_arcminutes(radians):
    """Convert radians to arcminutes."""
    return radians * (60 * 180 / math.pi)

# arcminutes to degrees and radians
def arcminutes_to_degrees(arcminutes):
    """Convert arcminutes to degrees."""
    return arcminutes / 60

def arcminutes_to_radians(arcminutes):
    """Convert arcminutes to radians."""
    return arcminutes * (math.pi / 180 / 60)

"""
PRESSURE
"""
# pascals to millibars and pounds per square inch (psi)
def pascals_to_millibars(pascals):
    """Convert pascals to millibars."""
    return pascals * 0.01

def pascals_to_psi(pascals):
    """Convert pascals to psi."""
    return pascals * 0.000145038

# millibars to pascals and psi
def millibars_to_pascals(millibars):
    """Convert millibars to pascals."""
    return millibars * 100

def millibars_to_psi(millibars):
    """Convert millibars to psi."""
    return millibars * 0.0145038

# psi to pascals and millibars
def psi_to_pascals(psi):
    """Convert psi to pascals."""
    return psi * 6894.76

def psi_to_millibars(psi):
    """Convert psi to millibars."""
    return psi * 68.9476


"""
PHYSICS
"""
# joules to electronvolts
def joules_to_electronvolts(joules):
    """Convert joules to electronvolts."""
    return joules / 1.60218e-19

# electronvolts to joules
def electronvolts_to_joules(electronvolts):
    """Convert electronvolts to joules."""
    return electronvolts * 1.60218e-19

# tesla to gauss
def tesla_to_gauss(tesla):
    """Convert tesla to gauss."""
    return tesla * 10000

# gauss to tesla
def gauss_to_tesla(gauss):
    """Convert gauss to tesla."""
    return gauss / 10000

# hertz to angular frequency (radians per second)
def hertz_to_angular_frequency(hertz):
    """Convert hertz to angular frequency."""
    return 2 * math.pi * hertz

# angular frequency (radians per second) to hertz
def angular_frequency_to_hertz(angular_frequency):
    """Convert angular frequency to hertz."""
    return angular_frequency / (2 * math.pi)

# astronomical units to meters
def astronomical_units_to_meters(astronomical_units):
    """Convert astronomical units to meters."""
    return astronomical_units * 1.496e+11

# meters to astronomical units
def meters_to_astronomical_units(meters):
    """Convert meters to astronomical units."""
    return meters / 1.496e+11


"""
MATHEMATICS
"""
# base-10 logarithm to natural logarithm
def log10_to_ln(log10):
    """Convert base-10 logarithm to natural logarithm."""
    return log10 / math.log(10)

# natural logarithm to base-10 logarithm
def ln_to_log10(ln):
    """Convert natural logarithm to base-10 logarithm."""
    return ln * math.log(10)

# natural logarithm to base-e exponential
def ln_to_exp(ln):
    """Convert natural logarithm to base-e exponential."""
    return math.exp(ln)

# base-e exponential to natural logarithm
def exp_to_ln(exp):
    """Convert base-e exponential to natural logarithm."""
    return math.log(exp)

# degrees to gradians
def degrees_to_gradians(degrees):
    """Convert degrees to gradians."""
    return degrees * 10 / 9

# gradians to degrees
def gradians_to_degrees(gradians):
    """Convert gradians to degrees."""
    return gradians * 9 / 10

# binary to decimal
def binary_to_decimal(binary):
    """Convert binary to decimal."""
    decimal = 0
    binary = str(binary)[::-1]
    for i in range(len(binary)):
        decimal += int(binary[i]) * 2**i
    return decimal

# decimal to binary
def decimal_to_binary(decimal):
    """Convert decimal to binary."""
    binary = ''
    while decimal > 0:
        binary += str(decimal % 2)
        decimal = decimal // 2
    return binary[::-1]

# octal to decimal
def octal_to_decimal(octal):
    """Convert octal to decimal."""
    decimal = 0
    octal = str(octal)[::-1]
    for i in range(len(octal)):
        decimal += int(octal[i]) * 8**i
    return decimal

# decimal to octal
def decimal_to_octal(decimal):
    """Convert decimal to octal."""
    octal = ''
    while decimal > 0:
        octal += str(decimal % 8)
        decimal = decimal // 8
    return octal[::-1]

# hexadecimal to decimal
def hexadecimal_to_decimal(hexadecimal):
    """Convert hexadecimal to decimal."""
    decimal = 0
    hexadecimal = str(hexadecimal)[::-1]
    for i in range(len(hexadecimal)):
        if hexadecimal[i] in 'abcdef':
            decimal += (ord(hexadecimal[i]) - 87) * 16**i
        else:
            decimal += int(hexadecimal[i]) * 16**i
    return decimal

# decimal to hexadecimal
def decimal_to_hexadecimal(decimal):
    """Convert decimal to hexadecimal."""
    hexadecimal = ''
    while decimal > 0:
        remainder = decimal % 16
        if remainder >= 10:
            hexadecimal += chr(remainder + 87)
        else:
            hexadecimal += str(remainder)
        decimal = decimal // 16
    return hexadecimal[::-1]



def hms_to_decimal(hours, minutes, seconds):
    """Convert hours, minutes, and seconds to decimal hours."""
    decimal_hours = hours + (minutes / 60) + (seconds / 3600)
    return decimal_hours

def decimal_to_hms(decimal_hours):
    """Convert decimal hours to hours, minutes, and seconds."""
    hours = int(decimal_hours)
    minutes = int((decimal_hours - hours) * 60)
    seconds = round((((decimal_hours - hours) * 60) - minutes) * 60, 2)
    return hours, minutes, seconds

def degrees_to_hms(degrees):
    """Convert degrees to hours, minutes, and seconds."""
    total_seconds = degrees * 240
    hours = int(total_seconds / 3600)
    minutes = int((total_seconds - (hours * 3600)) / 60)
    seconds = round(total_seconds - (hours * 3600) - (minutes * 60), 2)
    return hours, minutes, seconds

"""
BIOLOGY
"""

def dna_base_complement(base):
    """Convert DNA base to its complementary base."""
    if base == "A":
        return "T"
    elif base == "T":
        return "A"
    elif base == "C":
        return "G"
    elif base == "G":
        return "C"
    else:
        return None

def amino_acid_mw(aa):
    """Get the molecular weight of an amino acid."""
    mw_dict = {
        "A": 89.09,
        "R": 174.20,
        "N": 132.12,
        "D": 133.10,
        "C": 121.15,
        "E": 147.13,
        "Q": 146.15,
        "G": 75.07,
        "H": 155.16,
        "I": 131.17,
        "L": 131.17,
        "K": 146.19,
        "M": 149.21,
        "F": 165.19,
        "P": 115.13,
        "S": 105.09,
        "T": 119.12,
        "W": 204.23,
        "Y": 181.19,
        "V": 117.15
    }
    return mw_dict.get(aa, None)

def ng_per_ul_to_mg_per_ml(ng_per_ul):
    """Convert ng/ul to mg/ml."""
    return round(ng_per_ul / 1000, 2)

"""
CHEMISTRY
"""

def mass_to_moles(mass, molar_mass):
    """Convert mass to moles."""
    return round(mass / molar_mass, 2)

def moles_to_mass(moles, molar_mass):
    """Convert moles to mass."""
    return round(moles * molar_mass, 2)

def ph_to_hydrogen_ion_concentration(ph):
    """Convert pH to hydrogen ion concentration (in mol/L)."""
    return round(10**(-ph), 2)

def hydrogen_ion_concentration_to_ph(hydrogen_ion_concentration):
    """Convert hydrogen ion concentration (in mol/L) to pH."""
    return round(-math.log10(hydrogen_ion_concentration), 2)

def percent_to_molarity(percent_concentration, molar_mass):
    """Convert percent concentration to molarity."""
    return round((percent_concentration / 100) * 10 / molar_mass, 2)

def molarity_to_percent(molar_concentration, molar_mass):
    """Convert molarity to percent concentration."""
    return round(molar_concentration * molar_mass * 100 / 10, 2)

def liter_to_milliliter(volume_liter):
    """Convert liter to milliliter."""
    return round(volume_liter * 1000, 2)

def milliliter_to_liter(volume_milliliter):
    """Convert milliliter to liter."""
    return round(volume_milliliter / 1000, 2)

def joule_to_calorie(energy_joule):
    """Convert joule to calorie."""
    return round(energy_joule / 4.184, 2)

def calorie_to_joule(energy_calorie):
    """Convert calorie to joule."""
    return round(energy_calorie * 4.184, 2)

def gram_per_cubic_cm_to_kilogram_per_cubic_m(gram_per_cubic_cm):
    """Convert grams per cubic centimeter to kilograms per cubic meter."""
    return round(gram_per_cubic_cm * 1000, 2)

def kilogram_per_cubic_m_to_gram_per_cubic_cm(kilogram_per_cubic_m):
    """Convert kilograms per cubic meter to grams per cubic centimeter."""
    return round(kilogram_per_cubic_m / 1000, 2)


def joule_per_mole_to_kilojoule_per_mole(joule_per_mole):
    """Convert joules per mole to kilojoules per mole."""
    return round(joule_per_mole / 1000, 2)

def kilojoule_per_mole_to_joule_per_mole(kilojoule_per_mole):
    """Convert kilojoules per mole to joules per mole."""
    return round(kilojoule_per_mole * 1000, 2)

def stoichiometry(moles_reactant, stoichiometry_ratio, moles_product=None):
    """
    Calculate the moles of product or reactant given the moles of the other and the stoichiometry ratio.
    If the moles of product are not given, the function returns the moles of product.
    If the moles of reactant are not given, the function returns the moles of reactant.
    """
    if moles_product is None:
        return round(moles_reactant * stoichiometry_ratio, 2)
    else:
        return round(moles_product / stoichiometry_ratio, 2)
