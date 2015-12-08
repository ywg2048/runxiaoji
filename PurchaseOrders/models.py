from django.db import models

# Create your models here.
class MiPurchaseOrderData(models.Model):
    AppId = models.CharField(max_length=80, blank = True, null = True)
    CpOrderId = models.CharField(max_length=40, blank = True, null = True)
    CpUserInfo = models.CharField(max_length=40, blank = True, null = True)     #开发商透传信息
    UId = models.CharField(max_length=40, blank=True, null=True)
    OrderId = models.CharField(max_length=40, blank = True, null = True)
    OrderStatus = models.CharField(max_length=40, blank = True, null = True)
    PayFee = models.CharField(max_length=40, blank = True, null = True)         #支付金额,单位为分,即0.01 米币。
    ProductCode = models.CharField(max_length=40, blank = True, null = True)
    ProductName = models.CharField(max_length=40, blank = True, null = True)
    ProductCount = models.CharField(max_length=40, blank = True, null = True)
    PayTime = models.CharField(max_length=40, blank = True, null = True)
    OrderConsumeType = models.CharField(max_length=40, blank = True, null = True)  #10：普通订单11：直充直消订单
    PartnerGiftConsume = models.CharField(max_length=40, blank = True, null = True)
    Signature = models.CharField(max_length=40, blank = True, null = True)


    def __str__(self):
        return "Appid: %s OrderId: %s ProductName: %s Order Status: %s PayTime: %s" % (self.AppId, self.OrderId, self.ProductName, self.OrderStatus, self.PayTime)