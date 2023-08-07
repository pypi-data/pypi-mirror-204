# whatsappChat2dataFrame


Currently experimenting and planning!

Developed by Kiran Busch 2023

## Examples of How To Use (Buggy Alpha Version)

Creating a Converter and calling chat2dataframe function

```python
#load package with converter
from whatsappchat2dataframe import Converter
#create converter
conv = Converter()
#create dataframe from whatsapp .txt file
file_path = 'data/_chat.txt'
df = conv.chat2dataframe(path_to_filename = file_path)
```