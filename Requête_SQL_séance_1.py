# Antoine ROBIN, Dimitri DERAMOND
# BUT 31 EMS

# Requête séance 1

# Importation des modules utilisÃ©s
import sqlite3
import pandas

# CrÃ©ation de la connexion
conn = sqlite3.connect("ClassicModel.sqlite")

# RÃ©cupÃ©ration du contenu de Customers avec une requÃªte SQL
customers = pandas.read_sql_query("SELECT * FROM Customers;", conn)
print(customers)


# Question 1

# Lister les clients n’ayant jamais effecuté une commande

q1 = pandas.read_sql_query("""
                      SELECT c.customerNumber,c.customerName
                      from Customers as c
                      left join Orders as o on c.customerNumber = O.customerNumber
                      where O.customerNumber IS NULL;
                      """, conn)

print(q1)


# Question 2

# Pour chaque employé, le nombre de clients, le nombre de commandes et le montant total de celles-ci

q2 = pandas.read_sql_query("""
                      SELECT e.employeeNumber, e.firstName, e.lastName, COUNT(distinct o.orderNumber) as nombre_commande, SUM(p.amount) as montant_total, count(distinct c.customerNumber) as Nombre_client
                      from Employees as e
                      left join Customers as c on e.employeeNumber = c.salesRepEmployeeNumber
                      left join Payments as p on c.customerNumber = p.customerNumber
                      left join Orders as o on c.customerNumber = o.customerNumber
                      GROUP BY e.employeeNumber
                      
                      ;
                      
                      """, conn)
                      
print(q2)


# Question 3

# Idem pour chaque bureau (nombre de clients, nombre de commandes et montant total), avec en plus le nombre de clients d’un pays différent, s’il y en a

q3 = pandas.read_sql_query("""
                      SELECT of.officeCode, COUNT(distinct o.orderNumber) as nombre_commande, SUM(p.amount) as montant_total, count(distinct c.customerNumber) as Nombre_client, count(distinct case when c.country != of.country then c.customerNumber end) as customersFromDifferentCountry
                      from Offices as of
                      left join Employees as e on of.officeCode = e.officeCode
                      left join Customers as c on e.employeeNumber = c.salesRepEmployeeNumber
                      left join Payments as p on c.customerNumber = p.customerNumber
                      left join Orders as o on c.customerNumber = o.customerNumber
                      GROUP BY of.officeCode
                      ;
                      
                      """, conn)

print(q3)


# Question 4

# Pour chaque produit, donner le nombre de commandes, la quantité totale commandée, et le nombre de clients différents (110 lignes)

q4 = pandas.read_sql_query("""
                      SELECT p.productCode, p.productName, COUNT(distinct o.orderNumber) as nombre_commande, SUM(quantityOrdered) as quantite_commande, count(distinct c.customerNumber) as Nombre_client
                      from Products as p 
                      left join OrderDetails as d on p.productCode = d.productCode
                      left join Orders as o on d.orderNumber = o.orderNumber
                      left join Customers as c on o.customerNumber = c.customerNumber
                      GROUP BY p.productCode
                      ;
                      
                      """, conn)

print(q4)



# Question 5

# Donner le nombre de commande pour chaque pays, ainsi que le montant total des commandes et le montant total payé : on veut conserver les clients n’ayant jamais commandé dans le résultat final

q5 = pandas.read_sql_query("""
                      SELECT c.country, count(distinct o.orderNumber) as nombre_commande, sum(d.priceEach * d.quantityOrdered) as Montant_total_commande, sum(p.amount) as Montant_payer
                      from Customers as c 
                      left join Orders as o on c.customerNumber= o.customerNumber
                      left join Payments as p on c.customerNumber = p.customerNumber
                      left join OrderDetails as d on o.orderNumber = d.orderNumber
                      GROUP BY c.country
                      ;
                      
                      """, conn)

print(q5)




# Question 6

# On veut la table de contigence du nombre de commande entre la ligne de produits et le pays du client (127 lignes)

q6 = pandas.read_sql_query("""
                      SELECT p.productLine, c.country, count(distinct o.orderNumber) as nombre_commande
                      from Products as p 
                      left join OrderDetails as d on p.productCode = d.productCode
                      left join Orders as o on d.orderNumber= o.orderNumber
                      left join Customers as c on c.customerNumber = o.customerNumber
                      GROUP BY p.productLine, c.country
                      
                      ;
                      
                      """, conn)
                      
print(q6)


# Question 7

# On veut la même table croisant la ligne de produits et le pays du client, mais avec le montant total payé dans chaque cellule

q7 = pandas.read_sql_query("""
                      SELECT p.productLine, c.country, sum(amount) as total_payments
                      from Products as p 
                      left join OrderDetails as d on p.productCode = d.productCode
                      left join Orders as o on d.orderNumber= o.orderNumber
                      left join Customers as c on c.customerNumber = o.customerNumber
                      left join Payments as t on c.customerNumber = t.customerNumber
                      GROUP BY p.productLine, c.country
                      
                      ;
                      
                      """, conn)
                      
print(q7)




# Question 8

# Donner les 10 produits pour lesquels la marge moyenne est la plus importante (79 lignes)

q8 = pandas.read_sql_query("""
                      SELECT p.productCode, p.productName, AVG(d.priceEach-p.buyPrice) as marge_moyenne
                      from Products as p 
                      left join OrderDetails as d on p.productCode = d.productCode
                      GROUP BY p.productCode, p.productName
                      ORDER BY marge_moyenne desc
                      limit 10
                      ;
                      """, conn)
print(q8)



# Question 9

# Lister les produits (avec le nom et le code du client) qui ont été vendus à perte :
# Si un produit a été dans cette situation plusieurs fois, il doit apparaître plusieurs fois,
# Une vente à perte arrive quand le prix de vente est inférieur au prix d’achat

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

# (bonus) Lister les clients pour lesquels le montant total payé est supérieur aux montants totals des achats

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


conn.close()



