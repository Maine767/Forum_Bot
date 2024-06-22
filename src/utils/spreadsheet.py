import gspread

class SpreadSheet():
    def __init__():
        gc = gspread.service_account(filename='telegramm-bot-391616-8b3ffc75a2df.json')

    def open(self, start_sheet):
        sheet = self.gc.open("Work Tool")
        worksheet = sheet.worksheet(start_sheet)
        worksheet_registration = sheet.worksheet("Зарегистрирован")
        worksheet_send = sheet.worksheet("Отобранные")


Tests = "Новые ответы"
Work_version = "Начали (start)"
