from django.db import models

# Create your models here.

class CustomerConfig(models.Model):
    """Base Customers config: sever type, sv adress, log/pass to server.."""
    class Meta:
        db_table = "Customer_config"

    customer_id = models.IntegerField()
    customer_name = models.CharField(max_length=100)
    customer_conn_type = models.CharField(max_length=10)
    customer_sv_adr = models.CharField(max_length=100)
    customer_log = models.CharField(max_length=100)
    customer_pass = models.CharField(max_length=100)
    customer_sv_type = models.CharField(max_length=25)


class CardIndent(models.Model):
    """Identification cards table"""
    class Meta:
        db_table = "card"

    card_id = models.IntegerField()
    card_name = models.CharField(max_length=100)
    card_customer = models.ForeignKey(CustomerConfig)


class WareHouse(models.Model):
    class Meta:
        db_table = 'ware house'

    ware_id = models.CharField(max_length=15)
    ware_in = models.FloatField()
    ware_customer = models.ForeignKey(CustomerConfig)


class TrkConfig(models.Model):
    class Meta:
        db_table = "trk_config"

    trk_oid = models.IntegerField()
    trk_name = models.CharField(max_length=10)
    client_sensors_name = models.CharField(max_length=200)
    trk_type = models.IntegerField(default=0)
    trk_cln_id = models.IntegerField(default=0)
    trk_customer = models.ForeignKey(CustomerConfig)


class FuelReports(models.Model):
    class Meta:
        db_table = 'report_days'

    fuel_data = models.TextField()
    fuel_number = models.IntegerField(default=0)
    fuel_trk_name = models.CharField(max_length=10)
    fuel_summary_out = models.IntegerField(default=0)
    fuel_summary_in = models.IntegerField(default=0)
    fuel_customer = models.ForeignKey(CustomerConfig)


class FuelOut(models.Model):
    class Meta:
        db_table = "out_fuel"

    fuel_id = models.IntegerField(default=0)
    fuel_out_start = models.DateTimeField()
    fuel_out_end = models.DateTimeField()
    fuel_in_quantity = models.FloatField(default=0.00)
    fuel_out_quantity = models.FloatField(default=0.00)
    fuel_out_rfid = models.IntegerField(default=0)
    fuel_out_name = models.CharField(max_length=100)
    fuel_out_wh = models.CharField(max_length=100)
    fuel_trk = models.ForeignKey(TrkConfig)
    fuel_customer = models.ForeignKey(CustomerConfig)












