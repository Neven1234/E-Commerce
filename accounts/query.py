﻿
#***(1) Returns all customers from customer table 
customers = Customer.objects.all()
#(2) Returns first customer in table
 firstCustomer=Customer.objects.first()
#(3) Returns last customer in table 
lastCustomer=Customer.objects.last()
#(4) Returns single customer by name
customerByName = Customer.objects.get(name='Peter Piper')
#***(5) Returns single customer by name
customerById= Customer.objects.get(id=4)
#***(6) Returns all orders related to customer (first Customer variable set above) firstCustomer.order_set.all()
#(7)***Returns orders customer name: (Query parent model values)
order= Order.objects.first()
parentName = order.customer.name
#(8)***Returns products from products table with value of "Out Door" in category attribute
 products= Product.objects.filter(category="Out Door")
#(9)***Order/Sort Objects by id
least ToGreatest =Product.objects.all().order_by('id')
greatestToLeast = Product.objects.all().order_by('id')
#(10) Returns all products with tag of "Sports": (Query Many to Many Fields) 
productsFiltered = Product.objects.filter(tags_name="Sports")

#(11) Bonus
#Q: If the customer has more than 1 ball, how would you
#A: Because there are many different products and this v 39 likly not want to store the value in the database but r each time we load the customers profile

#Returns the total count for number of time a "Ball" wa 
ballOrders = firstCustomer.order_set.filter(product_name)
#Returns total count for each product orderd 
allOrders = {}

for order in firstCustomer.order_set.all(): 
	if order.product.name in allOrders: 
		allOrders [order.product.name] += 1
	﻿
	else:
		allOrders [order.product.name] = 1
#Returns: allOrders: {'Ball: 2, 'BBQ Grill': 1}
#RELATED SET EXAMPLE
class ParentModel(models.Model):
    name = models.CharField(max_length=200, null=True)
class ChildModel(models.Model):
	parent = models.ForeignKey(ParentModel)
	name = models.CharField(max_length=200, null=True)
parent = ParentModel.objects.first()
#Returns all child models related to parent
parent.childmodel_set.all()