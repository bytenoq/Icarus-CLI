import urllib.request
import urllib.parse
import getpass
from bs4 import BeautifulSoup

# urls
auth_url = "https://icarus-icsd.aegean.gr/authentication.php"
logout_url = "https://icarus-icsd.aegean.gr/logout.php"
origin_url = "https://icarus-icsd.aegean.gr/"

username = input("Όνομα χρήστη : ")
password = getpass.getpass(prompt="Συνθηματικό  : ")

# get cookie
request = urllib.request.Request(url=origin_url)
responce = urllib.request.urlopen(request)
cookie = responce.info().get("Set-Cookie")

# generate headers and data
headers = {"Referer": origin_url, "Cookie": cookie}
credentials = {"username": username, "pwd": password}
data = urllib.parse.urlencode(credentials)
data = data.encode("utf-8")

# send authentication request
request = urllib.request.Request(url=auth_url, data=data, headers=headers)
responce = urllib.request.urlopen(request)

# get responce
html = responce.read().decode("ISO-8859-7")

# handle html
soup = BeautifulSoup(html, "lxml")
user = soup.find(id="header_login", attrs={
                 "style": "display:inline"}).find("u")

# check if login successful
if not user:
    print("invalid credentials")
    exit()

# send logout request
request = urllib.request.Request(url=logout_url, headers=headers)
responce = urllib.request.urlopen(request)

# automate table scraping
def scrap_table(table_id):
    contents = []
    table = soup.find(id=table_id).find("tbody")
    table_rows = table.find_all("tr")
    for tr in table_rows:
        td = tr.find_all("td")
        contents.append({
            "code": td[1].text,
            "title": td[2].text,
            "grade": td[3].text,
            "semester": td[4].text,
            "declaration_date": td[5].text,
            "examination_date": td[6].text,
            "status": td[7].text
        })
    return contents

# color styling
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"

# exams_grades
exams_grades = scrap_table("exetastiki_grades")

# succeeded_grades
succeeded_grades = scrap_table("succeeded_grades")

# analytic_grades
analytic_grades = scrap_table("analytic_grades")

