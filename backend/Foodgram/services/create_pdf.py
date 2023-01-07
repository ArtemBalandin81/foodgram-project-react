import io
from typing import TextIO

from reportlab.lib.colors import navy, olive
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def create_pdf(data: list, title: str) -> TextIO:
    """ Создает pdf-файл c помощью ReportLab."""
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    items_per_page = 30
    pdf_pages = max(0, (data.count() - 1)) // items_per_page + 1

    counter = 0

    while counter < pdf_pages:
        pdfmetrics.registerFont(
            TTFont('AlfiosBold', './static/AlfiosBold.ttf')
        )
        pdfmetrics.registerFont(TTFont(
            'AlfiosRegular', './static/AlfiosRegular.ttf')
        )

        p.setFont('AlfiosBold', 24)
        y = 800
        p.setFillColor(olive)
        p.drawString(
            60,
            y,
            f'{title}'
            f' ({1+items_per_page*counter} -'
            f' {min(items_per_page*(counter+1), data.count())}'
            f' поз., стр: {counter+1}/{pdf_pages}):'
        )
        y -= 40

        p.setFont('AlfiosRegular', 16)
        p.setFillColor(navy)
        start_position = counter * items_per_page
        for i in range(start_position, data.count()):
            if y > 30:
                p.drawString(
                    60,
                    y,
                    f'{list(enumerate(data))[i][0]+1}. '  # №
                    f'{list(enumerate(data))[i][1][0].capitalize()} '  # ingredient
                    f'({list(enumerate(data))[i][1][1]}) - '  # measurement_unit
                    f'{list(enumerate(data))[i][1][2]}'  # total
                )
                y -= 25

        p.showPage()
        counter += 1

    p.save()

    buffer.seek(0)

    return buffer
