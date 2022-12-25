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
    pdfmetrics.registerFont(
        TTFont('AlfiosBold', './static/AlfiosBold.ttf')
    )
    pdfmetrics.registerFont(TTFont(
        'AlfiosRegular', './static/AlfiosRegular.ttf')
    )

    p.setFont('AlfiosBold', 24)
    y = 800
    p.setFillColor(olive)
    p.drawString(60, y, f'{title}:')
    y -= 40

    p.setFont('AlfiosRegular', 16)
    p.setFillColor(navy)
    string_number = 1
    for i in data:
        p.drawString(
            60, y,
            f'{string_number}. {i[0].capitalize()} ({i[1]}) - {i[2]}'
        )
        y -= 25
        string_number += 1

    p.showPage()
    p.save()
    buffer.seek(0)

    return buffer