def calc_average_grade():
    total = len(succeeded_grades)
    average = 0
    exams = 0
    grades_sum = 0
    mandatory = 0
    english = False
    circle_1 = 0
    circle_2 = 0
    circle_3 = 0
    circle_4 = 0
    circle_5 = 0
    circle_6 = 0
    other = 0

    for course in succeeded_grades:
        grades_sum += float(course["grade"])
        if ("321-" not in course["code"] or course["code"] == "321-0823 " or course["code"] == "321-0833 " or course["code"] == "321-0843 " or course["code"] == "321-0853 " or course["code"] == "321-0161 " or course["code"] == "321-0151 " or course["code"] == "321-2600 " or course["code"] == "321-2631 " or course["code"] == "321-7602 "):
            other += 1

        elif (course["code"] == "321-0101 "):
            english = True

        elif (course["code"] == "321-9703 " or course["code"] == "321-5753 " or course["code"] == "321-8053 " or course["code"] == "321-10753 " or course["code"] == "321-99101 " or course["code"] == "321-7406 "):
            circle_1 += 1

        elif (course["code"] == "321-8953 " or course["code"] == "321-5155 " or course["code"] == "321-8504 " or course["code"] == "321-11102 " or course["code"] == "321-7653 " or course["code"] == "321-5607 " or course["code"] == "321-5403 "):
            circle_2 += 1

        elif (course["code"] == "321-10302 " or course["code"] == "321-7051 " or course["code"] == "321-7803 " or course["code"] == "321-9703 " or course["code"] == "321-8752 " or course["code"] == "321-7853 " or course["code"] == "321-10652 " or course["code"] == "321-6555 " or course["code"] == "321-8653 "):
            circle_3 += 1

        elif (course["code"] == "321-8354 " or course["code"] == "321-7003 " or course["code"] == "321-7256 " or course["code"] == "321-11001 " or course["code"] == "321-6257 " or course["code"] == "321-9404 " or course["code"] == "321-9120 "):
            circle_4 += 1

        elif (course["code"] == "321-7754 " or course["code"] == "321-3553 " or course["code"] == "321-9253 " or course["code"] == "321-10202 " or course["code"] == "321-7406 " or course["code"] == "321-6606 "):
            circle_5 += 1

        elif (course["code"] == "321-8603 " or course["code"] == "321-99002 " or course["code"] == "321-9455 " or course["code"] == "321-8001 " or course["code"] == "321-9855 " or course["code"] == "321-9003 " or course["code"] == "321-10001 "):
            circle_6 += 1

    for course in exams_grades:
        if (course["code"] == "321-0121 "):
            if (course["status"] == "Επιτυχία "):
                exams += 1
            
            continue

        if (course["code"] == "321-0131 "):
            if (course["status"] == "Επιτυχία "):
                exams += 1
            
            continue

        if (course["code"] == "321-0141 "):
            if (course["status"] == "Επιτυχία "):
                english = True
                exams += 1
                total += 1
                english_sum = float(course["grade"])
                english_div = 1
                for english in analytic_grades:
                    if (english["code"] == "321-0121 "):
                        english_sum += float(english["grade"])
                        english_div += 1

                    if (english["code"] == "321-0131 "):
                        english_sum += float(english["grade"])
                        english_div += 1

                    if (english_div == 3):
                        break

                english_sum = english_sum/english_div
                grades_sum += english_sum

        elif ("321-" not in course["code"] or course["code"] == "321-0823 " or course["code"] == "321-0833 " or course["code"] == "321-0843 " or course["code"] == "321-0853 " or course["code"] == "321-0161 " or course["code"] == "321-0151 " or course["code"] == "321-2600 " or course["code"] == "321-2631 " or course["code"] == "321-7602 "):
            if (course["status"] == "Επιτυχία "):
                other += 1
                grades_sum += float(course["grade"])
                total += 1
                exams += 1

        elif (course["code"] == "321-9703 " or course["code"] == "321-5753 " or course["code"] == "321-8053 " or course["code"] == "321-10753 " or course["code"] == "321-99101 " or course["code"] == "321-7406 "):
            if (course["status"] == "Επιτυχία "):
                circle_1 += 1
                grades_sum += float(course["grade"])
                total += 1
                exams += 1

        elif (course["code"] == "321-8953 " or course["code"] == "321-5155 " or course["code"] == "321-8504 " or course["code"] == "321-11102 " or course["code"] == "321-7653 " or course["code"] == "321-5607 " or course["code"] == "321-5403 "):
            if (course["status"] == "Επιτυχία "):
                circle_2 += 1
                grades_sum += float(course["grade"])
                total += 1
                exams += 1

        elif (course["code"] == "321-10302 " or course["code"] == "321-7051 " or course["code"] == "321-7803 " or course["code"] == "321-9703 " or course["code"] == "321-8752 " or course["code"] == "321-7853 " or course["code"] == "321-10652 " or course["code"] == "321-6555 " or course["code"] == "321-8653 "):
            if (course["status"] == "Επιτυχία "):
                circle_3 += 1
                grades_sum += float(course["grade"])
                total += 1
                exams += 1

        elif (course["code"] == "321-8354 " or course["code"] == "321-7003 " or course["code"] == "321-7256 " or course["code"] == "321-11001 " or course["code"] == "321-6257 " or course["code"] == "321-9404 " or course["code"] == "321-9120 "):
            if (course["status"] == "Επιτυχία "):
                circle_4 += 1
                grades_sum += float(course["grade"])
                total += 1
                exams += 1

        elif (course["code"] == "321-7754 " or course["code"] == "321-3553 " or course["code"] == "321-9253 " or course["code"] == "321-10202 " or course["code"] == "321-7406 " or course["code"] == "321-6606 "):
            if (course["status"] == "Επιτυχία "):
                circle_5 += 1
                grades_sum += float(course["grade"])
                total += 1
                exams += 1

        elif (course["code"] == "321-8603 " or course["code"] == "321-99002 " or course["code"] == "321-9455 " or course["code"] == "321-8001 " or course["code"] == "321-9855 " or course["code"] == "321-9003 " or course["code"] == "321-10001 "):
            if (course["status"] == "Επιτυχία "):
                circle_6 += 1
                grades_sum += float(course["grade"])
                total += 1
                exams += 1

        else :
            if (course["status"] == "Επιτυχία "):
                grades_sum += float(course["grade"])
                total += 1
                exams += 1

        if (course["status"] == "Επιτυχία "):
            print(course["title"].ljust(40), ":\033[32m", course["grade"], "\033[0m")
        elif (course["status"] == "Αποτυχία "):
            print(course["title"].ljust(40), ":\033[31m", course["grade"], "\033[0m")
        else:
            print(course["title"])

    average = grades_sum/total
    mandatory = total - circle_1 - circle_2 - circle_3 - circle_4 - circle_5 - circle_6 - english - other

    print()
    if (exams >= len(exams_grades) and exams > 0):
        print("Τρέχουσα εξεταστική                      :\033[32m", exams, "/", len(exams_grades), "\033[0m")
    else:
        print("Τρέχουσα εξεταστική                      :", exams, "/", len(exams_grades))
    if (mandatory == 36):
        print("Υποχρεωτικά μαθήματα                     :\033[32m", mandatory, "/ 36\033[0m")
    else:
        print("Υποχρεωτικά μαθήματα                     :", mandatory, "/ 36")
    print("Κύκλοι :")
    if (circle_1 >= 4):
        print("  Κ1 - Ασφάλεια                          :\033[32m", circle_1, "/ 4\033[0m")
    else:
        print("  Κ1 - Ασφάλεια                          :", circle_1, "/ 4")
    if (circle_2 >= 4):
        print("  Κ2 - Επιχειρηματικότητα                :\033[32m", circle_2, "/ 4\033[0m")
    else:
        print("  Κ2 - Επιχειρηματικότητα                :", circle_2, "/ 4")
    if (circle_3 >= 4):
        print("  Κ3 - Τηλεπικοινωνίες                   :\033[32m", circle_3, "/ 4\033[0m")
    else:
        print("  Κ3 - Τηλεπικοινωνίες                   :", circle_3, "/ 4")
    if (circle_4 >= 4):
        print("  Κ4 - Δίκτυα                            :\033[32m", circle_4, "/ 4\033[0m")
    else:
        print("  Κ4 - Δίκτυα                            :", circle_4, "/ 4")
    if (circle_5 >= 4):
        print("  Κ5 - Ευφυή Συστήματα                   :\033[32m", circle_5, "/ 4\033[0m")
    else:
        print("  Κ5 - Ευφυή Συστήματα                   :", circle_5, "/ 4")
    if (circle_6 >= 4):
        print("  Κ6 - Θεμελιώσεις Υπολογιστών           :\033[32m", circle_6, "/ 4\033[0m")
    else:
        print("  Κ6 - Θεμελιώσεις Υπολογιστών           :", circle_6, "/ 4")
    if (total >= 55):
        print("Σύνολο                                   :\033[32m", total, "/ 55\033[0m")
    else:
        print("Σύνολο                                   :", total, "/ 55")
    print("Μέσος όρος                               :", "{:.2f}".format(average))

calc_average_grade()
print()
