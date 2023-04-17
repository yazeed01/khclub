from datetime import datetime
def get_date_today(request):
    today = datetime.today()
    return {'today':today}