# Changes immutable data types (in-place)

## pip install evilvars

#### Important: As the module's name suggests, it should not be used in a real project. 


```python

go_to_purgatory(v, new):
    """
    Copies the bytes of a new value to a buffer of an existing value.

    Args:
        v (Any): The existing value to copy the bytes to.
        new (Any): The new value to copy the bytes from.

    Returns:
        bool: True if the bytes were successfully copied, False otherwise.
    """
	
	
from evilvars import go_to_purgatory
t = ("275", 54000, "0.0", "5000.0", "0.0")
newvar = "200"  # the new string needs to be  <=  the old string
index = 0
print(id(t), t)
go_to_purgatory(v=t[index], new=newvar)
print(id(t), t)
index = 1
newvar = 20.1
go_to_purgatory(v=t[index], new=newvar)
print(id(t), t)
mystring = "hallo"
newvar = "XallY"
print(mystring)
print(id(mystring))
go_to_purgatory(v=mystring, new=newvar)
print(mystring)
print(id(mystring))
mystringb = b"hallo"
newvarb = b"XallY"
print(mystringb)
print(id(mystringb))
go_to_purgatory(v=mystringb, new=newvarb)
print(mystringb)
print(id(mystringb))
2218474368960 ('275', 54000, '0.0', '5000.0', '0.0')
2218474368960 ('200', 54000, '0.0', '5000.0', '0.0')
2218474368960 ('200', 20.1, '0.0', '5000.0', '0.0')
hallo
2218646391856
XallY
2218646391856
b'hallo'
2218646405792
b'XallY'
2218646405792
```