from jalali_date import date2jalali

from django import template

register = template.Library()


# @register.filter
def gregorian_to_jalali(date):
    print(date)
    jalali_date = date2jalali(date)
    day_name = jalali_date.strftime('%A')
    month_name = jalali_date.strftime('%B')

    # Mapping Persian month names
    persian_month_names = {
        'Farvardin': 'فروردین',
        'Ordibehesht': 'اردیبهشت',
        'Khordad': 'خرداد',
        'Tir': 'تیر',
        'Mordad': 'مرداد',
        'Shahrivar': 'شهریور',
        'Mehr': 'مهر',
        'Aban': 'آبان',
        'Azar': 'آذر',
        'Dey': 'دی',
        'Bahman': 'بهمن',
        'Esfand': 'اسفند',
    }

    # Mapping Persian weekday names
    persian_weekday_names = {
        'Saturday': 'شنبه',
        'Sunday': 'یک‌شنبه',
        'Monday': 'دوشنبه',
        'Tuesday': 'سه‌شنبه',
        'Wednesday': 'چهارشنبه',
        'Thursday': 'پنج‌شنبه',
        'Friday': 'جمعه',
    }

    jalali_month_name = persian_month_names.get(month_name, month_name)
    jalali_weekday_name = persian_weekday_names.get(day_name, day_name)

    return f'{jalali_weekday_name} {jalali_date.day} {jalali_month_name} {jalali_date.year}'
