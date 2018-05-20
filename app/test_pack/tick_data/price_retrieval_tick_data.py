from datetime import timedelta, date

from quant.dao import price_retrieval_tick_data


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)




if __name__ == "__main__":
    #price_retrieval_tick_data('600179','2018-05-02')
    start_date = date(2018, 5, 3)
    end_date = date(2018, 5, 4)
    for single_date in daterange(start_date, end_date):
        price_retrieval_tick_data('600179', single_date.strftime('%Y-%m-%d'))

