from billboard import ChartData


def get_billboard_chart_data(chart_name="hot-100", date=None):
    chart_data = ChartData(chart_name, date)
    return chart_data