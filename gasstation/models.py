from django.db import models


class Product(models.Model):
    productID = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=50)
    price = models.FloatField()
    """GENDER = [
        (gas, '油品'),
        (car, '车用品'),
        (other, '其他'),
    ]"""
    type = models.CharField(max_length=20)  # 要不要用choices?
    description = models.TextField()
    credit_needed = models.FloatField()
    sales = models.FloatField()
    stock = models.FloatField()

    def __str__(self):
        return self.name


class Client(models.Model):
    tel = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=20)
    pwd = models.CharField(max_length=20, default='jiayoubao666')
    MALE = 1
    FEMALE = 2
    GENDER = [
        (MALE, '男'),
        (FEMALE, '女'),
    ]
    gender = models.CharField(max_length=20, choices=GENDER, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    credit = models.FloatField(default=0)
    REGULARMEMBERS = 'RM'
    SILVERMEMBERS = 'SM'
    GOLDMEMBERS = 'GM'
    DIAMONDMEMBERS = 'DM'
    LEVEL = [
        (REGULARMEMBERS, 'RegularMembers'),
        (SILVERMEMBERS, 'SilverMembers'),
        (GOLDMEMBERS, 'GoldMembers'),
        (DIAMONDMEMBERS, 'DiamondMembers'),
    ]
    level = models.CharField(
        max_length=20,
        choices=LEVEL,
        default=REGULARMEMBERS,
    )
    plate_number = models.CharField(null=True, blank=True, max_length=20)
    district = models.TextField(max_length=20, null=True, blank=True)
    products = models.ManyToManyField(Product, through='ShoppingCart')

    def __str__(self):
        return self.tel


"""class ShoppingCart(models.Model):
    clientID = models.ForeignKey(
        to="Client",
        to_field="tel",
        on_delete=models.CASCADE,
    )
    productID = models.ForeignKey(
        to="Product",
        to_field="productID",
        on_delete=models.CASCADE,
    )
    quantity = models.FloatField()"""


class ShoppingCart(models.Model):  # 购物车
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()

    class Meta:
        db_table = "Shopping_Cart"


class Invoice(models.Model):  # 发票
    invoiceID = models.CharField(primary_key=True, max_length=20)
    taxID = models.CharField(max_length=20)
    Corporate = 'Cor'
    Personal = 'Per'
    INVOICE_TYPE = [
        (Corporate, '企业的'),
        (Personal, '个人的'),
    ]
    invoice_type = models.CharField(choices=INVOICE_TYPE, max_length=20)
    email = models.EmailField()
    tel = models.CharField(max_length=20)
    address = models.TextField(max_length=100)
    bank_account = models.CharField(max_length=30)
    bank_address = models.TextField(max_length=100)

    def __str__(self):
        return self.invoiceID


class Ticket(models.Model):  # 优惠券
    ticketID = models.CharField(primary_key=True, max_length=20)
    ticket_name = models.CharField(max_length=20)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    DAZHE = 'DZ'
    MANJIAN = 'MJ'
    TICKET_TYPE = [
        (DAZHE, '打折券'),
        (MANJIAN, '满减券'),
    ]
    ticket_type = models.CharField(choices=TICKET_TYPE, max_length=20)
    discount = models.FloatField()  # 打折时是折扣，满减时是减少的金额
    threshold = models.FloatField(blank=True, null=True)  # 门槛
    ticket_description = models.TextField(max_length=200)

    def __str__(self):
        return self.ticket_name


class Order(models.Model):  # 订单
    orderID = models.CharField(primary_key=True, max_length=20)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, blank=True, null=True)
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, blank=True, null=True)
    total_money = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)
    credit_increment = models.FloatField()
    products = models.ManyToManyField(Product, through='OrderProduct')

    def __str__(self):
        return self.orderID


class OrderProduct(models.Model):  # 订单各商品的购买数量以及评价
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.FloatField()
    star_rating = models.CharField(max_length=20, blank=True, null=True)  # 要不要用choices?
    review_text = models.TextField(blank=True, null=True)
    review_time = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        db_table = "order_review"


class Administrator(models.Model):
    employeeID = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=20)
    pwd = models.CharField(max_length=20)
    MALE = 1
    FEMALE = 2
    GENDER = [
        (MALE, '男'),
        (FEMALE, '女'),
    ]
    gender = models.CharField(max_length=20, choices=GENDER, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    position = models.CharField(max_length=20, null=True, blank=True)
    clients = models.ManyToManyField(Client, through='AdministratorClient')
    products = models.ManyToManyField(Product, through='AdministratorProduct')
    tickets = models.ManyToManyField(Ticket, through='AdministratorTicket')

    def __str__(self):
        return self.name


class AdministratorClient(models.Model):
    administrator = models.ForeignKey(Administrator, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    operation = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)


class AdministratorProduct(models.Model):
    administrator = models.ForeignKey(Administrator, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    operation = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)


class AdministratorTicket(models.Model):
    administrator = models.ForeignKey(Administrator, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    operation = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)
