import math
import os
import sqlite3
from datetime import datetime

import PySimpleGUI as sg

sg.theme("DarkGrey15")
sg.set_options(font="Arial 12")

path = os.getcwd() + "/MilitaryRetirementCalculator/PayChart.db"
with sqlite3.connect(path) as db:
    cursor = db.cursor()

grades = [
    "E-1 <4 Mon",
    "E-1 >4 Mon",
    "E-2",
    "E-3",
    "E-4",
    "E-5",
    "E-6",
    "E-7",
    "E-8",
    "E-9",
    "W-1",
    "W-2",
    "W-3",
    "W-4",
    "W-5",
    "O-1E",
    "O-2E",
    "O-3E",
    "O-1",
    "O-2",
    "O-3",
    "O-4",
    "O-5",
    "O-6",
    "O-7",
    "O-8",
    "O-9",
    "O-10",
]


def windowRetirementCalculator():

    layout = [
        [
            sg.Text(
                "Pay Grade",
                size=(10, 1),
                key="lblPayGrade",
                visible=True,
            ),
            sg.Combo(
                grades,
                key="cboPayGrade",
                default_value="E-7",
                visible=True,
                enable_events=True,
            ),
        ],
        [
            sg.Text("Years of Service", key="lblYearsOfService"),
            sg.InputText(
                "20",
                key="txtYearsOfService",
                size=(10, 1),
                enable_events=True,
            ),
        ],
        [
            sg.Text("Date of Rank", key="lblDateOfRank"),
            sg.InputText("2014-6-1 0:0:0", key="txtDateOfRank", size=(10, 1)),
            sg.CalendarButton(
                "",
                close_when_date_chosen=True,
                target="txtDateOfRank",
                location=(0, 0),
                no_titlebar=False,
            ),
        ],
        [
            sg.Text("Monthly VA Payment", key="lblMonthlyVAPayment"),
            sg.InputText(
                "1517.03", key="txtMonthlyVAPayment", size=(10, 1), enable_events=True
            ),
        ],
        [
            sg.Text("Monthly Retirement Pay", key="lblMonthlyRetirementPay"),
            sg.Text("", key="txtMonthlyRetirementPay", size=(10, 1)),
        ],
        [
            sg.Text("Annual Retirement Pay (Including VA Payment)", key="lblAnnualPay"),
            sg.Text("", key="txtAnnualPay", size=(10, 1)),
        ],
        [sg.Button("Calculate", key="btnCalculate")],
    ]

    return sg.Window(
        "2023 Military Retirement Pay Calculator", layout, element_justification="c"
    )


def getDays(inputDate):
    now = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    currentDate = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
    dto = datetime.strptime(inputDate, "%Y-%m-%d %H:%M:%S")
    return (currentDate - dto).days


def getPay(yearsOfService, year, grade):
    cursor.execute(
        "SELECT * FROM '" + year + "' WHERE PayGrade = ?",
        [(grade)],
    )
    yearsOfService = int(yearsOfService)
    if yearsOfService >= 40:
        column = 22
    match yearsOfService:
        case 0 | 1:
            column = 1
        case 2:
            column = 2
        case 3:
            column = 3
        case 4 | 5:
            column = 4
        case 6 | 7:
            column = 5
        case 8 | 9:
            column = 6
        case 10 | 11:
            column = 7
        case 12 | 13:
            column = 8
        case 14 | 15:
            column = 9
        case 16 | 17:
            column = 10
        case 18 | 19:
            column = 11
        case 20 | 21:
            column = 12
        case 22 | 23:
            column = 13
        case 24 | 25:
            column = 14
        case 26 | 27:
            column = 15
        case 28 | 29:
            column = 16
        case 30 | 31:
            column = 17
        case 32 | 33:
            column = 18
        case 34 | 35:
            column = 19
        case 36 | 37:
            column = 20
        case 38 | 39:
            column = 21
    return float(cursor.fetchall()[0][column]) / 2


window = windowRetirementCalculator()


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "txtYearsOfService" and values["txtYearsOfService"]:
        if values["txtYearsOfService"][-1] not in ("0123456789"):
            window["txtYearsOfService"].update(values["txtYearsOfService"][:-1])
    if event == "txtMonthlyVAPayment" and values["txtMonthlyVAPayment"]:
        if values["txtMonthlyVAPayment"][-1] not in ("0123456789"):
            window["txtMonthlyVAPayment"].update(values["txtMonthlyVAPayment"][:-1])
    if (
        event == "btnCalculate"
        and values["txtDateOfRank"]
        and values["cboPayGrade"]
        and values["txtYearsOfService"]
    ):
        index = grades.index(values["cboPayGrade"])
        year1Index = index
        year2Index = index

        year1 = getPay(
            values["txtYearsOfService"],
            "2023",
            values["cboPayGrade"],
        )
        if getDays(values["txtDateOfRank"]) <= 365:
            year1Index = index - 1
        year2 = getPay(
            int(values["txtYearsOfService"]) - 1,
            "2022",
            grades[year1Index],
        )
        if getDays(values["txtDateOfRank"]) <= 730:
            year2Index = index - 1
        year3 = getPay(
            int(values["txtYearsOfService"]) - 2,
            "2021",
            grades[year2Index],
        )
        retPay = (year1 + year2 + year3) / 3
        vAPay = float(values["txtMonthlyVAPayment"])
        window["txtMonthlyRetirementPay"].update("${:0,.2f}".format(retPay))
        window["txtAnnualPay"].update("${:0,.2f}".format((retPay + vAPay) * 12))
window.close()
