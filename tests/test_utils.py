# -*- code utf-8 -*-
from datetime import datetime, date, timedelta

from mock import patch

from helpers.config import config
from helpers.sundial import Sundial


def test_sundial():

    with patch('helpers.sundial.date') as mock_date:
        mock_date.today.return_value = date(2019, 6, 2)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

        sundial = Sundial()
        sun = sundial.get_sun()

        with patch('helpers.sundial.datetime') as mock_datetime:
            mock_datetime.now.return_value = sun['sunrise']
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

            assert sundial.is_day() is False

        # DAY mode `DAY_LIGHT_OFFSET` minutes after sunrise.
        with patch('helpers.sundial.datetime') as mock_datetime:
            mock_datetime.now.return_value = sun['sunrise'] \
                + timedelta(minutes=int(config.get('DAY_LIGHT_OFFSET')))
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

            assert sundial.is_day() is True

        # NIGHT mode at sunset
        with patch('helpers.sundial.datetime') as mock_datetime:
            mock_datetime.now.return_value = sun['sunset']
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

            assert sundial.is_day() is False

        # NIGHT mode `DAY_LIGHT_OFFSET` minutes before sunset
        with patch('helpers.sundial.datetime') as mock_datetime:
            mock_datetime.now.return_value = sun['sunset'] \
                - timedelta(minutes=int(config.get('DAY_LIGHT_OFFSET')))
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

            assert sundial.is_day() is False

        # DAY mode `DAY_LIGHT_OFFSET` minutes and 1 sec. before sunset
        with patch('helpers.sundial.datetime') as mock_datetime:
            mock_datetime.now.return_value = sun['sunset'] \
                - timedelta(minutes=int(config.get('DAY_LIGHT_OFFSET')),
                            seconds=1)
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

            assert sundial.is_day() is True
