CREATE (:Person {name: '42'})
WITH 0 as x
MATCH (p:Person { name: '42' })
WITH *
MATCH (n)
RETURN toInteger(n.name) AS name
