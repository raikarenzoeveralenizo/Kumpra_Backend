from django.db import models


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
    amount = models.FloatField()
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