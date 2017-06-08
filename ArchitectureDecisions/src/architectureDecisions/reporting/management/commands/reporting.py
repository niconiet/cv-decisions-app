#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import sqlite3
from fpdf import FPDF
from ...report_settings import ReportSettings
from django.core.management.base import BaseCommand, CommandError
from ...models import MailAccount
from utils.EmailSender import *
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Command(BaseCommand):
    """
    Command class
    """
    help = 'Reporting'

    def handle(self, *args, **options):
        """
        Command handler
        :param args:
        :param options:
        :return: None
        """
        report()


def pop_not_latin1_characters(text):
    """
    Pops \u2022, \u2013, \u201c and \u201d characters
    :param text: str
    :return: str
    """
    text = str(text).replace('\u2022', '*')
    text = str(text).replace('\u2013', '.')
    text = str(text).replace('\u201c', '\"')
    text = str(text).replace('\u201d', '\"')
    return text


def not_latin1_characters(text):
    """
    If \u2022, \u2013, \u201c and \u201d characters appears in text
    :param text: str
    :return: bool
    """
    return '\u2022' in text or '\u2013' in text or '\u201c' in text or '\u201d' in text


def sqlite3_connector(db):
    """
    Returns cursor
    :param db: path + db name
    :return: cursor
    """
    database = db
    db_connection = sqlite3.connect(database)
    cursor = db_connection.cursor()
    return cursor


def set_title(pdf):
    """
    Sets pdf object title
    :param pdf:
    :return: None
    """
    pdf.set_font('Arial', 'B', 15)
    pdf.cell(0, 20, ReportSettings.title, align='C')


def set_subtitle(pdf):
    """
    Sets pdf object title
    :param pdf:
    :return: None
    """
    pdf.set_xy(9, 30.0)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 15, ReportSettings.subtitle, align='L')


def set_decision(pdf, text):
    """
    Sets decision in pdf object
    :param pdf:
    :param text: str
    :return: None
    """
    pdf.set_font('helvetica', '', 8.0)
    pdf.set_x(25)
    pdf.multi_cell(w=150, h=7, align='L', border=1, txt=text)


def get_project(project_id):
    """
    Returns project name of the given project id
    :param project_id: str
    :return:
    """
    project_cursor = sqlite3_connector(ReportSettings.db_path)
    cursor = project_cursor.execute("select name from projects_project where id = " + project_id)
    for value in cursor:
        return value[0]


def yyyy_dd_mm_to_dd_mm_yyyy(date):
    """
    Converts date string yyyy/dd/mm to dd/mm/yyyy
    :param date:
    ..........str
    :return: date string
    """
    notification_date = date.split("-")
    return notification_date[2] + "-" + notification_date[1] + "-" + notification_date[0]


def report():
    """
    Main function
    :return: None
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=False, margin=10)
    pdf.image(BASE_DIR + '/commands/logo.jpg', 7, 0, 55)
    set_title(pdf)
    set_subtitle(pdf)
    pdf.set_xy(10, 45.0)
    cursor = sqlite3_connector(ReportSettings.db_path)
    cursor.execute("SELECT * FROM decisions_decision where decision_state = 'Tomada' ORDER BY id DESC")
    for decision in cursor:
        notification_date = yyyy_dd_mm_to_dd_mm_yyyy(decision[2])
        project = get_project(str(decision[8]))
        text = str("ID: " + str(decision[0]) +
                   "\nProyecto: " +
                   project +
                   "\nDefinicion: " +
                   decision[3] +
                   "\nFecha: " +
                   notification_date)
        if not_latin1_characters(text):
            text = pop_not_latin1_characters(text)
        if pdf.get_y() > 260:
            pdf.add_page()
        set_decision(pdf, text)
    pdf.output('./' + ReportSettings.attachment_filename + str(datetime.date.today().strftime('%d-%m-%Y')) + '.pdf', 'F')
    email_sender = EmailSender(ReportSettings.body_text,
                               ReportSettings.subject,
                               ReportSettings.from_addr,
                               ReportSettings.to_list,
                               filename=ReportSettings.attachment_filename +
                               str(datetime.date.today().strftime('%d-%m-%Y')) +
                               '.pdf')
    email_sender.send()

