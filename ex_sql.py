# Importation des modules utilisés
import sqlite3
import pandas

# Création de la connexion
conn = sqlite3.connect("ClassicModel.sqlite")

# Récupération du contenu de Customers avec une requête SQL
customers = pandas.read_sql_query("SELECT * FROM Customers;", conn)
print(customers)


# Question 1
clients = pandas.read_sql_query("""
                      SELECT *
                      from Customers as c
                      left join Orders as o on c.customerNumber = O.customerNumber
                      where O.customerNumber IS NULL;
                      """, conn)

print(clients)


# Question 2
employe = pandas.read_sql_query("""
                      SELECT e.employeeNumber, e.lastName, COUNT(distinct o.orderNumber) as nombre_commande, SUM(p.amount) as montant_total, count(distinct c.customerNumber) as Nombre_client
                      from Employees as e
                      left join Customers as c on e.employeeNumber = c.salesRepEmployeeNumber
                      left join Payments as p on c.customerNumber = p.customerNumber
                      left join Orders as o on c.customerNumber = o.customerNumber
                      GROUP BY e.employeeNumber
                      
                      ;
                      
                      """, conn)
                      
print(employe)


# Question 3

bureau = pandas.read_sql_query("""
                      SELECT of.officeCode, COUNT(distinct o.orderNumber) as nombre_commande, SUM(p.amount) as montant_total, count(distinct c.customerNumber) as Nombre_client, count(distinct case when c.country != of.country then c.customerNumber end) as pays_diff
                      from Offices as of
                      left join Employees as e on of.officeCode = e.officeCode
                      left join Customers as c on e.employeeNumber = c.salesRepEmployeeNumber
                      left join Payments as p on c.customerNumber = p.customerNumber
                      left join Orders as o on c.customerNumber = o.customerNumber
                      GROUP BY of.officeCode
                      ;
                      
                      """, conn)

print(bureau)


# Question 4


produit = pandas.read_sql_query("""
                      SELECT p.productCode, p.productName, COUNT(distinct o.orderNumber) as nombre_commande, SUM(quantityOrdered) as quantite_commande, count(distinct c.customerNumber) as Nombre_client
                      from Products as p 
                      left join OrderDetails as d on p.productCode = d.productCode
                      left join Orders as o on d.orderNumber = o.orderNumber
                      left join Customers as c on o.customerNumber = c.customerNumber
                      GROUP BY p.productCode
                      ;
                      
                      """, conn)

print(produit)



# Question 5

pays = pandas.read_sql_query("""
                      SELECT c.country, count(distinct o.orderNumber) as nombre_commande, sum(d.priceEach * d.quantityOrdered) as Montant_total_commande, sum(p.amount) as Montant_payer
                      from Customers as c 
                      left join Orders as o on c.customerNumber= o.customerNumber
                      left join Payments as p on c.customerNumber = p.customerNumber
                      left join OrderDetails as d on o.orderNumber = d.orderNumber
                      GROUP BY c.country
                      ;
                      
                      """, conn)

print(pays)




# Question 6

pays = pandas.read_sql_query("""
                      SELECT p.productLine, c.country, count(distinct o.orderNumber) as nombre_commande
                      from Products as p 
                      left join OrderDetails as d on p.productCode = d.productCode
                      left join Orders as o on d.orderNumber= o.orderNumber
                      left join Customers as c on c.customerNumber = o.customerNumber
                      GROUP BY p.productLine, c.country
                      
                      ;
                      
                      """, conn)
                      
print(pays)


# Question 7

montant = pandas.read_sql_query("""
                      SELECT p.productLine, c.country, sum(amount) as total_payments
                      from Products as p 
                      left join OrderDetails as d on p.productCode = d.productCode
                      left join Orders as o on d.orderNumber= o.orderNumber
                      left join Customers as c on c.customerNumber = o.customerNumber
                      left join Payments as t on c.customerNumber = t.customerNumber
                      GROUP BY p.productLine, c.country
                      
                      ;
                      
                      """, conn)
                      
print(montant)




# Question 8

montant = pandas.read_sql_query("""
                      SELECT p.productCode, p.productName, AVG(d.priceEach-p.buyPrice) as marge_moyenne
                      from Products as p 
                      left join OrderDetails as d on p.productCode = d.productCode
                      GROUP BY p.productCode, p.productName
                      ORDER BY marge_moyenne desc
                      limit 10
                      ;
                      """, conn)
print(montant)



# Question 9

q9 = pandas.read_sql_query("""
                      SELECT p.productCode, p.productName, c.customerName, c.customerNumber, d.priceEach, p.buyPrice
                      from Products as p 
                      left join OrderDetails as d on p.productCode = d.productCode
                      left join Orders as o on d.orderNumber= o.orderNumber
                      left join Customers as c on c.customerNumber = o.customerNumber
                      WHERE d.priceEach < p.buyPrice
                      ;
                      """, conn)
print(q9)




# Question 10


q10 = pandas.read_sql_query("""
                      SELECT c.customerName, c.customerNumber,sum(d.priceEach * d.quantityOrdered) as Montant_total_commande, sum(t.amount) as Montant_payer
                      from Products as p 
                      left join OrderDetails as d on p.productCode = d.productCode
                      left join Orders as o on d.orderNumber= o.orderNumber
                      left join Customers as c on c.customerNumber = o.customerNumber
                      left join Payments as t on c.customerNumber = t.customerNumber
                      GROUP BY c.customerNumber
                      HAVING Montant_payer > Montant_total_commande
                      ;
                      """, conn)


print(q10)

# Fermeture de la connexion : IMPORTANT à faire dans un cadre professionnel
conn.close()



