
import random
import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

class Accounttitle(models.Model):
    label = models.TextField()
    orgid = models.ForeignKey('Organization', models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.
    code = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'AccountTitle'
        unique_together = (('orgid', 'label'),)


class Attendance(models.Model):
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    shiftid = models.ForeignKey('Shift', models.DO_NOTHING, db_column='shiftId')  # Field name made lowercase.
    shiftdate = models.DateTimeField(db_column='shiftDate')  # Field name made lowercase.
    timein = models.DateTimeField(db_column='timeIn', blank=True, null=True)  # Field name made lowercase.
    timeout = models.DateTimeField(db_column='timeOut', blank=True, null=True)  # Field name made lowercase.
    breakstart = models.DateTimeField(db_column='breakStart', blank=True, null=True)  # Field name made lowercase.
    breakend = models.DateTimeField(db_column='breakEnd', blank=True, null=True)  # Field name made lowercase.
    photoin = models.TextField(db_column='photoIn', blank=True, null=True)  # Field name made lowercase.
    photoout = models.TextField(db_column='photoOut', blank=True, null=True)  # Field name made lowercase.
    photobreakstart = models.TextField(db_column='photoBreakStart', blank=True, null=True)  # Field name made lowercase.
    photobreakend = models.TextField(db_column='photoBreakEnd', blank=True, null=True)  # Field name made lowercase.
    status = models.TextField()  # This field type is a guess.
    orgid = models.ForeignKey('Organization', models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.
    notebreakend = models.TextField(db_column='noteBreakEnd', blank=True, null=True)  # Field name made lowercase.
    notebreakstart = models.TextField(db_column='noteBreakStart', blank=True, null=True)  # Field name made lowercase.
    notein = models.TextField(db_column='noteIn', blank=True, null=True)  # Field name made lowercase.
    noteout = models.TextField(db_column='noteOut', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Attendance'
        unique_together = (('userid', 'shiftdate'),)


class Auditlog(models.Model):
    id = models.TextField(primary_key=True)
    orgid = models.IntegerField(db_column='orgId')  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    pagekey = models.TextField(db_column='pageKey')  # Field name made lowercase.
    action = models.TextField()  # This field type is a guess.
    recordid = models.TextField(db_column='recordId', blank=True, null=True)  # Field name made lowercase.
    recordtype = models.TextField(db_column='recordType', blank=True, null=True)  # Field name made lowercase.
    oldvalue = models.JSONField(db_column='oldValue', blank=True, null=True)  # Field name made lowercase.
    newvalue = models.JSONField(db_column='newValue', blank=True, null=True)  # Field name made lowercase.
    ipaddress = models.TextField(db_column='ipAddress', blank=True, null=True)  # Field name made lowercase.
    useragent = models.TextField(db_column='userAgent', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AuditLog'


class Branch(models.Model):
    name = models.TextField()
    address = models.TextField()
    phone = models.TextField(blank=True, null=True)
    isactive = models.BooleanField(db_column='isActive')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    orgid = models.ForeignKey('Organization', models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.
    ownerid = models.ForeignKey('User', models.DO_NOTHING, db_column='ownerId')  # Field name made lowercase.
    locationid = models.IntegerField(db_column='locationId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Branch'
        unique_together = (('orgid', 'name'),)


class Brand(models.Model):
    email = models.TextField(blank=True, null=True)
    weburl = models.TextField(db_column='webUrl', blank=True, null=True)  # Field name made lowercase.
    contactnumber = models.TextField(db_column='contactNumber', blank=True, null=True)  # Field name made lowercase.
    name = models.TextField(unique=True)
    orgid = models.ForeignKey('Organization', models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Brand'
        unique_together = (('orgid', 'name'),)


class Budget(models.Model):
    year = models.IntegerField()
    account = models.TextField()
    begbal = models.FloatField(db_column='begBal')  # Field name made lowercase.
    months = models.JSONField()
    orgid = models.ForeignKey('Organization', models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Budget'


class Cartitem(models.Model):
    pk = models.CompositePrimaryKey('transactionId', 'itemId')
    transactionid = models.ForeignKey('Transaction', models.DO_NOTHING, db_column='transactionId')  # Field name made lowercase.
    itemid = models.ForeignKey('Item', models.DO_NOTHING, db_column='itemId')  # Field name made lowercase.
    quantity = models.FloatField()
    priceatsale = models.FloatField(db_column='priceAtSale')  # Field name made lowercase.
    unitid = models.ForeignKey('Inventoryitemunit', models.DO_NOTHING, db_column='unitId', blank=True, null=True)  # Field name made lowercase.
    unitname = models.TextField(db_column='unitName', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CartItem'


class Center(models.Model):
    label = models.TextField()
    orgid = models.ForeignKey('Organization', models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Center'
        unique_together = (('orgid', 'label'),)


class Color(models.Model):
    name = models.TextField(unique=True)
    hexcode = models.TextField(db_column='hexCode', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Color'


class Contact(models.Model):
    orgid = models.ForeignKey('Organization', models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.
    branchid = models.ForeignKey(Branch, models.DO_NOTHING, db_column='branchId', blank=True, null=True)  # Field name made lowercase.
    label = models.TextField()
    name = models.TextField()
    email = models.TextField()
    phone = models.TextField(blank=True, null=True)
    position = models.TextField(blank=True, null=True)
    department = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    isactive = models.BooleanField(db_column='isActive')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Contact'


class Costlines(models.Model):
    itemid = models.ForeignKey('Item', models.DO_NOTHING, db_column='itemId')  # Field name made lowercase.
    label = models.TextField()
    amount = models.FloatField()

    class Meta:
        managed = False
        db_table = 'CostLines'


class Customerdetails(models.Model):
    fullname = models.TextField(blank=True, null=True)
    username = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    phonenumber = models.TextField(db_column='phoneNumber', blank=True, null=True)  # Field name made lowercase.
    paymenttype = models.TextField(db_column='paymentType')  # Field name made lowercase. This field type is a guess.
    paymentmethodid = models.TextField(db_column='paymentMethodId', blank=True, null=True)  # Field name made lowercase.
    paymentintentid = models.TextField(db_column='paymentIntentId', blank=True, null=True)  # Field name made lowercase.
    client_key = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    transactionid = models.OneToOneField('Transaction', models.DO_NOTHING, db_column='transactionId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CustomerDetails'


class Customerdevicetoken(models.Model):
    customerid = models.ForeignKey('Kompracustomer', models.DO_NOTHING, db_column='customerId')  # Field name made lowercase.
    token = models.TextField(unique=True)
    platform = models.TextField()
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CustomerDeviceToken'


class Deliveryaddress(models.Model):
    customerid = models.ForeignKey('Kompracustomer', models.DO_NOTHING, db_column='customerId')  # Field name made lowercase.
    label = models.TextField()
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    isdefault = models.BooleanField(db_column='isDefault')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DeliveryAddress'


class Department(models.Model):
    label = models.TextField()
    color = models.TextField(blank=True, null=True)
    orgid = models.ForeignKey('Organization', models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Department'
        unique_together = (('orgid', 'label'),)


class Employee(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    role = models.TextField()
    department = models.TextField()
    status = models.TextField()  # This field type is a guess.
    salary = models.FloatField()
    hiredate = models.DateTimeField(db_column='hireDate')  # Field name made lowercase.
    email = models.TextField(unique=True)
    orgid = models.ForeignKey('Organization', models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Employee'
        unique_together = (('orgid', 'email'),)


class Gisrow(models.Model):
    main = models.TextField()
    group = models.TextField()
    code = models.TextField()
    description = models.TextField()
    debit = models.FloatField()
    credit = models.FloatField()
    total = models.FloatField()
    orgid = models.ForeignKey('Organization', models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    accounttitleid = models.ForeignKey(Accounttitle, models.DO_NOTHING, db_column='accountTitleId')  # Field name made lowercase.
    centerid = models.ForeignKey(Center, models.DO_NOTHING, db_column='centerId')  # Field name made lowercase.
    subcenterid = models.ForeignKey('Subcenter', models.DO_NOTHING, db_column='subCenterId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GISRow'


class Inventory(models.Model):
    name = models.TextField(blank=True, null=True)
    outletid = models.OneToOneField('Outlet', models.DO_NOTHING, db_column='outletId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Inventory'


class Inventoryitem(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    sku = models.TextField()
    stock = models.IntegerField()
    minstock = models.IntegerField(db_column='minStock')  # Field name made lowercase.
    category = models.TextField()
    price = models.FloatField()
    lowstock = models.BooleanField(db_column='lowStock')  # Field name made lowercase.
    orgid = models.ForeignKey('Organization', models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'InventoryItem'


class Inventoryitemunit(models.Model):
    inventoryitemid = models.ForeignKey('Inventoryitems', models.DO_NOTHING, db_column='inventoryItemId')  # Field name made lowercase.
    unitname = models.TextField(db_column='unitName')  # Field name made lowercase.
    unitlabel = models.TextField(db_column='unitLabel')  # Field name made lowercase.
    price = models.FloatField()
    quantity = models.FloatField()
    conversionfactor = models.FloatField(db_column='conversionFactor')  # Field name made lowercase.
    baseunit = models.TextField(db_column='baseUnit')  # Field name made lowercase.
    barcode = models.TextField(blank=True, null=True)
    isdefault = models.BooleanField(db_column='isDefault')  # Field name made lowercase.
    isactive = models.BooleanField(db_column='isActive')  # Field name made lowercase.
    minorderqty = models.FloatField(db_column='minOrderQty', blank=True, null=True)  # Field name made lowercase.
    maxorderqty = models.FloatField(db_column='maxOrderQty', blank=True, null=True)  # Field name made lowercase.
    reorderpoint = models.FloatField(db_column='reorderPoint', blank=True, null=True)  # Field name made lowercase.
    allowdecimal = models.BooleanField(db_column='allowDecimal')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'InventoryItemUnit'
        unique_together = (('inventoryitemid', 'unitname'),)

class Inventoryitems(models.Model):
    inventoryid = models.ForeignKey(Inventory, models.DO_NOTHING, db_column='inventoryId')  # Field name made lowercase.
    itemid = models.ForeignKey('Item', models.DO_NOTHING, db_column='itemId')  # Field name made lowercase.
    price = models.FloatField()
    quantity = models.IntegerField()
    locationid = models.OneToOneField('Location', models.DO_NOTHING, db_column='locationId', blank=True, null=True)  # Field name made lowercase.
    categoryid = models.ForeignKey('Itemcategory', models.DO_NOTHING, db_column='categoryId', blank=True, null=True)  # Field name made lowercase.
    baseunit = models.TextField(db_column='baseUnit')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'InventoryItems'
        unique_together = (('inventoryid', 'itemid'),)


class Item(models.Model):
    name = models.TextField(unique=True)
    image = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    barcode = models.TextField()
    brand = models.TextField(blank=True, null=True)
    orgid = models.ForeignKey('Organization', models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.
    categoryid = models.ForeignKey('Itemcategory', models.DO_NOTHING, db_column='categoryId', blank=True, null=True)  # Field name made lowercase.
    brandid = models.ForeignKey(Brand, models.DO_NOTHING, db_column='brandId', blank=True, null=True)  # Field name made lowercase.
    servicecharge = models.BooleanField(db_column='ServiceCharge')  # Field name made lowercase.
    assembly = models.BooleanField()
    itemcode = models.TextField(db_column='itemCode', blank=True, null=True)  # Field name made lowercase.
    skunumber = models.TextField(db_column='skuNumber', blank=True, null=True)  # Field name made lowercase.
    vatexempt = models.BooleanField(db_column='vatExempt', blank=True, null=True)  # Field name made lowercase.
    stock = models.FloatField()
    sellingprice = models.FloatField(db_column='sellingPrice')  # Field name made lowercase.
    minquantity = models.FloatField(db_column='minQuantity')  # Field name made lowercase.
    opexpct = models.FloatField(db_column='opExPct')  # Field name made lowercase.
    priceb = models.FloatField(db_column='priceB', blank=True, null=True)  # Field name made lowercase.
    pricec = models.FloatField(db_column='priceC', blank=True, null=True)  # Field name made lowercase.
    totalcost = models.FloatField(db_column='totalCost')  # Field name made lowercase.
    expiryenddate = models.DateTimeField(db_column='expiryEndDate', blank=True, null=True)  # Field name made lowercase.
    expirystartdate = models.DateTimeField(db_column='expiryStartDate', blank=True, null=True)  # Field name made lowercase.
    exactexpirydate = models.DateTimeField(db_column='exactExpiryDate', blank=True, null=True)  # Field name made lowercase.
    orgcategoryid = models.ForeignKey('Orgitemcategory', models.DO_NOTHING, db_column='orgCategoryId', blank=True, null=True)  # Field name made lowercase.
    vattypeid = models.ForeignKey('Vattype', models.DO_NOTHING, db_column='vatTypeId', blank=True, null=True)  # Field name made lowercase.
    stockdescription = models.TextField(db_column='stockDescription', blank=True, null=True)  # Field name made lowercase.
    stocklabel = models.TextField(db_column='stockLabel', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Item'
        unique_together = (('orgid', 'name'),)


class Itemcategory(models.Model):
    name = models.TextField(unique=True)
    description = models.TextField(blank=True, null=True)
    grouptype = models.TextField(db_column='groupType', blank=True, null=True)  # Field name made lowercase.
    sales = models.TextField(blank=True, null=True)
    stocks = models.TextField(blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    icon = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ItemCategory'


class Itemcategorymap(models.Model):
    pk = models.CompositePrimaryKey('itemId', 'categoryId')
    itemid = models.ForeignKey(Item, models.DO_NOTHING, db_column='itemId')  # Field name made lowercase.
    categoryid = models.ForeignKey('Orgitemcategory', models.DO_NOTHING, db_column='categoryId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ItemCategoryMap'



class Itemgroup(models.Model):
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    icon = models.TextField(blank=True, null=True)
    isactive = models.BooleanField(db_column='isActive')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    orgid = models.ForeignKey('Organization', models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ItemGroup'
        unique_together = (('orgid', 'name'),)


class Itemunit(models.Model):
    unitname = models.TextField(db_column='unitName', unique=True)  # Field name made lowercase.
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ItemUnit'


class Kompracdeliverytracking(models.Model):
    orderid = models.ForeignKey('Kompracorder', models.DO_NOTHING, db_column='orderId')  # Field name made lowercase.
    event = models.TextField()  # This field type is a guess.
    statusat = models.DateTimeField(db_column='statusAt')  # Field name made lowercase.
    currentlat = models.FloatField(db_column='currentLat', blank=True, null=True)  # Field name made lowercase.
    currentlng = models.FloatField(db_column='currentLng', blank=True, null=True)  # Field name made lowercase.
    note = models.TextField(blank=True, null=True)
    actortype = models.TextField(db_column='actorType')  # Field name made lowercase.
    actorid = models.IntegerField(db_column='actorId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KompraCDeliveryTracking'


class Kompracorder(models.Model):
    transactionnumber = models.TextField(db_column='transactionNumber', unique=True)  # Field name made lowercase.
    customerid = models.ForeignKey('Kompracustomer', models.DO_NOTHING, db_column='customerId')  # Field name made lowercase.
    outletid = models.ForeignKey('Outlet', models.DO_NOTHING, db_column='outletId')  # Field name made lowercase.
    deliveryaddressid = models.ForeignKey(Deliveryaddress, models.DO_NOTHING, db_column='deliveryAddressId')  # Field name made lowercase.
    subtotal = models.FloatField()
    total = models.FloatField()
    status = models.TextField()  # This field type is a guess.
    scheduleddeliveryat = models.DateTimeField(db_column='scheduledDeliveryAt', blank=True, null=True)  # Field name made lowercase.
    estimateddeliveryat = models.DateTimeField(db_column='estimatedDeliveryAt', blank=True, null=True)  # Field name made lowercase.
    deliveredat = models.DateTimeField(db_column='deliveredAt', blank=True, null=True)  # Field name made lowercase.
    paymentmethod = models.TextField(db_column='paymentMethod')  # Field name made lowercase. This field type is a guess.
    paymentstatus = models.TextField(db_column='paymentStatus')  # Field name made lowercase.
    paymentreference = models.TextField(db_column='paymentReference', blank=True, null=True)  # Field name made lowercase.
    ridername = models.TextField(db_column='riderName', blank=True, null=True)  # Field name made lowercase.
    riderphone = models.TextField(db_column='riderPhone', blank=True, null=True)  # Field name made lowercase.
    customernote = models.TextField(db_column='customerNote', blank=True, null=True)  # Field name made lowercase.
    outletnote = models.TextField(db_column='outletNote', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KompraCOrder'


class Kompracorderfee(models.Model):
    orderid = models.ForeignKey(Kompracorder, models.DO_NOTHING, db_column='orderId')  # Field name made lowercase.
    type = models.TextField()  # This field type is a guess.
    label = models.TextField()
    amount = models.FloatField()

    class Meta:
        managed = False
        db_table = 'KompraCOrderFee'


class Kompracorderitem(models.Model):
    orderid = models.ForeignKey(Kompracorder, models.DO_NOTHING, db_column='orderId')  # Field name made lowercase.
    inventoryitemid = models.ForeignKey(Inventoryitems, models.DO_NOTHING, db_column='inventoryItemId')  # Field name made lowercase.
    itemid = models.ForeignKey(Item, models.DO_NOTHING, db_column='itemId')  # Field name made lowercase.
    quantity = models.IntegerField()
    pricesnapshot = models.FloatField(db_column='priceSnapshot')  # Field name made lowercase.
    subtotal = models.FloatField()
    unitid = models.ForeignKey(Inventoryitemunit, models.DO_NOTHING, db_column='unitId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KompraCOrderItem'
        unique_together = (('orderid', 'inventoryitemid'),)


class Kompracustomer(models.Model):
    fullname = models.TextField()
    email = models.TextField(unique=True)
    passwordhash = models.TextField(db_column='passwordHash')  # Field name made lowercase.
    profilephoto = models.TextField(db_column='profilePhoto', blank=True, null=True)  # Field name made lowercase.
    isverified = models.BooleanField(db_column='isVerified')  # Field name made lowercase.
    isactive = models.BooleanField(db_column='isActive')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.
    phone = models.TextField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'KompraCustomer'


class Location(models.Model):
    aisle = models.TextField(blank=True, null=True)
    rack = models.TextField(blank=True, null=True)
    shelf = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Location'


class Media(models.Model):
    url = models.TextField()
    type = models.TextField(blank=True, null=True)  # This field type is a guess.
    itemid = models.ForeignKey(Item, models.DO_NOTHING, db_column='itemId', blank=True, null=True)  # Field name made lowercase.
    sortorder = models.IntegerField(db_column='sortOrder')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Media'


class Notification(models.Model):
    orgid = models.ForeignKey('Organization', models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.
    outletid = models.ForeignKey('Outlet', models.DO_NOTHING, db_column='outletId', blank=True, null=True)  # Field name made lowercase.
    itemid = models.ForeignKey(Item, models.DO_NOTHING, db_column='itemId', blank=True, null=True)  # Field name made lowercase.
    type = models.TextField()  # This field type is a guess.
    title = models.TextField()
    message = models.TextField()
    isread = models.BooleanField(db_column='isRead')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Notification'


class Orgitemcategory(models.Model):
    orgid = models.ForeignKey('Organization', models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.
    categoryid = models.ForeignKey(Itemcategory, models.DO_NOTHING, db_column='categoryId', blank=True, null=True)  # Field name made lowercase.
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    icon = models.TextField(blank=True, null=True)
    cost_of_sale = models.TextField(blank=True, null=True)
    grouptype = models.TextField(db_column='groupType', blank=True, null=True)  # Field name made lowercase.
    sales = models.TextField(blank=True, null=True)
    stocks = models.TextField(blank=True, null=True)
    groupid = models.ForeignKey(Itemgroup, models.DO_NOTHING, db_column='groupId', blank=True, null=True)  # Field name made lowercase.
    isactive = models.BooleanField(db_column='isActive')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OrgItemCategory'
        unique_together = (('orgid', 'name'),)


class Organization(models.Model):
    name = models.TextField()
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    bannerimg = models.TextField(db_column='bannerImg', blank=True, null=True)  # Field name made lowercase.
    contactnumber = models.TextField(db_column='contactNumber', blank=True, null=True)  # Field name made lowercase.
    email = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    profilephoto = models.TextField(db_column='profilePhoto', blank=True, null=True)  # Field name made lowercase.
    facebooklink = models.TextField(db_column='facebookLink', blank=True, null=True)  # Field name made lowercase.
    instagramlink = models.TextField(db_column='instagramLink', blank=True, null=True)  # Field name made lowercase.
    twitterlink = models.TextField(db_column='twitterLink', blank=True, null=True)  # Field name made lowercase.
    bio = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Organization'


class Outlet(models.Model):
    name = models.TextField()
    address = models.TextField()
    phone = models.TextField(blank=True, null=True)
    code = models.TextField(unique=True)
    nexttransactionnumber = models.IntegerField(db_column='nextTransactionNumber', blank=True, null=True)  # Field name made lowercase.
    governmenttax = models.FloatField(db_column='governmentTax', blank=True, null=True)  # Field name made lowercase.
    servicecharge = models.FloatField(db_column='serviceCharge', blank=True, null=True)  # Field name made lowercase.
    outlettype = models.TextField(db_column='outletType')  # Field name made lowercase. This field type is a guess.
    isactive = models.BooleanField(db_column='isActive')  # Field name made lowercase.
    wifissid = models.TextField(db_column='wifiSSID', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    orgid = models.ForeignKey(Organization, models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.
    branchid = models.ForeignKey(Branch, models.DO_NOTHING, db_column='branchId', blank=True, null=True)  # Field name made lowercase.
    ownerid = models.ForeignKey('User', models.DO_NOTHING, db_column='ownerId')  # Field name made lowercase.
    apikeyid = models.ForeignKey('Paymongoapikeys', models.DO_NOTHING, db_column='apiKeyId', blank=True, null=True)  # Field name made lowercase.
    haskey = models.BooleanField(db_column='hasKey')  # Field name made lowercase.
    status = models.TextField()  # This field type is a guess.
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    bannerimage = models.TextField(db_column='bannerImage', blank=True, null=True)  # Field name made lowercase.
    bir = models.TextField(blank=True, null=True)
    isvatregistered = models.BooleanField(db_column='isVatRegistered')  # Field name made lowercase.
    ptu = models.TextField(blank=True, null=True)
    tin = models.TextField(blank=True, null=True)
    vattypeid = models.ForeignKey('Vattype', models.DO_NOTHING, db_column='vatTypeId', blank=True, null=True)  # Field name made lowercase.
    vatzerosale = models.FloatField(db_column='vatZeroSale', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Outlet'
        unique_together = (('orgid', 'code'),)


class Outletdeliveryconfig(models.Model):
    outletid = models.OneToOneField(Outlet, models.DO_NOTHING, db_column='outletId')  # Field name made lowercase.
    isdeliveryactive = models.BooleanField(db_column='isDeliveryActive')  # Field name made lowercase.
    deliveryradiuskm = models.FloatField(db_column='deliveryRadiusKm')  # Field name made lowercase.
    basedeliveryfee = models.FloatField(db_column='baseDeliveryFee')  # Field name made lowercase.
    feeperkm = models.FloatField(db_column='feePerKm')  # Field name made lowercase.
    minorderamount = models.FloatField(db_column='minOrderAmount', blank=True, null=True)  # Field name made lowercase.
    maxorderamount = models.FloatField(db_column='maxOrderAmount', blank=True, null=True)  # Field name made lowercase.
    avgprepmins = models.IntegerField(db_column='avgPrepMins')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OutletDeliveryConfig'


class Outletitemsearchindex(models.Model):
    outletid = models.ForeignKey(Outlet, models.DO_NOTHING, db_column='outletId')  # Field name made lowercase.
    itemid = models.ForeignKey(Item, models.DO_NOTHING, db_column='itemId')  # Field name made lowercase.
    inventoryitemid = models.OneToOneField(Inventoryitems, models.DO_NOTHING, db_column='inventoryItemId')  # Field name made lowercase.
    quantity = models.IntegerField()
    price = models.FloatField()
    outletlatitude = models.FloatField(db_column='outletLatitude')  # Field name made lowercase.
    outletlongitude = models.FloatField(db_column='outletLongitude')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OutletItemSearchIndex'
        unique_together = (('outletid', 'itemid'),)


class Outletpromo(models.Model):
    outletid = models.ForeignKey(Outlet, models.DO_NOTHING, db_column='outletId')  # Field name made lowercase.
    promotypeid = models.ForeignKey('Promotype', models.DO_NOTHING, db_column='promoTypeId')  # Field name made lowercase.
    discount = models.FloatField()
    isactive = models.BooleanField(db_column='isActive')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    vatable = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'OutletPromo'
        unique_together = (('outletid', 'promotypeid'),)


class Outletstaff(models.Model):
    outletid = models.ForeignKey(Outlet, models.DO_NOTHING, db_column='outletId')  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    role = models.TextField()  # This field type is a guess.
    ispresent = models.BooleanField(db_column='isPresent')  # Field name made lowercase.
    logintime = models.DateTimeField(db_column='logInTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OutletStaff'
        unique_together = (('outletid', 'userid'),)


class Page(models.Model):
    id = models.TextField(primary_key=True)
    key = models.TextField(unique=True)
    label = models.TextField()
    parentkey = models.TextField(db_column='parentKey', blank=True, null=True)  # Field name made lowercase.
    sortorder = models.IntegerField(db_column='sortOrder')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Page'


class Paymongoapikeys(models.Model):
    public_key = models.TextField()
    secret_key = models.TextField()
    ownerid = models.OneToOneField('User', models.DO_NOTHING, db_column='ownerId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PaymongoAPIKeys'


class Placelocation(models.Model):
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    branchid = models.OneToOneField(Branch, models.DO_NOTHING, db_column='branchId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PlaceLocation'


class Position(models.Model):
    id = models.TextField(primary_key=True)
    orgid = models.ForeignKey(Organization, models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    description = models.TextField(blank=True, null=True)
    name = models.TextField()
    permissionsversion = models.DateTimeField(db_column='permissionsVersion')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Position'


class Positioncontrolpermission(models.Model):
    id = models.TextField(primary_key=True)
    positionid = models.ForeignKey(Position, models.DO_NOTHING, db_column='positionId')  # Field name made lowercase.
    controlkey = models.TextField(db_column='controlKey')  # Field name made lowercase.
    isallowed = models.BooleanField(db_column='isAllowed')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PositionControlPermission'


class Positionpermission(models.Model):
    id = models.TextField(primary_key=True)
    positionid = models.ForeignKey(Position, models.DO_NOTHING, db_column='positionId')  # Field name made lowercase.
    pageid = models.ForeignKey(Page, models.DO_NOTHING, db_column='pageId')  # Field name made lowercase.
    canview = models.BooleanField(db_column='canView')  # Field name made lowercase.
    cancreate = models.BooleanField(db_column='canCreate')  # Field name made lowercase.
    canedit = models.BooleanField(db_column='canEdit')  # Field name made lowercase.
    candelete = models.BooleanField(db_column='canDelete')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PositionPermission'


class Promotype(models.Model):
    name = models.TextField(unique=True)
    description = models.TextField(blank=True, null=True)
    isactive = models.BooleanField(db_column='isActive')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    orgid = models.ForeignKey(Organization, models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PromoType'
        unique_together = (('orgid', 'name'),)


class Restockcycle(models.Model):
    scheduleid = models.ForeignKey('Restockschedule', models.DO_NOTHING, db_column='scheduleId')  # Field name made lowercase.
    orgid = models.ForeignKey(Organization, models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.
    scheduledat = models.DateTimeField(db_column='scheduledAt')  # Field name made lowercase.
    emailrecipient = models.TextField(db_column='emailRecipient')  # Field name made lowercase.
    emailsubject = models.TextField(db_column='emailSubject', blank=True, null=True)  # Field name made lowercase.
    emailbody = models.TextField(db_column='emailBody', blank=True, null=True)  # Field name made lowercase.
    isactive = models.BooleanField(db_column='isActive')  # Field name made lowercase.
    firedat = models.DateTimeField(db_column='firedAt', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.
    address = models.TextField(blank=True, null=True)
    branchid = models.ForeignKey(Branch, models.DO_NOTHING, db_column='branchId', blank=True, null=True)  # Field name made lowercase.
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    outletid = models.ForeignKey(Outlet, models.DO_NOTHING, db_column='outletId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RestockCycle'


class Restockcycleitem(models.Model):
    cycleid = models.ForeignKey(Restockcycle, models.DO_NOTHING, db_column='cycleId')  # Field name made lowercase.
    itemid = models.ForeignKey(Item, models.DO_NOTHING, db_column='itemId')  # Field name made lowercase.
    quantity = models.FloatField()

    class Meta:
        managed = False
        db_table = 'RestockCycleItem'
        unique_together = (('cycleid', 'itemid'),)


class Restockschedule(models.Model):
    orgid = models.ForeignKey(Organization, models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.
    recurrence = models.TextField()  # This field type is a guess.
    startdate = models.DateTimeField(db_column='startDate')  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='endDate', blank=True, null=True)  # Field name made lowercase.
    timeofday = models.TextField(db_column='timeOfDay')  # Field name made lowercase.
    dayofweek = models.IntegerField(db_column='dayOfWeek', blank=True, null=True)  # Field name made lowercase.
    dayofmonth = models.IntegerField(db_column='dayOfMonth', blank=True, null=True)  # Field name made lowercase.
    emailrecipient = models.TextField(db_column='emailRecipient')  # Field name made lowercase.
    emailfrom = models.TextField(db_column='emailFrom', blank=True, null=True)  # Field name made lowercase.
    emailsubject = models.TextField(db_column='emailSubject', blank=True, null=True)  # Field name made lowercase.
    emailbody = models.TextField(db_column='emailBody', blank=True, null=True)  # Field name made lowercase.
    isactive = models.BooleanField(db_column='isActive')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.
    lasttriggeredat = models.DateTimeField(db_column='lastTriggeredAt', blank=True, null=True)  # Field name made lowercase.
    customtimes = models.JSONField(db_column='customTimes', blank=True, null=True)  # Field name made lowercase.
    branchid = models.ForeignKey(Branch, models.DO_NOTHING, db_column='branchId', blank=True, null=True)  # Field name made lowercase.
    outletid = models.ForeignKey(Outlet, models.DO_NOTHING, db_column='outletId', blank=True, null=True)  # Field name made lowercase.
    address = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'RestockSchedule'


class Restockscheduleitem(models.Model):
    scheduleid = models.ForeignKey(Restockschedule, models.DO_NOTHING, db_column='scheduleId')  # Field name made lowercase.
    itemid = models.ForeignKey(Item, models.DO_NOTHING, db_column='itemId')  # Field name made lowercase.
    quantity = models.FloatField()
    dayofmonth = models.IntegerField(db_column='dayOfMonth', blank=True, null=True)  # Field name made lowercase.
    dayofweek = models.IntegerField(db_column='dayOfWeek', blank=True, null=True)  # Field name made lowercase.
    timeofday = models.TextField(db_column='timeOfDay', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RestockScheduleItem'
        unique_together = (('scheduleid', 'itemid'),)


class Salesorder(models.Model):
    id = models.TextField(primary_key=True)
    customer = models.TextField()
    product = models.TextField()
    qty = models.IntegerField()
    total = models.FloatField()
    status = models.TextField()
    date = models.DateTimeField()
    outlet = models.TextField()
    orgid = models.ForeignKey(Organization, models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SalesOrder'


class Shift(models.Model):
    name = models.TextField()
    starttime = models.DateTimeField(db_column='startTime')  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='endTime')  # Field name made lowercase.
    breakduration = models.IntegerField(db_column='breakDuration')  # Field name made lowercase.
    orgid = models.ForeignKey(Organization, models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Shift'


class Stockbatch(models.Model):
    itemid = models.ForeignKey(Item, models.DO_NOTHING, db_column='itemId')  # Field name made lowercase.
    orgid = models.ForeignKey(Organization, models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.
    orderid = models.IntegerField(db_column='orderId', blank=True, null=True)  # Field name made lowercase.
    quantity = models.FloatField()
    remainingqty = models.FloatField(db_column='remainingQty')  # Field name made lowercase.
    expirystartdate = models.DateTimeField(db_column='expiryStartDate', blank=True, null=True)  # Field name made lowercase.
    expiryenddate = models.DateTimeField(db_column='expiryEndDate', blank=True, null=True)  # Field name made lowercase.
    exactexpirydate = models.DateTimeField(db_column='exactExpiryDate', blank=True, null=True)  # Field name made lowercase.
    receivedat = models.DateTimeField(db_column='receivedAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'StockBatch'


class Stocklocation(models.Model):
    name = models.TextField()
    address = models.TextField()

    class Meta:
        managed = False
        db_table = 'StockLocation'


class Stockmovement(models.Model):
    itemid = models.ForeignKey(Item, models.DO_NOTHING, db_column='itemId')  # Field name made lowercase.
    inventoryitemid = models.IntegerField(db_column='inventoryItemId', blank=True, null=True)  # Field name made lowercase.
    outletid = models.IntegerField(db_column='outletId', blank=True, null=True)  # Field name made lowercase.
    type = models.TextField()  # This field type is a guess.
    quantity = models.FloatField()
    quantitybefore = models.FloatField(db_column='quantityBefore')  # Field name made lowercase.
    quantityafter = models.FloatField(db_column='quantityAfter')  # Field name made lowercase.
    referenceid = models.TextField(db_column='referenceId', blank=True, null=True)  # Field name made lowercase.
    referencetype = models.TextField(db_column='referenceType', blank=True, null=True)  # Field name made lowercase.
    reason = models.TextField(blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    createdby = models.IntegerField(db_column='createdBy')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'StockMovement'


class Subcenter(models.Model):
    label = models.TextField()
    orgid = models.ForeignKey(Organization, models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SubCenter'
        unique_together = (('orgid', 'label'),)


class Subscription(models.Model):
    orgid = models.OneToOneField(Organization, models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.
    plan = models.TextField()  # This field type is a guess.
    expiresat = models.DateTimeField(db_column='expiresAt', blank=True, null=True)  # Field name made lowercase.
    features = models.JSONField(blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Subscription'


class Summaryrow(models.Model):
    itemcode = models.TextField(db_column='itemCode')  # Field name made lowercase.
    description = models.TextField()
    opexpct = models.FloatField(db_column='opExPct')  # Field name made lowercase.
    computedcost = models.FloatField(db_column='computedCost')  # Field name made lowercase.
    costcontribution = models.FloatField(db_column='costContribution')  # Field name made lowercase.
    sellingprice = models.FloatField(db_column='sellingPrice')  # Field name made lowercase.
    status = models.TextField(blank=True, null=True)
    orgid = models.ForeignKey(Organization, models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    itemid = models.ForeignKey(Item, models.DO_NOTHING, db_column='itemId', blank=True, null=True)  # Field name made lowercase.
    itemname = models.TextField(db_column='itemName', blank=True, null=True)  # Field name made lowercase.
    accounttitleid = models.ForeignKey(Accounttitle, models.DO_NOTHING, db_column='accountTitleId')  # Field name made lowercase.
    amount = models.FloatField()
    centerid = models.ForeignKey(Center, models.DO_NOTHING, db_column='centerId')  # Field name made lowercase.
    subcenterid = models.ForeignKey(Subcenter, models.DO_NOTHING, db_column='subCenterId')  # Field name made lowercase.
    vattypeid = models.ForeignKey('Vattype', models.DO_NOTHING, db_column='vatTypeId')  # Field name made lowercase.
    basecost = models.FloatField(db_column='baseCost')  # Field name made lowercase.
    costlines = models.JSONField(db_column='costLines', blank=True, null=True)  # Field name made lowercase.
    grossprofit = models.FloatField(db_column='grossProfit')  # Field name made lowercase.
    netprofit = models.FloatField(db_column='netProfit')  # Field name made lowercase.
    opexamount = models.FloatField(db_column='opExAmount')  # Field name made lowercase.
    vatinput = models.FloatField(db_column='vatInput', blank=True, null=True)  # Field name made lowercase.
    vatoutput = models.FloatField(db_column='vatOutput', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SummaryRow'


class Supplierorder(models.Model):
    orgid = models.ForeignKey(Organization, models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.
    scheduleid = models.ForeignKey(Restockschedule, models.DO_NOTHING, db_column='scheduleId', blank=True, null=True)  # Field name made lowercase.
    supplieremail = models.TextField(db_column='supplierEmail')  # Field name made lowercase.
    suppliertoken = models.TextField(db_column='supplierToken', unique=True)  # Field name made lowercase.
    tokenexpiresat = models.DateTimeField(db_column='tokenExpiresAt')  # Field name made lowercase.
    status = models.TextField()  # This field type is a guess.
    suppliermessage = models.TextField(db_column='supplierMessage', blank=True, null=True)  # Field name made lowercase.
    usermessage = models.TextField(db_column='userMessage', blank=True, null=True)  # Field name made lowercase.
    expectedarrival = models.DateTimeField(db_column='expectedArrival')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.
    cycleid = models.ForeignKey(Restockcycle, models.DO_NOTHING, db_column='cycleId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SupplierOrder'


class Supplierorderitem(models.Model):
    orderid = models.ForeignKey(Supplierorder, models.DO_NOTHING, db_column='orderId')  # Field name made lowercase.
    itemid = models.ForeignKey(Item, models.DO_NOTHING, db_column='itemId')  # Field name made lowercase.
    requestedqty = models.FloatField(db_column='requestedQty')  # Field name made lowercase.
    deliveredqty = models.FloatField(db_column='deliveredQty', blank=True, null=True)  # Field name made lowercase.
    confirmedqty = models.FloatField(db_column='confirmedQty', blank=True, null=True)  # Field name made lowercase.
    expirystartdate = models.DateTimeField(db_column='expiryStartDate', blank=True, null=True)  # Field name made lowercase.
    expiryenddate = models.DateTimeField(db_column='expiryEndDate', blank=True, null=True)  # Field name made lowercase.
    exactexpirydate = models.DateTimeField(db_column='exactExpiryDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SupplierOrderItem'


class Transaction(models.Model):
    outletid = models.ForeignKey(Outlet, models.DO_NOTHING, db_column='outletId')  # Field name made lowercase.
    cashierid = models.ForeignKey('User', models.DO_NOTHING, db_column='cashierId')  # Field name made lowercase.
    total = models.FloatField()
    vatamount = models.FloatField(db_column='vatAmount')  # Field name made lowercase.
    subtotal = models.FloatField()
    cashreceived = models.FloatField(db_column='cashReceived', blank=True, null=True)  # Field name made lowercase.
    change = models.FloatField(blank=True, null=True)
    paymentmethod = models.TextField(db_column='paymentMethod')  # Field name made lowercase. This field type is a guess.
    status = models.TextField()  # This field type is a guess.
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    syncedat = models.DateTimeField(db_column='syncedAt')  # Field name made lowercase.
    customerdetailsid = models.IntegerField(db_column='customerDetailsId', blank=True, null=True)  # Field name made lowercase.
    isvatexempt = models.BooleanField(db_column='isVatExempt')  # Field name made lowercase.
    scpwddiscountamt = models.FloatField(db_column='scPwdDiscountAmt', blank=True, null=True)  # Field name made lowercase.
    vatexemptamount = models.FloatField(db_column='vatExemptAmount', blank=True, null=True)  # Field name made lowercase.
    vatexemptrefno = models.TextField(db_column='vatExemptRefNo', blank=True, null=True)  # Field name made lowercase.
    vatexempttype = models.TextField(db_column='vatExemptType', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Transaction'


class Unauthorizedattempt(models.Model):
    outletid = models.IntegerField(db_column='outletId')  # Field name made lowercase.
    attempteddeviceid = models.TextField(db_column='attemptedDeviceId')  # Field name made lowercase.
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'UnauthorizedAttempt'


class User(models.Model):
    fullname = models.TextField()
    username = models.TextField(unique=True)
    email = models.TextField(unique=True)
    role = models.TextField()  # This field type is a guess.
    password = models.TextField()
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    profilephoto = models.TextField(db_column='profilePhoto', blank=True, null=True)  # Field name made lowercase.
    managerid = models.ForeignKey('self', models.DO_NOTHING, db_column='managerId', blank=True, null=True)  # Field name made lowercase.
    enabledpaymentmethod = models.BooleanField(db_column='enabledPaymentMethod')  # Field name made lowercase.
    contactnumber = models.TextField(db_column='contactNumber', blank=True, null=True)  # Field name made lowercase.
    orgid = models.ForeignKey(Organization, models.DO_NOTHING, db_column='orgId', blank=True, null=True)  # Field name made lowercase.
    isverified = models.BooleanField(db_column='isVerified')  # Field name made lowercase.
    verificationcode = models.TextField(db_column='verificationCode', blank=True, null=True)  # Field name made lowercase.
    isowner = models.BooleanField(db_column='isOwner')  # Field name made lowercase.
    positionid = models.ForeignKey(Position, models.DO_NOTHING, db_column='positionId', blank=True, null=True)  # Field name made lowercase.
    departmentid = models.ForeignKey(Department, models.DO_NOTHING, db_column='departmentId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'User'
        unique_together = (('orgid', 'email'), ('orgid', 'username'),)


class Userpermissionoverride(models.Model):
    id = models.TextField(primary_key=True)
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    pageid = models.ForeignKey(Page, models.DO_NOTHING, db_column='pageId')  # Field name made lowercase.
    canview = models.BooleanField(db_column='canView', blank=True, null=True)  # Field name made lowercase.
    cancreate = models.BooleanField(db_column='canCreate', blank=True, null=True)  # Field name made lowercase.
    canedit = models.BooleanField(db_column='canEdit', blank=True, null=True)  # Field name made lowercase.
    candelete = models.BooleanField(db_column='canDelete', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserPermissionOverride'


class Usershift(models.Model):
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    shiftid = models.ForeignKey(Shift, models.DO_NOTHING, db_column='shiftId')  # Field name made lowercase.
    assignedat = models.DateTimeField(db_column='assignedAt')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserShift'
        unique_together = (('userid', 'shiftid'),)


class Vattype(models.Model):
    orgid = models.ForeignKey(Organization, models.DO_NOTHING, db_column='orgId')  # Field name made lowercase.
    name = models.TextField()
    rate = models.FloatField()

    class Meta:
        managed = False
        db_table = 'VatType'
        unique_together = (('orgid', 'name'),)


class Colortoitem(models.Model):
    pk = models.CompositePrimaryKey('A', 'B')
    a = models.ForeignKey(Color, models.DO_NOTHING, db_column='A')  # Field name made lowercase.
    b = models.ForeignKey(Item, models.DO_NOTHING, db_column='B')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '_ColorToItem'


class Itemtoitemunit(models.Model):
    pk = models.CompositePrimaryKey('A', 'B')
    a = models.ForeignKey(Item, models.DO_NOTHING, db_column='A')  # Field name made lowercase.
    b = models.ForeignKey(Itemunit, models.DO_NOTHING, db_column='B')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = '_ItemToItemUnit'


class PrismaMigrations(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    checksum = models.CharField(max_length=64)
    finished_at = models.DateTimeField(blank=True, null=True)
    migration_name = models.CharField(max_length=255)
    logs = models.TextField(blank=True, null=True)
    rolled_back_at = models.DateTimeField(blank=True, null=True)
    started_at = models.DateTimeField()
    applied_steps_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = '_prisma_migrations'


class ApiCart(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_active = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.OneToOneField('ApiUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_cart'


class ApiCartitem(models.Model):
    id = models.BigAutoField(primary_key=True)
    product_id = models.IntegerField()
    branch_id = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    cart = models.ForeignKey(ApiCart, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_cartitem'
        unique_together = (('cart', 'product_id', 'branch_id'),)


class ApiDeliveryaddress(models.Model):
    id = models.BigAutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    region = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    barangay = models.CharField(max_length=100)
    street_address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)
    label = models.CharField(max_length=20)
    is_default = models.BooleanField()
    lat = models.DecimalField(max_digits=12, decimal_places=9)
    lng = models.DecimalField(max_digits=12, decimal_places=9)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey('ApiUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_deliveryaddress'


class ApiOrder(models.Model):
    id = models.BigAutoField(primary_key=True)
    order_number = models.CharField(unique=True, max_length=30)
    branch_id = models.IntegerField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=12, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20)
    payment_status = models.CharField(max_length=20)
    order_status = models.CharField(max_length=20)
    notes = models.TextField(blank=True, null=True)
    placed_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    delivery_address = models.ForeignKey(ApiDeliveryaddress, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('ApiUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_order'


class ApiOrderitem(models.Model):
    id = models.BigAutoField(primary_key=True)
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    order = models.ForeignKey(ApiOrder, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_orderitem'


class ApiPayment(models.Model):
    id = models.BigAutoField(primary_key=True)
    payment_method = models.CharField(max_length=20)
    payment_reference = models.CharField(max_length=100, blank=True, null=True)
    payment_intent_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20)
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()
    order = models.OneToOneField(ApiOrder, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_payment'


class ApiReview(models.Model):
    id = models.BigAutoField(primary_key=True)
    product_id = models.IntegerField()
    rating = models.SmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey('ApiUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_review'
        unique_together = (('user', 'product_id'),)


class ApiStore(models.Model):
    id = models.BigAutoField(primary_key=True)
    store_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    business_permit = models.CharField(max_length=100)
    dti_sec_registration = models.CharField(max_length=100)
    status = models.CharField(max_length=15)
    created_at = models.DateTimeField()
    user = models.OneToOneField('ApiUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_store'


class ApiSupplier(models.Model):
    id = models.BigAutoField(primary_key=True)
    company_name = models.CharField(max_length=255)
    business_type = models.CharField(max_length=100)
    product_category = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    min_order_value = models.DecimalField(max_digits=12, decimal_places=2)
    delivery_areas = models.TextField()
    registration_cert = models.CharField(max_length=100)
    bir_2303 = models.CharField(max_length=100)
    catalog = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=15)
    created_at = models.DateTimeField()
    user = models.OneToOneField('ApiUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_supplier'


class ApiUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    email = models.CharField(unique=True, max_length=254)
    full_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=11)
    is_verified = models.BooleanField()
    otp = models.CharField(max_length=6, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    role = models.CharField(max_length=10)
    profile_image = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'api_user'


class ApiUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(ApiUser, models.DO_NOTHING)
    group = models.ForeignKey('AuthGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_user_groups'
        unique_together = (('user', 'group'),)


class ApiUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(ApiUser, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_user_user_permissions'
        unique_together = (('user', 'permission'),)


class ApiWishlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    product_id = models.IntegerField()
    created_at = models.DateTimeField()
    user = models.ForeignKey(ApiUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_wishlist'
        unique_together = (('user', 'product_id'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(ApiUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


















