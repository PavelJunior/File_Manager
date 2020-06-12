#!/usr/bin/python3
import os
import shutil
import mimetypes
import time
from datetime import datetime, timedelta


class FolderOrganizer:
    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.marking_file_name = '.marking_file'
        self.file_types = {
            'image': 'Images',
            'video': 'Video',
            'text': 'Text',
            'audio': 'Audio',
            'font': 'Fonts'
        }

    def __get_file_type(self, obj):
        mime = mimetypes.guess_type(obj)[0]
        try:
            file_type = mime.split('/')[0]
            return self.file_types.get(file_type, 'Other')
        except AttributeError:
            return 'Other'

    def __get_timezone_difference(self):
        t = time.localtime()
        if t.tm_isdst == 0:
            return time.timezone
        else:
            return time.altzone

    def __get_folder_name_by_month(self, file_bd, amount):
        file_bd_date = datetime.fromtimestamp(file_bd)
        start_month = (file_bd_date.month // amount * amount) + 1
        period_start_date = file_bd_date.replace(day=1, month=start_month)
        end_month = period_start_date.month + amount - 1
        period_start_date_formatted = period_start_date.strftime("%B")
        if amount == 1:
            return "{} {}".format(period_start_date_formatted, period_start_date.year)
        period_end_date = period_start_date.replace(month=end_month)
        period_end_date_formatted = period_end_date.strftime("%B")
        return "{} - {} {}".format(period_start_date_formatted, period_end_date_formatted, period_end_date.year)

    def __get_folder_name_by_day_or_week(self, file_bd, isDay, amount):
        shift_to_monday = 259200
        timezone_difference = self.__get_timezone_difference()
        day_in_seconds = 86400
        week_in_seconds = day_in_seconds * 7

        if isDay:
            current_period_in_seconds = day_in_seconds * amount
            current_period_in_days = amount
        else:
            current_period_in_seconds = week_in_seconds * amount
            current_period_in_days = amount * 7
        raw_period_start_date_in_seconds = file_bd // current_period_in_seconds * current_period_in_seconds
        period_start_date_in_seconds = raw_period_start_date_in_seconds + timezone_difference - shift_to_monday
        period_start_date = datetime.fromtimestamp(period_start_date_in_seconds)
        if isDay and amount == 1:
            period_start_date_formatted = period_start_date.strftime("%d %B")
            return "{} {}".format(period_start_date_formatted, period_start_date.year)
        period_start_date_formatted = period_start_date.strftime("%d %b")
        period_end_date = period_start_date + timedelta(days=current_period_in_days-1)
        period_end_date_formatted = period_end_date.strftime("%d %b")
        return "{} - {} {}".format(period_start_date_formatted, period_end_date_formatted, period_end_date.year)

    def _get_folder_name_by_date(self, file_bd, frame, amount):
        if frame == 'm':
            return self.__get_folder_name_by_month(file_bd, amount)
        elif frame == 'd' or frame == 'w':
            return self.__get_folder_name_by_day_or_week(file_bd, frame == 'd', amount)
        else:
            raise ValueError("Frame is not correct!")

    def sort_files_by_date(self, time_period='m', amount_of_periods=1):
        list_of_files = os.listdir(self.directory_path)
        for file in list_of_files:
            file_path = os.path.join(self.directory_path, file)
            if file.startswith('.'):
                continue
            if os.path.isdir(file_path) and self.marking_file_name in os.listdir(file_path):
                continue
            file_bd = os.stat(file_path).st_birthtime
            folder_name = self._get_folder_name_by_date(file_bd, time_period, amount_of_periods)

            related_directory_path = os.path.join(self.directory_path, folder_name)
            file_path = os.path.join(self.directory_path, file)
            new_file_path = os.path.join(related_directory_path, file)

            if not os.path.exists(related_directory_path):
                os.mkdir(related_directory_path)
                hidden_file_path = os.path.join(related_directory_path, self.marking_file_name)
                open(hidden_file_path, 'w+').close()
            shutil.move(file_path, new_file_path)

    def sort_files_by_type(self):
        list_of_files = os.listdir(self.directory_path)
        for file in list_of_files:
            file_path = os.path.join(self.directory_path, file)

            if file.startswith('.'):
                continue
            if os.path.isdir(file_path) and self.marking_file_name in os.listdir(file_path):
                continue

            file_type = self.__get_file_type(file)
            related_directory_path = os.path.join(self.directory_path, file_type)

            new_file_path = os.path.join(related_directory_path, file)

            if not os.path.exists(related_directory_path):
                os.mkdir(related_directory_path)
                hidden_file_path = os.path.join(related_directory_path, self.marking_file_name)
                open(hidden_file_path, 'w+').close()

            shutil.move(file_path, new_file_path)


    def sort_files_by_extention(self):
        list_of_files = os.listdir(self.directory_path)
        for file in list_of_files:
            file_path = os.path.join(self.directory_path, file)

            if file.startswith('.'):
                continue
            if os.path.isdir(file_path) and self.marking_file_name in os.listdir(file_path):
                continue
            if os.path.isdir(file_path):
                file_extention = 'folders'
            else:
                file_extention = file.split('.')[-1]
            related_directory_path = os.path.join(self.directory_path, file_extention)

            new_file_path = os.path.join(related_directory_path, file)

            if not os.path.exists(related_directory_path):
                os.mkdir(related_directory_path)
                hidden_file_path = os.path.join(related_directory_path, self.marking_file_name)
                open(hidden_file_path, 'w+').close()

            shutil.move(file_path, new_file_path)

    def sort_files(self, sort_order=['t'], time_period='m', amount_of_periods=1):
        list_of_files = os.listdir(self.directory_path)

        for file in list_of_files:
            file_path = os.path.join(self.directory_path, file)

            if file.startswith('.'):
                continue
            if os.path.isdir(file_path) and self.marking_file_name in os.listdir(file_path):
                continue

            new_file_path = self.directory_path

            for step in sort_order:
                if step == 'd':
                    file_bd = os.stat(file_path).st_birthtime
                    file_time_frame = self._get_folder_name_by_date(file_bd, time_period, amount_of_periods)
                    new_file_path = os.path.join(new_file_path, file_time_frame)
                elif step == 'e':
                    if os.path.isdir(file_path):
                        file_extention = 'folders'
                    else:
                        file_extention = file.split('.')[-1]
                    new_file_path = os.path.join(new_file_path, file_extention)
                elif step == 't':
                    file_type = self.__get_file_type(file)
                    new_file_path = os.path.join(new_file_path, file_type)

                if not os.path.exists(new_file_path):
                    os.mkdir(new_file_path)
                    hidden_file_path = os.path.join(new_file_path, self.marking_file_name)
                    open(hidden_file_path, 'w+').close()

            shutil.move(file_path, new_file_path)
