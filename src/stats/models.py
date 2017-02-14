from datetime import datetime
from django.db import models


def _breakdown_date():
    dt = datetime.now().date()
    return dt.year, dt.month, dt.day


class StatRecord(models.Model):

    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    organisation_id = models.CharField(max_length=64)
    dataset_id = models.CharField(max_length=64)
    dataset_title = models.CharField(max_length=200, blank=True)
    statistic = models.CharField(max_length=32)
    counter = models.IntegerField(default=0)

    def as_dict(self):
        return {
            'day': self.day,
            'month': self.month,
            'year': self.year,
            'organisation_id': self.organisation_id,
            'dataset_id': self.dataset_id,
            'dataset_title': self.dataset_title,
            'statistic': self.statistic,
            'counter': self.counter
        }

    @classmethod
    def record_now(clz, org_id, dataset_id, dataset_title, stat):
        ''' Records an entry for the given dataset and organisation using
        the specific stat label. As we record a counter for the day we may
        end up just updating an existing record '''
        year, month, day = _breakdown_date()
        r,created = clz.objects.get_or_create(
            organisation_id=org_id,
            dataset_id=dataset_id,
            statistic=stat,
            dataset_title=dataset_title,
            year=year, month=month, day=day)
        r.counter = r.counter + 1
        r.save()


    @classmethod
    def record_bulk_now(clz, org_ids, dataset_ids, dataset_titles, stat):
        ''' Records an entry for the given datasets and organisations using
        the specific stat label. As we record a counter for the day we may
        end up just updating an existing record '''
        for n in range(0, len(org_ids)):
            clz.record_now(org_ids[n], dataset_ids[n], dataset_titles[n], stat)

