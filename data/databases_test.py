import sqlite3

# Connect to the dataset1 SQLite database
conn1 = sqlite3.connect('data/dataset1.sqlite')
cursor1 = conn1.cursor()

# Query data from dataset1
cursor1.execute("SELECT * FROM dataset1")
data1 = cursor1.fetchall()

# Close the connection to dataset1
conn1.close()

# Connect to the dataset2 SQLite database
conn2 = sqlite3.connect('data/dataset2.sqlite')
cursor2 = conn2.cursor()

# Query data from dataset2
cursor2.execute("SELECT * FROM dataset2")
data2 = cursor2.fetchall()

# Close the connection to dataset2
conn2.close()

# Print data from dataset1
print("Data from dataset1:")
for row in data1:
    print(row)

# Print data from dataset2
print("\nData from dataset2:")
for row in data2:
    print(row)
