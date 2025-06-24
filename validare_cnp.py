def validare_cnp(cnp):
    if not cnp.isdigit():
        return False, "CNP-ul trebuie să conțină doar cifre."
    
    if len(cnp) != 13:
        return False, "CNP-ul trebuie să aibă exact 13 cifre."
    
    if cnp[0] not in ['6', '5']:
        return False, "CNP-ul trebuie să înceapă cu 5 penntru bărbat sau 6 pentru femeie."
    
    if int(cnp[3]) >= 2:
        return False, "CNP invalid."
    
    suma_4_5 = int(cnp[3]) + int(cnp[4])
    if suma_4_5 >= 10:
        return False, "CNP invalid."
    
    if int(cnp[5]) >= 4:
        return False, "CNP invalid."
    
    return True, "CNP valid."
